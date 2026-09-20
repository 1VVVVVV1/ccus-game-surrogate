import pytest
from src.stage_game import pure_nash, solve_stage


def test_matching_pennies():
    game = {(0,0):(1,-1),(0,1):(-1,1),(1,0):(-1,1),(1,1):(1,-1)}
    assert pure_nash(game) == []
    result = solve_stage(game,"TRANSFER")
    assert result.equilibrium_type == "MIXED_NASH"
    assert result.pure_ne_count == 0
    probabilities = dict(result.actions)
    assert sum(probabilities.values()) == pytest.approx(1,abs=1e-10)
    assert probabilities[(1,0)] + probabilities[(1,1)] == pytest.approx(.5,abs=1e-10)
    assert probabilities[(0,1)] + probabilities[(1,1)] == pytest.approx(.5,abs=1e-10)


def test_asymmetric_mixed_indifference():
    game = {(0,0):(2,-2),(0,1):(-1,1),(1,0):(-2,2),(1,1):(3,-3)}
    result = solve_stage(game,"TRANSFER")
    probabilities = dict(result.actions)
    pc = probabilities[(1,0)] + probabilities[(1,1)]
    pu = probabilities[(0,1)] + probabilities[(1,1)]
    assert 2*(1-pu)-pu == pytest.approx(-2*(1-pu)+3*pu)
    assert -2*(1-pc)+2*pc == pytest.approx(1*(1-pc)-3*pc)
