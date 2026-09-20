"""Pure Nash, interior mixed Nash and centralized cooperative selection."""
from dataclasses import dataclass
import math
from .config import EQUILIBRIUM_TOLERANCE, TIE_TOLERANCE
from .equilibrium_selection import select_pure


@dataclass(frozen=True)
class Equilibrium:
    actions: tuple  # ((d_C, d_U), probability)
    equilibrium_type: str
    pure_ne_count: int
    equilibrium_selection_reason: str


def pure_nash(payoffs):
    return [a for a in payoffs if all(
        payoffs[a][0] >= payoffs[b][0] - EQUILIBRIUM_TOLERANCE
        for b in payoffs if b[1] == a[1]) and all(
        payoffs[a][1] >= payoffs[b][1] - EQUILIBRIUM_TOLERANCE
        for b in payoffs if b[0] == a[0])]


def solve_stage(payoffs, mode):
    if mode == "STATE_OWNED":
        best = max(v[3] for v in payoffs.values())
        candidates = [a for a in payoffs if best-payoffs[a][3] <= TIE_TOLERANCE]
        selected = min(candidates, key=lambda a: (sum(a), a))
        return Equilibrium(((selected, 1.0),), "COOPERATIVE", 0, "MAX_SYSTEM_MIN_INVEST_LEX")
    candidates = pure_nash(payoffs)
    if candidates:
        selected, reason = select_pure(candidates, payoffs)
        return Equilibrium(((selected, 1.0),), "PURE_NASH", len(candidates), reason)
    if set(payoffs) != {(0,0), (0,1), (1,0), (1,1)}:
        raise RuntimeError("MIXED_NE_NUMERIC_FAILURE")
    a00, a01, a10, a11 = (payoffs[a][0] for a in ((0,0),(0,1),(1,0),(1,1)))
    b00, b01, b10, b11 = (payoffs[a][1] for a in ((0,0),(0,1),(1,0),(1,1)))
    denominator_u = a01-a00-a11+a10
    denominator_c = b10-b00-b11+b01
    if denominator_u == 0 or denominator_c == 0:
        raise RuntimeError("MIXED_NE_NUMERIC_FAILURE")
    p_u = (a10-a00) / denominator_u
    p_c = (b01-b00) / denominator_c
    if not (math.isfinite(p_c) and math.isfinite(p_u) and 0 < p_c < 1 and 0 < p_u < 1):
        raise RuntimeError("MIXED_NE_NUMERIC_FAILURE")
    distribution = tuple((a, (p_c if a[0] else 1-p_c) * (p_u if a[1] else 1-p_u)) for a in payoffs)
    return Equilibrium(distribution, "MIXED_NASH", 0, "NO_PURE_INTERIOR_MIXED")
