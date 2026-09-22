"""Absolute static-accounting budget, in the model's million-CNY units."""
import math

from .config import SOURCE_BACKED

# User decision 2026-09-22: static discrepancies no greater than 100 CNY.
SOURCE_STATIC_ERROR_LIMIT_CNY = 100.0
SOURCE_STATIC_ERROR_LIMIT = SOURCE_STATIC_ERROR_LIMIT_CNY / 1_000_000


def static_accounting_passes(error):
    if not math.isfinite(error) or error < 0:
        return False
    if SOURCE_BACKED:
        return error <= SOURCE_STATIC_ERROR_LIMIT
    return error < 1e-10
