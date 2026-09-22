"""4000 CNY/t-oil is a synthetic test input, not the formal oil price."""
import copy
import json

import pytest

from src.config import BASELINE, CONFIG, ROOT
from src.economics import stage_outcome
from src.eor_revenue_calibration import (EOR_CO2_OIL_RATIO, incremental_oil_tonnes,
                                         revenue_per_fresh_co2_tonne)


@pytest.mark.parametrize("fresh,oil", [(4, 1), (0, 0), (100000, 25000)])
def test_oil_conversion(fresh, oil):
    assert incremental_oil_tonnes(fresh) == oil
    assert fresh * revenue_per_fresh_co2_tonne(4000) == oil * 4000


def test_unit_revenue():
    assert revenue_per_fresh_co2_tonne(4000) == 1000


def test_doubling_fresh_doubles_oil_and_revenue():
    assert incremental_oil_tonnes(200000) == 2 * incremental_oil_tonnes(100000)
    assert 200000 * revenue_per_fresh_co2_tonne(4000) == 2 * 100000 * revenue_per_fresh_co2_tonne(4000)


@pytest.mark.parametrize("mode", ["TRANSFER", "JOINT_VENTURE", "STATE_OWNED"])
def test_existing_flow_and_bargaining_use_unit_revenue(monkeypatch, mode):
    config = copy.deepcopy(CONFIG)
    config["utilization_storage"]["utilization_revenue_per_ton"] = revenue_per_fresh_co2_tonne(4000)
    monkeypatch.setattr("src.economics.CONFIG", config)
    monkeypatch.setattr("src.bargaining.CONFIG", config)
    first = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert first.q_u == pytest.approx(.1)  # Model flow is Mt/year, not tonnes/year.
    assert incremental_oil_tonnes(first.q_u * 1e6) == pytest.approx(25000)
    config["co2_quantity"]["recycled_co2_reference"] = 99
    recycled_changed = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert recycled_changed.q_u == first.q_u
    assert recycled_changed.profits == pytest.approx(first.profits, nan_ok=True)
    config["co2_quantity"]["utilization_fraction"] = .4
    second = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert second.q_u == 2 * first.q_u
    assert EOR_CO2_OIL_RATIO == 4


def test_approved_ratio_is_independent_of_figure(monkeypatch):
    approved = json.loads((ROOT / "config/source_backed_approved_inputs.json").read_text(encoding="utf-8"))
    assert approved["utilization_storage"]["eor_co2_oil_ratio"] == EOR_CO2_OIL_RATIO == 4
    assert approved["utilization_storage"]["utilization_revenue_per_ton"] == pytest.approx(
        revenue_per_fresh_co2_tonne(90 * 7.1 * 6.8974))
    # No figure-file reads in the revenue calculation.
    monkeypatch.setattr(type(ROOT), "read_text", lambda *a, **k: (_ for _ in ()).throw(AssertionError("figure read")))
    assert incremental_oil_tonnes(100000) == 25000
    assert revenue_per_fresh_co2_tonne(4000) == 1000
