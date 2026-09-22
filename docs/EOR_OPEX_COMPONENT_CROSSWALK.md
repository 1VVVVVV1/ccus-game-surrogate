# EOR 两部制运营费用组件审计

用户决定见 USER_EOR_TWO_PART_OPEX_DECISION.txt。此前全成本吨均化提案不采用；原映射规则停止点已解除。机器可读逐组件结果见 `results/source_backed_formal/source_audit/eor_opex_component_crosswalk.csv`。

## 已核验

Li2022为主，Miao2025用于交叉核验。Li式(3)分别扣除资本TC、固定运营FOM、可变运营VOM和税费TA。因此运营维护按资本额百分比估计，不因此变成资本回收年金；不能把资本本金或税费加进OPEX。Li第4.2节明确2019年价格和2019年美元；电价85USD/MWh=0.085USD/kWh，不能混用Miao的0.0548USD/kWh。

Li第4.1节10.68Mt来自捕集源并运往EOR；第4.2.5节明确回收量=注入量−捕集量，支持fresh累计分母10.68Mt。于是参考平均年fresh=0.712Mt，用户基准EOR能力0.10Mt，固定费缩放系数=0.1404494382022472。这不等于取得15个逐年量。

## 固定费

明确的Li固定维护项目包括注入站0.04×6.25=0.25、内部布置管线0.04×21=0.84、回收0.16×14.61=2.3376 million USD/year。这些均待历史汇率和完整边界闭环后换算，不提前冻结总U固定费。

注入井和采油井行分别写million USD/well/year、new wells/each new production well。不能未经核查将其直接乘含改造井、废弃封井费用的总体资本额；Miao6.84和1.77不能反过来替代Li完整定义。Miao6.84近似0.04×171.05、1.77近似0.02×88.7、2.34近似0.16×14.61，仅说明数值相近，不证明资产计费基数完全相同。

Miao三项不与Li相加；回收行标题为“investment fixed cost”，正文称运营固定费，以Li分列定义为主，不自行改原文。独立storage和shared fixed仍待独立审计，不能默认零或将EOR固定分量当作U总固定费。

## 变动费

每年先按原币种计算：`V_t=0.085*[10.2*(F_t+R_t)+38*R_t+22*B_t]+8.2*B_t`，F/R单位为吨，B为桶。这是当前已核验Li组件表达式，不是已完成正式费用数值。其他流量费只有证明无重复且属于授权边界才可补充，Wei举升费不能直接再加。

固定分量=`sum(K_USD)*FX*0.10/sum(F_tonnes)`，单位million CNY/year；变动系数=`sum(V_USD)*FX/sum(F_tonnes)`，单位CNY/t fresh CO2。无折现、无资本年金、无内部转移价；回收CO2只影响成本分子，不再次计入q_u。基准校准冻结后，运行时xi变化不自动重标定固定费。

## 原始年度数据的具体缺口

Li表2/4/5/6的年度捕集、注入、采油、回收均指向Fig5，没有数值表。出版商原图已在浏览器核对：15个年度点，四条曲线、双纵轴，没有逐点数值标签。CO2轴为thousand tons，油轴为thousand bbl。原文数据声明为“Data will be made available on request.” 当前可读页面未找到补充数值表。

只有10.68Mt和2.97Mt累计文字数值，不能推定每年的R、I、B；2.97Mt油也不能未核验密度/换算就替代图中的桶数。图像数字化将引入估读误差，并非原文精确数据；未经授权不生成伪精确年度输入，不以凑合计量修正曲线。

新停止依据为研究规范第3节：核心输入不能可靠唯一确定。需要决定是否允许对Fig5作透明的图像数字化并将其标记为近似来源输入，或由作者原始数值表解决。自动联系作者尚未获授权，因此未发邮件。此处不重新询问两部制规则。

## 已实现验证

src/eor_cost_calibration.py添加独立两部制换算函数，接收15年已核验年度费用，要求EOR/OPEX_ONLY、禁止相同物理组件重复输入；不读取运行时xi、不修改求解器。测试采用明确标注的合成费用和汇率，仅检验公式和原有stage_outcome成本发生规律，不把测试数字写入正式注册表。数字校准尚未完成，正式两个参数不填猜测值。


### 2026-09-20固定回收比更新

Recycled CO2 is represented by a stationary lifecycle-average ratio of one tonne per tonne of fresh CO2 routed to EOR. Actual recycle rates vary over project life. R=q_u and I=2q_u affect internal injection/recycling electricity only; external flow, credits, transport and oil revenue are not doubled. Li Fig5 CO2 curves are reference-only. The 58.4kWh/t fresh (4.964USD2019/t) component is not full EOR variable OPEX. Fixed OPEX still applies after U is built, including zero-flow years.


## 2026-09-21 决策014：正式 EOR 简化成本（覆盖此前两部制映射）

正式 c_u=15×6.8974=103.461 CNY/t fresh CO2，MODEL_ASSUMPTION、A-，以 Guo et al. (2020), DOI 10.1016/j.petrol.2019.106720 的 O&M benchmark 为依据。国家统计局2020统计公报已独立核实汇率6.8974；Guo表1的15目前来自用户明确决定，独立表格核验继续。该来源的注入量口径迁移到本模型 fresh CO2 分母属于明确的模型假设，不是齐鲁观测。

EOR-specific fixed OPEX=0；Li/Miao逐井维护费、10.9536 million USD/year和4.964 USD/t电费均不叠加。rho=1仅保留技术工作量解释，4:1收益不变。q_u为Mt时，q_u×103.461直接得到million CNY。共享U CAPEX、运输和q_s储存成本独立计费；EOR固定分量为0不代表未经审计的其他平台费用已被确定。

Li/Miao组件表及历史工具保留为REFERENCE_ONLY_NOT_USED_IN_FORMAL_EOR_OPEX。解除EOR_FIXED_MAINTENANCE_BASE及相关井资本基数/固定费聚合停止项。今后标量来源优先直接代表值，不为设备级拆分停工；仅按本次用户决定第15节A–D及原规范Gate失败规则停下询问。SOURCE_AUDIT仍在进行，未冻结正式配置或启动12288行。
