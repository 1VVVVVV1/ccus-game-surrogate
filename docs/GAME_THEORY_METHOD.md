# 动态博弈方法

状态 s=(t,j,x_C,x_U)，t=0,...,29。碳价为物理概率 CRR 树节点，
p=(exp(mu*dt)-d)/(u-d)，u=exp(sigma*sqrt(dt))，d=1/u。
终期 continuation=0。J_i=pi_i+(1/1.08) E[V_i(next state)]。

动作 d_i 属于 {0,1-x_i}，当前利润使用旧 built state，投资当期支付 CAPEX，
下一期设施状态 max(x_i,d_i)。按 t 降序、j 升序、x_C 后 x_U 的 0/1 顺序递推。

TRANSFER/JV 先枚举容差 1e-10 的纯 Nash。保留 tie-break 前数量。
多重均衡先按规范的精确 Pareto 不等式删除被支配者，再最大化双方总价值、
最大化双方价值较小者、最小化投资数量、字典序。并列比较使用固定 tie_tolerance。
无纯均衡时仅在完整 2×2 游戏求内点混合均衡；失败即停止。
STATE_OWNED 最大化系统价值，再按投资数量和字典序选择。

从 (0,0,0,0) 以概率 1 前向传播，逐状态逐动作按联合概率累计折现利润。
该计算独立于后向价值的提取，两者严格核验。每年状态质量容差 1e-12。
均衡复杂性及交易概率定义见 USER_DECISIONS.md。

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


### Source-backed EOR revenue amendment: fixed 4:1 conversion

A fixed EOR conversion ratio of 4 tCO2 per tonne of incremental oil is imposed as a structural model assumption. Accordingly, incremental oil production is calculated as q_u/4, and gross EOR revenue equals (q_u/4) times the oil price. This ratio is not claimed to be an observed operating performance of the Qilu–Shengli project.

P_o=P_oil(CNY/t-oil)/4 denotes gross revenue per tonne of fresh EOR CO2; the existing bid P_o-c_u is unchanged. In solver units q_u is Mt/year and monetary outcomes are million CNY/year. Recycled CO2 is not added to q_u. Fig5 oil values and textual2.97Mt are reference-only for revenue. The two-part OPEX mapping remains unchanged and its remaining data gaps are separate from revenue. No formal oil price is assigned before currency/unit audit.


### 2026-09-20固定回收比更新

Recycled CO2 is represented by a stationary lifecycle-average ratio of one tonne per tonne of fresh CO2 routed to EOR. Actual recycle rates vary over project life. R=q_u and I=2q_u affect internal injection/recycling electricity only; external flow, credits, transport and oil revenue are not doubled. Li Fig5 CO2 curves are reference-only. The 58.4kWh/t fresh (4.964USD2019/t) component is not full EOR variable OPEX. Fixed OPEX still applies after U is built, including zero-flow years.


## 2026-09-21 决策014：正式 EOR 简化成本（覆盖此前两部制映射）

正式 c_u=15×6.8974=103.461 CNY/t fresh CO2，MODEL_ASSUMPTION、A-，以 Guo et al. (2020), DOI 10.1016/j.petrol.2019.106720 的 O&M benchmark 为依据。国家统计局2020统计公报已独立核实汇率6.8974；Guo表1的15目前来自用户明确决定，独立表格核验继续。该来源的注入量口径迁移到本模型 fresh CO2 分母属于明确的模型假设，不是齐鲁观测。

EOR-specific fixed OPEX=0；Li/Miao逐井维护费、10.9536 million USD/year和4.964 USD/t电费均不叠加。rho=1仅保留技术工作量解释，4:1收益不变。q_u为Mt时，q_u×103.461直接得到million CNY。共享U CAPEX、运输和q_s储存成本独立计费；EOR固定分量为0不代表未经审计的其他平台费用已被确定。

Li/Miao组件表及历史工具保留为REFERENCE_ONLY_NOT_USED_IN_FORMAL_EOR_OPEX。解除EOR_FIXED_MAINTENANCE_BASE及相关井资本基数/固定费聚合停止项。今后标量来源优先直接代表值，不为设备级拆分停工；仅按本次用户决定第15节A–D及原规范Gate失败规则停下询问。SOURCE_AUDIT仍在进行，未冻结正式配置或启动12288行。


## 2026-09-21 Guo原文独立核验完成及归因更正

出版商全文表1确认h=15 USD/tCO2，式2.9支持源端新鲜捕集量对应注入量，脚注7说明CO2回收费用包含在EOR运营费中。式2.7另列固定F，式2.8因其在原文运营优化中恒定而删除。当前模型存在投资进入决策，不能以该代数处理证明固定费为零。严格保留用户批准的103.461及EOR fixed=0，但后者明确标记为用户简化假设，不声称所有固定费被原文h覆盖。此前原文访问阻塞已解除；没有更改算法或增加工程拆分。证据：source_audit/eor_reduced_form/guo_original_verification.md。
