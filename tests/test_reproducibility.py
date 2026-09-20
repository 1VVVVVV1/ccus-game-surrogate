import pytest
from src.protocol import final_report
from src.reproducibility import write_json, write_text, sha256, identity


def completed_artifacts(folder):
    write_text(folder/"FINAL_EXECUTION_REPORT.md","Completed report\n")
    write_text(folder/"example.csv","x\n1\n")
    write_json(folder/"reproducibility_manifest.json",{
        **identity(),"artifacts_sha256":{"example.csv":sha256(folder/"example.csv")}})
    write_json(folder/"completion.json",{
        "report_sha256":sha256(folder/"FINAL_EXECUTION_REPORT.md"),
        "manifest_sha256":sha256(folder/"reproducibility_manifest.json")})


def test_completed_report_resume_preserves_existing_artifacts(tmp_path):
    completed_artifacts(tmp_path)
    before = {p.name:p.read_bytes() for p in tmp_path.iterdir()}
    final_report(tmp_path,None,None,None,None,None)
    assert {p.name:p.read_bytes() for p in tmp_path.iterdir()} == before


def test_completed_report_resume_rejects_modified_artifact(tmp_path):
    completed_artifacts(tmp_path)
    (tmp_path/"example.csv").write_text("x\n2\n")
    with pytest.raises(RuntimeError,match="FORMAL_ARTIFACT_ERROR"):
        final_report(tmp_path,None,None,None,None,None)
