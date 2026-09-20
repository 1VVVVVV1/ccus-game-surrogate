"""Surrogate-proposed brackets verified and refined with the exact solver."""
from pathlib import Path
import math
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from .config import FEATURES, DOMAIN, MODES, BASELINE
from .scenario_solver import solve_scenario
from .reproducibility import identity, sha256, read_json, write_json, write_csv

BOUNDARY_TARGETS = {
    "SYSTEM_NPV_ZERO":("system_npv",0.0), "C_VALUE_ZERO":("value_C",0.0),
    "U_VALUE_ZERO":("value_U",0.0), "C_INVEST_PROB_50":("invest_prob_C",.5),
    "U_INVEST_PROB_50":("invest_prob_U",.5), "CO2_PRICE_ZERO":("mean_co2_price_conditional",0.0),
    "STORAGE_FEE_ZERO":("mean_storage_fee_conditional",0.0),
}
APPLICABLE = {"TRANSFER":tuple(BOUNDARY_TARGETS),
              "JOINT_VENTURE":tuple(k for k in BOUNDARY_TARGETS if k != "STORAGE_FEE_ZERO"),
              "STATE_OWNED":("SYSTEM_NPV_ZERO","C_INVEST_PROB_50","U_INVEST_PROB_50")}


def crossing_brackets(grid, responses, threshold):
    brackets = []
    for i in range(len(grid)-1):
        left, right = responses[i]-threshold, responses[i+1]-threshold
        if not (math.isfinite(left) and math.isfinite(right)):
            continue
        if left == 0 and right == 0:
            raise RuntimeError("UNDEFINED_RESEARCH_CHOICE: zero plateau boundary definition")
        if left*right < 0 or left == 0 or right == 0:
            brackets.append((float(grid[i]),float(grid[i+1])))
    return brackets


def verify_bracket(exact, left, right, threshold, domain_width):
    yl, yr = exact(left), exact(right)
    audit = [{"z":left,"response":yl},{"z":right,"response":yr}]
    if not (math.isfinite(yl) and math.isfinite(yr)) or (yl-threshold)*(yr-threshold)>0:
        return None, "SURROGATE_FALSE_BRACKET", audit
    if yl == threshold and yr == threshold:
        raise RuntimeError("UNDEFINED_RESEARCH_CHOICE: exact zero plateau boundary definition")
    if yl == threshold:
        return (left,left,yl,yl), "EXACT_GRID_ROOT", audit
    if yr == threshold:
        return (right,right,yr,yr), "EXACT_GRID_ROOT", audit
    while right-left > 1e-4*domain_width:
        middle = (left+right)/2
        ym = exact(middle)
        audit.append({"z":middle,"response":ym})
        if not math.isfinite(ym):
            raise RuntimeError("UNDEFINED_RESEARCH_CHOICE: structurally undefined response within exact bracket")
        if ym == threshold:
            return (middle,middle,ym,ym),"EXACT_ROOT",audit
        if (yl-threshold)*(ym-threshold)<0:
            right,yr = middle,ym
        else:
            left,yl = middle,ym
    return (left,right,yl,yr),"EXACT_CROSSING_INTERVAL",audit


def search_boundaries(formal,resume=False):
    folder = Path(formal)/"boundaries"
    rows = []
    cache = {}
    for variable,(lower,upper) in zip(FEATURES,DOMAIN):
        for mode in MODES:
            targets = APPLICABLE[mode] if variable == "carbon_scale" else ("SYSTEM_NPV_ZERO","C_INVEST_PROB_50","U_INVEST_PROB_50")
            for boundary_type in targets:
                target,threshold = BOUNDARY_TARGETS[boundary_type]
                model_path = Path(formal)/"surrogate"/"models"/f"{mode}__{target}.joblib"
                label = f"{variable}__{mode}__{boundary_type}"
                record_path = folder/"verification"/f"{label}.json"
                frozen = {**identity(),"surrogate_hash":sha256(model_path),"variable":variable,"mode":mode,
                          "target":boundary_type,"interval":[lower,upper],"grid_size":401}
                if record_path.exists():
                    record = read_json(record_path)
                    if not resume or record["identity"] != frozen or not record["exact_verification_completed"]:
                        raise RuntimeError("FORMAL_ARTIFACT_ERROR: boundary resume")
                    if sha256(folder/"response_curves"/f"{label}.csv") != record["curve_hash"]:
                        raise RuntimeError("FORMAL_ARTIFACT_ERROR: boundary curve hash")
                    rows.extend(record["rows"])
                    continue
                grid = np.linspace(lower,upper,401)
                parameters = pd.DataFrame([dict(BASELINE,**{variable:float(z)}) for z in grid])
                model = joblib.load(model_path)
                with threadpool_limits(limits=1):
                    predicted = model.predict(parameters[list(FEATURES)])
                brackets = crossing_brackets(grid,predicted,threshold)
                def exact(z):
                    key = (mode,variable,z)
                    if key not in cache:
                        cache[key] = solve_scenario(dict(BASELINE,**{variable:z}),mode)
                    return cache[key][target]
                found, audit, false_brackets = [], [], []
                for left,right in brackets:
                    crossing,status,details = verify_bracket(exact,left,right,threshold,upper-lower)
                    audit.append({"surrogate_bracket":[left,right],"status":status,"evaluations":details})
                    if crossing is None:
                        false_brackets.append([left,right])
                    elif crossing not in found:
                        found.append(crossing)
                base = {"variable":variable,"mode":mode,"boundary_type":boundary_type,
                        "role":"main" if variable=="carbon_scale" else "supplementary",
                        "surrogate_false_brackets":len(false_brackets)}
                local = [{**base,"found":True,"boundary_value":(l+r)/2,"bracket_lower":l,"bracket_upper":r,
                          "response_lower":yl,"response_upper":yr,"closest_grid_value":math.nan,"closest_response":math.nan}
                         for l,r,yl,yr in found]
                if not local:
                    closest = int(np.nanargmin(np.abs(predicted-threshold)))
                    local = [{**base,"found":False,"boundary_value":math.nan,"bracket_lower":math.nan,
                              "bracket_upper":math.nan,"response_lower":math.nan,"response_upper":math.nan,
                              "closest_grid_value":float(grid[closest]),"closest_response":float(predicted[closest])}]
                curve_path = folder/"response_curves"/f"{label}.csv"
                write_csv(curve_path,pd.DataFrame({variable:grid,"surrogate_response":predicted,
                                                 "exact_response":[cache.get((mode,variable,float(z)),{}).get(target,math.nan) for z in grid]}))
                write_json(record_path,{"identity":frozen,"curve_hash":sha256(curve_path),"rows":local,
                                         "exact_verification_completed":True,"verification":audit,
                                         "false_brackets":false_brackets,"closest_response_source":"SURROGATE_GRID"})
                rows.extend(local)
                print(f"BOUNDARY {label}: {len(found)} exact crossing(s)",flush=True)
    result = pd.DataFrame(rows)
    path = folder/"boundary_results.csv"
    if not path.exists():
        write_csv(path,result)
    elif not resume:
        raise RuntimeError("FORMAL_ARTIFACT_ERROR: boundary output exists")
    return result
