import math
import pytest

from src.boundary_v2 import exact_grid_search, NO_CROSSING


def test_continuous_bisection():
    r = exact_grid_search(lambda x: x-.314159, 0, 1)['roots'][0]
    assert abs(r['boundary_value']-.314159) <= 1e-5
    assert r['bracket_upper']-r['bracket_lower'] <= 1e-5


def test_jump_is_not_reported_as_root():
    r = exact_grid_search(lambda x: .2 if x < .314159 else .8, 0, 1, .5, True)['roots'][0]
    assert r['crossing_type'] == 'JUMP_CROSSING'
    assert 'boundary_value' not in r
    assert r['response_lower'] < .5 < r['response_upper']


def test_exact_level():
    r = exact_grid_search(lambda x: x, 0, 1, .5, True)['roots'][0]
    assert r['crossing_type'] == 'EXACT_LEVEL'
    assert r['boundary_value'] == .5


def test_all_multiple_crossings_retained():
    r = exact_grid_search(lambda x: (x-.2134)*(x-.6789), 0, 1)
    assert len(r['roots']) == 2
    assert all(x['root_count'] == 2 for x in r['roots'])


def test_no_grid_crossing_is_not_a_global_proof():
    r = exact_grid_search(lambda x: x+1, 0, 1)
    assert not r['found']
    assert r['explanation'] == NO_CROSSING
    assert len(r['grid']) == 1001


def test_nan_breaks_intervals():
    r = exact_grid_search(lambda x: math.nan if .49 <= x <= .51 else x-.5, 0, 1)
    assert not r['found']


def test_exact_grid_needs_no_surrogate_proposal():
    # A constant surrogate would miss this narrow negative region entirely.
    r = exact_grid_search(lambda x: (x-.5005)**2-1e-6, 0, 1)
    assert len(r['roots']) == 2


def test_plateau_requires_research_decision():
    with pytest.raises(RuntimeError, match='UNDEFINED_RESEARCH_CHOICE'):
        exact_grid_search(lambda x: 0, 0, 1)
