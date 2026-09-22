"""Reference workload/energy check only; never adds formal EOR OPEX or flows."""
import math


EOR_RECYCLE_RATIO = 1.0


def eor_co2_handling(fresh_co2_tonnes):
    if not math.isfinite(fresh_co2_tonnes) or fresh_co2_tonnes < 0:
        raise ValueError("Fresh CO2 must be finite and nonnegative")
    recycled = EOR_RECYCLE_RATIO * fresh_co2_tonnes
    injected = fresh_co2_tonnes + recycled
    injection_kwh = 10.2 * injected
    recycling_kwh = 38 * recycled
    return {
        "recycled_co2_tonnes": recycled,
        "total_injected_co2_tonnes": injected,
        "injection_electricity_kwh": injection_kwh,
        "recycling_electricity_kwh": recycling_kwh,
        "combined_electricity_kwh": injection_kwh + recycling_kwh,
        "co2_handling_cost_usd_2019": (injection_kwh + recycling_kwh) * .085,
    }
