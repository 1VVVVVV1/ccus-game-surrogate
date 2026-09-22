# Wei 2015 原文访问成功与公式冲突

2026-09-20，ScienceDirect 浏览器自动验证通过，无需点击验证码，Wei 开放 HTML 全文可读。Table 1、2、4 及相关正文已读取；结构化摘录见 results/source_backed_formal/source_audit/sciencedirect_browser/wei_browser_verified.json。全文导出功能不受支持，故该文件仅是核验摘录，不能称完整 HTML/PDF 下载。PDF 页仍为验证页。

Table 4 的八项用户指定参照值已登记为 literature.wei2015.*，均为 MODEL_ASSUMPTION；23.66 的建模依据含循环装置 O&M 为 CAPEX 16% 的假设，未误标直接经验值。全部仅文献参照，不进入正式 config。

## 冲突记录（处理状态由下方用户规则更新）

- Table 1 fluid pumping：1 USD/STB；§2.3.2 fluid lifting：0.25 USD/STB。两处描述均涉及生产井流体举升，当前原文未给出足以唯一解释四倍差异的口径信息。
- 公式（7）网页两个分支均显示相同指数式，正文却说幂函数或指数函数；不能自行补入井深。
- 公式（9）网页钻完井系数与 Table 2 China 的系数不同；尚无可靠解释。
- 公式（12）网页 CRF 表达式存在疑点，不能静默替换为常见资本回收公式。需要 PDF/勘误/来源方程核对，当前不能认定一定是论文错误。
- 压缩单位费用的正文明确包含平准化 CAPEX 和 O&M，不能与完整 CAPEX 不加辨别地重复计费。

依新规范第 3 节及用户不得自行改公式/参数的要求，停止依赖这些歧义的成本模块实现和正式校准。待明确冲突处理原则后继续核对原 PDF/引用来源，仍不得猜齐鲁—胜利井深/井数等项目输入。

Li 2022 浏览器显示 Access through your organization 和 Purchase PDF，故该篇仍无全文。项目/路线/109 km 不再提问，现停止原因已从 Wei 不可访问转为来源内部冲突。

## 2026-09-20 用户统一规则：取代上文停止条件

完整授权见 USER_SOURCE_CONFLICT_RULES.txt。优先级为出版商勘误/补充材料、PDF 正式参数表、PDF 公式、HTML 正式表格、正文、二手索引；同变量同单位的数值冲突按参数表取值，不平均、不择优。

- fluid_pumping_cost = 1.0 USD/STB，OPEX_ONLY，TABLE_VS_TEXT_TABLE_SELECTED；长状态 SOURCE_INTERNAL_CONFLICT_TABLE_SELECTED。0.25 只保留冲突记录，不进入 baseline、surrogate、boundary 或敏感性分析。映射为每吨 CO2 成本仍需项目流体量，不能直接换算。
- 公式（7）、（9）结构尚未唯一恢复，保持 UNRESOLVED_REFERENCE_ONLY，不实现、不拼接中国系数。若以后需要，依次追溯 PDF、补充材料、勘误及明确引用的原始来源；结构确认后使用 China-specific 系数表并登记冲突。
- 公式（12）：WEI_CRF_FORMULA_UNRESOLVED。现有 src/economics.py 在投资时直接扣除 CAPEX，主模型按现金流贴现，未使用 CRF；该参考公式不阻塞主模型。
- 不要求复刻全部 Wei 模型。优先取得同项目、同资产边界、可核验的直接 U CAPEX/OPEX。未使用的未解决公式不作为 Gate 失败理由。
- 压缩/循环的平准化成本不能与相应设备 CAPEX 重复计入。注册表新增 cost_boundary 与 source_conflict_status；REFERENCE_ONLY 表示尚不能进入正式成本核算，对非成本行表示不适用成本分类。
- Yuan 2023 只作独立参照，不能充当 Wei 勘误。

当前为 AUDIT_IN_PROGRESS：原 table/prose 决策停止点已解决；来源 Gate 尚未通过，原因是核心成本和项目映射仍未闭环，而非未使用的 CRF。历史 STOP 文件保留，已由本决定取代。
