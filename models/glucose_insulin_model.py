import numpy as np
from numba import njit

@njit(cache=True)
def glucose_insulin_ode( states, time, parameters, inputs):
    G, X, I = states
    p1, p2, p3, n, gamma, h, Gb, Ib = parameters
    u = inputs

    dGdt = -p1 * (G - Gb) - G * X
    dXdt = -p2 * X + p3 * (I - Ib)
    dIdt = -n * (I - Ib) + gamma * (G - h) * time + u

    return np.array([dGdt, dXdt, dIdt])
