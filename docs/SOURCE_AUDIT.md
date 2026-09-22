> 2026-09-22更新：source-profile静态会计STOP已由用户100元绝对误差预算解除；完整测试及9端点/基准案例通过。下文相关STOP为历史记录。

# Empirical Source Audit — SOURCE GATE PASS

状态：SOURCE_GATE_PASS；后续source-profile静态会计预检失败，详见results/source_backed_formal/SOURCE_PROFILE_PREFLIGHT_STOP.md。决策014已解除EOR固定维护费停止项，并以103.461 CNY/t完整标量O&M覆盖历史两部制方案；下文旧停止和候选状态仅为历史，最新状态见末尾。

## 来源完成记录（覆盖下文历史待办）

1257条官方日价完整性通过，GBM三产物及source-backed配置已生成；GATE_SOURCE_AUDIT PASS。当前停止原因是后续浮点会计预检，不是来源缺失。

## 较早状态快照（2026-09-21）

已核验并进入approved inputs：C CAPEX385 million CNY、capture OPEX240、eta0.70、T资源成本28.1656、共享U CAPEX759.2857142857143、EOR OPEX103.461、EOR毛收益1101.85965、q_s注入成本代理55；以及用户固定r8%、T30、Q0.5、xi0.2、4:1换油率和rho1。油收益90×7.1×6.8974/4为跨年份文献锚定MODEL_ASSUMPTION，非实测齐鲁收益。储存55的OPEX_ONLY为模型会计归属，原文未给工程资本拆分。所有来源转换见registry及scalar_followup验证记录。

当前继续事项：官方日行情全部采集、完整性审计及GBM；其后汇总完整参数追溯、执行GATE_SOURCE_AUDIT。尚未冻结或运行source-backed正式配置。144tests通过，原formal257文件及原配置哈希不变。以下内容按时间追加，早期待办不代表当前仍未解决。

## 已完成

- Git 已按用户提供的本地 identity 初始化，冻结提交 4f34c2ba31dc3167e4bbfbd67d2a371c6a0d9a6f；没有 remote 或上传。
- 原方法验证源码、配置及正式结果哈希保持一致。
- Grade 标准、候选来源目录和原始检索响应已保存。
- Engineering 原文支持其他 CCUS 碳注入成本 50–60 CNY/t；按规范可导出 55，严格限于 injection-cost proxy。
- 议价权和 JV 股份仅作为用户授权的 MODEL_ASSUMPTION，不宣称行业观测。

## 历史决策阻塞：运输市场价格基准（已解决）

旧 transport_market_price=125 CNY/t 尚无已验证 Grade A/A- 的实际收费依据。规范指定运输论文题名与 DOI 已交叉确认，但原文抓取受阻。0.26 CNY/(t·km) 尚未完成原文核验，即使核实也属于单位运输成本，不能自动当作收费或外推为 125 CNY/t。

公开检索未建立 125 元的可靠来源闭环；这不证明此类来源不存在。不可将搜索命中、索引摘要或无关研究的参数表当作实证收费。不得擅自假定距离、收费加成或跨项目缩放。

用户已于本轮明确改为 MODEL_ASSUMPTION，不再要求将 125 元验证成实际收费，不再就此项询问。真实成本和距离仍待核实。

### Transport market price

Baseline: 125 CNY/tCO2。Status: MODEL_ASSUMPTION。

Paper use: Internal transport-service transfer-price benchmark。

Reason: No Grade A/A- source was verified that supports 125 CNY/tCO2 as an observed Chinese CCUS transport tariff. Do not confuse with empirical transport cost coefficients.

情景域 [75,200] CNY/tCO2：DESIGN_RANGE_ASSUMPTION；Scenario domain for contractual transport-service pricing。不是实际收费统计分布或经验置信区间。

### Pipeline transport real-cost coefficient

Candidate empirical value: 0.2584 CNY/(tCO2·km)。Status: EMPIRICAL（候选值，数值由用户提供，原文数值尚待独立核验）。Source: Journal of CO2 Utilization, 2025, DOI 10.1016/j.jcou.2025.103057。

