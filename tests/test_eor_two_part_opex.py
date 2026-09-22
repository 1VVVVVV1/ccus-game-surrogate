"""Synthetic unit fixtures verify mappings, not unverified literature values."""
import copy

import pytest

from src.config import BASELINE, CONFIG, MODES
from src.economics import stage_outcome
from src.eor_cost_calibration import two_part_eor_opex


def component(name, kind, annual, **changes):
    result = dict(component=name, fixed_or_variable=kind, route="EOR",
                  cost_boundary="OPEX_ONLY", annual_cost_usd=[annual] * 15)
    result.update(changes)
    return result


def test_two_part_mapping_keeps_fixed_out_of_unit_cost():
    result = two_part_eor_opex([1e6] * 15, [
        component("recovery_maintenance", "fixed", 2e6),
        component("injection_electricity", "variable", 3e6)], 7, .1)
    assert result["eor_fixed_opex_component"] == pytest.approx(1.4)
    assert result["utilization_cost_per_ton"] == pytest.approx(21)
    assert result["scale_EOR_fixed"] == pytest.approx(.1)


def test_recycling_cost_uses_only_fresh_denominator():
    # Synthetic fresh=1Mt/year, recycle=2Mt/year; cost=4USD/recycled tonne.
    result = two_part_eor_opex([1e6] * 15, [
        component("recycling_electricity", "variable", 2e6 * 4)], 7, .1)
    assert result["utilization_cost_per_ton"] == 56


@pytest.mark.parametrize("boundary", ["CAPEX_ONLY", "LEVELIZED_CAPEX_PLUS_OPEX"])
def test_capital_cannot_enter_opex(boundary):
    with pytest.raises(ValueError, match="OPEX_ONLY"):
        two_part_eor_opex([1e6] * 15, [component(
            "recovery_maintenance", "fixed", 1, cost_boundary=boundary)], 7, .1)


@pytest.mark.parametrize("route", ["TRANSPORT", "DEDICATED_STORAGE", "CAPTURE"])
def test_other_routes_cannot_enter_eor_cost(route):
    with pytest.raises(ValueError, match="Only EOR"):
        two_part_eor_opex([1e6] * 15, [component(
            "injection_electricity", "variable", 1, route=route)], 7, .1)


def test_li_miao_duplicate_component_rejected():
    with pytest.raises(ValueError, match="Duplicate"):
        two_part_eor_opex([1e6] * 15, [
            component("recovery_maintenance", "fixed", 1, source="Li2022"),
            component("recovery_maintenance", "fixed", 1, source="Miao2025")], 7, .1)


@pytest.fixture
def two_part_config(monkeypatch):
    config = copy.deepcopy(CONFIG)
    config["utilization_storage"]["fixed_opex"] = 1.4
    config["utilization_storage"]["utilization_cost_per_ton"] = 21
    monkeypatch.setattr("src.economics.CONFIG", config)
    monkeypatch.setattr("src.bargaining.CONFIG", config)
    return config


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("state", [(0, 0), (0, 1), (1, 1)])
def test_built_and_zero_flow_costs(two_part_config, mode, state):
    paid = stage_outcome(mode, BASELINE, 1000, state, (0, 0))
    two_part_config["utilization_storage"]["fixed_opex"] = 0
    fixed_removed = stage_outcome(mode, BASELINE, 1000, state, (0, 0))
    assert fixed_removed.profits[3] - paid.profits[3] == pytest.approx(1.4 * state[1])
    two_part_config["utilization_storage"]["utilization_cost_per_ton"] = 0
    all_removed = stage_outcome(mode, BASELINE, 1000, state, (0, 0))
    assert all_removed.profits[3] - fixed_removed.profits[3] == pytest.approx(21 * paid.q_u)


def test_doubling_route_flow_leaves_frozen_fixed_fee(two_part_config):
    first = stage_outcome("STATE_OWNED", BASELINE, 1000, (1, 1), (0, 0))
    two_part_config["co2_quantity"]["utilization_fraction"] = .4
    second = stage_outcome("STATE_OWNED", BASELINE, 1000, (1, 1), (0, 0))
    assert second.q_u == 2 * first.q_u
    assert 21 * second.q_u == 2 * (21 * first.q_u)
    assert two_part_config["utilization_storage"]["fixed_opex"] == 1.4
    assert second.q_u + second.q_s == .5  # No recycled stream added.


def test_failed_eor_bargain_retains_fixed_fee(two_part_config):
    two_part_config["utilization_storage"]["utilization_revenue_per_ton"] = 0
    two_part_config["utilization_storage"]["utilization_cost_per_ton"] = 1e6
    paid = stage_outcome("TRANSFER", BASELINE, 1000, (1, 1), (0, 0))
    assert paid.q_u == 0
    assert not paid.co2_matched
    two_part_config["utilization_storage"]["fixed_opex"] = 0
    removed = stage_outcome("TRANSFER", BASELINE, 1000, (1, 1), (0, 0))
    assert removed.profits[1] - paid.profits[1] == pytest.approx(1.4)
