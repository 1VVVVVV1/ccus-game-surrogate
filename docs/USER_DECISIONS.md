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


## 决策 004：齐鲁—胜利 CO2-EOR 工程锚点

用户完整授权原文保存在 docs/USER_DECISION_QILU_SHENGLI.txt。

- U 路线固定 CHINA_ONSHORE_CO2_EOR：onshore CO2-EOR + associated geological storage，WAG；经济含义为 CO2-EOR economic value。
- 工程锚点固定 Qilu Petrochemical–Shengli Oilfield，109 km 待官方来源核验；不再询问路线、项目或距离选择。
- Wei et al. (2015), DOI 10.1016/j.ijggc.2015.01.014 为主技术经济来源。先核实 Table 1/2/4 再登记数值或编码公式；按来源实际性质区分经验值和情景假设。
- 优先建立 eor_cost_calibration.py 并逐公式测试，但不能凭摘要或用户列举的组件猜公式；计算项目 CAPEX 还必须具备同口径井数、井深、井组数、面积等输入。
- 同项目补充来源：10.1016/j.jclepro.2022.133724；10.1016/j.eiar.2024.107684。不跨接其他项目固定 CAPEX，不沿用 40.3566 或 780。
- 0.2584 原文确认后才可与已核实 109 相乘，所得 28.1656 不取整；125 仍为内部定价模型假设。
- 50 USD/t 仅文献参照，不能替代内生 Nash 价格；12 年/12% 仅来源参照，不能自动改变本项目 30 年/统一折现率。8%/12% 正式选择须另行决定。
- 百万吨级工程为物理及路线锚点，并不意味着完整复刻或三种商业模式均在实地存在。
- GATE_SOURCE_AUDIT 通过前不启动 12288 行正式计算。

## 决策 005：统一来源内部冲突规则

完整原文见 USER_SOURCE_CONFLICT_RULES.txt，适用于所有后续来源。数值表格优先；Wei 举升成本固定1 USD/STB；0.25不得进入正式计算或敏感性分析。公式结构未确定不可猜补；不使用的未解决参考公式不阻塞 Gate。此决定取代决策004中完整复刻 Wei 成本模块的要求。所有成本登记边界，避免平准化成本与设备 CAPEX 重复计费。

## 2026-09-20 决策006：FORMAL UNIFIED DISCOUNT RATE DECISION — 8%

完整授权见 docs/USER_UNIFIED_DISCOUNT_DECISION.txt。simulation.economic_discount_rate=0.08，MODEL_ASSUMPTION；所有主体、模式、commit-now、边界和代理目标统一 gamma=1/1.08。30年继续保留。决策依据为 integrated CCUS system scope consistency，不是为提高NPV。Wei12%保留REFERENCE_ONLY_CO2_EOR，Yuan10%保留REFERENCE_ONLY_COAL_CCUS；不平均、不做折现率敏感性分析。

IEA2020网页检索确认8%/30年，但其具体适用段落为制氢成本比较，不能表述为所有CCUS实际融资率或全链统一寿命。继续取得原始PDF定位页码。历史 STOP_FOR_USER_DECISION_discount_rate.json 由本授权取代，保留审计轨迹；SOURCE_AUDIT仍未通过。

## Stylized downstream CO2 routing versus EOR-associated storage

用户决策007：保留xi=0.20及现有双流结构，MODEL_ASSUMPTION；完整授权见 docs/USER_DOWNSTREAM_ROUTING_DECISION.txt。其含义为 baseline routing share of captured CO2 allocated to the CO2-utilization/EOR commercial route, with the remainder allocated to a dedicated geological-storage route。20/80是本研究结构假设，不是齐鲁—胜利实测分流、物理利用效率、EOR封存率或全国统计比例。

q_u是EOR路径，q_s是独立地质封存路径，实际Q=q_u+q_s。EOR-associated storage is embedded in the reduced-form abatement/value treatment and is not counted as a second physical flow。eta是reduced-form effective net-abatement proxy，统一表示捕集链残余排放及两路净减排效应；其数值仍须单独审计。

