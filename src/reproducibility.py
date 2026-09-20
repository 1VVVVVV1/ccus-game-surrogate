"""Content hashes, exclusive writes, and verified resume identities."""
import hashlib
import importlib.metadata
import json
import platform
import subprocess
from pathlib import Path
from .config import ROOT, CONFIG_PATH, CONFIG


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def source_manifest():
    files = sorted((ROOT / "src").glob("*.py")) + sorted(ROOT.glob("*.py"))
    return {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in files}


def identity():
    source = source_manifest()
    return {"config_sha256": sha256(CONFIG_PATH), "source_manifest_hash": canonical_hash(source)}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_csv(path, frame):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", float_format="%.17g")


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def manifest(formal):
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    source = source_manifest()
    return {"git_commit": git.stdout.strip() if git.returncode == 0 else None,
            "git_status_note": "NOT_A_GIT_REPOSITORY" if git.returncode else "RECORDED",
            **identity(), "source_files_sha256": source,
            "test_files_sha256": {p.name: sha256(p) for p in sorted((ROOT/"tests").glob("*.py"))},
            "python": platform.python_version(),
            "versions": {name: importlib.metadata.version(name) for name in ("numpy","pandas","scipy","scikit-learn")},
            "sobol_seed": CONFIG["dataset"]["sobol_seed"], "split_seed": CONFIG["dataset"]["split_seed"],
            "artifacts_sha256": {str(p.relative_to(formal)).replace("\\","/"): sha256(p)
                                  for p in sorted(Path(formal).rglob("*")) if p.is_file()}}


def append_progress(text):
    with (ROOT / "PROJECT_PROGRESS.md").open("a", encoding="utf-8") as handle:
        handle.write("\n\n" + text + "\n")
