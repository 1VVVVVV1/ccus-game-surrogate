# 固定生命周期回收比及成本审计

用户决定见docs/USER_EOR_RECYCLE_RATIO_DECISION.txt。rho_R=1.0，MODEL_ASSUMPTION。F=q_u、R=q_u、I=2q_u仅表示内部工作量；交易、碳收益、外运和Nash流量仍只使用原fresh流量。固定4:1油收益不受回收量影响。停止所有Li CO2曲线数字化，原图与旧文件全部保留；旧遮挡导致的EOR_OPEX_DATA_GAP已解决。

## 原文核验

MIT The Economics of CO2 Storage原PDF115页，PDF41/印刷37、第3.4.4节明确1.1平均回收比用于回收站功率估计，且实际比值随项目寿命变化；该页另述Rangely案例累计net购买9billion scm、回收10billion scm。此为文献参照，不是本项目实测。原PDF已下载，SHA见download_log.json。

Abuov et al.2022，Environmental Science & Technology56(12):8571–8580，DOI10.1021/acs.est.1c06834。全文XML已下载，Results明确gross15.77、net7.96、recycle7.81mscf/bbl，因此7.81/7.96=0.9811557788944724；仅交叉参照。本文25年模型设定不替换本研究30年。

后续IJGGC论文How green is my oil?的出版商检索正文支持约50%total injection回收及gross−net=recycle。页面完整读取失败，未声称取得其PDF；本次独立数值核验以MIT和Abuov全文为主，不以检索摘要作为唯一核心来源。

## 费用分量

每吨fresh：注入20.4kWh，回收38kWh，合计58.4kWh。Li2019电价0.085USD/kWh得到4.964USD/t，仅CO2处理电费。原参考成本剩余采油可变O&M及电力=10.07USD/bbl，仍需完成成本端桶数映射；4:1尚未自动替换此前成本定义。不得将4.964填作全额utilization_cost_per_ton。fixed_opex和独立storage/shared组成仍待各自审计。

国家统计局2019公报支持年均6.8985CNY/USD，网页检索已核实；本轮直接下载结果另见fx_audit.json（若未生成则为下载未完成）。使用2019汇率不等于统一其他来源价格年，不进行通胀升级。

## 下一固定维护费停止点

Li表4井维护行写million USD/well/year、4%*capital cost of new wells and their facilities；表5写2%*capital cost of each new oil production well and gathering pipeline。总体capital条目含新井、改造及封井构成，但没有清楚给出用于这些维护费的汇总资本基数。Miao6.84和1.77近似按171.05和88.7整体资本乘比例，不能据此证明Li的per-well定义与其一致。

以整项资本为维护费基数的解释会得到参考固定费0.04*171.05+0.02*88.7+0.16*14.61=10.9536million USD/year；这是尚未采用的条件演算，不是已核验正式值。仅按new井/排除改造和封井计算则不同，且需逐项可核验组成。维护费系数乘资本不等于资本年金，但计费基数仍不能自选。

依照严格规范第3节的核心口径不唯一规则，暂不冻结EOR固定分量。需要用户明确是否将Li列示整项井设施资本（含改造/封井部分）作为维护费代理基数，并标MODEL_ASSUMPTION。此决定与已批准回收比、4:1及固定費发生方式无关。

## 验证

src/eor_recycle_calibration.py只提供内部工作量和电费分量；动态求解器不改，正式费用汇总前不加载完整配置。新增11个参数化案例覆盖用户10项要求，完整126passed in2.57s。旧formal257文件及冻结config逐一哈希一致。无新增敏感性、Sobol维数或样本量调整。
