"""One frozen HistGradientBoostingRegressor per applicable mode/target."""
import math
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits
from .config import FEATURES, MODES, TARGETS, HGB_PARAMETERS
from .metrics import metrics, passes
from .sobol_design import scenario_split
from .reproducibility import write_csv, write_json, read_json, write_text, sha256


def feature_matrix(frame):
    return frame.loc[:,list(FEATURES)]


def _same_metrics(a,b):
    return all(a[k] == b[k] or (math.isnan(a[k]) and math.isnan(b[k])) for k in a)


def fit_surrogates(formal, dataset, resume=False):
    folder = Path(formal)/"surrogate"
    split_path = folder/"scenario_split.csv"
    split = scenario_split()
    if split_path.exists():
        if not resume or not pd.read_csv(split_path).equals(split):
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: split mismatch")
    else:
        write_csv(split_path,split)
    data_hash = sha256(Path(formal)/"exact_dataset"/"exact_equilibrium_outputs.csv")
    split_hash = sha256(split_path)
    data = dataset.merge(split,on="scenario_id",validate="many_to_one")
    rows, failures, distributions, worst_errors = [], [], {}, {}
    for mode in MODES:
        for target in TARGETS[mode]:
            subset = data[(data["mode"] == mode) & data[target].notna()]
            chunks = {name:subset[subset.split == name] for name in ("train","validation","test")}
            if any(len(group)==0 for group in chunks.values()):
                raise RuntimeError(f"UNDEFINED_RESEARCH_CHOICE: empty applicable target split: {mode}/{target}")
            model_path = folder/"models"/f"{mode}__{target}.joblib"
            metadata_path = model_path.with_suffix(".json")
            frozen = {"dataset_hash":data_hash,"split_hash":split_hash,"features":list(FEATURES),
                      "mode":mode,"target":target,"hyperparameters":HGB_PARAMETERS}
            previous = None
            if model_path.exists() or metadata_path.exists():
                if not resume or not (model_path.exists() and metadata_path.exists()):
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: incomplete or existing surrogate")
                previous = read_json(metadata_path)
                if previous["identity"] != frozen or previous["model_hash"] != sha256(model_path):
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: surrogate identity")
                model = joblib.load(model_path)
                if any(model.get_params()[k] != v for k,v in HGB_PARAMETERS.items()):
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: surrogate parameters")
            else:
                model = HistGradientBoostingRegressor(**HGB_PARAMETERS)
                with threadpool_limits(limits=1):
                    model.fit(feature_matrix(chunks["train"]),chunks["train"][target])
            measured = {}
            for name, group in chunks.items():
                with threadpool_limits(limits=1):
                    predictions = model.predict(feature_matrix(group))
                measured[name] = metrics(group[target].to_numpy(),predictions)
                rows.append({"mode":mode,"target":target,"split":name,"n":len(group),
                             **measured[name],"predictions":"UNCLIPPED",
                             "gate_pass":passes(target,measured[name]) if name=="test" else None})
                if name == "test":
                    errors = group[["scenario_id",*FEATURES,target]].copy()
                    errors["prediction"] = predictions
                    errors["absolute_error"] = np.abs(group[target].to_numpy()-predictions)
                    worst_errors[(mode,target)] = errors.sort_values("absolute_error",ascending=False).head(20)
            if previous:
                if any(not _same_metrics(measured[name],previous["metrics"][name]) for name in measured):
                    raise RuntimeError("FORMAL_ARTIFACT_ERROR: surrogate metric recomputation")
            else:
                model_path.parent.mkdir(parents=True,exist_ok=True)
                with model_path.open("xb") as handle:
                    joblib.dump(model,handle)
                write_json(metadata_path,{"identity":frozen,"model_hash":sha256(model_path),
                                          "effective_parameters":model.get_params(),"metrics":measured})
            distributions[(mode,target)] = subset.groupby("split")[target].describe(percentiles=[.05,.5,.95]).to_string()
            if not passes(target,measured["test"]):
                failures.append((mode,target))
            print(f"SURROGATE {mode}/{target}: test {measured['test']} gate={passes(target,measured['test'])}",flush=True)
    result = pd.DataFrame(rows)
    metrics_path = folder/"surrogate_metrics.csv"
    if metrics_path.exists():
        saved = pd.read_csv(metrics_path,float_precision="round_trip")
        if not resume or saved.to_csv(index=False) != pd.read_csv(__import__('io').StringIO(result.to_csv(index=False)),float_precision="round_trip").to_csv(index=False):
            raise RuntimeError("FORMAL_ARTIFACT_ERROR: metrics table mismatch")
    else:
        write_csv(metrics_path,result)
    if failures:
        parts = ["# SURROGATE_FAILURE_REPORT\n", "Status: GATE_SURROGATE_FAIL. All metrics use unclipped predictions. No tuning or sample deletion was performed.\n"]
        for mode,target in failures:
            selected = result[(result["mode"]==mode)&(result.target==target)]
            parts.extend([f"\n## {mode} / {target}\n", "```text\n"+selected.to_string(index=False)+"\n```\n",
                          "Target distribution by split:\n```text\n"+distributions[(mode,target)]+"\n```\n",
                          "Worst 20 test rows:\n```text\n"+worst_errors[(mode,target)].to_string(index=False)+"\n```\n"])
        path = folder/"SURROGATE_FAILURE_REPORT.md"
        if not path.exists():
            write_text(path,"\n".join(parts))
    return result, failures
