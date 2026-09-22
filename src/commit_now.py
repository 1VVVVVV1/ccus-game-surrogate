"""Forced initial joint construction, retaining the one-year construction lag."""
import numpy as np

from .config import GAMMA


def commit_now_from_backward(backward, p, mode):
    initial = backward.outcomes[(0, 0, 0, 0, 1, 1)]
    profits = np.asarray(initial.profits).copy()
    if mode == 'STATE_OWNED':
        profits[2] = 0.0
    # Both facilities are built at t=1; these states have no investment choices.
    value = profits + GAMMA * (p * backward.values[1, 1, 1, 1]
                              + (1-p) * backward.values[1, 0, 1, 1])
    result = {'commit_now_system_npv': float(value[3])}
    if mode != 'STATE_OWNED':
        result.update(commit_now_value_C=float(value[0]),
                      commit_now_value_U=float(value[1]),
                      commit_now_value_T=float(value[2]))
    return result


def solve_commit_now_value(mode, scenario):
    from .carbon_tree import carbon_tree
    from .dynamic_solver import backward_solve
    prices, _, _, p = carbon_tree(scenario['carbon_scale'])
    return commit_now_from_backward(backward_solve(mode, scenario, prices, p), p, mode)
