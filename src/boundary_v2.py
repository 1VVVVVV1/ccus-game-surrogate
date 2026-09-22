"""Prescribed 1001-point exact grids followed by exact bisection."""
import math
import numpy as np

NO_CROSSING = 'No crossing detected on the prescribed 1001-point exact grid within the specified domain.'
BOUNDARY_TARGETS = {
    'COMMIT_NOW_SYSTEM_NPV_ZERO': ('commit_now_system_npv', 0.0),
    'COMMIT_NOW_C_VALUE_ZERO': ('commit_now_value_C', 0.0),
    'COMMIT_NOW_U_VALUE_ZERO': ('commit_now_value_U', 0.0),
    'C_INVEST_PROB_50': ('invest_prob_C', .5),
    'U_INVEST_PROB_50': ('invest_prob_U', .5),
    'CO2_PRICE_ZERO': ('mean_co2_price_conditional', 0.0),
    'STORAGE_FEE_ZERO': ('mean_storage_fee_conditional', 0.0),
}


def exact_grid_search(exact, lower, upper, threshold=0.0, probability=False):
    grid = lower + np.arange(1001) * (upper-lower)/1000
    responses = [float(exact(float(z))) for z in grid]
    roots, audit = [], []
    for i, (z, value) in enumerate(zip(grid, responses)):
        if not math.isfinite(value):
            continue
        if value == threshold:
            if i and responses[i-1] == threshold:
                raise RuntimeError('UNDEFINED_RESEARCH_CHOICE: zero plateau boundary definition')
            roots.append(dict(boundary_value=float(z), response_at_boundary=value,
                              bracket_lower=float(z), bracket_upper=float(z),
                              response_lower=value, response_upper=value, iterations=0,
                              crossing_type='EXACT_LEVEL' if probability else 'EXACT_ROOT'))
        if i == 0:
            continue
        left, right = float(grid[i-1]), float(z)
        yl, yr = responses[i-1], value
        if not math.isfinite(yl) or (yl-threshold)*(yr-threshold) >= 0:
            continue
        iterations = 0
        hit = None
        while right-left > 1e-5*(upper-lower):
            middle = (left+right)/2
            ym = float(exact(middle))
            iterations += 1
            audit.append(dict(z=middle, response=ym))
            if not math.isfinite(ym):
                raise RuntimeError('UNDEFINED_RESEARCH_CHOICE: NaN inside exact refinement bracket')
            if ym == threshold or (probability and abs(ym-threshold) <= 1e-8):
                hit = (middle, ym)
                break
            if (yl-threshold)*(ym-threshold) < 0:
                right, yr = middle, ym
            else:
                left, yl = middle, ym
        middle = hit[0] if hit else (left+right)/2
        ym = hit[1] if hit else float(exact(middle))
        if not math.isfinite(ym):
            raise RuntimeError('UNDEFINED_RESEARCH_CHOICE: NaN at refined boundary')
        if probability and abs(ym-threshold) > 1e-8:
            row = dict(crossing_type='JUMP_CROSSING', boundary_lower=left,
                       boundary_upper=right, boundary_midpoint=middle,
                       response_lower=yl, response_upper=yr, iterations=iterations)
        else:
            row = dict(crossing_type='EXACT_LEVEL' if probability else 'EXACT_BISECTION',
                       boundary_value=middle, response_at_boundary=ym,
                       bracket_lower=left, bracket_upper=right,
                       response_lower=yl, response_upper=yr, iterations=iterations)
        roots.append(row)
    for i, row in enumerate(roots):
        row.update(found=True, root_index=i+1, root_count=len(roots))
    return dict(found=bool(roots), roots=roots, grid=grid.tolist(), responses=responses,
                refinement_evaluations=audit, explanation=None if roots else NO_CROSSING)
