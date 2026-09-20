"""Recombining physical-measure binomial approximation to standard GBM."""
import math
import numpy as np
from .config import CONFIG


def carbon_tree(carbon_scale, horizon=30):
    parameters = CONFIG["carbon_price"]
    dt = CONFIG["simulation"]["dt_years"]
    u = math.exp(parameters["sigma"] * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp(parameters["mu"] * dt) - d) / (u - d)
    if not 0 < p < 1:
        raise RuntimeError("INVALID_PHYSICAL_PROBABILITY")
    prices = np.full((horizon + 1, horizon + 1), np.nan)
    for t in range(horizon + 1):
        for j in range(t + 1):
            prices[t, j] = parameters["P0"] * carbon_scale * u**j * d**(t-j)
    return prices, u, d, p
