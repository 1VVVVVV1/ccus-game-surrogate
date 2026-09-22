"""Ground-truth scenario solution: no surrogate imports or calls."""
from .carbon_tree import carbon_tree
from .dynamic_solver import backward_solve
from .forward_propagation import forward_propagate
from .config import SOURCE_BACKED
from .commit_now import commit_now_from_backward


def solve_scenario(scenario, mode, details=False):
    prices, _, _, p = carbon_tree(scenario["carbon_scale"])
    backward = backward_solve(mode, scenario, prices, p)
    summary, diagnostics = forward_propagate(backward, p, mode)
    if SOURCE_BACKED:
        summary.update(commit_now_from_backward(backward, p, mode))
    summary.update(mode=mode, **scenario, solver_status="OK")
    summary["initial_equilibrium_type"] = backward.policy[(0,0,0,0)].equilibrium_type
    # Full state decisions are retained in baseline audit output, not ML features.
    if details:
        diagnostics["policy"] = [
            {"state": key, "equilibrium_type": eq.equilibrium_type,
             "equilibrium_multiplicity": eq.pure_ne_count,
             "equilibrium_selection_reason": eq.equilibrium_selection_reason,
             "actions": eq.actions} for key, eq in backward.policy.items()
        ]
        return summary, diagnostics
    return summary
