# 用户确认的规范补充

## 决策 001：均衡复杂性统计（2026-09-20）

第 27 节两个概率字段统一采用平均年度发生概率，正式 T=30。

M_t = sum_s Pr_t(s) * 1{pure_ne_count(s)=0 且成功求得 MIXED_NASH}。

P_t_multi = sum_s Pr_t(s) * 1{tie-break 前 pure_ne_count(s)>1}。

- mixed_equilibrium_state_probability = sum_t M_t / 30。
- multiple_pure_equilibrium_state_probability = sum_t P_t_multi / 30。
- expected_mixed_equilibrium_years = sum_t M_t。
- expected_multiple_pure_equilibrium_years = sum_t P_t_multi。

概率范围 [0,1]；预期年数范围 [0,30]。仅正概率可达状态贡献统计。
multiple 的判断使用 Pareto 删除及 tie-break 之前的原始纯均衡数。
STATE_OWNED 的四项统计均为 0.0。不存在路径历史事件标记。
这些指标不是 30 年内至少发生一次的路径事件概率。

本次确认明确针对以上均衡统计字段，不擅自扩展为其他研究性字段的定义。

## 决策 002：内部交易概率（2026-09-20）

用户选择 B。交易概率为 30 年内平均年度实际内部交易发生概率。
权重为 Pr_t(s) * pi_eq(a|s)，pure 和 mixed 均逐 state-action-year 累计。
指示变量同时要求：相应实际流量 >0、对应议价 matched、实现价格 finite。
负 CO2 价格允许；未建成导致零流量时不计交易。

每类交易 denominator = sum_t sum_s sum_a 权重 * 指示变量。
年度交易概率 = denominator / 30。
条件价格 numerator = sum_t sum_s sum_a 权重 * 指示变量 * 价格；
denominator < 1e-12 时条件价格 NaN，否则 numerator / denominator。

适用矩阵：TRANSFER 两类交易适用；JV 仅 CO2 交易适用；
STATE_OWNED 两类交易均不适用。结构性不适用的概率和价格均 NaN，
含义为 STRUCTURALLY_NOT_APPLICABLE。适用但无交易的概率为 0，价格为 NaN。
不新增物理活动频率 target。

补充说明：在规范的一年建设滞后时序下，当年流量由旧 built state 决定，
因而同一状态的不同投资动作实际上不改变当年流量；实现仍严格使用用户要求的
state probability × action probability 权重，不改变原有时序。
