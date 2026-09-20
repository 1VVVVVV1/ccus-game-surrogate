import pytest
from src.config import BASELINE, MODES
from src.economics import stage_outcome
from src.state import next_state


def test_construction_lag():
    result = stage_outcome("TRANSFER", BASELINE, 1000, (0,1), (1,0))
    assert result.q_u + result.q_s == 0
    assert result.profits[0] == -450
    assert next_state((0,1),(1,0)) == (1,1)
    following = stage_outcome("TRANSFER", BASELINE, 1000, (1,1), (0,0))
    assert following.q_u + following.q_s == .5


@pytest.mark.parametrize("mode", MODES)
def test_independent_system_accounting(mode):
    result = stage_outcome(mode, BASELINE, 1000, (1,1), (0,0))
    # Hand calculation: carbon 350, application revenue 78, capture 120,
    # utilization 9.41654, storage 17.48786, transport real cost 62.5.
    assert result.profits[3] == pytest.approx(218.5956)
    assert result.accounting_error < 1e-10


def test_jv_capex_shares():
    result = stage_outcome("JOINT_VENTURE", BASELINE, 96.23, (0,0), (1,1))
    assert result.profits[:3] == pytest.approx((-245.1783,-147.10698,-98.07132))
