"""Regression for the observed one-ULP source-profile accounting discrepancy."""
import json
import math
from decimal import Decimal, localcontext

from src.config import ROOT, BASELINE
from src.economics import stage_outcome


def test_source_profile_one_ulp_aggregation(monkeypatch):
    config = json.loads((ROOT / 'config/model_config.source_backed.json').read_text(encoding='utf-8'))
    evidence = json.loads((ROOT / 'results/source_backed_formal/source_audit/static_accounting_endpoint_failure.json').read_text(encoding='utf-8'))
    monkeypatch.setattr('src.economics.CONFIG', config)
    monkeypatch.setattr('src.bargaining.CONFIG', config)
    assert abs(evidence['pc'] + evidence['pu'] + evidence['pt'] - evidence['direct']) == evidence['system_ulp']
    result = stage_outcome('TRANSFER', dict(BASELINE, carbon_scale=6.25),
                           evidence['carbon_price'], (1, 1), (0, 0))
    # Same cash-flow terms, independently summed at high precision before float rounding.
    with localcontext() as context:
        context.prec = 60
        c_terms = (evidence['rc'], evidence['payment_u'], -evidence['transport_payment'],
                   -evidence['payment_s'], -evidence['oc'], -evidence['ic'])
        u_terms = (evidence['oil'], -evidence['payment_u'], evidence['payment_s'],
                   evidence['subsidy'], -evidence['ou'], -evidence['iu'])
        assert result.profits[0] == float(sum(map(Decimal.from_float, c_terms)))
        assert result.profits[1] == float(sum(map(Decimal.from_float, u_terms)))
    assert result.profits[2] == evidence['pt']
    expected = math.fsum((evidence['rc'], evidence['oil'], evidence['subsidy'],
                          -evidence['oc'], -evidence['ou'], -evidence['ct'],
                          -evidence['ic'], -evidence['iu']))
    assert result.profits[3] == expected
    assert result.accounting_error == 0.0


def test_source_profile_subject_sum_roundoff(monkeypatch):
    config = json.loads((ROOT / 'config/model_config.source_backed.json').read_text(encoding='utf-8'))
    monkeypatch.setattr('src.economics.CONFIG', config)
    monkeypatch.setattr('src.bargaining.CONFIG', config)
    result = stage_outcome('TRANSFER', dict(BASELINE, carbon_scale=6.25),
                           3577959.1584167466, (1, 1), (0, 0))
    assert result.accounting_error == 0.0
