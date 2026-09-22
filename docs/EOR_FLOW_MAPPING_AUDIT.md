# CO2-EOR路线与流量分配映射审查

## 已核验事实

现有 src/economics.py 的 stage_outcome 定义两条互斥流量：q_u=xi*Q*co2_matched；q_s=(1-xi)*Q*storage_matched（TRANSFER），其余模式按既定逻辑匹配。利用收益只计q_u，独立封存成本与补贴只计q_s；TRANSFER两条流分别议价。

冻结旧配置xi=0.20，仅属于方法验证参数。新规范第7节要求重新核验 utilization_fraction，未授权直接沿用。

用户固定U路线为中国陆上CO2-EOR及伴生封存。Lu2025全文明确捕集CO2输往胜利油田驱油并封存，属于同一批CO2先驱油并留存地下；未提供“20% EOR、80%独立封存”的分配比例。原文证据见source_audit/conflict_rule_followup/lu_fulltext.xml，段落以“This project establishes the precedent”开头。不能将油采收率、封存率或油/CO2质量比当作xi。

## 不能自行完成的映射

保留双流结构及xi=.20，需用户将其明确授权为MODEL_ASSUMPTION；工程锚点仍仅用于路线与来源，不能声称项目实测分流。

将xi改为1会使q_s恒为0，独立storage议价和补贴通道失去作用，并影响原规范中的条件交易价格、代理目标及边界。不能仅凭EOR工程叙述自行选择1。

将伴生封存另加为q_s会对同一吨CO2重复计量，并改变模型结构，禁止自动实施。

因此这是研究设计映射问题，不是继续查一篇公式即可自动解决的数值缺失。当前不修改xi、议价、target或边界定义。8%决定及30年已落实，不再提问。

## Stylized downstream CO2 routing versus EOR-associated storage

用户决策007：保留xi=0.20及现有双流结构，MODEL_ASSUMPTION；完整授权见 docs/USER_DOWNSTREAM_ROUTING_DECISION.txt。其含义为 baseline routing share of captured CO2 allocated to the CO2-utilization/EOR commercial route, with the remainder allocated to a dedicated geological-storage route。20/80是本研究结构假设，不是齐鲁—胜利实测分流、物理利用效率、EOR封存率或全国统计比例。

q_u是EOR路径，q_s是独立地质封存路径，实际Q=q_u+q_s。EOR-associated storage is embedded in the reduced-form abatement/value treatment and is not counted as a second physical flow。eta是reduced-form effective net-abatement proxy，统一表示捕集链残余排放及两路净减排效应；其数值仍须单独审计。

storage_subsidy仅用于q_s，是独立封存政策工具；TRANSFER的storage-service bargaining也仅用于q_s。q_u仅参与CO2销售议价与EOR经济活动。JV/SOE公式保持原样，交易未匹配时实际流量仍按原逻辑处理。齐鲁—胜利仅为物理源汇、EOR路线、运输距离及EOR技术经济证据锚点。

正确论文表述：A baseline routing share of 20% is assumed for the utilization/EOR pathway, while the remaining 80% is assigned to a dedicated geological-storage pathway. This split is a structural model assumption rather than an observed feature of the Qilu–Shengli project.

历史STOP_FOR_USER_DECISION_utilization_fraction.json已由本授权解决，保留历史文件供追溯。该假设不导致来源Gate失败；继续其余来源审计，不改变求解器、状态、流量、议价或补贴公式。