Use restriction: May only be converted into CNY/t after a source-backed source-sink distance is established。未假定任何距离，不将成本包装为市场收费。此 registry 行不等于 GATE_SOURCE_AUDIT 已通过。

会计原则保持：TRANSFER 的 P_tr_market×Q 在 C 支付和 T 收入中抵消；系统真实成本仅为 C_T_real。固定流量下内部支付不创造系统价值，但市场收费仍可能通过交易条件和投资激励改变均衡流量，因此不能推论 equilibrium system value 对 tariff 必然不变。

## 尚待审计，不表示已穷尽检索

| 参数 | 当前状态 |
|---|---|
| horizon、discount rate | 未完成来源核查 |
| P0、mu、sigma | 尚未采集官方碳价完整日序列，未校准 |
| capture capacity、capture CAPEX | 泰州论文书目已确认，数值及工程边界待全文核验 |
| capture OPEX | 240/208 数值及总成本/运营成本边界未核实 |
| utilization fraction | 未完成来源核查 |
| transport real cost、source-sink distance | 成本系数原文及适用距离未闭环；market tariff 已明确为模型假设 |
| U CAPEX | 未找到已验证的同容量、同资产边界数值，未缩放旧值 |
| utilization revenue、cost | 780 与 94.1654 均未形成原始证据链，未沿用 |
| effective abatement fraction | 尚未定位具体 LCA 来源及其系统边界 |

注册表目前登记已支持的注入成本代理、明确模型假设及用户允许登记的候选管道成本系数，其他核心参数不填入虚构 formal_value。source-backed baseline、12288 行、33 个代理 target、同步诊断与 61 项 V2 搜索均未执行。

## 本轮补充核查与停止点

用户的 125 元定价决定已完全落实；历史 STOP_FOR_USER_DECISION.json 中的 tariff 阻塞由该决定取代，文件保留供追溯。

- S06：Economic evaluation of CO2 pipeline transport in China，DOI 10.1016/j.enconman.2011.10.022，Crossref/OpenAlex 书目一致。用户提供的 1–5 Mt/year、100–500 km 和 0.1–0.6 CNY/(t km) 尚未完成原文核验，也不是本模型某个源—汇项目的实际距离。
- S07：Economic evaluation on CO2-EOR of onshore oil fields in China，DOI 10.1016/j.ijggc.2015.01.014，索引发现 OSTI 开放版本；本轮下载 TLS 握手超时，未获得正文，不能用摘要支持 U CAPEX 或收益。
- 泰州出版商 PDF 返回 HTTP 403；Carbon Neutrality PDF 地址返回 3038 字节 HTML 验证页，未将其保存或认作 PDF。
- 检索响应及请求结果保存于 transport_followup/。这些结果证明本轮证据未闭环，不证明相关来源不存在。

**位置：新规范第 3、12、14、15、21 节及用户运输补充决定第 3、8、9 项。**

当前不能唯一确定本模型对应的源—汇项目、U 端利用路线及资产范围。即使取得另一项目的距离和成本，也不能擅自将其与泰州捕集规模拼接或缩放。需要用户指定拟校准的源—汇项目及 U 端利用路线，或提供相应项目资料以锁定口径，然后继续来源核查。这是新的研究设计缺口，不是再次询问 125 元定价。

GATE_SOURCE_AUDIT 尚未通过。其余未核实参数仍保持待审计；尚未开始官方序列校准、新配置冻结、正式求解、代理、同步诊断和 V2 边界。源码和既有方法验证结果未改动。

## 最新决定：齐鲁—胜利锚点已固定

本节取代前文要求选择项目/路线的停止点。用户原文已归档 docs/USER_DECISION_QILU_SHENGLI.txt。项目、路线和 109 km 已指定；距离的官方证据仍待补齐，但不以该选择再次提问。

The Qilu Petrochemical–Shengli Oilfield project is used as the physical source–sink and CO2-EOR route anchor, while the stochastic game retains the study's own institutional structures for TRANSFER, JOINT_VENTURE, and STATE_OWNED.

