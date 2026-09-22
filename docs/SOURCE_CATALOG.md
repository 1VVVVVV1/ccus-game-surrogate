# Source catalog — initial audit, 2026-09-20

本目录属于尚未通过 GATE_SOURCE_AUDIT 的审计工作，不能视作实证校准完成。

| ID | 文献 | DOI/URL | 核验程度 |
|---|---|---|---|
| S01 | Taizhou 500kt per year post-combustion carbon capture demonstration project, Clean Energy, 2025 | https://doi.org/10.1093/ce/zkaf011 | Crossref 书目确认，全文页访问受阻；未核实 CAPEX |
| S02 | Several key issues for CCUS development in China targeting carbon neutrality, Carbon Neutrality, 2022 | https://doi.org/10.1007/s43979-022-00019-3 | Crossref 确认；Springer 返回 JavaScript challenge，未核实 240 元口径 |
| S03 | Comparative life cycle assessment of CO2 onshore transport in China: Pipeline or tanker truck?, Journal of CO2 Utilization, 2025 | https://doi.org/10.1016/j.jcou.2025.103057 | Crossref/OpenAlex 题名及 DOI 交叉一致；ScienceDirect 403，未核实 0.26 或市场收费 |
| S04 | Large-Scale Carbon Dioxide Storage in Salt Caverns: Evaluation of Operation, Safety, and Potential in China, Engineering, 2024 | https://doi.org/10.1016/j.eng.2024.06.013 ; https://www.engineering.org.cn/engi/EN/10.1016/j.eng.2024.06.013 | Crossref 确认，期刊全文可读；成本段已核验，Grade A |
| S05 | The geomechanics of Shenhua carbon dioxide capture and storage (CCS) demonstration project in Ordos Basin, China | https://doi.org/10.1016/j.jrmge.2016.07.002 | OpenAlex 发现，摘要涉及 2010–2015 合计注入 0.3 Mt；不是本模型 0.5 Mt/年利用+封存 CAPEX 证据 |

## 已核实成本原文

S04 的 “(3) Decreasing cost for carbon injection” 段原文：

> At present, the cost of gas injection-brine extraction in salt caverns is about 20 CNY·m−3, and the cost of carbon injection in most other CCUS is about 50–60 CNY·ton−1 ...

按用户第 13 节明确授权，可取 (50+60)/2=55 CNY/t 作为 injection-cost proxy；不能表述为盐穴统一单价、全国全链条封存成本或包括 U 端 CAPEX 的总成本。

## 检索与证据

原始响应/提取文本保存于 results/source_backed_formal/source_audit/discovery/，文件 SHA256 见同级 evidence_manifest.json。Crossref 初始并行检索部分返回 429，随后用单篇 DOI API 和 OpenAlex 补充；Springer challenge、ScienceDirect 403 等访问限制如实保留。无用户账号、密码或邮箱传给文献 API。

## 运输补充决策后的候选来源

- S06：Economic evaluation of CO2 pipeline transport in China，Energy Conversion and Management，DOI https://doi.org/10.1016/j.enconman.2011.10.022。Crossref/OpenAlex 书目确认，数值原文未核实。不可将研究情景距离解释为本模型实测距离。
- S07：Economic evaluation on CO2-EOR of onshore oil fields in China，International Journal of Greenhouse Gas Control，DOI https://doi.org/10.1016/j.ijggc.2015.01.014。OpenAlex 发现 OSTI PDF https://www.osti.gov/servlets/purl/1212318；本轮连接超时，未读取全文、未接受其参数。
- S03 精确候选系数更新为用户提供的 0.2584 CNY/(tCO2 km)，原文数值仍未独立确认。125 CNY/t 不再作为文献待验证收费，而是用户明确授权的模型假设。

本轮证据及失败记录：results/source_backed_formal/source_audit/transport_followup/。最新哈希清单为 evidence_manifest_transport_followup.json；旧 evidence_manifest.json 只描述此前版本。

## 齐鲁—胜利定向核查

S07（Wei 2015）已补充 Crossref/OpenAlex 双源确认。新增 S08（Li 2022），DOI 10.1016/j.jclepro.2022.133724；S09（Miao 2025），DOI 10.1016/j.eiar.2024.107684。三篇题名均与用户指定一致，出版商 API 仅返回元数据，未获取成本表格。原始记录位于 source_audit/eor_anchor/。未通过原文数值核验，不用于正式经济参数计算。

## Yuan 补充轮

- S10：袁鑫等，热力发电 2023，52(7):33–40，DOI 10.19666/j.rlfd.202303034；本地 PDF 原文及相关页已视觉核验。文件名 2024 不作为出版年；仅背景/假设辨析，不作为齐鲁 EOR 核心参数唯一来源。
- S11：中国二氧化碳捕集利用与封存（CCUS）年度报告（2023），中国21世纪议程管理中心/全球碳捕集与封存研究院/清华大学，Grade A-。印刷第 11 页支持 109 km；与 UK-China 报告 108 km 施工中条目的差异保留待业主核验。
- S02 更新：取得公开 HTML 全文，3.2.4 节 240 为在建项目预计 OPEX，不能标为实测。实际读取 URL 和原始内容见 yuan_followup/oa_reader_log.json 及 carbon_neutrality_oa_reader.raw。
- Wei 原文仍未取得；大体积验证码/脚本响应未被误认全文。详细逐项结果见 docs/YUAN_AND_EOR_SOURCE_FOLLOWUP.md。


## ScienceDirect 浏览器核验更新

