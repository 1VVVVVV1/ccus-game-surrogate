"""Approved scalar benchmark through existing stage accounting; no new solver."""
import copy
import json

import pytest

from src.config import CONFIG, BASELINE, ROOT
from src.economics import stage_outcome


@pytest.fixture
def reduced(monkeypatch):
    cfg = copy.deepcopy(CONFIG)
    approved = json.loads((ROOT / 'config/source_backed_approved_inputs.json').read_text(encoding='utf-8'))
    cfg['utilization_storage'].update(approved['utilization_storage'])
    # Isolate operating costs; remaining platform costs are separate audit inputs.
    cfg['utilization_storage']['fixed_opex'] = 0.0
    monkeypatch.setattr('src.economics.CONFIG', cfg)
    monkeypatch.setattr('src.bargaining.CONFIG', cfg)
    return cfg


def eor_charge(cfg, mode='STATE_OWNED'):
    before = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    cost = cfg['utilization_storage']['utilization_cost_per_ton']
    cfg['utilization_storage']['utilization_cost_per_ton'] = 0.0
    without = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    cfg['utilization_storage']['utilization_cost_per_ton'] = cost
    assert before.q_u == without.q_u
    return without.profits[3] - before.profits[3]


@pytest.mark.parametrize('tonnes', [0, 1, 2, 100000])
def test_flow_units(reduced, tonnes):
    reduced['co2_quantity'].update(Q_bar=tonnes / 1e6, utilization_fraction=1.0)
    assert eor_charge(reduced) * 1e6 == pytest.approx(tonnes * 103.461)


def test_doubling(reduced):
    initial = eor_charge(reduced)
    reduced['co2_quantity']['Q_bar'] *= 2
    assert eor_charge(reduced) == pytest.approx(2 * initial)


@pytest.mark.parametrize('mode', ['TRANSFER', 'JOINT_VENTURE', 'STATE_OWNED'])
def test_reference_components_never_added(reduced, mode):
    u = reduced['utilization_storage']
    assert u['utilization_cost_per_ton'] == 103.461
    assert u['eor_specific_fixed_opex_component'] == 0.0
    before = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    u.update(eor_recycle_ratio=7, li_miao_fixed_reference=10.9536,
             co2_handling_electricity_cost_usd_component=4.964)
    after = stage_outcome(mode, BASELINE, 1000, (1, 1), (0, 0))
    assert after.profits == pytest.approx(before.profits, nan_ok=True)
    assert eor_charge(reduced, mode) == pytest.approx(before.q_u * 103.461)


@pytest.mark.parametrize('section,key,value', [
    ('utilization_storage', 'capex_initial', 999),
    ('transport_market', 'variable_opex_per_ton', 99),
    ('utilization_storage', 'storage_cost_per_ton', 99),
])
def test_other_costs_are_independent(reduced, section, key, value):
    assert reduced['utilization_storage']['capex_initial'] == 759.2857142857143
    before = eor_charge(reduced)
    reduced[section][key] = value
    assert eor_charge(reduced) == pytest.approx(before)
