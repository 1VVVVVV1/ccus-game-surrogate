from math import nan
import numpy as np
import pytest
from src.config import GAMMA, BASELINE, MODES
from src.dynamic_solver import backward_solve
from src.economics import Outcome
from src.forward_propagation import forward_propagate
from src.scenario_solver import solve_scenario


def synthetic(mode, scenario, price, state, action):
    c = 10*state[0]*state[1] - 2*action[0]
    u = 10*state[0]*state[1] - 2*action[1]
    return Outcome((c,u,0,c+u), 0,0,nan,nan,False,False,0)


def test_two_year_hand_calculation():
    solution = backward_solve("TRANSFER", {}, np.ones((3,3)), .4, horizon=2, outcome_function=synthetic)
    # Year 1: built pair earns 10 each; no terminal investment is worthwhile.
    assert tuple(solution.values[1,0,1,1]) == (10,10,0,20)
    assert tuple(solution.values[1,0,0,0]) == (0,0,0,0)
    # Year 0: (wait,wait) and (invest,invest) are NE. Latter Pareto dominates.
    assert solution.policy[(0,0,0,0)].pure_ne_count == 2
    assert solution.policy[(0,0,0,0)].actions == (((1,1),1.0),)
    assert solution.values[0,0,0,0,0] == pytest.approx(-2+GAMMA*10)
    result, diagnostic = forward_propagate(solution,.4,"TRANSFER",horizon=2)
    assert result["system_npv"] == pytest.approx(-4+GAMMA*20)
    assert result["invest_prob_C"] == 1
    assert result["expected_tau_C_conditional"] == 0
    assert all(abs(m-1)<1e-12 for m in diagnostic["annual_probability_mass"])


@pytest.mark.parametrize("mode", MODES)
def test_baseline_backward_forward(mode):
    result = solve_scenario(BASELINE,mode)
    assert result["max_backward_forward_value_error"] < 1e-8
    assert result["max_probability_mass_error"] < 1e-12
    assert result["max_static_accounting_error"] < 1e-10
    assert result["solver_status"] == "OK"
