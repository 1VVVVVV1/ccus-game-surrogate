import math
import pytest

from src import accounting_validation as gate


@pytest.mark.parametrize('error,accepted', [
    (0, True), (99/1_000_000, True), (100/1_000_000, True),
    (math.nextafter(100/1_000_000, math.inf), False),
    (101/1_000_000, False), (math.inf, False), (math.nan, False), (-1, False),
])
def test_source_static_absolute_cny_budget(monkeypatch, error, accepted):
    monkeypatch.setattr(gate, 'SOURCE_BACKED', True)
    assert gate.static_accounting_passes(error) is accepted


def test_method_validation_keeps_original_gate(monkeypatch):
    monkeypatch.setattr(gate, 'SOURCE_BACKED', False)
    assert gate.static_accounting_passes(0)
    assert not gate.static_accounting_passes(1e-10)
