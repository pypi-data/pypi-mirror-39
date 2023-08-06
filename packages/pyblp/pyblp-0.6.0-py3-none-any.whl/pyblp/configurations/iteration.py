"""Fixed-point iteration routines."""

import functools
from typing import Any, Callable, Optional, Tuple, Union

import numpy as np

from ..utilities.basics import Array, Options, StringRepresentation, format_options


class Iteration(StringRepresentation):
    r"""Configuration for solving fixed point problems.

    Parameters
    ----------
    method : `str or callable`
        The fixed point iteration routine that will be used. One of the following:

            - ``'simple'`` - Non-accelerated iteration.

            - ``'squarem'`` - SQUAREM acceleration method of :ref:`references:Varadhan and Roland (2008)` and considered
              in the context of the BLP problem in :ref:`references:Reynaerts, Varadhan, and Nash (2012)`. This
              implementation uses a first-order squared non-monotone extrapolation scheme. If there are any errors
              during the acceleration step, it uses the last values for the next iteration of the algorithm.

        The following trivial routine can be used to simply return the initial values:

            - ``'return'`` - Assume that the initial values are the optimal ones.

        Also accepted is a custom callable method with the following form::

            method(initial, contraction, callback, **options) -> (final, converged)

        where ``initial`` is an array of initial values, ``contraction`` is a callable contraction mapping, ``callback``
        is a function that should be called without any arguments after each major iteration (it is used to record the
        number of major iterations), ``options`` are specified below, ``final`` is an array of final values, and
        ``converged`` is a flag for whether the routine converged.

        Regardless of the chosen routine, if there are any computational issues that create infinities or null values,
        ``final`` will be the second to last iteration's values.

    method_options : `dict, optional`
        Options for the fixed point iteration routine. Non-custom routines other than ``'return'`` support the following
        options:

            - **max_evaluations** : (`int`) - Maximum number of contraction mapping evaluations. The default value is
              ``5000``.

            - **tol** : (`float`) - Tolerance for convergence of the configured norm. The default value is ``1e-14``.

            - **norm** : (`callable`) - The norm to be used. By default, the :math:`\ell^\infty`-norm is used. If
              specified, this should be a function that accepts an array of differences and that returns a scalar norm.

        The ``'squarem'`` routine accepts additional options that mirror those in the
        `SQUAREM <https://cran.r-project.org/web/packages/SQUAREM/index.html>`_ package, written in R by Ravi Varadhan,
        which identifies the step length with :math:`-\alpha` from :ref:`references:Varadhan and Roland (2008)`:

            - **scheme** : (`int`) - The default value is ``3``, which corresponds to S3 in
              :ref:`references:Varadhan and Roland (2008)`. Other acceptable schemes are ``1`` and ``2``, which
              correspond to S1 and S2.

            - **step_min** : (`float`) - The initial value for the minimum step length. The default value is ``1.0``.

            - **step_max** : (`float`) - The initial value for the maximum step length. The default value is ``1.0``.

            - **step_factor** : (`float`) - When the step length exceeds ``step_max``, it is set equal to ``step_max``,
              but ``step_max`` is scaled by this factor. Similarly, if ``step_min`` is negative and the step length is
              below ``step_min``, it is set equal to ``step_min`` and ``step_min`` is scaled by this factor. The default
              value is ``4.0``.

    Examples
    --------
    .. raw:: latex

       \begin{examplenotebook}

    .. toctree::

       /_notebooks/api/iteration.ipynb

    .. raw:: latex

       \end{examplenotebook}

    """

    _iterator: functools.partial
    _description: str
    _method_options: Options

    def __init__(self, method: Union[str, Callable], method_options: Optional[Options] = None) -> None:
        """Validate the method and configure default options."""
        methods = {
            'squarem': (functools.partial(squarem_iterator), "the SQUAREM acceleration method"),
            'simple': (functools.partial(simple_iterator), "no acceleration"),
            'return': (functools.partial(return_iterator), "a trivial routine that returns the initial values")
        }

        # validate the configuration
        if method not in methods and not callable(method):
            raise ValueError(f"method must be one of {list(methods.keys())} or a callable object.")
        if method_options is not None and not isinstance(method_options, dict):
            raise ValueError("method_options must be None or a dict.")

        # options are by default empty
        if method_options is None:
            method_options = {}

        # options are simply passed along to custom methods
        if callable(method):
            self._iterator = functools.partial(method)
            self._description = "a custom method"
            self._method_options = method_options
            return

        # identify the non-custom iterator and set default options
        self._iterator, self._description = methods[method]
        self._method_options: Options = {}
        if method != 'return':
            self._method_options.update({
                'tol': 1e-14,
                'max_evaluations': 5000,
                'norm': infinity_norm
            })
        if method == 'squarem':
            self._method_options.update({
                'scheme': 3,
                'step_min': 1.0,
                'step_max': 1.0,
                'step_factor': 4.0
            })

        # validate options for non-custom methods
        invalid = [k for k in method_options if k not in self._method_options]
        if invalid:
            raise KeyError(f"The following are not valid iteration options: {invalid}.")
        if method == 'return':
            return
        self._method_options.update(method_options)
        if not isinstance(self._method_options['tol'], float) or self._method_options['tol'] <= 0:
            raise ValueError("The iteration option tol must be a positive float.")
        if not isinstance(self._method_options['max_evaluations'], int) or self._method_options['max_evaluations'] < 1:
            raise ValueError("The iteration option max_evaluations must be a positive int.")
        if not callable(self._method_options['norm']):
            raise ValueError("The iteration option norm must be callable.")
        if method == 'squarem':
            if self._method_options['scheme'] not in {1, 2, 3}:
                raise ValueError("The iteration option scheme must be 1, 2, or 3.")
            if not isinstance(self._method_options['step_min'], float):
                raise ValueError("The iteration option step_min must be a float.")
            if not isinstance(self._method_options['step_max'], float) or self._method_options['step_max'] <= 0:
                raise ValueError("The iteration option step_max must be a positive float.")
            if self._method_options['step_min'] > self._method_options['step_max']:
                raise ValueError("The iteration option step_min must be smaller than step_max.")
            if not isinstance(self._method_options['step_factor'], float) or self._method_options['step_factor'] <= 0:
                raise ValueError("The iteration option step_factor must be a positive float.")

    def __str__(self) -> str:
        """Format the configuration as a string."""
        return f"Configured to iterate using {self._description} with options {format_options(self._method_options)}."

    def _iterate(self, initial: Array, contraction: Callable[[Array], Any]) -> Tuple[Array, bool, int, int]:
        """Solve a fixed point iteration problem."""

        # initialize counters
        iterations = evaluations = 0

        # define an iteration callback
        def iteration_callback() -> None:
            """Count the number of major iterations."""
            nonlocal iterations
            iterations += 1

        # define a contraction wrapper
        def contraction_wrapper(raw_values: Any) -> Array:
            """Normalize arrays so they work with all types of routines. Also count the total number of contraction
            evaluations.
            """
            nonlocal evaluations
            evaluations += 1
            if not isinstance(raw_values, np.ndarray):
                raw_values = np.asarray(raw_values)
            values = raw_values.reshape(initial.shape).astype(initial.dtype, copy=False)
            return contraction(values).astype(np.float64, copy=False).reshape(raw_values.shape)

        # normalize the starting values
        raw_initial = initial.astype(np.float64, copy=False).flatten()

        # solve the problem and convert the raw final values to the same data type and shape as the initial values
        raw_final, converged = self._iterator(
            raw_initial, contraction_wrapper, iteration_callback, **self._method_options
        )
        if not isinstance(raw_final, np.ndarray):
            raw_final = np.asarray(raw_final)
        final = raw_final.reshape(initial.shape).astype(initial.dtype, copy=False)
        return final, converged, iterations, evaluations


