import math
import pandas as pd
from src.config import BASELINE, FEATURES, HGB_PARAMETERS
from src.surrogate import feature_matrix
from src.metrics import metrics, passes
from sklearn.ensemble import HistGradientBoostingRegressor


def test_feature_leakage():
    data = pd.DataFrame([dict(BASELINE,scenario_id=17,mode="TRANSFER",target=999,solver_metadata=1)])
    assert tuple(feature_matrix(data).columns) == FEATURES


def test_fixed_model_parameters():
    model = HistGradientBoostingRegressor(**HGB_PARAMETERS)
    assert model.get_params()["max_iter"] == 500
    assert model.get_params()["learning_rate"] == .05
    assert model.get_params()["max_leaf_nodes"] == 31
    assert model.get_params()["min_samples_leaf"] == 20
    assert model.get_params()["l2_regularization"] == 1e-3
    assert model.get_params()["random_state"] == 42


def test_metrics_no_clipping_and_degenerate_spread():
    result = metrics([0,1],[-1,2])
    assert result["MAE"] == 1
    assert not passes("invest_prob_C",result)
    assert math.isnan(metrics([0,0,0],[0,0,0])["NMAE"])
    assert not passes("system_npv",dict(R2=1,NMAE=math.nan))


def test_all_gate_thresholds():
    assert passes("system_npv",dict(R2=.98,NMAE=.05))
    assert not passes("value_C",dict(R2=.979,NMAE=.01))
    assert passes("invest_prob_C",dict(MAE=.03))
    assert passes("expected_tau_C_conditional",dict(MAE=1.0))
    assert passes("mean_co2_price_conditional",dict(R2=.95,NMAE=.08))
