# PAPER_RESULTS_INTERPRETATION

本文件是独立的 paper-analysis 层，只读使用正式 source-backed 结果。它不修改正式模型、配置、状态空间、均衡规则、代理模型或 `results/source_backed_formal/` 产物。正式身份为 Git `bc0d0fe4d2fff35a32caae1e74f87e1ea74f0786`；配置、source、registry 和官方碳价 CSV 的哈希分别为 `8c7501f0ee4a27fa8f13c561a9b2205888b7c6660cbef88f83df256b3583ac5c`、`a4af0372bad0729fd178cc2f1107ba683b6eb6406e6d7b790475058b4afe6e3d`、`43b07f4c82a0485f6e4502385c99919eef704643623211ccc756d0b353f8834f` 和 `a5e60f21e0c065a4c3ef361274c7dfbc8a8d1664ee133cad979286462494000e`。

## Formal findings

### Baseline comparison

|组织模式|动态系统 NPV (百万 CNY)|立即投资 NPV|`option_value` = 动态−立即|相对立即投资|C 投资概率|U 投资概率|C 条件年份|U 条件年份|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|TRANSFER|3885.1864|3871.4608|13.7256|0.35%|0.853660|0.853660|11.6793|11.6793|
|JOINT_VENTURE|3894.5786|3324.6759|569.9026|17.14%|0.930814|0.934506|10.2544|10.2358|
|STATE_OWNED|3896.2939|3324.6759|571.6180|17.19%|0.918044|0.918044|10.1931|10.1931|

动态 NPV 的高低不能直接被解释为现实制度优劣排名。TRANSFER 的条件投资年较晚、且动态值与立即投资值接近，原因是其分散式交易规则可以在低碳价状态关闭储存交易，避免一部分负贡献流量，但转移价格和交易可行性也会排除部分本可产生系统贡献的流量。JV 与 SOE 的立即投资值相同，是因为两者的 commit-now 基准都强制根节点立即同时建设并沿共同的后续物理过程计算；它们的动态路径规则仍不同。JV 采用 Nash 均衡和内部收益分配，SOE 在投资行动上采用系统收益规则，因此两者的动态增量不能被归因于单一价格变量。

### JV 非同步投资

正式 baseline 的同步诊断为：TRANSFER `true`、JV `false`、SOE `true`。JV 的累计 30 年 action mass 为 `mass_action_01=0.037913`、`mass_action_10=0.034221`、总非对称 action mass `0.072134`；这些是逐年行动质量的和，不是路径事件概率。baseline JV 年度审计显示：第 20 年出现 U-only 行动质量 0.037913；第 21、23、26 年出现 C-only 跟进行动质量 0.027084、0.005526、0.001611。因而可确认 baseline 的非同步模式是 U 先建、C 后跟随；不能据此声称所有 Sobol 情景都具有相同年份结构。

JV 的结构机制来自收益分配和成本归属。模型中 C、运输主体 T 和 U 的 pool 分成分别为 0.5、0.2 和 0.3；U 还保留 EOR application 收益。U 的私有 application 收益使其在低价或等待状态下有较强的先行投资动机，而 C 承担其自有捕集资本并只取得 pool 分成，因此 C 更容易等待对其自身净收益有利的价格状态。共享 pool 中同时包含两项资本支出，所以单纯比较累计 action mass 不能理解为“某方承担了全部系统投资”。

联合 exact 样本的描述性关联显示，JV 非同步最敏感的变量是碳价尺度和 U 端 CAPEX：碳价尺度与 `prob_gap` 的 Spearman 相关为 −0.526、与非对称 action mass 为 −0.515；U CAPEX 倍数与 `prob_gap` 为 0.153、与非对称 action mass 为 0.189、与条件年份差为 −0.343。有效减排比例与 `prob_gap` 为 −0.150。运输市场价格的相关接近零，说明在既定域内它不是主要的 JV 非同步区分变量。四分位描述也显示：最低碳价四分位的非对称情景占比约 0.540，而最高四分位约 0.003；U CAPEX 最高四分位的平均非对称 action mass 约 0.0691，最低四分位约 0.0028。上述是模型内的关联诊断，不是因果估计。

### Dynamic versus commit-now and timing increment