storage_subsidy仅用于q_s，是独立封存政策工具；TRANSFER的storage-service bargaining也仅用于q_s。q_u仅参与CO2销售议价与EOR经济活动。JV/SOE公式保持原样，交易未匹配时实际流量仍按原逻辑处理。齐鲁—胜利仅为物理源汇、EOR路线、运输距离及EOR技术经济证据锚点。

正确论文表述：A baseline routing share of 20% is assumed for the utilization/EOR pathway, while the remaining 80% is assigned to a dedicated geological-storage pathway. This split is a structural model assumption rather than an observed feature of the Qilu–Shengli project.

历史STOP_FOR_USER_DECISION_utilization_fraction.json已由本授权解决，保留历史文件供追溯。该假设不导致来源Gate失败；继续其余来源审计，不改变求解器、状态、流量、议价或补贴公式。

## 2026-09-20 决策008：综合平台与线性总能力映射（资产边界前置条件未通过）

完整用户规则归档于 docs/USER_U_CAPEX_LINEAR_MAPPING_DECISION.txt。U正式含义为 Integrated downstream utilization-and-storage platform CAPEX；共享单次投资覆盖两路设施，保留一个x_U；排除捕集、已计入C的源端压缩、109 km长输干线、T运输资源成本及重复设备成本。路径OPEX分别按q_u/q_s计费，不另加storage_capex。

用户已授权总能力线性映射1063×(.50/.70)=759.2857142857143 million CNY，不使用xi、q_u、q_s缩放或拆分投资，不使用规模指数。该条件成立后的正式值为MODEL_ASSUMPTION，capex_U_multiplier范围[.70,1.30]仍为DESIGN_RANGE_ASSUMPTION。各模式、动态、commit-now、代理目标和边界统一使用同一基准。

**前置核验结果**：再次检查业主24页原报告，PDF16–19页/印刷14–17页。表4.3分列捕集3.4115亿元与驱油封存10.63亿元，但未明确排除109 km干线或给出资产组成。不能以项目名或捕集分列推断长输管道必定排除。也没有证据认定它一定包含管道。

按本次决定第3节“如果原始报告无法判断……立即STOP_FOR_USER_DECISION”，暂不使用1063计算正式U CAPEX。第18节不再询问容量映射已遵守；当前问题仅为资产边界证据不足。注册表两个参考条目按用户指定名称与EMPIRICAL身份登记，资本条目保持REFERENCE_ONLY，未经核验不升级CAPEX_ONLY。

未写入759.2857142857143正式配置，未启动依赖该资本值的校准模块或八项测试；这些应在前置条件解决后实施，不能通过代码测试声称资产边界已经得到原文证明。已有58项测试结果仍为上一阶段验证，未重跑无关测试。

## 2026-09-20 决策009：PIPELINE_EXCLUDED，U CAPEX停止点解除

用户已完成资产边界专项核查，完整原文归档 docs/USER_PIPELINE_EXCLUDED_DECISION.txt。正式接受PIPELINE_EXCLUDED，资产边界证据等级A；不再就1063是否包含干线询问。年度报告投资/能力为本地独立核验，审批号、招标及槽车时间线为用户核查提供，未冒称本轮独立下载验证。

1063 million CNY与.70 Mt/year为经验工程参照；正式综合平台CAPEX=1063×(.50/.70)=759.2857142857143 million CNY，MODEL_ASSUMPTION。xi不参与换算，管道不再次扣减或另行加资本支出，1.70 Mt/year运输能力不用于U缩放。历史8.1亿元仅EARLY_PROJECT_INVESTMENT_ESTIMATE_REFERENCE_ONLY。

