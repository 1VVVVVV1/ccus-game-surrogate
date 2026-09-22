# Codex 严格实施规范：从 0 构建 CCUS 双主体随机动态博弈 + Nash 议价 + 代理模型快速求解框架

> **用途**：本文件是新的主线实施规范。它不再以多主体强化学习（MARL/PPO）作为主求解器，而改用“有限期随机动态博弈 / 实物期权思想 + 广义 Nash 议价 + 机器学习代理模型”的结构。  
> **原则**：Codex 必须按本文件逐项实现，不得自行改变经济含义、均衡定义、参数、阈值、样本规模、测试口径或输出格式。  
> **目标**：得到一个更可解释、更稳定、更容易达到高精度、可用于论文正式结果和经济边界分析的 CCUS 双主体求解框架。

---

# 0. 总体要求与禁止事项

## 0.1 新项目必须与旧 RL 项目隔离

现有 RL 项目和正式结果不得删除、覆盖或“就地改造成”新模型。

在仓库根目录新建独立目录：

```text
ccus_game_surrogate/
```

旧目录：

```text
ccus_two_agent_topjournal/
```

只允许作为：
- 参数来源；
- 经济公式核对来源；
- RL benchmark / supplementary comparison 来源。

**禁止修改旧目录下任何正式 checkpoint、formal_run_lock、Gate 4/5 结果。**

## 0.2 新主线名称固定

论文方法主线统一称为：

```text
Two-agent stochastic dynamic investment game
with generalized Nash bargaining
and surrogate-assisted equilibrium mapping
```

中文：

```text
双主体随机动态投资博弈 + 广义 Nash 议价 + 代理辅助均衡映射
```

不要再把新主线称为 MAPPO、MADDPG、MARL、PPO 或 Actor-Critic。

## 0.3 新方法的核心逻辑固定

```text
随机碳价
→ 有限期 Markov 状态
→ C/U 不可逆投资决策
→ 运营阶段广义 Nash 议价
→ 动态博弈后向递推
→ Markov-perfect equilibrium
→ 前向概率传播
→ 精确期望经济结果
→ Sobol 参数场景
→ 代理模型拟合
→ 快速输入输出映射
→ 经济临界边界
```

不允许再次引入神经网络策略作为主求解器。

## 0.4 本项目不做的内容

本轮不做：
- 鲁棒性实验；
- OOD 泛化实验；
- 额外商业模式；
- 政策冲击模型；
- 油价随机过程；
- 多区域网络；
- 三主体 RL；
- endogenous transport routing；
- structural ETS 模块；
- 自动超参数搜索；
- 自动调参直到“结果好看”；
- 挑选最优 seed；
- 人为删掉不利场景。

---


## 0.5 决策权边界与“不确定就问用户”规则

Codex 在本项目中是**严格执行者**，不是共同研究设计者。除本规范已经明确写出的内容外，Codex 不得自行补充新的经济假设、算法结构、参数、阈值、样本规模、均衡概念、边界定义、代理模型、数据清洗规则或论文结论。

### 0.5.1 允许 Codex 自行决定的内容，仅限纯工程细节

仅以下事项可自行处理，且不得改变研究结果：

```text
文件夹创建
模块拆分
函数命名
局部变量命名
日志格式
进度条
缓存文件格式（Parquet不可用时退回CSV）
并行任务调度
异常信息排版
README中的安装说明
```

即使是上述工程细节，也不得改变：
- 随机种子；
- 计算顺序对应的数学含义；
- 浮点容差；
- 输出字段；
- Gate；
- 数据行数；
- 经济参数；
- 均衡定义。

### 0.5.2 以下任何情况必须立即停下并询问用户

如果遇到以下任意情况，Codex 必须停止当前研究性计算，不得自行选方案：

1. 本规范存在两个可能的数学解释；
2. 某经济公式无法从本规范唯一确定；
3. pure/mixed Nash 之外出现本规范未覆盖的均衡数值问题；
4. 某 target 是否结构性适用不明确；
5. surrogate Gate 失败；
6. exact solver Gate 失败；
7. 边界是否应定义、如何定义不明确；
8. 需要修改任何经济参数才能继续；
9. 需要修改任何 Gate 阈值才能继续；
10. 想更换 surrogate 算法；
11. 想改变 Sobol 样本量；
12. 想改变 train/validation/test 划分；
13. 想新增、删除或合并输出 target；
14. 出现大量 mixed equilibrium，怀疑模型制度假设需要改变；
15. 出现大量 multiple pure equilibrium，想改 tie-break；
16. 某一商业模式结果长期不投资或 NPV 为负，想“修正参数”；
17. 任何会影响论文方法或经济解释的决定。

### 0.5.3 向用户提问的固定格式

遇到不确定性时，只允许输出一个短问题包，格式必须是：

```text
STOP_FOR_USER_DECISION

位置：
<文件/模块/公式/阶段>

已确定事实：
<只写已经验证的事实>

不确定点：
<只写一个具体问题>

允许选项：
A. ...
B. ...
C. ...

每个选项的后果：
A. ...
B. ...
C. ...

当前未执行：
<明确说明哪些后续步骤没有继续>
```

不得只说“你想怎么办？”。
不得私自推荐一个会改变研究设计的选项并直接执行。

### 0.5.4 禁止“为了效果好”而自由发挥

“效果好”只允许理解为：
- 数值实现正确；
- 计算稳定；
- 可复现；
- 输出完整；
- 代理精度满足预设 Gate；
- 运行效率合理。

绝对不能理解为：
- 让 NPV 更高；
- 让投资更多；
- 让边界更漂亮；
- 让某商业模式更优；
- 让 R² 人为提高；
- 选择性删除困难样本；
- 调参直到通过 Gate。

---

# 1. 研究问题

研究对象固定为：

```text
2 个战略主体 + 1 个被动运输模块
```

其中：
- Agent C：碳源 / CO₂ 捕集企业；
- Agent U：CO₂ 利用与封存运营商；
- T：运输模块，不是博弈主体。

研究问题：

> 在未来碳价随机、CCUS 投资不可逆、投资存在建设滞后、不同商业组织模式具有不同收益分配机制的条件下，C 与 U 应在何时投资？交易价格如何形成？不同商业模式下系统和主体价值、投资概率和投资时点如何变化？能否用代理模型快速近似高精度博弈均衡求解器？

---

# 2. 三种商业模式固定

枚举：

```python
TRANSFER
JOINT_VENTURE
STATE_OWNED
```

## 2.1 TRANSFER
- C 与 U 为独立经济主体；
- C/U 各自决定是否投资；
- CO₂ 利用交易通过广义 Nash 议价决定；
- 封存服务交易通过广义 Nash 议价决定；
- transport T 被动收费；
- 属于 general-sum dynamic game。

## 2.2 JOINT_VENTURE
- C、T、U 的部分业务进入 JV；
- C/U 仍各自决定投资；
- 利用端与 JV 之间保留 CO₂ 交易；
- 封存不再单独议价；
- JV 利润按固定股份分配；
- 仍属于 general-sum dynamic game。