|组织模式|动态系统 NPV|commit-now 系统 NPV|`option_value`|相对 commit-now|
|---|---:|---:|---:|---:|
|TRANSFER|3885.1864|3871.4608|13.7256|0.35%|
|JOINT_VENTURE|3894.5786|3324.6759|569.9026|17.14%|
|STATE_OWNED|3896.2939|3324.6759|571.6180|17.19%|

这里的 `option_value` 保留用户指定的差值定义，但对于 TRANSFER/JV 必须称为“相对立即投资基准的均衡择时增量”，而不能无条件称为非负的集中式最优期权价值。联合 exact 样本中，TRANSFER 有 2500 个情景的差值小于 −1e−8，JV 有 17 个，SOE 没有超过数值误差的负值。这是因为 TRANSFER/JV 的动态值是所选 Nash 均衡的系统收益，并非强制系统最优化；SOE 的负值仅剩舍入级别。基准中 JV/SOE 的大增量来自不可逆资本支出可以延迟到更有利的碳价状态，同时避免 commit-now 在低价状态立即承担两端 CAPEX 和持续运营成本。TRANSFER 的交易可行性本身提供了部分运营筛选，因而立即投资基准与动态均衡更接近。

## Mechanism interpretation

模型中的碳价采用物理测度 GBM 二叉树，初始价格为 95.63 CNY/t，年波动率约 0.3106，漂移约 0.1689；折现率为 8%。这些参数使未来高价状态具有较大的上行价值，但等待也会损失早期现金流。不可逆投资与一年建设滞后把这种权衡传递到 C/U 的各自行动。JV 的固定收益分配进一步造成私人边际收益不对称：U 的 EOR application 收益在 pool 外部保留，而 C 的回报主要来自 pool 分成；这解释了 U-only 行动出现在 C-only 行动之前的 baseline 事实。SOE 没有这种分配冲突，因此 C/U 投资概率和年份完全同步。TRANSFER 没有 JV 的 pool 分配，但其 bargain gate 使低价状态下的储存流量可能不成交，形成另一种运营层面的等待机制。

图 `fig1_baseline_timing_option` 展示三种模式的投资概率、差值和条件年份；`fig2_jv_asynchrony` 展示 baseline 年度行动质量及 exact JV 情景的非对称质量；`fig3_key_response_curves` 使用已有 1001 点 exact 单变量网格展示碳价尺度和 U CAPEX 对系统 NPV 与投资概率的响应。图中不加入推断误差条，因为这些点是确定性的模型网格结果。

## Boundary findings

61 项 Boundary V2 搜索均在规定的 1001 点网格中 `found=false`。这只表示指定 domain 内没有检测到规定的 crossing；不表示全域没有边界，也不允许向 domain 外推 root。为避免量纲错误，`boundary_proximity_ranked_by_unit.csv` 按 NPV（百万 CNY）、概率和价格（CNY/t）分开排序。

在 NPV 组中，最接近的是 JV `carbon_scale–COMMIT_NOW_C_VALUE_ZERO`，规定域内最小绝对距离为 57.083 百万 CNY；随后是 TRANSFER `carbon_scale–COMMIT_NOW_U_VALUE_ZERO` 的 503.471 百万 CNY 和 JV `carbon_scale–COMMIT_NOW_U_VALUE_ZERO` 的 696.489 百万 CNY。NPV 响应在这些情形中随 carbon scale 单调上升，整个域都在阈值之上。概率组的阈值为 0.5，必须用离 0.5 的距离比较；价格组的阈值为 0，必须保留价格单位。完整 61 行、最小/最大响应、最近点、端点方向、单调性及分组排名见 `tables/boundary_proximity_ranked_by_unit.csv`；没有一个 crossing 可被外推为精确边界。

## Robustness / numerical reliability

- 正式数据为 4096 个 Sobol 情景、三种模式共 12288 行，solver failures 为 0；exact、integrity、baseline、synchronization、surrogate 和 Boundary V2 gates 已通过。
- 33/33 surrogate targets 通过既定门槛。正式最大静态会计误差为 `0.00023283064365386963 CNY`，最大动态误差为 `7.275957614183427e-11 million CNY`，最大概率质量误差为 `4.440892098500625e-16`。静态 Gate 使用用户批准的 100 CNY 绝对误差预算；这里如实报告实际误差，没有改写为 0。
- paper-analysis 脚本在运行前验证了正式 reproducibility manifest 中的 source/artifact hashes、配置哈希、Git commit、12288 exact 行、4096 scenario 行、61 boundary 行、18 个 1001 点网格及 solver status；分析输入哈希记录在 `audit/analysis_input_manifest.json`。分析完成后再次比较正式目录快照，正式文件没有被改写。
- JV 参数响应中的相关系数和四分位平均是描述统计，不是因果估计；同步诊断使用 baseline 审计和既有 exact 汇总，未为论文分析重新求解 12288 行。

