import copy
import json

import pytest

from src.config import BASELINE, CONFIG, MODES, ROOT
from src.economics import stage_outcome
from src.eor_cost_calibration import integrated_downstream_capex
from src.state import actions, next_state


@pytest.fixture
def source_capex_config(monkeypatch):
    config = copy.deepcopy(CONFIG)
    approved = json.loads((ROOT / "config/source_backed_approved_inputs.json").read_text(encoding="utf-8"))
    config["utilization_storage"]["capex_initial"] = approved["utilization_storage"]["capex_initial"]
    monkeypatch.setattr("src.economics.CONFIG", config)
    monkeypatch.setattr("src.bargaining.CONFIG", config)
    return config


def test_reference_capacity_mapping():
    assert integrated_downstream_capex(1063, .70, .50) == 759.2857142857143


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("multiplier", [1.0, .7, 1.3])
def test_platform_capex_payment_and_multiplier(source_capex_config, mode, multiplier):
    scenario = dict(BASELINE, capex_U_multiplier=multiplier)
    invest = stage_outcome(mode, scenario, 1000, (1, 0), (0, 1))
    wait = stage_outcome(mode, scenario, 1000, (1, 0), (0, 0))
    expected = 759.2857142857143 * multiplier
    assert wait.profits[3] - invest.profits[3] == expected
    if mode == "TRANSFER":
        assert wait.profits[1] - invest.profits[1] == expected
    elif mode == "JOINT_VENTURE":
        for index, name in enumerate(("theta_C", "theta_U", "theta_T")):
            assert wait.profits[index] - invest.profits[index] == pytest.approx(
                expected * source_capex_config["joint_venture"][name])


@pytest.mark.parametrize("xi", [.20, .30])
def test_routing_split_changes_flows_but_not_capex(source_capex_config, xi):
    source_capex_config["co2_quantity"]["utilization_fraction"] = xi
    flow = stage_outcome("STATE_OWNED", BASELINE, 1000, (1, 1), (0, 0))
    assert flow.q_u == pytest.approx(.50 * xi)
    assert flow.q_s == pytest.approx(.50 * (1 - xi))
    payment = stage_outcome("STATE_OWNED", BASELINE, 1000, (1, 0), (0, 1))
    assert payment.profits[3] == -759.2857142857143


def test_investment_paid_once(source_capex_config):
    state = (1, 0)
    first = stage_outcome("STATE_OWNED", BASELINE, 1000, state, (0, 1))
    built = next_state(state, (0, 1))
    assert actions(built) == ((0, 0),)
    operating = stage_outcome("STATE_OWNED", BASELINE, 1000, built, (0, 0))
    source_capex_config["utilization_storage"]["capex_initial"] *= 2
    unchanged = stage_outcome("STATE_OWNED", BASELINE, 1000, built, (0, 0))
    assert operating.profits[3] == unchanged.profits[3]
    assert first.profits[3] == -759.2857142857143


@pytest.mark.parametrize("cost_change", ["storage_opex", "transport_cost", "pipeline_capex"])
def test_other_costs_do_not_change_platform_investment(source_capex_config, cost_change):
    if cost_change == "storage_opex":
        source_capex_config["utilization_storage"]["storage_cost_per_ton"] = 999
    elif cost_change == "transport_cost":
        source_capex_config["transport_market"]["variable_opex_per_ton"] = 999
    else:
        # Hypothetical reference metadata only; no new pipeline charge is introduced.
        source_capex_config["transport_market"]["pipeline_capex_reference"] = 999
    assert source_capex_config["utilization_storage"]["capex_initial"] == 759.2857142857143
    payment = stage_outcome("STATE_OWNED", BASELINE, 1000, (1, 0), (0, 1))
    assert payment.profits[3] == -759.2857142857143


def test_registered_value_matches_boundary_decision():
    decision = json.loads((ROOT / "config/U_CAPEX_ASSET_BOUNDARY_DECISION.json").read_text(encoding="utf-8"))
    approved = json.loads((ROOT / "config/source_backed_approved_inputs.json").read_text(encoding="utf-8"))
    assert decision["classification"] == "PIPELINE_EXCLUDED"
    assert decision["pipeline_capex_million_cny"] is None
    assert integrated_downstream_capex(decision["net_reference_u_capex_million_cny"],
                                      decision["reference_capacity_mt_per_year"], .50) == approved["utilization_storage"]["capex_initial"]
