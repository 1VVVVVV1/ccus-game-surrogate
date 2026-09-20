# 动态博弈方法

状态 s=(t,j,x_C,x_U)，t=0,...,29。碳价为物理概率 CRR 树节点，
p=(exp(mu*dt)-d)/(u-d)，u=exp(sigma*sqrt(dt))，d=1/u。
终期 continuation=0。J_i=pi_i+(1/1.08) E[V_i(next state)]。

动作 d_i 属于 {0,1-x_i}，当前利润使用旧 built state，投资当期支付 CAPEX，
下一期设施状态 max(x_i,d_i)。按 t 降序、j 升序、x_C 后 x_U 的 0/1 顺序递推。

TRANSFER/JV 先枚举容差 1e-10 的纯 Nash。保留 tie-break 前数量。
多重均衡先按规范的精确 Pareto 不等式删除被支配者，再最大化双方总价值、
最大化双方价值较小者、最小化投资数量、字典序。并列比较使用固定 tie_tolerance。
无纯均衡时仅在完整 2×2 游戏求内点混合均衡；失败即停止。
STATE_OWNED 最大化系统价值，再按投资数量和字典序选择。

从 (0,0,0,0) 以概率 1 前向传播，逐状态逐动作按联合概率累计折现利润。
该计算独立于后向价值的提取，两者严格核验。每年状态质量容差 1e-12。
均衡复杂性及交易概率定义见 USER_DECISIONS.md。