## Limitations

这是 representative multi-source source-backed calibration，不是齐鲁—胜利项目财务报表复刻。正式 registry 中的 26 个 `MODEL_ASSUMPTION` 和 6 个 `DESIGN_RANGE_ASSUMPTION` 必须与经验或派生参数区分。U CAPEX、EOR 换油率、减排比例和双流结构等均是模型边界内的规定设定，不能被解读为项目审计事实。条件投资年份是“已投资情景”中的条件均值，不是所有路径的平均日历年份。JV baseline 年度非同步解释来自保存的 baseline audit；联合 exact 数据没有保存每个情景的完整年度状态路径，因此不能把 baseline 年份模式推广到全部 Sobol 情景。Boundary V2 的 61 个 `found=false` 仅限规定网格和 domain。静态会计误差仍按实际最大值报告，100 CNY 预算不适用于其他数值 Gate。

## Claims that must NOT be made

- 不得把 baseline NPV 的轻微排序写成现实世界 TRANSFER、JV、SOE 的制度优劣排名。
- 不得把 `option_value` 对所有模式都写成非负的全系统最优期权价值；TRANSFER/JV 的动态解是所选均衡，差值可为负。
- 不得把 JV 的累计 `mass_action_01`、`mass_action_10` 或 `mass_asymmetric_invest_action` 写成“30 年内至少发生一次”的路径概率。
- 不得把 baseline 的 U 先建、C 后建年份序列推广为所有参数情景的必然顺序。
- 不得把 61 个 `found=false` 写成“没有经济边界”或“全域不存在 crossing”。
- 不得把 26 个模型假设、6 个设计域或代表性多源校准写成实测项目参数、财务报表或中国 CCUS 普遍规律。
- 不得把静态会计最大实际误差改写为 0，也不得因为 100 CNY 预算而放宽其他 Gate。

## Paper-ready English result paragraphs

Under the calibrated baseline, the dynamic system NPV was 3,885.19, 3,894.58 and 3,896.29 million CNY for TRANSFER, JOINT VENTURE and STATE OWNED, respectively. Investment probabilities were 0.854/0.854 in TRANSFER, 0.931/0.935 in JOINT VENTURE and 0.918/0.918 in STATE OWNED (C/U). The corresponding conditional investment years were 11.68/11.68, 10.25/10.24 and 10.19/10.19. These differences are generated by the model's bargaining gates, irreversible capital expenditures and organization-specific payoff allocation; they should not be interpreted as an empirical institutional ranking.

The dynamic-minus-commit-now system-NPV increments were 13.73, 569.90 and 571.62 million CNY for TRANSFER, JOINT VENTURE and STATE OWNED. For TRANSFER and JOINT VENTURE, this quantity is a signed equilibrium timing increment because the dynamic solution is the selected Nash equilibrium rather than a centralized system optimum. In the baseline JV audit, the only asymmetric initiating action was U-only construction at year 20 (probability mass 0.0379), followed by C-only actions at years 21, 23 and 26. Across the exact joint sample, carbon-price scale and U-side CAPEX were the strongest descriptive correlates of JV asymmetry, whereas the transport-market price showed near-zero correlation.

## Files

- Tables: `tables/baseline_comparison.csv`, `tables/dynamic_commit_option_value.csv`, `tables/synchronization_diagnostic.csv`, `tables/exact_option_and_sync_summary.csv`, `tables/JV_parameter_quartiles.csv`, `tables/boundary_proximity_ranked_by_unit.csv`.
- Figures: `figures/fig1_baseline_timing_option.(png|svg)`, `figures/fig2_jv_asynchrony.(png|svg)`, `figures/fig3_key_response_curves.(png|svg)`.
- Reproducibility: `analyze_results.py`, `audit/analysis_input_manifest.json`, `audit/formal_before.json`.
