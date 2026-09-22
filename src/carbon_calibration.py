"""Physical GBM calibration using protocol sections 17–18 (calendar time)."""
from datetime import date
import math

import numpy as np


def fit_official_gbm(dates, closes):
    """Fit unmodified positive official closes; never fill, clip, or smooth."""
    if len(dates) != len(closes) or len(dates) < 2:
        raise ValueError('At least two paired observations are required')
    days = [date.fromisoformat(d) for d in dates]
    prices = np.asarray(closes, dtype=float)
    if not np.all(np.isfinite(prices)) or np.any(prices <= 0):
        raise ValueError('Official closes must be positive and finite')
    dt = np.asarray([(b-a).days / 365.25 for a, b in zip(days, days[1:])])
    if np.any(dt <= 0):
        raise ValueError('Official dates must be strictly increasing')
    returns = np.log(prices[1:] / prices[:-1])
    m = float(returns.sum() / dt.sum())
    variance = float(np.mean((returns-m*dt)**2 / dt))
    result = dict(n_observations=len(prices), start_date=dates[0], end_date=dates[-1],
                  P0=float(prices[-1]), mu=m+variance/2, sigma=math.sqrt(variance),
                  mean_log_return=float(returns.mean()),
                  return_std=float(returns.std(ddof=0)), return_std_ddof=0,
                  min_price=float(prices.min()), max_price=float(prices.max()))
    diagnostics = [dict(date=dates[i+1], dt_years=float(dt[i]),
                        log_return=float(returns[i]),
                        drift_residual=float(returns[i]-m*dt[i]))
                   for i in range(len(returns))]
    return result, diagnostics