Wei 2015 开放 HTML 全文已可读取，取代此前“未取得原文”的当前状态（历史记录保留）。Table 4 八项文献参照已登记；Table 1/正文存在费用冲突，公式显示亦有疑点。详见 docs/WEI_2015_FORMULA_AUDIT.md。尚无 PDF 下载成功，来源 Gate 未通过。

## 统一冲突规则后补充检索

S12 Lu2025全文XML已下载，捕集端表格已核验；S13业主驱油封存投资披露仍待原件表格及资产边界核对；S14省能源局提供109 km交叉线索。详见 docs/QILU_DIRECT_COST_FOLLOWUP.md。新成本未进入正式配置。

### IEA与官方碳价入口核验结果

S15：IEA2020官方PDF已下载（14417258字节，SHA256 98357d3403375b2aa2f25dc061c3fce39b03719d65d6d6f155962802435aa187）。PDF第75页/印刷第74页图2.14注释经文字及页面图像核验，明确8%与30年；其范围是不同制氢路线成本比较。两个正式参数登记MODEL_ASSUMPTION、Grade A基准，不宣称实测融资成本。

上海环交所每日概况官方目录已保存。2021年目录提供历史分页；本轮2026年目录响应PublishDate为2026-08-14，未覆盖校准日。不能将该目录完整性或第三方收盘数据当作官方完整序列。尚未生成P0/mu/sigma或填补任何缺失数据。

## 2026-09-20：双流决定、完整测试及新增原始证据

新增tests/test_downstream_routing.py五个测试案例：三模式0.10+0.40=.50；无独立封存时EOR不触发storage支付/补贴；独立封存费用转移及补贴仅按.40计入。重点核算测试10项通过，完整pytest58项通过（8.01秒）。未改src或冻结配置，也未覆写旧formal结果。

S13业主债券报告已下载并视觉核验表4.3/4.4及后页，解决先前访问限制。总投资3.4115/10.63亿元及年度能力披露保留为文献参照，不冒充匹配本模型的CAPEX。注册表现26行21列。

官方碳价目录采集58页（请求均成功），发现863个唯一日报URL：2021年114，2022–2025各150，2026年149，最近2026-08-14。页数/覆盖不足以证明完整历史序列；仅保存检索目录，未填补、平滑或校准。目录和哈希见routing_followup/carbon_catalog/catalog_manifest.json。

当前需要研究决定为U CAPEX资产范围及跨容量映射（详见docs/U_CAPEX_MAPPING_DECISION.md）。工程总投资不能自动按Q_bar或xi缩放，亦不代表独立封存渠道投资为零。根据新规范第3节第3项停止依赖该参数的正式实现；本停止点不是对已授权xi=.20重新提问。


## 最新核验状态：2026-09-20 PIPELINE_EXCLUDED之后

本节取代上文历史访问状态，历史记录保留。

| 来源 | 最新证据及限制 |
|---|---|
| S03，10.1016/j.jcou.2025.103057 | 出版商HTML第2–3节、表2可读，0.2584=设备0.2163+运维0.0421；20年/8%/2022年价格/250km/0.60Mt年情景，LEVELIZED_CAPEX_PLUS_OPEX。28.1656按此前用户授权换算，不是实测收费。 |
| S08，10.1016/j.jclepro.2022.133724 | 出版商HTML第4节、表2–7可读。15年10.68Mt CO2和2.97Mt增量油是案例规划/预测，固定年费及变动费须另作模型映射。文献80km是历史规划，不替换109km。 |
| S09，10.1016/j.eiar.2024.107684 | 出版商HTML第3节、表1–3可读，提供注入/采油/回收OPEX及电耗；净减排边界排除采出油后续燃烧。 |
| S13 | 原报告投资与能力已核验；最新用户专项核查接受PIPELINE_EXCLUDED。审批/时间线补充证据来自用户审计，不冒称本地另行下载。 |
| S01，10.1093/ce/zkaf011 | Crossref规范链接https://academic.oup.com/ce/article/9/4/15/8071291；浏览器连接超时，捕集资本未核实。 |
| 官方碳价查询 | https://shyx.cneeex.com/qdata.html?1785740461457，2026-09-18综合收盘95.63元/吨，单日页面已保存；完整历史及价格定义仍待核查，不构成GBM校准完成。 |

三篇出版商证据保存为post_u_capex/*browser*.txt原文摘录，并非PDF或整篇全文下载。来源、日期和哈希见post_u_capex/evidence_manifest.json。EOR运营费用映射的未决研究规则见docs/EOR_OPERATING_COST_MAPPING_DECISION.md。


## 2026-09-21 final scalar and official-series additions

- S_NETL_TAO2023: Tao Wang, Perspectives on China CCUS Developments and Plans, Zhejiang University,2023-08-30 FECM/NETL meeting. https://netl.doe.gov/sites/default/files/netl-file/23CM_GP_Tao.pdf page9; downloaded PDF and rendered panel verified.
- S_SINOPEC2020: China Petroleum & Chemical2020 issuer annual results, SEC Form6-K. https://www.sec.gov/Archives/edgar/data/1123658/000134100421000143/form6k.htm CONVERSION: domestic7.1barrels/tonne. Raw HTML SHA in scalar_followup/oil_revenue_verification.json.
- S_CNEEEX_COMCEA: official https://shyx.cneeex.com/gateway/common/queryMarketByDate,2021-07-16–2026-09-18,1257close observations. Single API gap sourced from https://overview.cneeex.com/c/2025-10-13/496807.shtml (57.15). Raw responses, official holiday calendar, complete audit and SHA256 preserved; no interpolation.
