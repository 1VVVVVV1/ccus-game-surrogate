import numpy as np
import pytest
from src.boundary import crossing_brackets, verify_bracket, APPLICABLE


def test_single_root():
    grid = np.linspace(0,1,401)
    brackets = crossing_brackets(grid,grid-.501,0)
    assert len(brackets)==1
    crossing,status,_ = verify_bracket(lambda x:x-.501,*brackets[0],0,1)
    assert crossing[0] <= .501 <= crossing[1]
    assert crossing[1]-crossing[0] <= 1e-4


def test_multiple_roots():
    grid = np.linspace(0,1,401)
    assert len(crossing_brackets(grid,(grid-.201)*(grid-.701),0))==2


def test_no_root():
    assert crossing_brackets([0,1],[2,3],0)==[]


def test_false_surrogate_bracket():
    crossing,status,_ = verify_bracket(lambda x:x+1,0,1,0,1)
    assert crossing is None
    assert status=="SURROGATE_FALSE_BRACKET"


def test_exact_investment_half_crossing():
    crossing,status,_ = verify_bracket(lambda x:.2 if x<.6 else .9,0,1,.5,1)
    assert crossing[0] <= .6 <= crossing[1]
    assert crossing[1]-crossing[0] <= 1e-4
    assert status=="EXACT_CROSSING_INTERVAL"


def test_undefined_zero_plateau_stops():
    with pytest.raises(RuntimeError,match="UNDEFINED_RESEARCH_CHOICE"):
        verify_bracket(lambda x:0,0,1,0,1)


def test_applicability_matrix():
    assert "STORAGE_FEE_ZERO" not in APPLICABLE["JOINT_VENTURE"]
    assert set(APPLICABLE["STATE_OWNED"])=={"SYSTEM_NPV_ZERO","C_INVEST_PROB_50","U_INVEST_PROB_50"}
