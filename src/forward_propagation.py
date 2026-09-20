"""Independent forward state/action probability propagation and reporting."""

from dataclasses import dataclass
from math import fsum, isfinite, nan
import numpy as np
from .config import GAMMA
from .state import STATES, next_state


@dataclass(frozen=True)
class EquilibriumStateMass:
    probability: float
    equilibrium_type: str
    pure_ne_count: int


def annual_equilibrium_complexity(states, mode):
    """Return reachable mixed/multiple-pure mass before equilibrium selection.

    pure_ne_count is the number before Pareto filtering and tie-breaking.
    MIXED_NASH identifies a successfully solved interior mixed equilibrium.
    """
    if mode == "STATE_OWNED":
        return 0.0, 0.0
    reachable = [state for state in states if state.probability > 0.0]
    mixed = fsum(
        state.probability
        for state in reachable
        if state.pure_ne_count == 0 and state.equilibrium_type == "MIXED_NASH"
    )
    multiple = fsum(
        state.probability for state in reachable if state.pure_ne_count > 1
    )
    return mixed, multiple


def equilibrium_complexity_summary(years, mode):
    """Average annual state probabilities over all decision years.

    Formal runs supply exactly 30 years. A synthetic solver test may supply
    a shorter horizon. No history flag is added to the game state.
    """
    annual = [annual_equilibrium_complexity(states, mode) for states in years]
    horizon = len(annual)
    mixed_years = fsum(mixed for mixed, _ in annual)
    multiple_years = fsum(multiple for _, multiple in annual)
    return {
        "mixed_equilibrium_state_probability": mixed_years / horizon,
        "multiple_pure_equilibrium_state_probability": multiple_years / horizon,
        "expected_mixed_equilibrium_years": mixed_years,
        "expected_multiple_pure_equilibrium_years": multiple_years,
    }


class TransactionAccumulator:
    """The same realized trade indicator weights prices and annual frequencies."""

    def __init__(self, mode):
        self.mode = mode
        self.co2_denominator = 0.0
        self.co2_numerator = 0.0
        self.storage_denominator = 0.0
        self.storage_numerator = 0.0

    def add(self, state_probability, action_probability, outcome):
        weight = state_probability * action_probability
        if self.mode != "STATE_OWNED" and outcome.q_u > 0 and outcome.co2_matched and isfinite(outcome.co2_price):
            self.co2_denominator += weight
            self.co2_numerator += weight * outcome.co2_price
        if self.mode == "TRANSFER" and outcome.q_s > 0 and outcome.storage_matched and isfinite(outcome.storage_fee):
            self.storage_denominator += weight
            self.storage_numerator += weight * outcome.storage_fee

    def summary(self, horizon=30):
        co2_applicable = self.mode != "STATE_OWNED"
        storage_applicable = self.mode == "TRANSFER"
        return {
            "co2_trade_year_probability": self.co2_denominator / horizon if co2_applicable else nan,
            "storage_trade_year_probability": self.storage_denominator / horizon if storage_applicable else nan,
            "mean_co2_price_conditional": self.co2_numerator / self.co2_denominator if co2_applicable and self.co2_denominator >= 1e-12 else nan,
            "mean_storage_fee_conditional": self.storage_numerator / self.storage_denominator if storage_applicable and self.storage_denominator >= 1e-12 else nan,
        }


def forward_propagate(solution, p, mode, horizon=30):
    mass = np.zeros((horizon + 1, horizon + 1, 2, 2))
    mass[0, 0, 0, 0] = 1.0
    investment = np.zeros((horizon, 2))
    npv = np.zeros(4)
    active_years = total_u = total_s = 0.0
    trade = TransactionAccumulator(mode)
    complexity_years, policy_rows = [], []
    for t in range(horizon):
        year_complexity = []
        for j in range(t + 1):
            for x_c, x_u in STATES:
                state_probability = mass[t, j, x_c, x_u]
                if state_probability <= 0:
                    continue
                key = (t, j, x_c, x_u)
                equilibrium = solution.policy[key]
                year_complexity.append(EquilibriumStateMass(float(state_probability), equilibrium.equilibrium_type, equilibrium.pure_ne_count))
                for action, action_probability in equilibrium.actions:
                    weight = state_probability * action_probability
                    outcome = solution.outcomes[key + action]
                    profits = np.asarray(outcome.profits)
                    if mode == "STATE_OWNED":
                        profits = profits.copy()
                        profits[2] = 0.0
                    npv += GAMMA**t * weight * profits
                    trade.add(state_probability, action_probability, outcome)
                    active_years += weight * (outcome.q_u + outcome.q_s > 0)
                    total_u += weight * outcome.q_u
                    total_s += weight * outcome.q_s
                    investment[t, 0] += weight * action[0]
                    investment[t, 1] += weight * action[1]
                    nc, nu = next_state((x_c, x_u), action)
                    mass[t+1, j+1, nc, nu] += weight * p
                    mass[t+1, j, nc, nu] += weight * (1-p)
                policy_rows.append({"t": t, "j": j, "x_C": x_c, "x_U": x_u,
                                    "state_probability": float(state_probability),
                                    "equilibrium_type": equilibrium.equilibrium_type,
                                    "equilibrium_multiplicity": equilibrium.pure_ne_count,
                                    "equilibrium_selection_reason": equilibrium.equilibrium_selection_reason})
        complexity_years.append(year_complexity)
    mass_errors = [abs(float(mass[t].sum()) - 1.0) for t in range(horizon+1)]
    if max(mass_errors) > 1e-12:
        raise RuntimeError("PROBABILITY_MASS_ERROR")
    initial = solution.values[0, 0, 0, 0]
    indices = (3,) if mode == "STATE_OWNED" else (0, 1, 2, 3)
    value_error = max(abs(float(initial[i] - npv[i])) for i in indices)
    if not value_error < 1e-8:
        raise RuntimeError("DYNAMIC_VALUE_ACCOUNTING_FAILURE")
    result = {"system_npv": float(npv[3]), "value_C": float(npv[0]),
              "value_U": float(npv[1]), "value_T": float(npv[2]) if mode != "STATE_OWNED" else nan,
              "expected_active_years": float(active_years),
              "expected_total_quantity": float(total_u + total_s),
              "expected_total_utilization": float(total_u), "expected_total_storage": float(total_s),
              "max_static_accounting_error": solution.max_accounting_error,
              "max_backward_forward_value_error": value_error,
              "max_probability_mass_error": max(mass_errors)}
    for i, agent in enumerate(("C", "U")):
        probability = float(investment[:, i].sum())
        result[f"invest_prob_{agent}"] = probability
        result[f"never_invest_prob_{agent}"] = 1 - probability
        result[f"expected_tau_{agent}_conditional"] = float(np.arange(horizon) @ investment[:, i] / probability) if probability >= 1e-12 else nan
    result.update(trade.summary(horizon))
    result.update(equilibrium_complexity_summary(complexity_years, mode))
    return result, {"annual_probability_mass": [float(mass[t].sum()) for t in range(horizon+1)],
                    "investment_time_probabilities": investment.tolist(),
                    "co2_trade_denominator": trade.co2_denominator,
                    "storage_trade_denominator": trade.storage_denominator,
                    "reachable_policy": policy_rows}
