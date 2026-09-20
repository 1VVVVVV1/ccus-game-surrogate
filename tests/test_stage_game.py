from src.stage_game import solve_stage, pure_nash
from src.equilibrium_selection import select_pure


def test_unique_nash():
    game = {(0,0):(0,0), (0,1):(0,1), (1,0):(1,0), (1,1):(1,1)}
    result = solve_stage(game, "TRANSFER")
    assert result.actions == (((1,1),1.0),)
    assert result.pure_ne_count == 1


def test_coordination_pareto():
    game = {(0,0):(1,1), (0,1):(0,0), (1,0):(0,0), (1,1):(2,2)}
    assert len(pure_nash(game)) == 2
    result = solve_stage(game,"TRANSFER")
    assert result.pure_ne_count == 2
    assert result.actions == (((1,1),1.0),)
    assert result.equilibrium_selection_reason == "PARETO_DOMINATED_REMOVAL"


def test_all_tie_break_levels():
    cases = [
        ({(0,0):(1,1),(1,1):(2,2)}, (1,1), "PARETO_DOMINATED_REMOVAL"),
        ({(0,0):(5,1),(1,1):(2,3)}, (0,0), "MAX_TOTAL_PAYOFF"),
        ({(0,0):(4,0),(1,1):(2,2)}, (1,1), "MAX_MIN_PAYOFF"),
        ({(0,0):(2,2),(1,1):(2,2)}, (0,0), "MIN_INVESTMENT_COUNT"),
        ({(0,1):(2,2),(1,0):(2,2)}, (0,1), "LEXICOGRAPHIC"),
    ]
    for game, action, reason in cases:
        assert select_pure(list(game),game) == (action,reason)


def test_cooperative_tie_break():
    game = {a:(0,0,0,5) for a in ((0,0),(0,1),(1,0),(1,1))}
    assert solve_stage(game,"STATE_OWNED").actions == (((0,0),1.0),)
