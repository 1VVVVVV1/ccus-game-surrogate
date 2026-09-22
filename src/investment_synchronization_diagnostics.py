"""Forward-weighted investment actions and asymmetric built states."""
import numpy as np


class SynchronizationAccumulator:
    def __init__(self, horizon):
        self.action_mass = {(0, 0): 0.0, (0, 1): 0.0, (1, 0): 0.0, (1, 1): 0.0}
        self.asymmetric = np.zeros(horizon)

    def add_state(self, t, state, probability):
        if state[0] != state[1]:
            self.asymmetric[t] += probability

    def add_action(self, action, state_probability, action_probability):
        self.action_mass[action] += state_probability * action_probability

    def summary(self):
        result = {'mass_action_'+str(a)+str(b): v for (a, b), v in self.action_mass.items()}
        result.update(mass_asymmetric_invest_action=self.action_mass[(0, 1)]+self.action_mass[(1, 0)],
                      mean_annual_asymmetric_built_state_probability=float(self.asymmetric.mean()),
                      expected_asymmetric_built_years=float(self.asymmetric.sum()),
                      max_year_asymmetric_probability=float(self.asymmetric.max()))
        return result


def summarize_mode(frame):
    probability_difference = np.abs(frame.invest_prob_C-frame.invest_prob_U)
    c, u = frame.expected_tau_C_conditional, frame.expected_tau_U_conditional
    tau_difference = np.abs(c[np.isfinite(c) & np.isfinite(u)]-u[np.isfinite(c) & np.isfinite(u)])
    result = dict(max_abs_invest_prob_difference=float(probability_difference.max()),
                  mean_abs_invest_prob_difference=float(probability_difference.mean()),
                  max_abs_tau_difference=float(tau_difference.max()) if len(tau_difference) else None,
                  mean_abs_tau_difference=float(tau_difference.mean()) if len(tau_difference) else None,
                  fraction_invest_prob_equal_1e12=float((probability_difference <= 1e-12).mean()),
                  fraction_tau_equal_1e12=float((tau_difference <= 1e-12).mean()) if len(tau_difference) else None)
    result['SYNCHRONOUS_COMPLEMENTARITY_RESULT'] = bool(
        result['max_abs_invest_prob_difference'] <= 1e-12
        and frame.mean_annual_asymmetric_built_state_probability.max() <= 1e-12
        and frame.mass_asymmetric_invest_action.max() <= 1e-12)
    return result


def check_identical_target_hashes(left, right, left_hash, right_hash):
    identical = np.array_equal(np.asarray(left), np.asarray(right), equal_nan=True)
    if left_hash == right_hash and not identical:
        raise RuntimeError('SURROGATE_ARTIFACT_COLLISION')
    return 'IDENTICAL_TARGETS_DUE_TO_EQUILIBRIUM_SYMMETRY' if identical else 'DISTINCT_TARGETS'
