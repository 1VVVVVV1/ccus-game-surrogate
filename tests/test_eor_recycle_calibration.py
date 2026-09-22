import copy
import json

import pytest

from src.config import BASELINE, CONFIG, ROOT, MODES
from src.economics import stage_outcome
from src.eor_recycle_calibration import EOR_RECYCLE_RATIO, eor_co2_handling
from src.eor_revenue_calibration import incremental_oil_tonnes


@pytest.mark.parametrize("key,value", [
    ("recycled_co2_tonnes", 1), ("total_injected_co2_tonnes", 2),
    ("injection_electricity_kwh", 20.4), ("recycling_electricity_kwh", 38),
    ("combined_electricity_kwh", 58.4), ("co2_handling_cost_usd_2019", 4.964)])
def test_one_fresh_tonne(key, value):
    assert eor_co2_handling(1)[key] == pytest.approx(value)


def test_no_fresh_flow_no_handling_cost():
    assert all(value == 0 for value in eor_co2_handling(0).values())


@pytest.mark.parametrize("mode", MODES)
def test_internal_workload_does_not_change_external_accounting(monkeypatch, mode):
    config = copy.deepcopy(CONFIG)
    monkeypatch.setattr("src.economics.CONFIG", config)
    monkeypatch.setattr("src.bargaining.CONFIG", config)
    before = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    config["utilization_storage"]["eor_recycle_ratio"] = EOR_RECYCLE_RATIO
    workload = eor_co2_handling(before.q_u * 1e6)
    assert workload["total_injected_co2_tonnes"] == 2 * before.q_u * 1e6
    after = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert (after.q_u, after.q_s) == (before.q_u, before.q_s)
    assert after.profits == pytest.approx(before.profits, nan_ok=True)
    assert after.q_u + after.q_s == pytest.approx(.5)
    assert incremental_oil_tonnes(after.q_u * 1e6) == pytest.approx(25000)
    # Explicitly isolate the carbon-price effect for the sovereign mode.
    if mode == "STATE_OWNED":
        raised = stage_outcome(mode, BASELINE, 1001, (1, 1), (0, 0))
        assert raised.profits[3] - after.profits[3] == pytest.approx(.5 * BASELINE["effective_abatement_fraction"])


def test_approved_ratio_has_no_figure_dependency(monkeypatch):
    approved = json.loads((ROOT / "config/source_backed_approved_inputs.json").read_text(encoding="utf-8"))
    assert approved["utilization_storage"]["eor_recycle_ratio"] == EOR_RECYCLE_RATIO == 1
    monkeypatch.setattr(type(ROOT), "read_text", lambda *a, **k: (_ for _ in ()).throw(AssertionError("figure read")))
    assert eor_co2_handling(1)["recycled_co2_tonnes"] == 1
