# RL benchmark note

以下历史信息由主规范第 53、82 节提供；当前工作区没有旧项目及其正式产物，
尚不能通过 checkpoint、formal_run_lock 或 Gate 报告独立核验：

- 旧 AS-CTDE-PPO 已完成 15 个正式 policy。
- Gate 4 完整性通过，原 Critic accuracy Gate 未通过。
- 初始研究探索并完成正式策略训练与经济核验，但价值近似精度未达到预设标准。
- 因此本轮主框架采用可解释的有限期随机动态投资博弈，再训练代理用于参数映射和边界识别。

这些信息不构成对 RL 方法无效的判断。旧结果未混入精确求解数据集，
未修改旧 checkpoint、formal_run_lock 或 Gate 4/5 正式结果。
