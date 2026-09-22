"""User-authorized capacity mapping; not a reproduction of Wei's cost model."""
import math


def integrated_downstream_capex(reference_capex, reference_capacity, model_capacity):
    """Map million CNY using total MtCO2/year capacities, independent of routing."""
    if not all(math.isfinite(x) and x > 0 for x in
               (reference_capex, reference_capacity, model_capacity)):
        raise ValueError("CAPEX and capacities must be finite and positive")
    return reference_capex * (model_capacity / reference_capacity)


def two_part_eor_opex(fresh_co2_tonnes, components, cny_per_usd,
                     baseline_eor_capacity_mt):
    """Historical reference only: superseded by decision014 scalar EOR O&M.

    Map 15 annual USD cost entries per audited component; never discount.

    Component IDs identify physical costs, not publications, so Li and Miao
    cannot both supply the same cost. This returns only the EOR fixed component,
    not the integrated platform's total fixed OPEX.
    """
    if len(fresh_co2_tonnes) != 15:
        raise ValueError("Reference lifecycle must contain 15 years")
    if not all(math.isfinite(x) and x >= 0 for x in fresh_co2_tonnes):
        raise ValueError("Fresh CO2 must be finite and nonnegative")
    fresh_total = math.fsum(fresh_co2_tonnes)
    if fresh_total <= 0 or not all(math.isfinite(x) and x > 0 for x in
                                  (cny_per_usd, baseline_eor_capacity_mt)):
        raise ValueError("Fresh total, FX and baseline capacity must be positive")
    fixed_ids = {"injection_well_maintenance", "injection_station_maintenance",
                 "distribution_pipeline_maintenance", "oil_production_maintenance",
                 "recovery_maintenance"}
    variable_ids = {"injection_electricity", "recycling_electricity",
                    "oil_variable_maintenance", "oil_electricity", "fluid_pumping"}
    seen = set()
    totals = {"fixed": 0.0, "variable": 0.0}
    for component in components:
        key = component["component"]
        if key in seen:
            raise ValueError("Duplicate physical cost component")
        seen.add(key)
        if component["cost_boundary"] != "OPEX_ONLY" or component["route"] != "EOR":
            raise ValueError("Only EOR OPEX_ONLY components are permitted")
        kind = component["fixed_or_variable"]
        allowed = fixed_ids if kind == "fixed" else variable_ids if kind == "variable" else set()
        if key not in allowed:
            raise ValueError("Component is not an audited EOR operating-cost category")
        costs = component["annual_cost_usd"]
        if len(costs) != 15 or not all(math.isfinite(x) and x >= 0 for x in costs):
            raise ValueError("Each component requires 15 finite nonnegative annual USD costs")
        totals[kind] += math.fsum(costs)
    return {
        "eor_fixed_opex_component": totals["fixed"] * cny_per_usd * baseline_eor_capacity_mt / fresh_total,
        "utilization_cost_per_ton": totals["variable"] * cny_per_usd / fresh_total,
        "scale_EOR_fixed": baseline_eor_capacity_mt / (fresh_total / 1e6 / 15),
    }
