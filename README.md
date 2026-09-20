# CCUS stochastic dynamic investment game

Two-agent stochastic dynamic investment game with generalized Nash bargaining
and surrogate-assisted equilibrium mapping.

本项目独立于旧 RL 项目。主依据为工作区根目录的严格实施规范，
用户补充定义见 [docs/USER_DECISIONS.md](docs/USER_DECISIONS.md)。
进程与证据记录见 [PROJECT_PROGRESS.md](PROJECT_PROGRESS.md)。

## 运行

已验证环境为 Python 3.13.9，依赖见 requirements.txt。
如果需要新环境，应在项目虚拟环境内安装依赖，不安装全局包。

```powershell
python run_full_protocol.py
```

正式目录非空时拒绝覆盖。已核验完整的检查点可显式恢复：

```powershell
python run_full_protocol.py --resume
```

单独调试入口：solve_baseline.py、build_exact_dataset.py、fit_surrogates.py、
search_boundaries.py。正式主运行只使用 run_full_protocol.py。
所有命令在本项目目录执行。Gate 失败即停止；不存在自动调参或换模型路径。

## 方法与可解释性

不依赖 Critic 近似，每个状态直接求阶段均衡，有限期后向递推可审计。
不可逆投资和一年建设滞后显式进入状态转移；当年生产使用旧建成状态。
交易价格由 reservation values 和广义 Nash 议价内生确定，允许负 CO2 价格。
不投资是合法结果。精确求解器给定参数时确定性执行，代理仅近似该求解器。
正式边界必须由精确求解器复核，不能用代理根替代。

TRANSFER/JV 的数学定位为 finite-horizon Markov-perfect equilibrium under
the binomial approximation；STATE_OWNED 为合作集中决策基准。
不声称连续时间闭式解、TRANSFER/JV 全局社会最优或均衡唯一。

## 产物与限制

正式产物在 results/formal/。source/config/Sobol/split/dataset/model/boundary
哈希用于复现和恢复验证。每 128 个场景保存一次完整检查点。
没有 Parquet 引擎时按规范使用 CSV；并行只分派独立场景。

当前目录不是 Git 仓库，因此 Git commit 如实记录为 null/NOT_A_GIT_REPOSITORY，
不用虚构 SHA 替代。旧 RL 产物未提供，相关历史叙述标注为规范提供、未独立核验。

零值平台的边界定义若在实际搜索中出现而规范无法唯一决定，程序返回
UNDEFINED_RESEARCH_CHOICE 等待用户决策，不擅自挑平台端点。
