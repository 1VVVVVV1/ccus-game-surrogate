import pytest

from src.forward_propagation import (
    EquilibriumStateMass,
    annual_equilibrium_complexity,
    equilibrium_complexity_summary,
)


def test_no_mixed_years():
    result = equilibrium_complexity_summary(
        [[EquilibriumStateMass(1.0, "PURE_NASH", 1)] for _ in range(30)],
        "TRANSFER",
    )
    assert result["mixed_equilibrium_state_probability"] == 0.0
    assert result["expected_mixed_equilibrium_years"] == 0.0


def test_all_mixed_years():
    result = equilibrium_complexity_summary(
        [[EquilibriumStateMass(1.0, "MIXED_NASH", 0)] for _ in range(30)],
        "TRANSFER",
    )
    assert result["mixed_equilibrium_state_probability"] == 1.0
    assert result["expected_mixed_equilibrium_years"] == 30.0
    assert result["multiple_pure_equilibrium_state_probability"] == 0.0


def test_ten_mixed_years():
    years = [[EquilibriumStateMass(1.0, "MIXED_NASH", 0)] for _ in range(10)]
    years += [[EquilibriumStateMass(1.0, "PURE_NASH", 1)] for _ in range(20)]
    result = equilibrium_complexity_summary(years, "JOINT_VENTURE")
    assert result["mixed_equilibrium_state_probability"] == 10 / 30
    assert result["expected_mixed_equilibrium_years"] == 10.0


def test_reachable_state_probability_weighting():
    states = [
        EquilibriumStateMass(0.3, "MIXED_NASH", 0),
        EquilibriumStateMass(0.7, "PURE_NASH", 1),
        EquilibriumStateMass(0.0, "MIXED_NASH", 0),
        EquilibriumStateMass(0.0, "PURE_NASH", 2),
    ]
    assert annual_equilibrium_complexity(states, "TRANSFER") == (0.3, 0.0)


def test_multiple_count_is_before_tie_break():
    state = EquilibriumStateMass(1.0, "PURE_NASH", 2)
    assert annual_equilibrium_complexity([state], "TRANSFER") == (0.0, 1.0)
    result = equilibrium_complexity_summary([[state] for _ in range(30)], "TRANSFER")
    assert result["multiple_pure_equilibrium_state_probability"] == 1.0
    assert result["expected_multiple_pure_equilibrium_years"] == 30.0


def test_state_owned_statistics_are_zero():
    result = equilibrium_complexity_summary(
        [[EquilibriumStateMass(1.0, "COOPERATIVE", 0)] for _ in range(30)],
        "STATE_OWNED",
    )
    assert all(value == 0.0 for value in result.values())


@pytest.mark.parametrize("mode", ["TRANSFER", "JOINT_VENTURE"])
def test_only_successfully_solved_mixed_is_counted(mode):
    assert annual_equilibrium_complexity(
        [EquilibriumStateMass(1.0, "MIXED_NE_NUMERIC_FAILURE", 0)], mode
    ) == (0.0, 0.0)


def test_multiple_probability_uses_forward_mass_not_state_count():
    states = [
        EquilibriumStateMass(0.2, "PURE_NASH", 2),
        EquilibriumStateMass(0.8, "PURE_NASH", 1),
    ]
    result = equilibrium_complexity_summary([states for _ in range(30)], "TRANSFER")
    assert result["multiple_pure_equilibrium_state_probability"] == pytest.approx(0.2)
    assert result["expected_multiple_pure_equilibrium_years"] == pytest.approx(6.0)
