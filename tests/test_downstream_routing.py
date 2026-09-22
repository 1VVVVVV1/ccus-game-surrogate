import pytest

from src.bargaining import Bargain
from src.config import BASELINE, MODES
from src.economics import stage_outcome


@pytest.mark.parametrize("mode", MODES)
def test_routing_does_not_count_associated_storage_twice(mode):
    result = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert result.q_u == pytest.approx(0.10, abs=1e-12)
    assert result.q_s == pytest.approx(0.40, abs=1e-12)
    assert abs(result.q_u + result.q_s - 0.50) < 1e-12


def test_eor_only_has_no_storage_payment_or_subsidy(monkeypatch):
    # Isolate accounting with a successful EOR bargain and unavailable storage.
    monkeypatch.setattr("src.economics.operating_bargains",
                        lambda *args: (Bargain(True, 100), Bargain(False, float("nan"))))
    zero = stage_outcome("TRANSFER", BASELINE, 1000, (1, 1), (0, 0))
    subsidized = stage_outcome("TRANSFER", dict(BASELINE, storage_subsidy=80),
                              1000, (1, 1), (0, 0))
    assert zero.q_u == pytest.approx(0.10)
    assert zero.q_s == 0
    assert not zero.storage_matched
    # EOR revenue minus CO2 purchase and EOR operating cost, no storage payment.
    assert zero.profits[1] == pytest.approx((780 - 100 - 94.1654) * 0.10)
    assert subsidized.profits == pytest.approx(zero.profits)


def test_storage_payment_and_subsidy_apply_only_to_dedicated_flow(monkeypatch):
    def outcome(fee, subsidy):
        monkeypatch.setattr("src.economics.operating_bargains",
                            lambda *args: (Bargain(True, 100), Bargain(True, fee)))
        return stage_outcome("TRANSFER", dict(BASELINE, storage_subsidy=subsidy),
                             1000, (1, 1), (0, 0))

    base = outcome(10, 0)
    fee_changed = outcome(30, 0)
    subsidy_changed = outcome(10, 80)
    assert base.q_s == pytest.approx(0.40)
    assert fee_changed.profits[1] - base.profits[1] == pytest.approx(20 * 0.40)
    assert fee_changed.profits[0] - base.profits[0] == pytest.approx(-20 * 0.40)
    assert fee_changed.profits[3] == pytest.approx(base.profits[3])
    assert subsidy_changed.profits[1] - base.profits[1] == pytest.approx(80 * 0.40)
    assert subsidy_changed.profits[3] - base.profits[3] == pytest.approx(80 * 0.40)