def infinity_norm(x: Array) -> float:
    """Compute the infinity norm of a vector."""
    return np.abs(x).max()


def return_iterator(initial: Array, *_: Any, **__: Any) -> Tuple[Array, bool]:
    """Assume the initial values are the optimal ones."""
    success = True
    return initial, success


def squarem_iterator(
        initial: Array, contraction: Callable[[Array], Array], iteration_callback: Callable[[], None],
        max_evaluations: int, tol: float, norm: Callable[[Array], float], scheme: int, step_min: float, step_max: float,
        step_factor: float) -> Tuple[Array, bool]:
    """Apply the SQUAREM acceleration method for fixed point iteration."""
    x = initial
    failed = False
    evaluations = 0
    while True:
        # first step
        x0, x = x, contraction(x)
        if not np.isfinite(x).all():
            x = x0
            failed = True
            break

        # check for convergence
        g0 = x - x0
        evaluations += 1
        if evaluations >= max_evaluations or norm(g0) < tol:
            break

        # second step
        x1, x = x, contraction(x)
        if not np.isfinite(x).all():
            x = x1
            failed = True
            break

        # check for convergence
        g1 = x - x1
        evaluations += 1
        if evaluations >= max_evaluations or norm(g1) < tol:
            break

        # compute the step length
        r = g0
        v = g1 - g0
        if scheme == 1:
            alpha = (r.T @ v) / (v.T @ v)
        elif scheme == 2:
            alpha = (r.T @ r) / (r.T @ v)
        else:
            alpha = -np.sqrt((r.T @ r) / (v.T @ v))

        # bound the step length and update its bounds
        alpha = -np.maximum(step_min, np.minimum(step_max, -alpha))
        if -alpha == step_max:
            step_max *= step_factor
        if -alpha == step_min and step_min < 0:
            step_min *= step_factor

        # acceleration step
        x2, x = x, x0 - 2 * alpha * r + alpha**2 * v
        x3, x = x, contraction(x)
        if not np.isfinite(x).all():
            x = x2
            failed = True
            break

        # record the completion of a major iteration
        iteration_callback()

        # check for convergence
        evaluations += 1
        if evaluations >= max_evaluations or norm(x - x3) < tol:
            break

    # determine whether there was convergence
    converged = not failed and evaluations < max_evaluations
    return x, converged


def simple_iterator(
        initial: Array, contraction: Callable[[Array], Array], iteration_callback: Callable[[], None],
        max_evaluations: int, tol: float, norm: Callable[[Array], float]) -> Tuple[Array, bool]:
    """Apply simple fixed point iteration with no acceleration."""
    x = initial
    failed = False
    evaluations = 0
    while True:
        # contraction step
        x0, x = x, contraction(x)
        if not np.isfinite(x).all():
            x = x0
            failed = True
            break

        # record the completion of a major iteration, which is the same here as a contraction evaluation
        iteration_callback()

        # check for convergence
        evaluations += 1
        if evaluations >= max_evaluations or norm(x - x0) < tol:
            break

    # determine whether there was convergence
    converged = not failed and evaluations < max_evaluations
    return x, converged