资产判定文件：config/U_CAPEX_ASSET_BOUNDARY_DECISION.json。正式已批准数值写入config/source_backed_approved_inputs.json（批准输入集合，非可运行最终配置）；其他来源尚未通过，不以旧值填满新配置。换算函数src/eor_cost_calibration.py仅实现已授权线性公式，不复刻未确认Wei方程，未改动态求解器。

旧U CAPEX STOP文件保留历史，现由本决定解除。后续所有模式、commit-now、代理和V2边界必须使用同一CAPEX基准；完整执行仍待剩余来源Gate通过。


## 2026-09-20 决策010：EOR两部制生命周期映射

用户原文归档docs/USER_EOR_TWO_PART_OPEX_DECISION.txt。全成本吨均化提案明确不采用；历史STOP_FOR_USER_DECISION_eor_opex_mapping.json已由本授权解决。固定EOR年费按基准fresh支路能力缩放，并在x_U=1后每年发生，包括q_u=0；只有变动费生命周期吨均化后乘q_u。基准缩放冻结后xi变化不自动改固定费。总U固定费仍待独立封存/共享成本审计，不提前填零。

新增docs/EOR_OPEX_COMPONENT_CROSSWALK.md和source_audit/eor_opex_component_crosswalk.csv（24行，12必需字段）。Li2022为主；Miao重复组件不相加。式3已核实资本、固定运营、变动运营和税分列。10.68Mt可作为累计fresh分母，平均0.712Mt/年，对0.10Mt/年模型基准的缩放因子0.1404494382022472。费用仍缺完整井设施计费基数及2019美元到人民币的来源核验；不套用Miao三项条件合计，不使用当前汇率或通胀升级。

src/eor_cost_calibration.py实现独立两部制函数；新增19测试覆盖成本发生、零流量负担、xi冻结、回收只入成本、资本/其他路径排除及Li/Miao去重。完整pytest97 passed in2.48s。所有合成测试值仅为验证，不进入正式参数。新增6条Li文献模型输入注册记录，当前37行21列；正式EOR fixed component和unit cost仍不填猜测值。

新停止点为Fig5年度原始数值可得性：出版商图像已视觉核对，15年四条曲线双轴无逐点标签；表格引用图5，数据声明Data will be made available on request。文字累计油吨数不能直接替代逐年桶数。图像数字化需要承认估读误差并获得研究授权；没有擅自估点、调整曲线满足合计或联系作者。详见STOP_FOR_USER_DECISION_eor_annual_data.json。两部制规则和U CAPEX均不再询问，GATE_SOURCE_AUDIT未通过，正式12288行未启动。


## 2026-09-20 决策011：最小必要图像数字化

授权归档docs/USER_LI_FIG5_DIGITIZATION_DECISION.txt。纠正先前“必须完整15年路径”的前提：线性变动费只依赖累计F/R/B；F=10.68Mt来自正文，fixed缩放不依赖图形。出版商高分辨率原JPEG已下载1712×954/278131bytes，并记录SHA256、日期和URL。

完成右轴15个油产量marker坐标、逐点上下界及累计值，约20.8million bbl；不采用无来源桶吨换算、不向2.97Mt强制校正。回收曲线第11年完全被绿色marker遮挡，替代注入曲线第5年也遮挡中心，未推断隐藏点或插值。触发本次决定第22节C/E，新STOP仅为遮挡点处置，不重新询问数字化授权。

输出位于source_audit/li_fig5_digitization/，包括原图、metadata、points、uncertainty、totals及LI_FIG5_DIGITIZATION_AUDIT.md。R_total/正式费用尚未生成；新增轴转换和累计费用函数及9项测试，完整106项通过（2.20秒）。两部制固定费用仍需井设施基数/货币口径等来源审计，总SOURCE_AUDIT_GATE未通过，12288行未启动。


## 2026-09-20 决策012：固定4:1 EOR收益映射