Wei、Li、Miao 三篇指定论文的题名和 DOI 已分别经 Crossref/OpenAlex 确认。Elsevier 三个接口均只返回 coredata，未含原文表格或公式；Wei 的 ScienceDirect 页面/PDF 返回 403，FULL 接口返回 429，OSTI HTTPS/HTTP 下载超时。Bing 返回无关结果，百度返回验证码页面，均未用作 109 km 数值证据。这些访问失败不说明论文或项目数据不存在。

**当前真正缺口：U CAPEX/O&M 方程及同项目输入、增量产油/CO2 口径未核实。** 用户给出的参数值完整保存在授权原文中，但按“重新核验原文后登记”的要求，尚未当作已核验数值写入正式 registry。尚未编写 eor_cost_calibration.py，避免猜测回归系数；没有将 USD/bbl 直接转成 CNY/tCO2。换汇、价格基年、新注入/循环 CO2 分母、增量油与总产油、井数/井深/井组及面积仍需原文界定。

下一步需取得 Wei Table 1/2/4 与两篇同项目研究的可读取全文或表格附件，才能继续公式实现和参数映射。新停止依据是核心字段仍不能可靠映射（用户最新决定第 2–4、8、12 项），不是重问路线或锚点。原 30 年/折现率、内生 Nash 价格、125 内部收费保持原状；0.2584×109=28.1656 的算术关系成立，但尚未授权跳过系数原文核验进入正式配置。


## 用户提供 Yuan PDF 后的最新进展


1. 用户提供的 Yuan_2024_CCUS燃煤电厂经济性.pdf 实为袁鑫等，2023，热力发电 52(7):33–40，DOI 10.19666/j.rlfd.202303034。已提取全文并视觉核验 PDF 第 2、3 页；原文件未改名或改写。Crossref 此 DOI 返回 404，不能据此否定 PDF 出版信息。
2. 第 34 页表 1 是引用 2019 技术路线图的未来成本预测；第 35 页的 20 年、10%、200 km、100 元/t 属作者情景设定。其甲烷干重整部分不适用于已固定的 EOR 路线。没有把这些数值替换进本研究配置。
3. 本地《中国 CCUS 年度报告（2023）》PDF 第 19 页/印刷第 11 页、2.1 节，明确记载齐鲁—胜利已建管道 109 km、设计最大输量 170 万吨/年。报告署名中国21世纪议程管理中心、全球碳捕集与封存研究院、清华大学，按来源标准 Grade A- 登记距离。设计管道能力不等于捕集能力或实际年度注入量。
4. UK-China 2024 报告 PDF 第 15 页表 2-3 另列 108 km、Under construction；施工状态口径不同已记录，但“规划/竣工差异”仅是待核实解释，未当作已证实原因。用户固定 109 不变，不平均，业主/国家能源局交叉核验仍待补齐。
5. 已通过公开全文读取入口获取 Carbon Neutrality 原文。3.2.4 节的 240 CNY/t 是泰州在建项目预计运营成本，不是投产实测值；未以 EMPIRICAL 写入正式输入。208 的成本边界仍待原文核验。

## 下载与证据有效性

其余论文继续自主检索下载：Wei 的 OSTI 多个公开入口均超时，出版商返回 403/429 或验证页；Li/Miao 出版商全文亦未取得。112998 字节 Wei 响应实际为验证码及脚本，明确不算下载全文成功。PNNL 猜测路径是 404，不是原文。公开阅读代理来源路径完整记录，不混同为原始发布机构。已取得的 Carbon Neutrality 是 HTML 全文，不伪装成 PDF。

没有可复用的已配置图书馆访问入口。后续合法机构访问需要用户提供其实际使用的图书馆数据库入口网址，由用户在浏览器中登录；不请求或使用账号密码。

## Gate 与实现状态

U CAPEX/O&M 原始方程、回归系数及同项目必要输入、增量产油/CO2 比率尚未核实；GATE_SOURCE_AUDIT 未通过。不能据此编写 eor_cost_calibration.py 的猜测公式，不能生成正式 config 或运行 12288 行。