## 2.3 STATE_OWNED
- 视为统一集团；
- C/U 两个设施仍分别具有投资时点；
- 无内部 CO₂ 价格；
- 无内部封存费；
- 直接最大化系统总价值；
- 属于 cooperative centralized benchmark。

---

# 3. 单位与时间尺度

固定：

```text
时间步长 = 1 年
T = 30 年
t = 0,...,29
```

经济量单位：

```text
货币：million CNY
价格：CNY/tCO2
流量：MtCO2/year
```

利用：

```text
1 CNY/t × 1 Mt = 1 million CNY
```

因此不额外乘 1e6。

经济折现率：

\[
r=0.08
\]

折现因子：

\[
\gamma=\frac{1}{1.08}
\]

代码中必须：

```python
GAMMA = 1.0 / 1.08
```

禁止使用连续贴现。

---

# 4. 冻结基础经济参数

新项目复制旧正式 config 的经济基准，但必须独立保存。

新建：

```text
ccus_game_surrogate/config/model_config.game.json
```

固定为：

```json
{
  "scenario_label": "CCUS_TWO_AGENT_STOCHASTIC_GAME_2026",
  "simulation": {
    "horizon": 30,
    "economic_discount_rate": 0.08,
    "dt_years": 1.0
  },
  "carbon_price": {
    "P0": 96.23,
    "mu": 0.04,
    "sigma": 0.15,
    "process": "STANDARD_GBM",
    "tree": "PHYSICAL_MEASURE_CRR_BINOMIAL"
  },
  "carbon_market": {
    "value_model": "REDUCED_FORM",
    "effective_abatement_fraction": 0.70
  },
  "co2_quantity": {
    "Q_bar": 0.50,
    "utilization_fraction": 0.20
  },
  "carbon_source": {
    "capex_initial": 450.0,
    "capex_decline_rate": 0.0,
    "fixed_opex": 0.0,
    "variable_opex_per_ton": 240.0,
    "idle_cost": 0.0
  },
  "transport_market": {
    "market_price_per_ton": 125.0,
    "fixed_opex_if_active": 0.0,
    "variable_opex_per_ton": 125.0
  },
  "utilization_storage": {
    "capex_initial": 40.3566,
    "capex_decline_rate": 0.0,
    "fixed_opex": 0.0,
    "utilization_revenue_per_ton": 780.0,
    "utilization_cost_per_ton": 94.1654,
    "storage_cost_per_ton": 43.71965,
    "storage_subsidy_per_ton": 0.0,
    "idle_cost": 0.0
  },
  "joint_venture": {
    "theta_C": 0.50,
    "theta_T": 0.20,
    "theta_U": 0.30
  },
  "bargaining": {
    "co2_seller_weight": 0.50,
    "storage_provider_weight": 0.50
  },
  "scenario_domain": {
    "transport_market_price": [75.0, 200.0],
    "effective_abatement_fraction": [0.50, 1.00],
    "storage_subsidy": [0.0, 120.0],
    "capex_C_multiplier": [0.70, 1.30],
    "capex_U_multiplier": [0.70, 1.30],
    "carbon_scale": [0.50, 6.25]
  },
  "solver": {
    "equilibrium_tolerance": 1e-10,
    "tie_tolerance": 1e-10
  },
  "dataset": {
    "sobol_n": 4096,
    "sobol_seed": 20260921,
    "split_seed": 42,
    "train_n": 2868,
    "validation_n": 614,
    "test_n": 614
  }
}
```

除非用户明确授权，Codex 不得更改上述数值。

---

# 5. Scenario 定义

每个场景：

\[
X=(P_{tr},\eta,S_s,m_C,m_U,\lambda_c)
\]

其中：
- \(P_{tr}\)：运输市场价格；
- \(\eta\)：有效减排价值比例；
- \(S_s\)：封存补贴；
- \(m_C\)：C CAPEX multiplier；
- \(m_U\)：U CAPEX multiplier；
- \(\lambda_c\)：carbon scale。

场景固定后：

\[
CAPEX_C=450m_C
\]

\[
CAPEX_U=40.3566m_U
\]

初始碳价：

\[
P_{0,X}^c=96.23\lambda_c
\]

GBM 的 \(\mu,\sigma\) 不随 scenario 改变。

---

# 6. 碳价随机过程与二叉树

主随机过程仍是普通 GBM：

\[
dP_t=\mu P_tdt+\sigma P_tdW_t
\]

高精度动态博弈求解器使用与 GBM 一致的 recombining binomial approximation。

固定：

\[
u=e^{\sigma\sqrt{\Delta t}}
\]

\[
d=\frac1u
\]

由于这里做的是经济期望而不是风险中性资产定价，概率使用 physical drift：

\[
p=\frac{e^{\mu\Delta t}-d}{u-d}
\]

必须检查：

\[
0<p<1
\]

否则停止。

节点：

\[
P_{t,j}=P_{0,X}u^jd^{t-j},\quad j=0,\ldots,t
\]

禁止：
- floor；
- cap；
- monotonic envelope；
- risk-neutral drift；
- mean reversion；
- 跳跃过程。

---

# 7. 投资状态与一年建设滞后

设施状态：

\[
x_C,x_U\in\{0,1\}
\]

投资动作：

\[
d_i\in\{0,1-x_i\}
\]

一次投资后不可逆。

状态更新：

\[
x_{i,t+1}=\max(x_{i,t},d_{i,t})
\]

最重要的时序：

1. 读取旧 built state \(x_t\)；
2. C/U 做投资动作；
3. 当前年生产使用旧 built state；
4. 当前年支付 CAPEX；
5. 当前年利润计算完成；
6. 年末更新 built state；
7. 下一年新设施才可生产。

禁止“当年投资、当年立即运行”。

---

# 8. 当前年物理基础流量

基础能力：

\[
Base_t=\bar Q x_Cx_U
\]

其中：

\[
\bar Q=0.50
\]

利用比例：

\[
\xi=0.20
\]

---

# 9. 广义 Nash 议价：不再让神经网络学报价

所有交易报价都由经济 reservation value 推导。

---

# 10. TRANSFER 模式 CO₂ 利用交易

定义单位 CO₂ 的碳价值：

\[
v_c=P_t^c\eta
\]

C 若把一吨 CO₂ 卖给 U，单位边际收益：

\[
v_c+P_u-P_{tr}-c_C
\]

所以 C 的最低可接受卖价：

\[
A_u^{TR}=P_{tr}+c_C-v_c
\]

其中：

\[
c_C=240
\]

U 的单位利用利润：

\[
P_o-P_u-c_u
\]

所以最大支付意愿：

\[
B_u=P_o-c_u
\]

其中：

\[
P_o=780,\quad c_u=94.1654
\]

若：

\[
A_u^{TR}>B_u
\]

则利用交易失败：

\[
I_u=0
\]

否则：

\[
I_u=1
\]

成交价：

\[
P_u=A_u^{TR}+\omega_u(B_u-A_u^{TR})
\]

固定：

\[
\omega_u=0.5
\]

允许：

\[
P_u<0
\]

不要人为截断。

---

# 11. TRANSFER 模式封存服务议价

C 对每吨封存服务的最大支付意愿：

\[
B_s=v_c-c_C-P_{tr}
\]

U 的最低非负封存服务报价：

