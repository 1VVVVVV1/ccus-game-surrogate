"""Deterministic Pareto / payoff / investment / lexicographic selection."""
from .config import TIE_TOLERANCE


def select_pure(candidates, payoffs):
    if len(candidates) == 1:
        return candidates[0], "UNIQUE_PURE_NE"
    remaining = [a for a in candidates if not any(
        payoffs[b][0] >= payoffs[a][0] and payoffs[b][1] >= payoffs[a][1]
        and (payoffs[b][0] > payoffs[a][0] or payoffs[b][1] > payoffs[a][1])
        for b in candidates if b != a)]
    if len(remaining) == 1:
        return remaining[0], "PARETO_DOMINATED_REMOVAL"
    for reason, score in (("MAX_TOTAL_PAYOFF", lambda a: payoffs[a][0] + payoffs[a][1]),
                          ("MAX_MIN_PAYOFF", lambda a: min(payoffs[a][:2]))):
        best = max(score(a) for a in remaining)
        remaining = [a for a in remaining if best - score(a) <= TIE_TOLERANCE]
        if len(remaining) == 1:
            return remaining[0], reason
    fewest = min(sum(a) for a in remaining)
    remaining = [a for a in remaining if sum(a) == fewest]
    if len(remaining) == 1:
        return remaining[0], "MIN_INVESTMENT_COUNT"
    return min(remaining), "LEXICOGRAPHIC"