已完成的距离登记不等于总运输成本已通过；0.2584 原文数值仍待核验，因此 28.1656 未写入正式配置。原求解器、30 年设定、折现率和 Nash 内生价格均未改动。


## ScienceDirect 浏览器核验更新

Wei 2015 开放 HTML 全文已可读取，取代此前“未取得原文”的当前状态（历史记录保留）。Table 4 八项文献参照已登记；Table 1/正文存在费用冲突，公式显示亦有疑点。详见 docs/WEI_2015_FORMULA_AUDIT.md。尚无 PDF 下载成功，来源 Gate 未通过。

## 2026-09-20 统一冲突规则落实

采用 docs/USER_SOURCE_CONFLICT_RULES.txt；Wei 举升 1 USD/STB 已登记，0.25 仅冲突记录。注册表扩为 21 列，新增成本边界与受限冲突状态。公式 7/9 不实现；主模型未使用 CRF，公式 12 仅参考。来源 Gate 尚未评定通过，不启动正式数值计算。

工程距离 109 km 已在《中国 CCUS 年度报告 2023》PDF 第19页/印刷第11页核对；成本系数 .2584 尚待原文核验。后续逐项审计 U CAPEX、CO2-EOR 收益与 OPEX、减排边界以及捕集项目容量与成本口径。历史停止记录均不覆盖最新授权。

## 统一冲突规则后补充检索

S12 Lu2025全文XML已下载，捕集端表格已核验；S13业主驱油封存投资披露仍待原件表格及资产边界核对；S14省能源局提供109 km交叉线索。详见 docs/QILU_DIRECT_COST_FOLLOWUP.md。新成本未进入正式配置。

当前研究决策见 STOP_FOR_USER_DECISION_discount_rate.json；8%/12%尚未授权选择。其余文献审计仍不完整，选择折现率不等于来源Gate自动通过。

## 2026-09-20 决策006：FORMAL UNIFIED DISCOUNT RATE DECISION — 8%

完整授权见 docs/USER_UNIFIED_DISCOUNT_DECISION.txt。simulation.economic_discount_rate=0.08，MODEL_ASSUMPTION；所有主体、模式、commit-now、边界和代理目标统一 gamma=1/1.08。30年继续保留。决策依据为 integrated CCUS system scope consistency，不是为提高NPV。Wei12%保留REFERENCE_ONLY_CO2_EOR，Yuan10%保留REFERENCE_ONLY_COAL_CCUS；不平均、不做折现率敏感性分析。

IEA2020网页检索确认8%/30年，但其具体适用段落为制氢成本比较，不能表述为所有CCUS实际融资率或全链统一寿命。继续取得原始PDF定位页码。历史 STOP_FOR_USER_DECISION_discount_rate.json 由本授权取代，保留审计轨迹；SOURCE_AUDIT仍未通过。

### IEA与官方碳价入口核验结果

S15：IEA2020官方PDF已下载（14417258字节，SHA256 98357d3403375b2aa2f25dc061c3fce39b03719d65d6d6f155962802435aa187）。PDF第75页/印刷第74页图2.14注释经文字及页面图像核验，明确8%与30年；其范围是不同制氢路线成本比较。两个正式参数登记MODEL_ASSUMPTION、Grade A基准，不宣称实测融资成本。

上海环交所每日概况官方目录已保存。2021年目录提供历史分页；本轮2026年目录响应PublishDate为2026-08-14，未覆盖校准日。不能将该目录完整性或第三方收盘数据当作官方完整序列。尚未生成P0/mu/sigma或填补任何缺失数据。

## 当前阶段核查与研究设计停止点

注册表22行21列，8%、30年、Wei12%/Yuan10%参照行及枚举检查通过；旧配置哈希未变。IEA PDF页面证据已保存。

新发现的映射问题详见 docs/EOR_FLOW_MAPPING_AUDIT.md：现有模型xi表示EOR与独立封存两条互斥流量的分配，不能从EOR伴生封存事实直接推出xi=.20或1。前者缺经验依据，后者会使独立封存议价/补贴通道恒零。按新规范第3/7节及用户禁止擅改模型/参数要求，暂停依赖该值的正式校准并请用户决定。折现率问题不再询问。其余来源审核尚未全部完成，任何单项决定不等于总Gate通过。

