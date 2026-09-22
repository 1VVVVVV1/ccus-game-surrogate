import numpy as np
import pytest

from src.commit_now import commit_now_from_backward
from src.config import BASELINE, GAMMA, MODES
from src.dynamic_solver import backward_solve
from src.economics import stage_outcome


@pytest.mark.parametrize('mode', MODES)
def test_two_year_commitment_retains_lag_and_accounting(mode):
    prices = np.full((3, 3), 100.0)
    solution = backward_solve(mode, BASELINE, prices, .4, horizon=2)
    initial = stage_outcome(mode, BASELINE, 100, (0, 0), (1, 1))
    operating = stage_outcome(mode, BASELINE, 100, (1, 1), (0, 0))
    assert initial.q_u == initial.q_s == 0
    assert initial.profits[3] < 0
    assert solution.policy[(1, 0, 1, 1)].actions == (((0, 0), 1.0),)
    result = commit_now_from_backward(solution, .4, mode)
    assert result['commit_now_system_npv'] == pytest.approx(
        initial.profits[3] + GAMMA * operating.profits[3])
    assert result['commit_now_system_npv'] < 0
    if mode != 'STATE_OWNED':
        assert sum(result['commit_now_value_'+i] for i in ['C', 'U', 'T']) == pytest.approx(
            result['commit_now_system_npv'])
    else:
        assert set(result) == {'commit_now_system_npv'}
