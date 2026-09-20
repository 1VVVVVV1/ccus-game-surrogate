"""Unclipped regression metrics and frozen acceptance thresholds."""
import math
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from .config import VALUE_TARGETS, PROBABILITY_TARGETS, TIME_TARGETS


def metrics(y, predicted):
    if len(y) == 0:
        return dict(R2=math.nan, MAE=math.nan, RMSE=math.nan, NMAE=math.nan)
    mae = float(mean_absolute_error(y,predicted))
    spread = float(np.quantile(y,.95)-np.quantile(y,.05))
    return {"R2":float(r2_score(y,predicted)) if len(y)>1 else math.nan,
            "MAE":mae,"RMSE":float(math.sqrt(mean_squared_error(y,predicted))),
            "NMAE":mae/spread if spread>1e-12 else math.nan}


def passes(target, measured):
    if target in VALUE_TARGETS:
        return measured["R2"] >= .98 and measured["NMAE"] <= .05
    if target in PROBABILITY_TARGETS:
        return measured["MAE"] <= .03
    if target in TIME_TARGETS:
        return measured["MAE"] <= 1.0
    return measured["R2"] >= .95 and measured["NMAE"] <= .08