## Stylized downstream CO2 routing versus EOR-associated storage

用户决策007：保留xi=0.20及现有双流结构，MODEL_ASSUMPTION；完整授权见 docs/USER_DOWNSTREAM_ROUTING_DECISION.txt。其含义为 baseline routing share of captured CO2 allocated to the CO2-utilization/EOR commercial route, with the remainder allocated to a dedicated geological-storage route。20/80是本研究结构假设，不是齐鲁—胜利实测分流、物理利用效率、EOR封存率或全国统计比例。

q_u是EOR路径，q_s是独立地质封存路径，实际Q=q_u+q_s。EOR-associated storage is embedded in the reduced-form abatement/value treatment and is not counted as a second physical flow。eta是reduced-form effective net-abatement proxy，统一表示捕集链残余排放及两路净减排效应；其数值仍须单独审计。

storage_subsidy仅用于q_s，是独立封存政策工具；TRANSFER的storage-service bargaining也仅用于q_s。q_u仅参与CO2销售议价与EOR经济活动。JV/SOE公式保持原样，交易未匹配时实际流量仍按原逻辑处理。齐鲁—胜利仅为物理源汇、EOR路线、运输距离及EOR技术经济证据锚点。

正确论文表述：A baseline routing share of 20% is assumed for the utilization/EOR pathway, while the remaining 80% is assigned to a dedicated geological-storage pathway. This split is a structural model assumption rather than an observed feature of the Qilu–Shengli project.

历史STOP_FOR_USER_DECISION_utilization_fraction.json已由本授权解决，保留历史文件供追溯。该假设不导致来源Gate失败；继续其余来源审计，不改变求解器、状态、流量、议价或补贴公式。

## 2026-09-20：双流决定、完整测试及新增原始证据

新增tests/test_downstream_routing.py五个测试案例：三模式0.10+0.40=.50；无独立封存时EOR不触发storage支付/补贴；独立封存费用转移及补贴仅按.40计入。重点核算测试10项通过，完整pytest58项通过（8.01秒）。未改src或冻结配置，也未覆写旧formal结果。

S13业主债券报告已下载并视觉核验表4.3/4.4及后页，解决先前访问限制。总投资3.4115/10.63亿元及年度能力披露保留为文献参照，不冒充匹配本模型的CAPEX。注册表现26行21列。

官方碳价目录采集58页（请求均成功），发现863个唯一日报URL：2021年114，2022–2025各150，2026年149，最近2026-08-14。页数/覆盖不足以证明完整历史序列；仅保存检索目录，未填补、平滑或校准。目录和哈希见routing_followup/carbon_catalog/catalog_manifest.json。

当前需要研究决定为U CAPEX资产范围及跨容量映射（详见docs/U_CAPEX_MAPPING_DECISION.md）。工程总投资不能自动按Q_bar或xi缩放，亦不代表独立封存渠道投资为零。根据新规范第3节第3项停止依赖该参数的正式实现；本停止点不是对已授权xi=.20重新提问。

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


## 2026-09-20：U CAPEX实现验证、运输原文闭环及后续审计

完整pytest已由此前58项扩为78项并全部通过（2.58秒）：U CAPEX新增17项，运输资源成本核算新增3项。此前新增CAPEX测试曾因Windows默认编码读JSON失败，显式UTF-8后完整75项通过；随后新增运输测试的最新完整结果为78项。测试在隔离配置下验证已批准值，不代表尚未完成的source-backed正式运行。三模式资本支付、乘数、xi独立性、不可逆单次投资、运输/封存成本独立性以及内部运输支付抵消均通过。

冻结model_config.game.json SHA256仍为3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76。对照results/resume_before_1d8388dd.json，旧formal的257个文件逐一哈希一致。未改动态求解器；验证摘要见post_u_capex/validation.json。

