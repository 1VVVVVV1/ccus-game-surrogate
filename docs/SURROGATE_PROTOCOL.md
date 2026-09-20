# 固定代理协议

Sobol: scipy.stats.qmc.Sobol(d=6,scramble=True,seed=20260921).random_base2(m=12)。
每场景三模式完整求解，共 12288 行。不删除失败行。

np.random.default_rng(42).permutation(4096) 顺序切分 2868/614/614。
同 scenario_id 三模式共用 split。六项输入顺序与主规范相同；不输入 mode、id、
solver metadata 或输出变量。每个模式、每个适用 target 单独训练。

HistGradientBoostingRegressor(learning_rate=.05,max_iter=500,max_leaf_nodes=31,
min_samples_leaf=20,l2_regularization=1e-3,random_state=42)。
未指定的参数使用已记录 scikit-learn 版本的默认值，实际参数写入模型 metadata。
不做自动搜索、调参、择优 seed 或算法替换。

仅条件 target 的结构性 NaN 不进入该 target 拟合。全体概率 target 保留。
R2/MAE/RMSE/NMAE 对原始未裁剪预测报告。每个 split 的 NMAE 分母为该 split
真实 target 的 Q95-Q05，<=1e-12 时 NaN。训练/验证/测试数量逐 target 保存。
价值 Gate：R2>=.98 且 NMAE<=.05；概率 MAE<=.03；条件年份 MAE<=1；
价格 R2>=.95 且 NMAE<=.08。任一 test Gate 失败生成报告并停止。

边界搜索固定其他变量 baseline，用 401 点代理网格提候选，再精确验证两端并二分。
停止宽度为 1e-4×整个搜索区间宽度。保留所有 crossing，记录 false brackets。
跳跃 crossing 保存两端响应，不能声称中点的响应恰好等于目标阈值。
