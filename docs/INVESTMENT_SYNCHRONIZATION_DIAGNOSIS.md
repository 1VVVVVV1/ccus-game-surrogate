# Investment synchronization diagnosis

At each reachable decision state, action mass is forward-state probability times selected-equilibrium action probability. STATE_OWNED uses its cooperative action. The four mass_action fields sum these probabilities across all30decision years; their sum is30. mass_asymmetric_invest_action is the sum for01and10, in expected action-years, not a path-event probability.

Asymmetric built-state probability uses pre-action built states for t=0,...,29. Its annual mean, total expected years and annual maximum are reported. Scenario-level C/U probability differences use all rows; conditional-time differences use only rows with both times finite.

SYNCHRONOUS_COMPLEMENTARITY_RESULT is true only if the maximum investment-probability difference and every scenario's annual asymmetric-state mean and asymmetric-action mass are<=1e-12. If true: 两设施具有强互补性，只有共同建成后才能形成运营流量，因此均衡内生地产生同步投资。No model change is made to force actor differences.

Identical C/U targets permit identical model hashes. Distinct targets with identical model hashes cause SURROGATE_ARTIFACT_COLLISION and stop execution.