\[
A_s=\max(0,c_s-S_s)
\]

其中：

\[
c_s=43.71965
\]

若：

\[
A_s>B_s
\]

则封存交易失败：

\[
I_s=0
\]

否则：

\[
I_s=1
\]

成交封存费：

\[
P_s=A_s+\omega_s(B_s-A_s)
\]

固定：

\[
\omega_s=0.5
\]

且：

\[
P_s\ge0
\]

---

# 12. TRANSFER 物理流量

\[
q_u=\xi Base_t I_u
\]

\[
q_s=(1-\xi)Base_t I_s
\]

\[
Q=q_u+q_s
\]

---

# 13. JOINT_VENTURE CO₂ 议价

JV 运输使用真实运输成本而不是运输市场转移价格。

定义 transport marginal real cost：

\[
c_T=125
\]

JV 对利用 CO₂ 的最低可接受价格：

\[
A_u^{JV}=c_C+c_T-v_c
\]

U application side 最大支付意愿仍为：

\[
B_u=P_o-c_u
\]

如果：

\[
A_u^{JV}>B_u
\]

利用失败。

否则：

\[
P_u=A_u^{JV}+0.5(B_u-A_u^{JV})
\]

JV 下封存不议价：

\[
q_s=(1-\xi)Base_t
\]

利用：

\[
q_u=\xi Base_t I_u
\]

---

# 14. STATE_OWNED 物理流量

不议价。

只要两设施 built：

\[
q_u=\xi Base_t
\]

\[
q_s=(1-\xi)Base_t
\]

---

# 15. 经济利润公式

所有公式与旧正式模型保持经济含义一致。

## 15.1 公共项

碳价值：

\[
R_c=P_t^c\eta Q
\]

C OPEX：

\[
OPEX_C=F_Cx_C+c_CQ
\]

U OPEX：

\[
OPEX_U=F_Ux_U+c_uq_u+c_sq_s
\]

运输：

\[
R_T=P_{tr}Q
\]

\[
C_T=F_T1(Q>0)+c_TQ
\]

\[
\pi_T=R_T-C_T
\]

CAPEX：

\[
I_C=450m_Cd_C
\]

\[
I_U=40.3566m_Ud_U
\]

## 15.2 TRANSFER

\[
\pi_C=R_c+P_uq_u-P_{tr}Q-P_sq_s-OPEX_C-I_C
\]

\[
\pi_U=P_oq_u-P_uq_u+P_sq_s+S_sq_s-OPEX_U-I_U
\]

\[
\pi_T=P_{tr}Q-C_T
\]

系统价值：

\[
\pi_{sys}=\pi_C+\pi_U+\pi_T
\]

并必须等于：

\[
R_c+P_oq_u+S_sq_s-OPEX_C-OPEX_U-C_T-I_C-I_U
\]

容差：

```text
1e-10
```

## 15.3 JOINT_VENTURE

JV 利润池：

\[
\Pi^{JV}=R_c+P_uq_u+S_sq_s-OPEX_C-C_T-F_Ux_U-c_sq_s-I_C-I_U
\]

application profit：

\[
\Pi_U^{app}=P_oq_u-P_uq_u-c_uq_u
\]

股份：

\[
\theta_C=0.5,\quad \theta_T=0.2,\quad \theta_U=0.3
\]

主体利润：

\[
\pi_C=\theta_C\Pi^{JV}
\]

\[
\pi_T=\theta_T\Pi^{JV}
\]

\[
\pi_U=\Pi_U^{app}+\theta_U\Pi^{JV}
\]

系统：

\[
\pi_{sys}=\Pi^{JV}+\Pi_U^{app}
\]

## 15.4 STATE_OWNED

\[
\pi_{sys}=R_c+P_oq_u+S_sq_s-OPEX_C-C_T-OPEX_U-I_C-I_U
\]

新项目中：

```text
value_C = value_U = system value
```

用于 cooperative dynamic investment decision。

SOE 个体 C/U/T NPV 不作为主经济结果。

---

# 16. 动态博弈状态

每个树节点状态固定为：

\[
s=(t,j,x_C,x_U)
\]

其中：
- \(t\)：年份；
- \(j\)：binomial up-move 数；
- \(x_C,x_U\)：设施状态。

碳价由：

\[
P_{t,j}
\]

唯一确定。

scenario 参数在整个求解期间固定。

---

# 17. 动态价值函数

TRANSFER / JV：

\[
V_C(t,j,x_C,x_U)
\]

\[
V_U(t,j,x_C,x_U)
\]

并附带：

\[
V_T,\quad V_{sys}
\]

用于结果报告。

给定当前投资动作：

\[
a=(d_C,d_U)
\]

当前即时利润：

\[
\pi_i(s,a)
\]

下一状态：

\[
x_C'=\max(x_C,d_C),\quad x_U'=\max(x_U,d_U)
\]

continuation：

\[
EV_i=pV_i(t+1,j+1,x_C',x_U')+(1-p)V_i(t+1,j,x_C',x_U')
\]

总行动价值：

\[
J_i(s,a)=\pi_i(s,a)+\gamma EV_i
\]

终期：

```text
t = 29
continuation = 0
```

---

# 18. 可行动作集

若：

\[
x_i=0
\]

则：

```python
A_i = [0, 1]
```

若：

\[
x_i=1
\]

则：

```python
A_i = [0]
```

因此最多是 2×2 stage game。

---

# 19. TRANSFER / JV 的 stage-game Nash equilibrium

每个状态构造：

```text
J_C(d_C,d_U)
J_U(d_C,d_U)
```

定义 action pair \(a^*\) 为 pure NE，当：

