# Exact boundary V2

The frozen design domains are searched using1001exact points z=L+k(U-L)/1000. There are16carbon-scale searches and45supplementary searches,61in total. The complete vector of exact outputs at a mode/variable grid is shared across its targets; each target uses all1001points. Surrogate predictions never determine candidate existence.

COMMIT_NOW forces both construction actions at t=0, with zero operational flow until t=1. It includes all CAPEX payments and retains negative values. Existing option-value boundaries remain historical method-validation artifacts.

Finite adjacent opposite-sign responses or exact threshold hits form candidates. NaN breaks a grid interval. Exact bisection stops at width<=1e-5of the full domain width or an exact threshold hit. Investment responses within1e-8of0.5 are EXACT_LEVEL; otherwise a refined straddling interval is JUMP_CROSSING, with lower/upper responses and midpoint, not an exact root. All crossings are retained.

Adjacent exact-zero points (a plateau) or NaN encountered inside a finite refinement bracket require a user decision; this workflow does not invent a plateau boundary convention.

found=false means only: No crossing detected on the prescribed1001-point exact grid within the specified domain. Minimum, maximum, closest grid point and endpoint responses are retained. A closest point is not a boundary.
