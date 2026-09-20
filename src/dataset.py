"""Exact datasets, strict integrity checks and 128-scenario checkpoints."""
from concurrent.futures import ProcessPoolExecutor
import math
import os
from pathlib import Path
import numpy as np
import pandas as pd
from .config import FEATURES, MODES, BASELINE
from .scenario_solver import solve_scenario
from .sobol_design import design
from .reproducibility import (identity, read_json, write_json, write_csv, sha256, append_progress)


def read_csv_with_schema(path, reference):
    """Restore checkpoint dtypes without rounding or relaxing value equality."""
    return pd.read_csv(path, float_precision="round_trip", dtype=reference.dtypes.to_dict())


def validate_rows(frame, expected_ids):
    expected_ids = set(expected_ids)
    failures = []
    if len(frame) != 3*len(expected_ids):
        failures.append("row_count")
    if set(frame.scenario_id) != expected_ids or frame.duplicated(["scenario_id","mode"]).any():
        failures.append("scenario_id_identity")
    if not all(set(group["mode"]) == set(MODES) for _, group in frame.groupby("scenario_id")):
        failures.append("mode_completeness")
    for _, row in frame.iterrows():
        if row.solver_status != "OK":
            failures.append(f"solver_status:{row.scenario_id}:{row['mode']}")
        mandatory = ("system_npv", "value_C", "value_U", "expected_active_years", "expected_total_quantity",
                     "expected_total_utilization", "expected_total_storage", "mixed_equilibrium_state_probability",
                     "multiple_pure_equilibrium_state_probability")
        if row["mode"] != "STATE_OWNED":
            mandatory += ("value_T",)
        if not all(math.isfinite(row[target]) for target in mandatory):
            failures.append(f"nonfinite:{row.scenario_id}:{row['mode']}")
        for agent in ("C", "U"):
            probability = row[f"invest_prob_{agent}"]
            if not math.isfinite(probability) or not 0 <= probability <= 1:
                failures.append(f"investment_probability:{row.scenario_id}:{row['mode']}:{agent}:{probability}")
            conditional = row[f"expected_tau_{agent}_conditional"]
            if (probability < 1e-12) != math.isnan(conditional) or (probability >= 1e-12 and not math.isfinite(conditional)):
                failures.append("conditional_investment_nan")
        for probability_name, price_name, applicable in (
            ("co2_trade_year_probability","mean_co2_price_conditional",row["mode"] != "STATE_OWNED"),
            ("storage_trade_year_probability","mean_storage_fee_conditional",row["mode"] == "TRANSFER")):
            probability, price = row[probability_name], row[price_name]
            if not applicable:
                if not (math.isnan(probability) and math.isnan(price)):
                    failures.append("structural_trade_nan")
            elif not math.isfinite(probability) or not 0 <= probability <= 1:
                failures.append("trade_probability")
            elif (30*probability < 1e-12) != math.isnan(price) or (30*probability >= 1e-12 and not math.isfinite(price)):
                failures.append("conditional_price_nan")
        for name in ("mixed_equilibrium_state_probability", "multiple_pure_equilibrium_state_probability"):
            if not 0 <= row[name] <= 1:
                failures.append("complexity_probability")
        for target, tolerance in (("max_static_accounting_error",1e-10),
                                  ("max_backward_forward_value_error",1e-8),
                                  ("max_probability_mass_error",1e-12)):
            if not math.isfinite(row[target]) or not row[target] < tolerance:
                failures.append(target)
    if failures:
        raise RuntimeError("GATE_EXACT_SOLVER_FAIL: " + "; ".join(failures[:30]))