\[
J_C(a^*)\ge J_C(d_C',d_U^*)-\epsilon
\]

对 C 所有可行动作成立，同时：

\[
J_U(a^*)\ge J_U(d_C^*,d_U')-\epsilon
\]

固定：

\[
\epsilon=10^{-10}
\]

---

# 20. 多重 pure NE 的固定选择规则

若只存在 1 个 pure NE：直接选取。

若存在多个 pure NE：严格按以下顺序。

### Step 1：删除 Pareto-dominated equilibrium

若 NE A 满足存在 NE B：

\[
J_C(B)\ge J_C(A)
\]

且：

\[
J_U(B)\ge J_U(A)
\]

并至少一个严格大于，则删除 A。

### Step 2
若只剩 1 个，选它。

### Step 3
若仍多个，按以下顺序排序：

1. 最大化：
   \[
   J_C+J_U
   \]
2. 若并列，最大化：
   \[
   \min(J_C,J_U)
   \]
3. 若仍并列，最小化：
   \[
   d_C+d_U
   \]
4. 若仍并列，action tuple 字典序：
   ```text
   (0,0) < (0,1) < (1,0) < (1,1)
   ```

记录：

```text
equilibrium_multiplicity
equilibrium_selection_reason
```

不能随机选择 equilibrium。

---

# 21. 如果不存在 pure NE：使用 mixed Nash

只有在 C 和 U 都有两个动作且 pure NE 数量为 0 时计算 interior mixed Nash。

令 C 选择 invest 的概率为：

\[
p_C
\]

U 为：

\[
p_U
\]

C payoff matrix：

```text
A00 A01
A10 A11
```

U payoff：

```text
B00 B01
B10 B11
```

使 C 无差异：

\[
p_U=\frac{A_{10}-A_{00}}{A_{01}-A_{00}-A_{11}+A_{10}}
\]

使 U 无差异：

\[
p_C=\frac{B_{01}-B_{00}}{B_{10}-B_{00}-B_{11}+B_{01}}
\]

要求：

\[
0<p_C<1,\quad 0<p_U<1
\]

否则：

```text
MIXED_NE_NUMERIC_FAILURE
```

立即停止该 scenario。

mixed action pair probability：

\[
Pr(d_C,d_U)=Pr_C(d_C)Pr_U(d_U)
\]

价值函数取 mixed equilibrium 下行动价值期望。

---

# 22. STATE_OWNED cooperative decision

SOE 不求 Nash。

每个状态枚举全部可行 \((d_C,d_U)\)，计算：

\[
J_{sys}(s,a)=\pi_{sys}(s,a)+\gamma E[V_{sys}(s')]
\]

选择最大值。

若并列：
1. 最小化 \(d_C+d_U\)；
2. 再按字典序：
   ```text
   (0,0)<(0,1)<(1,0)<(1,1)
   ```

不得人为优先“尽早投资”。

---

# 23. 后向递推顺序

严格：

```python
for t in reversed(range(T)):
    for j in range(t + 1):
        for x_C in [0,1]:
            for x_U in [0,1]:
                solve_state(...)
```

每个 scenario 重新求完整 equilibrium。

不能复用其他 scenario 的 policy。

---

# 24. 数学定位

TRANSFER/JV 每个状态都基于当前状态、当前即时利润和 continuation value 求子博弈 Nash equilibrium。

正式文稿允许称：

```text
finite-horizon Markov-perfect equilibrium
under the binomial approximation
```

不得写成：
- global social optimum；
- unique Nash equilibrium（除非实际唯一）；
- continuous-time closed-form solution。

---

# 25. 前向概率传播

后向解出 equilibrium policy 后，从：

```text
t=0
j=0
x_C=0
x_U=0
probability=1
```

开始前向传播。

对于每个 state：
- pure equilibrium：action probability = 1；
- mixed equilibrium：按 mixed action probabilities；
- carbon up/down：分别乘 \(p,1-p\)。

必须保证每年概率质量：

\[
\sum_s Pr_t(s)=1
\]

容差：

```text
1e-12
```

否则：

```text
PROBABILITY_MASS_ERROR
```

---

# 26. 投资结果

对每个主体计算：

\[
Pr(\tau_i=t)
\]

总投资概率：

\[
Pr_i^{invest}=\sum_tPr(\tau_i=t)
\]

never-invest：

\[
Pr_i^{never}=1-Pr_i^{invest}
\]

条件投资年份：

\[
E[\tau_i\mid invest]=\frac{\sum_ttPr(\tau_i=t)}{Pr_i^{invest}}
\]

若：

\[
Pr_i^{invest}<10^{-12}
\]

则：

```text
expected_tau_i_conditional = NaN
```

不要写 30 或 999。

---

# 27. 必须输出的运营与价值结果

至少输出：

```text
system_npv
value_C
value_U
value_T

invest_prob_C
invest_prob_U

expected_tau_C_conditional
expected_tau_U_conditional

never_invest_prob_C
never_invest_prob_U

expected_active_years
expected_total_quantity
expected_total_utilization
expected_total_storage

co2_trade_year_probability
storage_trade_year_probability

mean_co2_price_conditional
mean_storage_fee_conditional

mixed_equilibrium_state_probability
multiple_pure_equilibrium_state_probability
```

---

# 28. 交易价格均值定义

禁止“无交易=0”。

CO₂ 价格：

\[
\bar P_u=
\frac{E[\sum_t1_{\{q_{u,t}>0\}}P_{u,t}]}{E[\sum_t1_{\{q_{u,t}>0\}}]}
\]

若分母：

\[
<10^{-12}
\]

则：

```text
mean_co2_price_conditional = NaN
```

封存费同理。

---

# 29. 动态价值与前向 NPV 双重核验

必须独立得到 initial value。

方法 A：

```text
backward value at initial state
```

方法 B：

```text
forward state/action probabilities × discounted stage profits
```

要求：

TRANSFER/JV：

```text
abs(V_C_backward - NPV_C_forward) < 1e-8
abs(V_U_backward - NPV_U_forward) < 1e-8
```

SOE：

```text
abs(V_system_backward - NPV_system_forward) < 1e-8
```

否则：

```text
DYNAMIC_VALUE_ACCOUNTING_FAILURE
```

---

# 30. 静态经济会计恒等式

每个：

```text
mode × scenario × state × feasible action pair
```

都必须验证经济会计。

TRANSFER/JV：

\[
\pi_{sys}=\pi_C+\pi_T+\pi_U
\]

容差：

```text
1e-10
```

SOE direct system formula 与分项计算误差：

```text
< 1e-10
```

---

# 31. Baseline scenario

固定：

```text
transport_market_price = 125
effective_abatement_fraction = 0.70
storage_subsidy = 0
capex_C_multiplier = 1.0
capex_U_multiplier = 1.0
carbon_scale = 1.0
```

首先单独求 baseline。

输出：

```text
results/baseline/TRANSFER.json
results/baseline/JOINT_VENTURE.json
results/baseline/STATE_OWNED.json
results/baseline/baseline_summary.csv
```

---

# 32. Ground-truth solver 不允许代理模型参与

`solve_scenario()` 必须完全由：

```text
economic equations
+ binomial tree
+ backward equilibrium
+ forward probability propagation
```

完成。

禁止调用任何 ML model。

这是 ground-truth solver。

---

# 33. Sobol 正式场景集

使用：

```python
scipy.stats.qmc.Sobol
```

维度：

```text
6
```

固定：

```text
n = 4096
scramble = True
seed = 20260921
```

由于：

\[
4096=2^{12}
\]

必须：

```python
random_base2(m=12)
```

不得使用普通随机抽样。

映射到：

```text
transport_market_price [75,200]
effective_abatement_fraction [0.50,1.00]
storage_subsidy [0,120]
capex_C_multiplier [0.70,1.30]
capex_U_multiplier [0.70,1.30]
carbon_scale [0.50,6.25]
```

scenario_id：

```text
0 ... 4095
```

---

# 34. 正式精确数据集

对每个 scenario 三种模式全部求解。

```text
4096 scenarios × 3 modes = 12288 exact solves
```

输出：

```text
results/exact_dataset/exact_scenarios.csv
results/exact_dataset/exact_equilibrium_outputs.csv
```

输出表必须：

```text
12288 rows
```

每行：

```text
scenario_id
mode
6 input features
all equilibrium outputs
solver_status
```

---

# 35. 非法 / 无解场景

有限 2×2 游戏理论上存在 mixed NE。

因此以下情况视为 solver bug：

```text
NO_EQUILIBRIUM
INVALID_MIXED_PROBABILITY
PROBABILITY_MASS_ERROR
DYNAMIC_VALUE_ACCOUNTING_FAILURE
NONFINITE_VALUE
```

正式 4096×3 数据集要求：

```text
solver_status == OK
for all 12288 rows
```

否则停止。

不允许 silently drop scenario。

---

# 36. Exact Solver Gate

进入 surrogate 前必须通过：

```text
GATE_EXACT_SOLVER
```

要求：

1. baseline 3 mode 全部成功；
2. 12288 rows 全部存在；
3. system_npv 必须 finite；
4. value_C/value_U 在适用模式必须 finite；
5. invest probability 必须 finite 且位于 [0,1]；
6. conditional tau / transaction price 只有结构性未定义时允许 NaN；
7. value accounting 全部通过；
8. probability mass 全部通过；
9. mixed probability 全部在 [0,1]；
10. 无非有限 stage payoff。

失败立即停止。

---

# 37. Dataset split

split 必须按 scenario_id，而不是按 row。

同一 scenario 的三种 mode 必须进入同一个 split。

固定：

```text
train = 2868 scenarios
validation = 614 scenarios
test = 614 scenarios
```

生成：

```python
rng = np.random.default_rng(42)
perm = rng.permutation(4096)
```

前：

```text
2868 train
614 validation
614 test
```

输出：

```text
results/surrogate/scenario_split.csv
```

不得重新随机。

---

# 38. 代理模型输入

只允许六个输入：

```text
transport_market_price
effective_abatement_fraction
storage_subsidy
capex_C_multiplier
capex_U_multiplier
carbon_scale
```

禁止加入：
- scenario_id；
- mode 编码混合训练；
- solver 内部状态；
- equilibrium multiplicity；
- 输出泄漏特征。

每个 mode 单独训练 surrogate。

---

# 39. 代理模型结构固定

连续输出统一使用：

```python
HistGradientBoostingRegressor(
    learning_rate=0.05,
    max_iter=500,
    max_leaf_nodes=31,
    min_samples_leaf=20,
    l2_regularization=1e-3,
    random_state=42
)
```

投资概率仍做 regression：

```text
target in [0,1]
```

预测后仅用于展示时可 clip 到 [0,1]。

测试指标必须对 unclipped prediction 同时报告。

不要自动调参。

---

# 40. Surrogate targets

TRANSFER：

```text
system_npv
value_C
value_T
value_U
invest_prob_C
invest_prob_U
expected_tau_C_conditional
expected_tau_U_conditional
mean_co2_price_conditional
mean_storage_fee_conditional
```

JOINT_VENTURE：

```text
system_npv
value_C
value_T
value_U
invest_prob_C
invest_prob_U
expected_tau_C_conditional
expected_tau_U_conditional
mean_co2_price_conditional
```

STATE_OWNED：

```text
system_npv
invest_prob_C
invest_prob_U
expected_tau_C_conditional
expected_tau_U_conditional
```

---

# 41. 结构性 NaN 的 surrogate 处理

对于：

```text
expected_tau_*_conditional
```

只有 exact target 非 NaN 的行参与该 target regression。

同时训练投资概率 surrogate。

不要把 never invest 编码成 tau=30 或 tau=999。

交易价格同理：无交易时 target 保持 NaN。

价格 surrogate 只使用有定义场景。

---

# 42. Surrogate metrics

统一：

```text
R2
MAE
RMSE
NMAE
```

其中：

\[
NMAE=\frac{MAE}{Q_{95}(y)-Q_{05}(y)}
\]

若：

\[
Q95-Q05\le10^{-12}
\]

则：

```text
NMAE = NaN
```

不得填 0。

---

# 43. Surrogate Gate 固定

## 43.1 价值类

适用：

```text
system_npv
value_C
value_T
value_U
```

要求 test：

\[
R^2\ge0.98
\]

且：

\[
NMAE\le0.05
\]

## 43.2 投资概率

要求 test：

```text
MAE <= 0.03
```

R² 只报告，不作为硬 Gate。

## 43.3 条件投资年份

要求 test：

```text
MAE <= 1.0 year
```

## 43.4 交易价格

要求 test：

\[
R^2\ge0.95
\]

且：

\[
NMAE\le0.08
\]

---

# 44. Gate 失败规则

任何 gating target 失败：

```text
GATE_SURROGATE_FAIL
```

立即停止。

生成：

```text
results/surrogate/SURROGATE_FAILURE_REPORT.md
```

禁止：
- 自动加样本；
- 自动调 HGBR；
- 自动换模型；
- 删除异常样本；
- 降低阈值。

等待用户决定。

---

# 45. 代理模型用途

代理模型只用于：
1. 快速预测；
2. 参数空间可视化；
3. 初步定位边界；
4. 交互式 scenario 查询。

正式论文关键边界必须由 exact game solver 再验证。

不要把 surrogate 当作 ground truth。

---

# 46. 边界变量

允许：

```text
transport_market_price
effective_abatement_fraction
storage_subsidy
capex_C_multiplier
capex_U_multiplier
carbon_scale
```

---

# 47. 正式边界类型

固定支持：

```text
SYSTEM_NPV_ZERO
C_VALUE_ZERO
U_VALUE_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
CO2_PRICE_ZERO
STORAGE_FEE_ZERO
```

适用矩阵：

```text
TRANSFER:
SYSTEM_NPV_ZERO
C_VALUE_ZERO
U_VALUE_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
CO2_PRICE_ZERO
STORAGE_FEE_ZERO

JOINT_VENTURE:
SYSTEM_NPV_ZERO
C_VALUE_ZERO
U_VALUE_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
CO2_PRICE_ZERO

STATE_OWNED:
SYSTEM_NPV_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
```

---

# 48. 投资边界的经济定义

C 投资 switch：

\[
Pr_C^{invest}=0.5
\]

U：

\[
Pr_U^{invest}=0.5
\]

不再使用模糊的“投资年份发生变化”。

---

# 49. 边界搜索流程

对变量 \(z\)：

### Step 1：surrogate 粗搜索

固定其他参数 baseline。

用：

```text
401 grid points
```

寻找目标相对阈值的全部 crossing interval。

### Step 2：exact solver 验证

每个 surrogate crossing interval 用 exact solver 重算两端。

若 exact response 没有 crossing：

```text
SURROGATE_FALSE_BRACKET
```

该 bracket 丢弃但必须记录。

### Step 3：exact interval refinement

对 exact crossing interval 二分。

终止：

```text
interval_width <= 1e-4 * (upper-lower)
```

NPV/价格目标：

```text
response = 0
```

投资目标：

```text
invest_prob = 0.5
```

### Step 4：允许多个边界

如果存在多个 crossing，全部保留。

不要只选一个“最好看的”。

---

# 50. 边界不是必然存在

若整个区间无 exact crossing：

```text
found = false
boundary_value = NaN
```

同时保存：

```text
closest_grid_value
closest_response
```

但不得把 closest point 称为 boundary。

---

# 51. 论文正式主边界

主变量：

```text
carbon_scale
```

三种模式都必须求：

```text
SYSTEM_NPV_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
```

TRANSFER/JV 再求：

```text
C_VALUE_ZERO
U_VALUE_ZERO
CO2_PRICE_ZERO
```

TRANSFER 再求：

```text
STORAGE_FEE_ZERO
```

---

# 52. 补充边界

对全部三种模式，以 baseline 其他变量固定，分别求：

```text
transport_market_price
effective_abatement_fraction
storage_subsidy
capex_C_multiplier
capex_U_multiplier
```

下的：

```text
SYSTEM_NPV_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
```

若某变量对某 mode 的 system value 数学上不产生影响，允许 found=false。

不要人为加入影响。

---

# 53. 旧 RL 模型处理

旧 RL：

```text
ccus_two_agent_topjournal/
```

保留。

新论文主线不再要求 RL Gate 5 通过。

新项目只生成：

```text
docs/RL_BENCHMARK_NOTE.md
```

必须客观写：
- 旧 AS-CTDE-PPO 已完成 15 个正式 policy；
- Gate 4 完整性通过；
- 原 Critic accuracy Gate 未通过；
- 因此 RL 不作为主 equilibrium solver；
- 新主线改用可解释的 stochastic dynamic game；
- 不得声称 RL “失败”或“无效”；
- 不得把 RL 结果混入新 exact solver dataset。

---

# 54. 新项目文件结构

必须创建：

```text
ccus_game_surrogate/
│
├── README.md
├── requirements.txt
│
├── config/
│   └── model_config.game.json
│
├── docs/
│   ├── MODEL_SPECIFICATION.md
│   ├── GAME_THEORY_METHOD.md
│   ├── NASH_BARGAINING.md
│   ├── SURROGATE_PROTOCOL.md
│   ├── PARAMETER_PROVENANCE.md
│   └── RL_BENCHMARK_NOTE.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── carbon_tree.py
│   ├── bargaining.py
│   ├── economics.py
│   ├── state.py
│   ├── stage_game.py
│   ├── equilibrium_selection.py
│   ├── dynamic_solver.py
│   ├── forward_propagation.py
│   ├── scenario_solver.py
│   ├── sobol_design.py
│   ├── dataset.py
│   ├── metrics.py
│   ├── surrogate.py
│   ├── boundary.py
│   └── reproducibility.py
│
├── tests/
│   ├── test_carbon_tree.py
│   ├── test_bargaining.py
│   ├── test_economics.py
│   ├── test_stage_game.py
│   ├── test_mixed_nash.py
│   ├── test_dynamic_solver.py
│   ├── test_forward_propagation.py
│   ├── test_dataset.py
│   ├── test_surrogate.py
│   └── test_boundary.py
│
├── solve_baseline.py
├── build_exact_dataset.py
├── fit_surrogates.py
├── search_boundaries.py
└── run_full_protocol.py
```

---

# 55. CLI 固定

Baseline：

```bash
python solve_baseline.py
```

Exact dataset：

```bash
python build_exact_dataset.py
```

Surrogate：

```bash
python fit_surrogates.py
```

Boundaries：

```bash
python search_boundaries.py
```

Full protocol：

```bash
python run_full_protocol.py
```

---

# 56. run_full_protocol.py 顺序

必须：

```text
Gate 1: compile/tests/config
↓
Gate 2: baseline exact solver
↓
Gate 3: exact 4096×3 dataset
↓
Gate 4: exact solver integrity
↓
Gate 5: surrogate fit
↓
Gate 6: surrogate accuracy
↓
Gate 7: exact-verified boundaries
↓
FINAL_REPORT
```

任何 Gate fail 立即停止。

---

# 57. 测试：碳价树

至少验证：
1. \(u>1\)；
2. \(d=1/u\)；
3. \(0<p<1\)；
4. root price = P0×carbon_scale；
5. recombination：up→down = down→up；
6. horizon=30 时节点数：
   \[
   \sum_{t=0}^{30}(t+1)=496
   \]

---

# 58. 测试：Nash bargaining

成交：

```text
ask=100
bid=200
omega=.5
→ price=150
→ matched=true
```

不成交：

```text
ask=201
bid=200
→ matched=false
→ price=NaN
```

负 CO₂ price：允许。

storage fee：必须非负。

---

# 59. 测试：建设滞后

初始：

```text
x_C=0
x_U=1
d_C=1
```

当前年：

```text
Q=0
CAPEX_C>0
```

下一年：

```text
x_C=1
```

绝对不能当年生产。

---

# 60. 测试：纯 Nash

构造手工 2×2 payoff：

```text
唯一 pure NE
两个 coordination NE
```

验证选择规则。

---

# 61. 测试：mixed Nash

使用 matching-pennies 型 payoff。

必须：

```text
pure NE count = 0
mixed probabilities = 0.5 / 0.5
```

容差：

```text
1e-10
```

---

# 62. 测试：多重均衡 tie-break

必须单独验证：
- Pareto dominated removal；
- max total payoff；
- max min payoff；
- min investment count；
- lexicographic final tie。

---

# 63. 测试：动态后向递推

使用 2-year synthetic model。

手算：

```text
terminal values
continuation
stage equilibrium
initial value
```

与代码完全一致。

---

# 64. 测试：forward probability mass

每个年份：

```text
sum(probabilities)=1
```

容差：

```text
1e-12
```

---

# 65. 测试：backward vs forward NPV

baseline 三模式：

```text
difference < 1e-8
```

---

# 66. 测试：Sobol

必须：

```text
4096 unique rows
scenario_id unique
all values inside domain
same seed reproduces byte-identical design
```

---

# 67. 测试：split leakage

同一个 scenario_id 的三种 mode 必须全部属于同一个 split。

---

# 68. 测试：surrogate feature leakage

禁止以下进入 feature matrix：

```text
scenario_id
mode
target
solver metadata
```

---

# 69. 测试：boundary

必须覆盖：
1. 单根；
2. 多根；
3. 无根；
4. surrogate false bracket；
5. exact crossing；
6. investment 0.5 crossing。

---

# 70. Pre-flight

正式 exact dataset 前执行：

```bash
python -m compileall -q .
python -m pytest -q
```

要求：

```text
0 failed
0 errors
```

然后：

```bash
python solve_baseline.py
```

baseline 三个 mode 必须全部 OK。

---

# 71. 结果目录保护

正式目录：

```text
results/formal/
```

若非空，默认拒绝覆盖。

必须显式：

```text
--resume
```

resume 只允许：
- 跳过完整 scenario solve；
- 跳过已验证 surrogate artifact；
- 不得覆盖已有 exact row。

---

# 72. Exact dataset checkpoint

每完成：

```text
128 scenarios
```

保存一次。

格式：

```text
results/formal/exact_dataset/chunks/chunk_XXXX.parquet
```

若 parquet 依赖不可用，使用 CSV。

完成后合并。

---

# 73. Reproducibility manifest

记录：

```text
git commit
config SHA256
Python version
NumPy
Pandas
SciPy
scikit-learn

all src/*.py SHA256
all root entry script SHA256

Sobol seed
split seed
```

输出：

```text
results/formal/reproducibility_manifest.json
```

---

# 74. Final report

最终生成：

```text
results/formal/FINAL_EXECUTION_REPORT.md
```

必须包含：
1. Git / config / source hash；
2. test summary；
3. baseline 3-mode results；
4. exact dataset row count；
5. pure vs mixed equilibrium incidence；
6. multiple equilibrium incidence；
7. 3-mode value summary；
8. investment probability summary；
9. investment timing summary；
10. bargaining price summary；
11. surrogate metrics；
12. Gate PASS/FAIL；
13. exact-verified boundary results；
14. RL benchmark note；
15. 所有结构性 NaN 的解释。

---

# 75. 不允许的“优化”

Codex 不得为了“让结果更好”：
- 改碳价过程；
- 改 \(\mu,\sigma\)；
- 改 CAPEX；
- 改 subsidy；
- 改 bargaining weights；
- 改 JV shares；
- 改 horizon；
- 改 discount rate；
- 改 scenario domain；
- 改 equilibrium selection；
- 改 Sobol n；
- 改 surrogate gate；
- 删掉难拟合 target；
- 选择性删除 scenario。

---

# 76. 如果 surrogate 精度不够

只允许停止并生成：

```text
SURROGATE_FAILURE_REPORT.md
```

报告：

```text
mode
target
train metric
validation metric
test metric
target distribution
worst 20 test errors
```

等待用户决定。

不允许自动调参。

---

# 77. 如果出现大量 mixed equilibrium

只报告：

```text
mixed_equilibrium_state_probability
```

不要自行改成 Stackelberg。

---

# 78. 如果出现大量多重 pure NE

只报告 multiplicity。

不要自行改 equilibrium selection rule。

---

# 79. 如果某模式系统 NPV 长期为负

如实保留。

不要改参数“制造投资”。

never-invest 是合法经济结果。

---

# 80. 论文解释重点

新主线的关键解释应该是：

```text
什么条件使投资概率从低变高？
什么条件使系统 NPV 穿越 0？
组织结构如何改变投资等待价值？
议价权如何分配运营剩余？
不同模式如何改变主体激励一致性？
```

而不是：

```text
哪个神经网络 loss 最低？
```

---

# 81. 数学定位

正式文稿允许称：

```text
finite-horizon stochastic dynamic game
real-options-style irreversible investment timing
generalized Nash bargaining
Markov-perfect equilibrium
surrogate-assisted equilibrium mapping
```

不要声称：

```text
closed-form real options solution
continuous-time MPE
global optimum in TRANSFER/JV
```

---

# 82. 旧 RL 与新主线的关系

论文叙事固定：

> 初始研究探索了基于 CTDE-PPO 的双主体动态学习方法，并完成了正式策略训练与经济核验。但由于价值函数近似的高精度验收没有达到预设标准，最终主研究框架采用可解释的有限期随机动态博弈作为高保真求解器，并进一步训练代理模型实现快速参数映射与边界识别。

不要写：

```text
RL 失败所以放弃
```

更不能隐瞒旧实验。

---

# 83. 新方法的核心优势

README / paper method note 必须强调：

1. 不再依赖 Critic 逼近；
2. 每个状态直接求 stage equilibrium；
3. 有限期后向递推可审计；
4. investment irreversibility 显式；
5. one-year construction lag 显式；
6. bargaining price 由 reservation value 内生决定；
7. never-invest 合法；
8. exact solver 结果确定性；
9. surrogate 只近似 exact solver；
10. boundary 再由 exact solver 验证。

---

# 84. 全流程一次性执行原则

本次不再分四轮等待用户逐阶段确认。

只要：
- 所有前置测试通过；
- 当前 Gate 通过；
- 不存在本规范未定义的研究性歧义；

Codex 必须**自动继续下一阶段**，直到全部完成：

```text
代码实现
→ 单元测试
→ baseline exact solve
→ 4096 Sobol scenarios × 3 modes exact dataset
→ exact solver Gate
→ surrogate training
→ surrogate Gate
→ exact-verified boundary search
→ final report
```

中途不得因为“阶段完成”而自行停下。

只有以下情况允许停止：

```text
STOP_FOR_USER_DECISION
GATE_EXACT_SOLVER_FAIL
GATE_SURROGATE_FAIL
FORMAL_ARTIFACT_ERROR
UNDEFINED_RESEARCH_CHOICE
```

如果只是计算耗时较长，不属于停止理由。

---

# 85. 全流程 Stage A：实现、测试与 baseline

先完成：

```text
ccus_game_surrogate/
完整源码
完整测试
完整docs
README
config
CLI
```

然后执行：

```bash
python -m compileall -q .
python -m pytest -q
python solve_baseline.py
```

要求：

```text
compileall exit code = 0
pytest = 0 failed / 0 errors
baseline 三种 mode = OK
```

必须核验：

```text
最大静态 accounting error < 1e-10
最大 backward-forward value error < 1e-8
每年 forward probability mass error < 1e-12
```

若全部通过：

**自动继续 Stage B。**

不得停下来等用户确认。

---

# 86. 全流程 Stage B：4096 Sobol × 3 modes 高保真精确数据集

自动执行：

```bash
python build_exact_dataset.py
```

必须得到：

```text
4096 scenarios
× 3 modes
= 12288 exact rows
```

scenario 设计必须严格使用：

```text
scipy.stats.qmc.Sobol
dimension = 6
scramble = True
seed = 20260921
random_base2(m=12)
```

数据必须逐 scenario 求解，不允许用 surrogate 或近似 policy 替代。

每 128 scenarios 保存 checkpoint chunk。

完成后执行 Exact Solver Gate。

必须报告并核验：

```text
exact scenario count = 4096
exact row count = 12288
solver_status OK count = 12288
failed solve count = 0
nonfinite mandatory target count = 0
probability mass failures = 0
dynamic accounting failures = 0
```

若 Gate 通过：

**自动继续 Stage C。**

若失败：

生成：

```text
results/formal/EXACT_SOLVER_FAILURE_REPORT.md
```

并停止，不得自行修改研究设计。

---

# 87. 全流程 Stage C：代理模型训练与 Gate

Exact Solver Gate 通过后自动执行：

```bash
python fit_surrogates.py
```

必须使用已经冻结的：

```text
HistGradientBoostingRegressor
```

及固定超参数。

不得尝试其他模型作为备选。

必须严格按照：

```text
2868 train
614 validation
614 test
```

按 scenario_id 划分。

三种 mode 的同一 scenario 必须处于同一 split。

完成后计算所有规定 target 的：

```text
R2
MAE
RMSE
NMAE
```

然后执行 Surrogate Gate。

若所有 gating targets 通过：

**自动继续 Stage D。**

若任意 target 失败：

生成：

```text
results/formal/surrogate/SURROGATE_FAILURE_REPORT.md
```

必须列出：

```text
mode
target
n_train
n_validation
n_test
train metrics
validation metrics
test metrics
target distribution
worst 20 test rows
```

然后停止并询问用户。

禁止：
- 自动增加样本；
- 自动调参；
- 自动换 XGBoost/LightGBM/MLP；
- 降低 Gate；
- 删除误差大的 test points。

---

# 88. 全流程 Stage D：正式边界搜索

Surrogate Gate 全部通过后，自动执行：

```bash
python search_boundaries.py
```

必须先用 surrogate：

```text
401 grid points
```

生成候选 crossing brackets。

然后每一个正式 boundary 都必须用 exact dynamic game solver 验证。

禁止直接把 surrogate root 当正式边界。

正式主边界必须全部完成：

```text
carbon_scale:
    TRANSFER:
        SYSTEM_NPV_ZERO
        C_VALUE_ZERO
        U_VALUE_ZERO
        C_INVEST_PROB_50
        U_INVEST_PROB_50
        CO2_PRICE_ZERO
        STORAGE_FEE_ZERO

    JOINT_VENTURE:
        SYSTEM_NPV_ZERO
        C_VALUE_ZERO
        U_VALUE_ZERO
        C_INVEST_PROB_50
        U_INVEST_PROB_50
        CO2_PRICE_ZERO

    STATE_OWNED:
        SYSTEM_NPV_ZERO
        C_INVEST_PROB_50
        U_INVEST_PROB_50
```

补充变量：

```text
transport_market_price
effective_abatement_fraction
storage_subsidy
capex_C_multiplier
capex_U_multiplier
```

对三种 mode 都求：

```text
SYSTEM_NPV_ZERO
C_INVEST_PROB_50
U_INVEST_PROB_50
```

如果某 target 对某 mode 结构性不适用：
按照本规范适用矩阵拒绝，不得生成伪结果。

如果没有 crossing：

```text
found = false
boundary_value = NaN
```

这是合法结果，不属于 Gate failure。

如果存在多个 crossing：

全部保留。

完成后自动进入 Stage E。

---

# 89. 全流程 Stage E：最终核验与正式报告

全部边界完成后执行最终一致性检查。

必须重新运行：

```bash
python -m compileall -q .
python -m pytest -q
```

并核验：

```text
config SHA256
source SHA256 manifest
Sobol design hash
split hash
exact dataset hash
surrogate model hashes
boundary result hashes
```

必须生成：

```text
results/formal/reproducibility_manifest.json
results/formal/FINAL_EXECUTION_REPORT.md
```

最终报告必须包含：

```text
1. 方法版本与Git commit
2. config SHA256
3. source manifest SHA256
4. compileall结果
5. pytest结果
6. baseline三模式
7. baseline equilibrium类型
8. baseline会计误差
9. baseline backward-forward value error
10. exact scenario count
11. exact row count
12. pure NE incidence
13. mixed NE incidence
14. multiple pure NE incidence
15. TRANSFER核心结果统计
16. JOINT_VENTURE核心结果统计
17. STATE_OWNED核心结果统计
18. system NPV分布
19. C/U投资概率分布
20. C/U条件投资年份分布
21. CO2价格分布
22. storage fee分布
23. surrogate全部test metrics
24. surrogate Gate状态
25. 主边界结果
26. 补充边界结果
27. 未找到的边界
28. surrogate false brackets
29. 结构性NaN解释
30. RL benchmark note
31. 所有Gate状态
32. 最终执行状态
```

---

# 90. 正式输出文件要求

最终至少必须存在：

```text
results/formal/baseline/baseline_summary.csv

results/formal/exact_dataset/exact_scenarios.csv
results/formal/exact_dataset/exact_equilibrium_outputs.csv

results/formal/surrogate/scenario_split.csv
results/formal/surrogate/surrogate_metrics.csv
results/formal/surrogate/models/

results/formal/boundaries/boundary_results.csv
results/formal/boundaries/response_curves/

results/formal/reproducibility_manifest.json
results/formal/FINAL_EXECUTION_REPORT.md
```

并保存：

```text
exact dataset chunk checkpoint
surrogate metrics
boundary verification details
```

---

# 91. 全流程 resume 规则

所有大计算必须支持：

```bash
python run_full_protocol.py --resume
```

resume 只允许复用已经严格验证完整的 artifact。

### Exact dataset chunk 可跳过的条件

必须同时满足：

```text
scenario_id范围正确
row count正确
mode count正确
config hash一致
source hash一致
Sobol design hash一致
所有mandatory target finite
solver_status全部OK
```

### Surrogate 可跳过的条件

必须：

```text
dataset hash一致
split hash一致
feature list一致
target一致
model hyperparameters一致
model file可加载
metrics可重算一致
```

### Boundary 可跳过的条件

必须：

```text
surrogate hash一致
exact solver hash一致
variable/target/mode一致
search interval一致
grid size=401
exact verification已完成
```

任何不一致：

拒绝复用。

禁止 silent overwrite。

---

# 92. 全流程失败处理

如果程序因系统原因中断：

```text
断电
终端关闭
Python异常退出
人工中止
```

不得删除已经完整验证的 artifacts。

允许使用：

```bash
python run_full_protocol.py --resume
```

从最后一个完整 checkpoint 继续。

但如果失败原因属于研究设计不确定性：

必须按第 0.5 节：

```text
STOP_FOR_USER_DECISION
```

向用户询问。

---

# 93. Codex 全流程执行命令

完成代码后，最终主入口固定为：

```bash
python run_full_protocol.py
```

该入口必须按以下顺序自动执行：

```text
PRECHECK
→ BASELINE
→ EXACT_DATASET
→ EXACT_GATE
→ SURROGATE
→ SURROGATE_GATE
→ BOUNDARIES
→ FINAL_VALIDATION
→ FINAL_REPORT
```

不得要求用户在阶段之间手工运行不同命令。

单独 CLI 仍保留用于调试，但正式主运行只认：

```text
run_full_protocol.py
```

---

# 94. Codex 最终回复固定格式

全部流程成功后，只允许按以下顺序报告：

```text
1. Git commit SHA
2. config SHA256
3. source_manifest_hash
4. compileall结果
5. pytest结果

6. baseline TRANSFER摘要
7. baseline JOINT_VENTURE摘要
8. baseline STATE_OWNED摘要

9. exact scenarios = 4096
10. exact rows = 12288
11. exact solver failures = 0
12. pure NE incidence
13. mixed NE incidence
14. multiple pure NE incidence

15. surrogate gating target通过数量 / 总数量
16. surrogate最差gating R2
17. surrogate最大gating NMAE
18. investment probability最大test MAE
19. conditional investment year最大test MAE

20. 主边界完成数量
21. 补充边界完成数量
22. found=false数量
23. multiple-root数量

24. 最大静态accounting error
25. 最大backward-forward value error
26. 最大probability mass error

27. 旧RL项目是否修改：必须NO
28. 旧RL formal结果是否覆盖：必须NO

29. FINAL_EXECUTION_REPORT.md路径
30. 最终状态：
    ALL_STAGES_COMPLETED
```

如果中途因本规范未定义的问题停止，回复格式改为第 0.5 节的：

```text
STOP_FOR_USER_DECISION
```

---

# 95. 最终授权与最终停止规则

现在授权 Codex：

```text
从 0 实现新项目，
自动完成 baseline，
自动完成 4096×3 exact solver，
自动完成 surrogate，
自动完成 surrogate Gate，
自动完成 exact-verified boundaries，
自动完成最终报告。
```

只要规范已经给出明确答案，就不要中途询问用户。

只有遇到**本规范没有唯一答案**或 Gate failure 时才停下询问。

不得因为阶段完成而暂停。

不得自行增加研究内容。

不得自行修改任何参数和 Gate。

不得对旧 RL 项目做任何修改。

全部成功后，最终状态必须为：

```text
ALL_STAGES_COMPLETED
```

然后停止。

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
