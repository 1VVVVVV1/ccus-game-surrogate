"""Ordered, fail-closed execution of the formal research protocol."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import pandas as pd
from .config import ROOT, CONFIG_PATH
from .dataset import baseline, build_dataset, validate_rows
from .surrogate import fit_surrogates
from .boundary import search_boundaries
from .reproducibility import (append_progress, identity, manifest, read_json, sha256,
                              write_json, write_text)

FROZEN_CONFIG_HASH = "3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76"


def prepare(formal,resume):
    if formal.exists() and any(formal.iterdir()):
        if not resume:
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: formal directory nonempty; explicit --resume required")
        lock = read_json(formal/"formal_run_lock.json")
        if lock["identity"] != identity():
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: configuration/source lock mismatch")
    else:
        write_json(formal/"formal_run_lock.json",{"identity":identity(),"python":sys.version})


def precheck(formal, label):
    if sha256(CONFIG_PATH) != FROZEN_CONFIG_HASH:
        raise RuntimeError("GATE_PRECHECK_FAIL: frozen configuration hash mismatch")
    outputs = {}
    for name,args in (("compileall",["-m","compileall","-q","."]),
                      ("pytest",["-m","pytest","-q"])):
        result = subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True)
        outputs[name] = {"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr}
        print(f"{label} {name}: exit={result.returncode}\n{result.stdout}",flush=True)
        if result.returncode:
            write_json(formal/f"{label}_failure.json",outputs)
            raise RuntimeError(f"GATE_PRECHECK_FAIL: {name}")
    path = formal/f"{label}.json"
    if not path.exists():
        write_json(path,outputs)
    return outputs


def record_gate(formal,number,name,evidence):
    path = formal/"gates"/f"gate_{number}_{name}.json"
    if not path.exists():
        write_json(path,{"status":"PASS","identity":identity(),"evidence":evidence})
    append_progress(f"Gate {number} {name}: PASS. {json.dumps(evidence,ensure_ascii=False)}")
    print(f"GATE {number} {name}: PASS",flush=True)


def final_report(formal,tests,base,exact,metrics,boundaries):
    report_path = formal/"FINAL_EXECUTION_REPORT.md"
    if report_path.exists():
        saved = read_json(formal/"reproducibility_manifest.json")
        if any(saved[key] != value for key,value in identity().items()):
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: final report identity")
        if any(sha256(formal/name) != expected for name,expected in saved["artifacts_sha256"].items()):
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: final artifact hash verification")
        completion = read_json(formal/"completion.json")
        if sha256(report_path) != completion["report_sha256"] or sha256(formal/"reproducibility_manifest.json") != completion["manifest_sha256"]:
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: final report/manifest hash")
        return
    provenance = manifest(formal)
    manifest_path = formal/"reproducibility_manifest.json"
    if not manifest_path.exists():
        write_json(manifest_path,provenance)
    parts = ["# FINAL_EXECUTION_REPORT\n", "Method: Two-agent stochastic dynamic investment game with generalized Nash bargaining and surrogate-assisted equilibrium mapping.\n",
             "Status: ALL_STAGES_COMPLETED\n", "## Reproducibility\n", "```json\n"+json.dumps(provenance,ensure_ascii=False,indent=2)+"\n```\n",
             "## Compile and tests\n", "```json\n"+json.dumps(tests,ensure_ascii=False,indent=2)+"\n```\n",
             "## Baseline three-mode results\n", "```text\n"+base.to_string(index=False)+"\n```\n",
             f"## Exact dataset\n\nScenarios: {exact.scenario_id.nunique()}; rows: {len(exact)}; solver failures: {int((exact.solver_status != 'OK').sum())}.\n",
             "## Mode-specific value, investment, timing and transaction summaries\n"]
    for mode,group in exact.groupby("mode"):
        parts.append(f"### {mode}\n\n```text\n"+group.select_dtypes("number").describe(percentiles=[.05,.5,.95]).to_string()+"\n```\n")
        if mode != "STATE_OWNED":
            parts.append(f"Mean annual mixed Nash frequency: {group.mixed_equilibrium_state_probability.mean():.17g}; pure Nash frequency: {1-group.mixed_equilibrium_state_probability.mean():.17g}; multiple-pure frequency: {group.multiple_pure_equilibrium_state_probability.mean():.17g}.\n")
        else:
            parts.append("Cooperative selection, not a Nash game; mixed and multiple-pure fields equal 0.0.\n")
    parts.extend(["## Surrogate test metrics\n", "```text\n"+metrics[metrics.split=="test"].to_string(index=False)+"\n```\n",
                  "## Exact-verified boundaries (all roots and found=false rows)\n", "```text\n"+boundaries.to_string(index=False)+"\n```\n",
                  "Surrogate false brackets and exact evaluations are in boundaries/verification. Crossing intervals may bracket jumps; a midpoint is not asserted to be an exact response-equality point.\n",
                  f"Searches: {boundaries.groupby(['variable','mode','boundary_type']).ngroups}; found=false rows: {int((~boundaries.found).sum())}; discarded surrogate false brackets: {int(boundaries.surrogate_false_brackets.sum())}.\n",
                  "Interpretation limit: found=false means the prescribed surrogate-candidate/exact-verification procedure retained no crossing. It does not prove absence of a crossing throughout the full economic domain. Candidates without an exact endpoint crossing are discarded, not widened. No alternative search algorithm was introduced. closest_response is from the surrogate grid, as labeled in each verification record.\n",
                  "## Structural NaN\n\nConditional investment times are NaN when investment probability <1e-12. Conditional prices are NaN when transaction-year denominator <1e-12. JV storage and both SOE internal transaction mechanisms are structurally inapplicable. SOE value_T is not an individual economic result and is NaN; SOE value_C=value_U=system value for cooperative decisions.\n",
                  "## RL benchmark and provenance\n", (ROOT/"docs"/"RL_BENCHMARK_NOTE.md").read_text(encoding="utf-8"),
                  "\nOld RL project modified: NO. Old RL formal results overwritten: NO.\n",
                  (ROOT/"docs"/"PYTEST_TEMPORARY_DIRECTORY_INCIDENT.md").read_text(encoding="utf-8"),
                  "## Gates\n\nGates 1–7 PASS; final compile/tests PASS. FINAL STATUS: ALL_STAGES_COMPLETED.\n"])
    write_text(report_path,"\n".join(parts))
    write_json(formal/"completion.json",{"report_sha256":sha256(report_path),
                                         "manifest_sha256":sha256(manifest_path),"status":"ALL_STAGES_COMPLETED"})


def main(stage="full"):
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume",action="store_true")
    args = parser.parse_args()
    formal = ROOT/"results"/"formal"
    current = "PRECHECK"
    try:
        prepare(formal,args.resume)
        if stage != "full":
            if stage == "baseline":
                baseline(formal,args.resume)
            elif stage == "dataset":
                build_dataset(formal,args.resume)
            elif stage == "surrogate":
                data = pd.read_csv(formal/"exact_dataset"/"exact_equilibrium_outputs.csv",float_precision="round_trip")
                validate_rows(data,range(4096))
                _,failures = fit_surrogates(formal,data,args.resume)
                if failures:
                    raise RuntimeError("GATE_SURROGATE_FAIL")
            elif stage == "boundaries":
                gate = read_json(formal/"gates"/"gate_6_SURROGATE_ACCURACY.json")
                if gate["status"] != "PASS" or gate["identity"] != identity():
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: surrogate gate missing")
                search_boundaries(formal,args.resume)
            return 0
        tests = precheck(formal,"precheck")
        record_gate(formal,1,"COMPILE_TESTS_CONFIG",tests)
        current = "BASELINE"
        base = baseline(formal,args.resume)
        record_gate(formal,2,"BASELINE",{"mode_count":len(base),"all_solver_status_OK":True})
        current = "EXACT_DATASET"
        exact = build_dataset(formal,args.resume)
        record_gate(formal,3,"EXACT_DATASET",{"scenario_count":exact.scenario_id.nunique(),"row_count":len(exact)})
        current = "EXACT_GATE"
        validate_rows(exact,range(4096))
        record_gate(formal,4,"EXACT_INTEGRITY",{"solver_OK":12288,"failed_solves":0,"nonfinite_mandatory":0,"probability_mass_failures":0,"dynamic_accounting_failures":0})
        current = "SURROGATE"
        measured,failures = fit_surrogates(formal,exact,args.resume)
        record_gate(formal,5,"SURROGATE_FIT",{"models":len(measured)//3})
        current = "SURROGATE_GATE"
        if failures:
            raise RuntimeError("GATE_SURROGATE_FAIL: "+str(failures))
        record_gate(formal,6,"SURROGATE_ACCURACY",{"gating_targets_passed":len(measured)//3})
        current = "BOUNDARIES"
        boundaries = search_boundaries(formal,args.resume)
        record_gate(formal,7,"EXACT_VERIFIED_BOUNDARIES",{"rows":len(boundaries),"searches":61})
        current = "FINAL_VALIDATION"
        tests = precheck(formal,"final_validation")
        if read_json(formal/"formal_run_lock.json")["identity"] != identity():
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: final hash mismatch")
        current = "FINAL_REPORT"
        final_report(formal,tests,base,exact,measured,boundaries)
        append_progress("## ALL_STAGES_COMPLETED\n\nFinal report: results/formal/FINAL_EXECUTION_REPORT.md")
        print("ALL_STAGES_COMPLETED",flush=True)
        return 0
    except Exception as error:
        message = f"Stage: {current}\n\n{type(error).__name__}: {error}"
        print(message,flush=True)
        append_progress("## EXECUTION_STOPPED\n\n"+message+"\n\nNo downstream stages executed; no parameter or gate changes.")
        if formal.exists():
            failure_name = "EXACT_SOLVER_FAILURE_REPORT.md" if current in ("BASELINE","EXACT_DATASET","EXACT_GATE") else "EXECUTION_STOP_REPORT.md"
            if not (formal/failure_name).exists():
                write_text(formal/failure_name,"# Execution stopped\n\n"+message+"\n")
            failure_manifest = formal/"interrupted_reproducibility_manifest.json"
            if not failure_manifest.exists():
                write_json(failure_manifest,manifest(formal))
        return 1
