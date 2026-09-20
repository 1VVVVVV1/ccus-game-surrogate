"""Finite-horizon backward equilibrium, with no policy reuse across scenarios."""
from dataclasses import dataclass
import numpy as np
from .config import GAMMA
from .economics import stage_outcome
from .stage_game import solve_stage
from .state import STATES, actions, next_state


@dataclass
class BackwardSolution:
    values: np.ndarray
    policy: dict
    outcomes: dict
    max_accounting_error: float


def backward_solve(mode, scenario, prices, p, horizon=30, outcome_function=stage_outcome):
    values = np.zeros((horizon + 1, horizon + 1, 2, 2, 4))
    policy, outcomes = {}, {}
    max_error = 0.0
    for t in reversed(range(horizon)):
        for j in range(t + 1):
            for x_c, x_u in STATES:
                state = (x_c, x_u)
                key = (t, j, x_c, x_u)
                payoffs = {}
                for action in actions(state):
                    outcome = outcome_function(mode, scenario, prices[t, j], state, action)
                    outcomes[key + action] = outcome
                    max_error = max(max_error, outcome.accounting_error)
                    nc, nu = next_state(state, action)
                    continuation = p * values[t+1, j+1, nc, nu] + (1-p) * values[t+1, j, nc, nu]
                    profits = np.asarray(outcome.profits)
                    if mode == "STATE_OWNED":
                        profits = profits.copy()
                        profits[2] = 0.0  # inapplicable reporting value is never used in decisions
                    payoffs[action] = profits + GAMMA * continuation
                equilibrium = solve_stage(payoffs, mode)
                policy[key] = equilibrium
                values[t, j, x_c, x_u] = sum(prob * payoffs[a] for a, prob in equilibrium.actions)
    return BackwardSolution(values, policy, outcomes, max_error)