def baseline(formal, resume=False):
    folder = Path(formal)/"baseline"
    complete = folder/"complete.json"
    if complete.exists():
        info = read_json(complete)
        if not resume or info["identity"] != identity():
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: baseline identity")
        for name, expected in info["files"].items():
            if sha256(folder/name) != expected:
                raise RuntimeError("FORMAL_ARTIFACT_ERROR: baseline hash")
        result = pd.read_csv(folder/"baseline_summary.csv", float_precision="round_trip")
        validate_rows(result.assign(scenario_id=0), [0])
        return result
    results = []
    for mode in MODES:
        result, audit = solve_scenario(BASELINE, mode, details=True)
        results.append(result)
        write_json(folder/f"{mode}.json", {"summary": result, "audit": audit})
    result = pd.DataFrame(results)
    validate_rows(result.assign(scenario_id=0), [0])
    write_csv(folder/"baseline_summary.csv", result)
    write_json(complete, {"identity":identity(), "files":{p.name:sha256(p) for p in folder.iterdir() if p.is_file()}})
    return result


def _solve_design_row(row):
    scenario_id, *values = row
    scenario = dict(zip(FEATURES, values))
    results = []
    for mode in MODES:
        result = solve_scenario(scenario, mode)
        result["scenario_id"] = int(scenario_id)
        results.append(result)
    return results


def build_dataset(formal, resume=False):
    folder = Path(formal)/"exact_dataset"
    design_path = folder/"exact_scenarios.csv"
    scenarios = design()
    if design_path.exists():
        saved = pd.read_csv(design_path, float_precision="round_trip")
        if not resume or not saved.equals(scenarios):
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: Sobol design mismatch")
    else:
        write_csv(design_path, scenarios)
    design_hash = sha256(design_path)
    frozen = {**identity(), "sobol_design_hash":design_hash}
    # CSV is the specified fallback when a Parquet engine is unavailable.
    try:
        import pyarrow  # noqa: F401
        parquet = True
    except ImportError:
        parquet = False
    workers = min(8, os.cpu_count() or 1)
    all_chunks = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for chunk_index, start in enumerate(range(0,4096,128)):
            chunk_path = folder/"chunks"/f"chunk_{chunk_index:04d}.{'parquet' if parquet else 'csv'}"
            metadata_path = chunk_path.with_suffix(".json")
            if chunk_path.exists() or metadata_path.exists():
                if not resume or not (chunk_path.exists() and metadata_path.exists()):
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: unverified or existing chunk")
                metadata = read_json(metadata_path)
                if metadata["identity"] != frozen or metadata["sha256"] != sha256(chunk_path):
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: chunk hash")
                chunk = pd.read_parquet(chunk_path) if parquet else pd.read_csv(chunk_path,float_precision="round_trip")
            else:
                work = list(scenarios.iloc[start:start+128].itertuples(index=False,name=None))
                solved = list(executor.map(_solve_design_row, work, chunksize=1))
                chunk = pd.DataFrame([row for rows in solved for row in rows])
                validate_rows(chunk, range(start,start+128))
                chunk_path.parent.mkdir(parents=True,exist_ok=True)
                if parquet:
                    chunk.to_parquet(chunk_path,index=False)
                else:
                    write_csv(chunk_path,chunk)
                write_json(metadata_path,{"identity":frozen,"sha256":sha256(chunk_path),
                                          "scenario_start":start,"scenario_stop":start+128,"row_count":384})
            validate_rows(chunk,range(start,start+128))
            if not np.array_equal(chunk.drop_duplicates("scenario_id").sort_values("scenario_id")[list(FEATURES)].to_numpy(),
                                  scenarios.iloc[start:start+128][list(FEATURES)].to_numpy()):
                raise RuntimeError("FORMAL_ARTIFACT_ERROR: chunk scenario parameters")
            all_chunks.append(chunk)
            print(f"EXACT_DATASET {start+128}/4096 scenarios, {(start+128)*3}/12288 rows",flush=True)
            append_progress(f"Exact checkpoint {chunk_index:04d}: {start+128}/4096 scenarios; chunk validated, hash {sha256(chunk_path)}.")
    result = pd.concat(all_chunks,ignore_index=True)
    validate_rows(result,range(4096))
    output = folder/"exact_equilibrium_outputs.csv"
    if output.exists():
        saved = read_csv_with_schema(output, result)
        if not resume or not saved.equals(result):
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: exact merged dataset")
    else:
        write_csv(output,result)
    return result
