"""Frozen model configuration and protocol constants."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "model_config.game.json"
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
GAMMA = 1.0 / 1.08
MODES = ("TRANSFER", "JOINT_VENTURE", "STATE_OWNED")
FEATURES = (
    "transport_market_price", "effective_abatement_fraction", "storage_subsidy",
    "capex_C_multiplier", "capex_U_multiplier", "carbon_scale",
)
DOMAIN = tuple(tuple(CONFIG["scenario_domain"][name]) for name in FEATURES)
BASELINE = dict(zip(FEATURES, (125.0, 0.70, 0.0, 1.0, 1.0, 1.0)))
VALUE_TARGETS = ("system_npv", "value_C", "value_T", "value_U")
PROBABILITY_TARGETS = ("invest_prob_C", "invest_prob_U")
TIME_TARGETS = ("expected_tau_C_conditional", "expected_tau_U_conditional")
PRICE_TARGETS = ("mean_co2_price_conditional", "mean_storage_fee_conditional")
TARGETS = {
    "TRANSFER": VALUE_TARGETS + PROBABILITY_TARGETS + TIME_TARGETS + PRICE_TARGETS,
    "JOINT_VENTURE": VALUE_TARGETS + PROBABILITY_TARGETS + TIME_TARGETS + PRICE_TARGETS[:1],
    "STATE_OWNED": VALUE_TARGETS[:1] + PROBABILITY_TARGETS + TIME_TARGETS,
}
HGB_PARAMETERS = dict(learning_rate=0.05, max_iter=500, max_leaf_nodes=31,
                      min_samples_leaf=20, l2_regularization=1e-3, random_state=42)
EQUILIBRIUM_TOLERANCE = CONFIG["solver"]["equilibrium_tolerance"]
TIE_TOLERANCE = CONFIG["solver"]["tie_tolerance"]
