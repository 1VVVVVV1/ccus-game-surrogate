"""User-defined fresh-CO2 conversion; oil prices must already be CNY/t-oil."""
import math


EOR_CO2_OIL_RATIO = 4.0


def incremental_oil_tonnes(fresh_co2_tonnes):
    if not math.isfinite(fresh_co2_tonnes) or fresh_co2_tonnes < 0:
        raise ValueError("Fresh CO2 must be finite and nonnegative")
    return fresh_co2_tonnes / EOR_CO2_OIL_RATIO


def revenue_per_fresh_co2_tonne(oil_price_cny_per_tonne):
    if not math.isfinite(oil_price_cny_per_tonne) or oil_price_cny_per_tonne < 0:
        raise ValueError("Oil price must be finite and nonnegative, in CNY/t-oil")
    return oil_price_cny_per_tonne / EOR_CO2_OIL_RATIO
