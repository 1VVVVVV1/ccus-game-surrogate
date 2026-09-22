import os
import subprocess
import sys

from src.config import ROOT
from src.metrics import passes


def test_commit_now_uses_value_gate_not_price_gate():
    assert not passes('commit_now_system_npv', {'R2': .97, 'NMAE': .04})
    assert not passes('commit_now_value_C', {'R2': .99, 'NMAE': .06})
    assert passes('commit_now_value_U', {'R2': .98, 'NMAE': .05})


def test_source_entry_selects_33_targets_without_changing_default():
    env = os.environ.copy()
    env.pop('CCUS_CONFIG_PATH', None)
    code = ('import run_source_backed_protocol; from src.config import SOURCE_BACKED,TARGETS; '
            'assert SOURCE_BACKED; assert sum(map(len,TARGETS.values()))==33')
    result = subprocess.run([sys.executable, '-c', code], cwd=ROOT, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
