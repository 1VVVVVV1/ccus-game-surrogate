# 广义 Nash 议价与交易口径

TRANSFER CO2 ask=P_tr+240-P_c*eta，bid=780-94.1654。
JV CO2 ask=240+125-P_c*eta，bid 不变。
ask<=bid 时 matched，price=ask+0.5*(bid-ask)，不截断负价格。

TRANSFER 封存 ask=max(0,43.71965-S_s)，bid=P_c*eta-240-P_tr。
成交条件相同，fee=ask+0.5*(bid-ask)，因此成交 fee 非负。
失败价格为 NaN，对应流量为零，计算支付时不执行 NaN×0。

JV 封存不议价；SOE 无两类内部交易。实际成交指示同时要求正流量、
matched 以及 finite price。均衡动作联合概率参与交易频率和条件价格的同一权重。
正式适用矩阵和十项新增验证要求见 USER_DECISIONS.md 与 test_transactions.py。
