import numpy as np
import pandas as pd
from src.dataset import read_csv_with_schema
from src.reproducibility import write_csv
from src.sobol_design import design, scenario_split
from src.config import FEATURES, DOMAIN, MODES


def test_sobol_design():
    sample = design()
    assert len(sample) == 4096
    assert sample.scenario_id.is_unique
    assert not sample[list(FEATURES)].duplicated().any()
    assert sample.to_csv(index=False).encode() == design().to_csv(index=False).encode()
    assert np.array_equal(sample.scenario_id,np.arange(4096))
    for feature,(lower,upper) in zip(FEATURES,DOMAIN):
        assert sample[feature].between(lower,upper).all()


def test_scenario_split_no_mode_leakage():
    split = scenario_split()
    assert split.split.value_counts().to_dict() == {"train":2868,"test":614,"validation":614}
    sample = design()
    sample = sample.loc[sample.index.repeat(3)].copy()
    sample["mode"] = list(MODES)*4096
    merged = sample.merge(split,on="scenario_id",validate="many_to_one")
    assert (merged.groupby("scenario_id").split.nunique()==1).all()
    permutation = np.random.default_rng(42).permutation(4096)
    assert set(split[split.split=="train"].scenario_id)==set(permutation[:2868])


def test_csv_resume_restores_zero_float_columns_without_value_changes(tmp_path):
    reference = pd.DataFrame({
        "scenario_id": [0, 1], "mode": ["TRANSFER", "STATE_OWNED"],
        "mixed_equilibrium_state_probability": [0.0, 0.0],
        "expected_mixed_equilibrium_years": [0.0, 0.0],
        "value_T": [np.nextafter(1.0, 2.0), np.nan],
    })
    path = tmp_path / "exact.csv"
    write_csv(path, reference)
    assert pd.read_csv(path).mixed_equilibrium_state_probability.dtype == np.dtype("int64")
    before = path.read_bytes()
    restored = read_csv_with_schema(path, reference)
    assert restored.equals(reference)
    assert path.read_bytes() == before
    changed = reference.copy()
    changed.loc[0, "value_T"] = 1.0
    assert not restored.equals(changed)
    assert not restored.equals(reference.iloc[::-1])
    changed_nan = reference.copy()
    changed_nan.loc[1, "value_T"] = 0.0
    assert not restored.equals(changed_nan)