S03出版商HTML原文表2确认：设备0.2163、维护0.0319、电力0.0102，合计0.2584 CNY/(tCO2 km)，因此cost_boundary=LEVELIZED_CAPEX_PLUS_OPEX。原情景为20年、8%、2022价格、250km和60万吨/年。按既有用户授权登记0.2584×109=28.1656 CNY/tCO2，DERIVED_FROM_EMPIRICAL；这是有情景条件的文献成本基准，不是实测纯OPEX或统一收费。源模型压缩站及电力已计入；最终捕集压缩资产仍需核对重叠。没有额外新增T资本支出，125仍为内部支付MODEL_ASSUMPTION。注册表现31行21列，已批准输入集合更新，完整正式配置仍未生成。

S08 Li2022第4节及表2–7、S09 Miao2025第3节及表1–3已从出版商HTML读取并保存原文摘录；未宣称取得PDF。Li规划15年新捕集10.68 Mt、增量油2.97 Mt，油量/CO2分母及固定费、回收再注入量必须统一；旧780及94.1654不沿用。Miao净减排核算不包含采出油后续燃烧，不把其CROI或净减排总量自动写成eta。

S01正确书目链接https://academic.oup.com/ce/article/9/4/15/8071291已确认，浏览器仍连接超时，不能声称核实450 million CNY。官方行情查询页https://shyx.cneeex.com/qdata.html?1785740461457可读，2026-09-18综合价格行情收盘95.63元/吨；该单日快照已存档。历史目录至8月14日不代表数据终点，未把不完整目录校准成GBM，也未自动拼接不同价格定义。

新研究停止点：EOR固定O&M及年际变化如何跨容量映射到本模型恒定成本参数。详见docs/EOR_OPERATING_COST_MAPPING_DECISION.md；依据新规范第3节第3/8项，不擅自将固定费吨均化或缩放。建议生命周期累计EOR运营费用/累计新CO2映射，须用户审定其成本发生方式。PIPELINE_EXCLUDED及U CAPEX无需重新决定。来源Gate未通过，正式12288行、33代理目标和61项V2尚未启动。


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

决策014验证：完整137项测试通过（8.37秒）；原formal257文件及冻结配置哈希不变。NBS2020汇率已核验，Guo原文HTTP403/浏览器读取超时，15 USD/t表格独立核验状态诚实保留待完成，不重新询问用户已批准的标量选择。

继续审计发现：泰州政府2025-12-07正式报道总投资3.85亿元，形成385 million CNY捕集项目资本候选，尚未写入正式输入；不是沿用未经核实的450。Carbon Neutrality原文明确240为建设期预期运营成本，可作为标量OPEX benchmark，不能称已实现实测成本。待核验项仍含油价、净减排比例、储存成本口径和完整官方碳价序列。证据及验证结果见source_audit/eor_reduced_form/。


## 2026-09-21 Guo原文独立核验完成及归因更正

出版商全文表1确认h=15 USD/tCO2，式2.9支持源端新鲜捕集量对应注入量，脚注7说明CO2回收费用包含在EOR运营费中。式2.7另列固定F，式2.8因其在原文运营优化中恒定而删除。当前模型存在投资进入决策，不能以该代数处理证明固定费为零。严格保留用户批准的103.461及EOR fixed=0，但后者明确标记为用户简化假设，不声称所有固定费被原文h覆盖。此前原文访问阻塞已解除；没有更改算法或增加工程拆分。证据：source_audit/eor_reduced_form/guo_original_verification.md。


## 2026-09-21 剩余标量校准推进

按最新简化原则与原规范第9/10节，将capture OPEX=240（MODEL_ASSUMPTION；Carbon Neutrality节3.2.4建设期预期运营成本）及eta=0.70（DERIVED_FROM_EMPIRICAL；Dong等JCP2025 DOI10.1016/j.jclepro.2024.144557出版商highlight约30%衍生排放抵消）加入已批准输入。eta仅reduced-form代理，不是ETS核证比例。Crossref确认卷486/144557；不是误用捕集率。两项均无需工程重建。未采用208总成本叠加。官方碳价分页缺口已定位：第10页以后跳到www.cneeex.com/zcms/ui/catalog/...动态页面，原先只抓静态目录不能说明完整性。
