from math import isnan, nan
import pytest
from src.economics import Outcome
from src.forward_propagation import TransactionAccumulator


def outcome(q_u=0.1, q_s=0.4, matched=True, price=150.0):
    return Outcome((0,0,0,0), q_u, q_s, price, 20.0, matched, matched, 0)


@pytest.mark.parametrize("years,expected", [(0,0.0),(15,0.5),(30,1.0)])
def test_transaction_frequency(years, expected):
    trade = TransactionAccumulator("TRANSFER")
    for t in range(30):
        trade.add(1.0, 1.0, outcome(q_u=0.1 if t < years else 0))
    summary = trade.summary()
    assert summary["co2_trade_year_probability"] == expected
    if not years:
        assert isnan(summary["mean_co2_price_conditional"])
    assert abs(trade.co2_denominator - 30 * summary["co2_trade_year_probability"]) < 1e-12
    assert abs(trade.storage_denominator - 30 * summary["storage_trade_year_probability"]) < 1e-12


def test_mixed_action_weighting():
    trade = TransactionAccumulator("TRANSFER")
    trade.add(1.0, 0.25, outcome())
    trade.add(1.0, 0.75, outcome(q_u=0))
    assert trade.co2_denominator == 0.25


def test_state_weighting():
    trade = TransactionAccumulator("TRANSFER")
    trade.add(0.3, 1.0, outcome())
    trade.add(0.7, 1.0, outcome(q_u=0))
    assert trade.co2_denominator == 0.3


def test_jv_applicability():
    trade = TransactionAccumulator("JOINT_VENTURE")
    trade.add(1, 1, outcome())
    result = trade.summary()
    assert result["co2_trade_year_probability"] == 1/30
    assert isnan(result["storage_trade_year_probability"])
    assert isnan(result["mean_storage_fee_conditional"])


def test_soe_positive_flow_is_not_trade():
    trade = TransactionAccumulator("STATE_OWNED")
    trade.add(1, 1, outcome())
    assert all(isnan(value) for value in trade.summary().values())


@pytest.mark.parametrize("actual", [outcome(matched=False), outcome(q_u=0,q_s=0)])
def test_applicable_but_no_realized_trade(actual):
    trade = TransactionAccumulator("TRANSFER")
    for _ in range(30):
        trade.add(1, 1, actual)
    assert trade.summary()["co2_trade_year_probability"] == 0.0
    assert trade.summary()["storage_trade_year_probability"] == 0.0
    assert isnan(trade.summary()["mean_co2_price_conditional"])


def test_price_and_frequency_use_identical_weights():
    trade = TransactionAccumulator("TRANSFER")
    trade.add(0.3, 0.25, outcome(price=-100))
    trade.add(0.7, 0.5, outcome(price=200))
    trade.add(0.3, 0.75, outcome(price=nan))
    result = trade.summary()
    assert result["mean_co2_price_conditional"] == pytest.approx((-100*.075+200*.35)/.425)
    assert trade.co2_denominator == pytest.approx(.425)
    assert abs(trade.co2_denominator - 30*result["co2_trade_year_probability"]) < 1e-12
    assert abs(trade.storage_denominator - 30*result["storage_trade_year_probability"]) < 1e-12
