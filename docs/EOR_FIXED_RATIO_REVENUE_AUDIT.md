# 固定4:1换油率正式收益映射

用户授权原文：docs/USER_EOR_FIXED_RATIO_DECISION.txt。正式ratio=4.0，MODEL_ASSUMPTION，未由10.68/2.97或图5反推。

Q_oil=q_u/4，P_o=P_oil_CNY_per_t_oil/4。这里P_o是每吨fresh CO2对应的毛收益，不是油价自身，不扣重复CO2购买费用。现有议价bid=P_o-c_u保持原样。

单位衔接：研究公式的q_u单位为t/年，现有求解器q_u为Mt/年、收益为million CNY/年。0.10Mt=100000t，产油25000t=0.025Mt；P_o(CNY/tCO2)×q_u(MtCO2)直接得到million CNY，因此不修改求解器的单位。src/eor_revenue_calibration.py独立实现吨制输出及单位收益换算。

油价CNY/t-oil尚未审定；Wei90USD/bbl只是文献假设，不直接除4。未沿用旧780，也未把测试4000CNY/t当正式油价。approved inputs只增加ratio，不增加utilization_revenue_per_ton。

## Fig5分类

已完成的原图、像素点、上下界和旧manifest均保留。油曲线正式分类REFERENCE_ONLY_NOT_USED_IN_FORMAL_REVENUE_CALIBRATION。正文2.97Mt为LITERATURE_REFERENCE_ONLY；不参与正式收益、产油量或4.0的校准。新的分类文件单独保存，旧证据不覆盖。

## EOR_OPEX_DATA_GAP仍成立

用户第11–12节明确保留两部制成本，4:1并未授权改变参考项目成本分子。原Li变动成本可展开为USD/t fresh CO2：

c=.867 + 4.097*(R_total/F_total) + 10.07*(B_total/F_total)。

F_total=10.68e6t；R为内部回收量，只进成本分子；B为参考成本模型的桶数。4:1收益映射不消除4.097*R/F项，也不能自动替代成本基准中的B或把R设0。图5油数据可保留为成本端审计参考，不能用于收益。R_total仍因回收第11年遮挡未确定；替代注入第5年中心也遮挡。当前不新增数字化，不通过未授权形状拟合或插值推断。

因此收益的图像依赖已解除，剩余原停止点重新分类EOR_OPEX_DATA_GAP。需要用户决定是否仅在成本端授权遮挡点几何区间估读；这不是再次请求整体图像数字化授权或4:1确认。没有授权就不计算R_total，不启动正式source-backed运行。油价、FX和独立storage等剩余来源仍需后续完成，但不为其虚构数值。

## 验证

新增9个参数化测试案例覆盖用户八项要求、三模式单位/流量衔接。首次用整个Outcome相等比较遇到NaN!=NaN，已将测试改为比较实际流量及收益（允许原有不适用的NaN字段）；没有修改求解器。完整115 passed in7.60s。初始测试断言问题不是正式Gate运行失败。


## 2026-09-21 正式油价单位闭环

依据用户最新标量来源优先级，Wei2015中国陆上EOR的90USD/bbl代表值优先于另选单一年份业主实测价格。中国石化2020 SEC原始披露CONVERSION段确认国产原油7.1bbl/t（非炼油7.35）；NBS2020FX6.8974，得到4407.43860CNY/t-oil，除用户固定4得到1101.85965CNY/t fresh CO2。整个跨年份代表值映射标MODEL_ASSUMPTION，不声称统一实测价格年，不做未授权通胀升级，不是当前市场价。1902为2020部门实现价格，2029为外部销售价格，口径不同且受疫情价格下跌影响，仅参考。正式收益不依赖Fig5。证据哈希见scalar_followup/oil_revenue_verification.json。
