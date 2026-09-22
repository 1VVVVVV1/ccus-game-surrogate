import pandas as pd
import pytest

from src.investment_synchronization_diagnostics import (
    SynchronizationAccumulator, summarize_mode, check_identical_target_hashes)


def test_joint_actions_and_states_are_synchronous():
    acc = SynchronizationAccumulator(2)
    acc.add_state(0, (0, 0), 1)
    acc.add_state(1, (1, 1), 1)
    acc.add_action((1, 1), 1, 1)
    acc.add_action((0, 0), 1, 1)
    row = dict(acc.summary(), invest_prob_C=1, invest_prob_U=1,
               expected_tau_C_conditional=0, expected_tau_U_conditional=0)
    assert summarize_mode(pd.DataFrame([row]))['SYNCHRONOUS_COMPLEMENTARITY_RESULT']
    assert row['mass_action_11'] == 1


def test_asymmetric_forward_weights_and_years():
    acc = SynchronizationAccumulator(2)
    acc.add_state(1, (1, 0), .3)
    acc.add_action((1, 0), .6, .5)
    row = dict(acc.summary(), invest_prob_C=.3, invest_prob_U=0,
               expected_tau_C_conditional=0, expected_tau_U_conditional=float('nan'))
    assert row['mass_asymmetric_invest_action'] == .3
    assert row['expected_asymmetric_built_years'] == .3
    assert row['mean_annual_asymmetric_built_state_probability'] == .15
    assert not summarize_mode(pd.DataFrame([row]))['SYNCHRONOUS_COMPLEMENTARITY_RESULT']


def test_identical_targets_allow_equal_model_hashes():
    assert check_identical_target_hashes([0, 1], [0, 1], 'a', 'a') == 'IDENTICAL_TARGETS_DUE_TO_EQUILIBRIUM_SYMMETRY'


def test_distinct_targets_cannot_share_model_hash():
    with pytest.raises(RuntimeError, match='SURROGATE_ARTIFACT_COLLISION'):
        check_identical_target_hashes([0, 1], [1, 0], 'a', 'a')
