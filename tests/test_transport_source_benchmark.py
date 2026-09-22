import copy
import json

import pytest

from src.config import BASELINE, CONFIG, MODES, ROOT
from src.economics import stage_outcome


@pytest.mark.parametrize("mode", MODES)
def test_source_transport_charge_and_internal_payment(monkeypatch, mode):
    approved = json.loads((ROOT / "config/source_backed_approved_inputs.json").read_text(encoding="utf-8"))
    config = copy.deepcopy(CONFIG)
    config["transport_market"].update(approved["transport_market"])
    monkeypatch.setattr("src.economics.CONFIG", config)
    monkeypatch.setattr("src.bargaining.CONFIG", config)
    charged = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    quantity = charged.q_u + charged.q_s
    assert quantity == pytest.approx(.50)
    assert config["transport_market"]["variable_opex_per_ton"] == 28.1656
    if mode == "TRANSFER":
        assert charged.profits[2] == pytest.approx((125 - 28.1656) * quantity)
        changed_price = stage_outcome(mode, dict(BASELINE, transport_market_price=150),
                                      1000, (1, 1), (0, 0))
        assert changed_price.profits[3] == pytest.approx(charged.profits[3])
        assert changed_price.profits[2] - charged.profits[2] == pytest.approx(25 * quantity)
    config["transport_market"]["variable_opex_per_ton"] = 0
    no_transport_charge = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert no_transport_charge.profits[3] - charged.profits[3] == pytest.approx(28.1656 * quantity)