归档docs/USER_EOR_FIXED_RATIO_DECISION.txt；正式ratio=4.0 t fresh CO2/t incremental oil，MODEL_ASSUMPTION。新校准函数实现Q_oil=q_u/4及P_o=P_oil(CNY/t-oil)/4。现有求解器q_u为Mt/年，吨制接口显式×1e6，基准25,000t-oil/年；B_u=P_o-c_u公式不变。已批准输入集合增加ratio，未填未经审计的正式油价或P_o。

Fig5油曲线/正文2.97Mt退出正式收益校准，旧文件不删除；新classification.json单独记录用途变化。两部制成本不变，R_total仍进入回收和再注入电耗，不设0、不以4:1消去。剩余遮挡停止点按本次第12节改为EOR_OPEX_DATA_GAP，收益图像依赖已解除。详见docs/EOR_FIXED_RATIO_REVENUE_AUDIT.md及STOP_FOR_USER_DECISION_eor_opex_data_gap.json。

新增9项收益测试，完整115项通过（7.60秒）。原Outcome包含NaN导致初始相等断言失败，修复测试比较方式后通过；没有求解器改动。原formal257文件及冻结config哈希复核一致。Source audit仍未通过，12288行未启动。


## 2026-09-20 决策013：固定回收比rho_R=1.0

归档docs/USER_EOR_RECYCLE_RATIO_DECISION.txt；fixed lifecycle-average回收比1.0为MODEL_ASSUMPTION，写入approved inputs。R=q_u、I=2q_u仅内部处理工作量，不增交易/碳收益/外运/产油，4:1收益不变。所有LiCO2精细数字化终止，历史文件保留并由新classification标为REFERENCE_ONLY_NOT_USED_IN_FORMAL_RECYCLE_CALIBRATION。原Fig5回收点OPEX数据停止解除。

MIT原报告PDF及Abuov2022全文XML已下载/核验：MIT PDF41/印刷37节3.4.4参照1.1，Abuov gross15.77/net7.96/recycle7.81，均只为文献支持，不改正式1.0。20.4+38=58.4kWh/t fresh，×0.085=4.964USD/t为CO2电费分量，不是完整OPEX。国家统计局2019汇率6.8985检索核验，未做价格年通胀升级。

新增11案例，完整126项通过（2.57秒），旧formal257文件及冻结config哈希一致。动态求解器未修改。

新停止项：Li表4/5的新井、逐井维护费的资本基数不明确，不能自动采用Miao整项资本百分比合计。条件整项计算10.9536million USD/year尚未采用；详见docs/EOR_RECYCLE_RATIO_AUDIT.md。需审定是否允许整项资本代理基数。Source audit未通过，完整正式费用/12288行未启动。


## 2026-09-21 决策014：正式 EOR 简化成本（覆盖此前两部制映射）

正式 c_u=15×6.8974=103.461 CNY/t fresh CO2，MODEL_ASSUMPTION、A-，以 Guo et al. (2020), DOI 10.1016/j.petrol.2019.106720 的 O&M benchmark 为依据。国家统计局2020统计公报已独立核实汇率6.8974；Guo表1的15目前来自用户明确决定，独立表格核验继续。该来源的注入量口径迁移到本模型 fresh CO2 分母属于明确的模型假设，不是齐鲁观测。

EOR-specific fixed OPEX=0；Li/Miao逐井维护费、10.9536 million USD/year和4.964 USD/t电费均不叠加。rho=1仅保留技术工作量解释，4:1收益不变。q_u为Mt时，q_u×103.461直接得到million CNY。共享U CAPEX、运输和q_s储存成本独立计费；EOR固定分量为0不代表未经审计的其他平台费用已被确定。

Li/Miao组件表及历史工具保留为REFERENCE_ONLY_NOT_USED_IN_FORMAL_EOR_OPEX。解除EOR_FIXED_MAINTENANCE_BASE及相关井资本基数/固定费聚合停止项。今后标量来源优先直接代表值，不为设备级拆分停工；仅按本次用户决定第15节A–D及原规范Gate失败规则停下询问。SOURCE_AUDIT仍在进行，未冻结正式配置或启动12288行。
