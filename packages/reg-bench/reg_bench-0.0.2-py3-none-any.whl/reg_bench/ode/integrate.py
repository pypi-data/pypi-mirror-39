from functools import wraps

import numpy as np
import scipy.integrate


def derivative(x, dt=1.0):
    """
    Compute time-derivative of the data matrix X along first axis.

    x : array-like, shape (n_samples,n_features)
        Input variables to be derived.
    """

    dx = np.zeros_like(x)
    dx[1:-1, :] = (x[2:, :] - x[:-2, :]) / (2.0 * dt)

    dx[0, :] = (x[1, :] - x[0, :]) / dt
    dx[-1, :] = (x[-1, :] - x[-2, :]) / dt

    return dx


def generate_ode_data(problem, x0, t, params):
    dy = problem(**params)
    x = scipy.integrate.odeint(dy, x0, t)
    dt = t[1] - t[0]
    dx = derivative(x, dt)
    return x, dx
