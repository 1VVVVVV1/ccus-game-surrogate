# CCUS 项目进程与核查记录

## 当前状态

SOURCE_BACKED_AUDIT_IN_PROGRESS — PIPELINE_EXCLUDED已接受，U CAPEX759.2857142857143已落实；继续剩余来源审计，未启动正式数值运行。

## 执行依据

- 主规范：../Codex_从0构建CCUS双主体随机动态博弈_Nash议价_代理模型_全流程严格实施规范.md
- 严格执行规范固定的参数、算法、均衡选择、样本量、划分、代理模型和 Gate。
- 仅在规范无法唯一决定研究性事项或 Gate 失败时停止。
- 每取得阶段成果，追加执行命令、验证证据、产物路径与 Gate 状态。

## 2026-09-20：阶段成果 001 — 输入审查与独立配置建立

已完成：

1. 阅读主规范第 0–95 节，核对全流程顺序及停止条件。
2. 检查工作区：初始仅有主规范文件，未发现旧 ccus_two_agent_topjournal 目录；git status 确认当前目录不是 Git 仓库。
3. 建立独立 ccus_game_surrogate/config 目录。
4. 将第 4 节 JSON 原样提取到 config/model_config.game.json，并通过 JSON 解析检查。未变更任何数值。
5. 建立本进程文档。

来源限制：旧正式配置及旧 RL 实验产物不在当前工作区，故配置来源目前为主规范，尚未完成旧产物交叉核验。规范对旧 RL 的叙述目前属于规范提供的信息，不是已检查产物所验证的事实。没有修改旧 RL 项目或其正式结果。

## 待决定事项 001 — 跨年份状态概率的定义

位置：第 25、27、74、77、78、89、94 节；forward_propagation.py 的输出定义。

事实：规范定义每年状态概率质量为 1，并要求输出 mixed_equilibrium_state_probability 与 multiple_pure_equilibrium_state_probability，但未给出跨 30 年汇总公式。逐年概率本身可确定，以下汇总量不等价：

A. 每年事件概率的算术平均：(1/30) × sum_t Pr(E_t)，范围 [0,1]。
B. 整个期间至少一次出现该类状态的概率：Pr(union_t E_t)，范围 [0,1]，需要保留是否曾发生事件的信息。
C. 每年事件概率之和：sum_t Pr(E_t)，范围 [0,30]，含义为预期发生年数。

已解决：用户明确选择 A，补充了完整公式、SOE 零值约定及六项测试。详见 docs/USER_DECISIONS.md。原问题保留供审计，不再重复询问。

## 尚未执行

- 研究求解代码及完整测试实现。
- Gate 1–7：全部 NOT_RUN。
- baseline、4096×3 精确数据集、代理训练与精度 Gate、正式边界搜索。
- 正式结果及最终执行报告。

明确：未改变参数、算法、阈值、样本量、均衡规则或代理模型；未生成研究结果。

## 文件校验

- 主规范 SHA256：52e0d777842a7fd8f24d0771fd651f97990f793675feab1eafc0a87b2da85227
- 独立配置 SHA256：3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76

## 2026-09-20：阶段成果 002 — 用户决策 001 实现与专项验证

- 新增 src/forward_propagation.py 中的状态概率统计函数，正式求解器尚待实现。
- mixed 仅计入 pure_ne_count=0 且成功求出 MIXED_NASH 的可达状态。
- multiple 使用 tie-break 前的纯均衡数量；SOE 两项概率及两项预期年数均为 0.0。
- 新增 tests/test_forward_propagation.py：覆盖用户六项测试及不可达状态、概率权重、未成功求解不计入 mixed 等检查，共 9 项。
- 验证命令：D:/anaconda3/python.exe -m compileall -q src tests，最终 exit=0。
- 验证命令：D:/anaconda3/python.exe -m pytest -q tests/test_forward_propagation.py -p no:cacheprovider，exit=0，9 passed in 0.03s。
- 初次受限 compileall 因 Windows 拒绝写入 __pycache__ 失败，获准在项目内写入后原命令通过；首次受限 pytest 已显示九项通过但未正常返回，授权重跑后确认正常退出。本项为局部工程验证，尚不构成完整 Gate 1。
- 已检查运行环境：Python 3.13.9、NumPy 2.3.5、SciPy 1.16.3、Pandas 2.3.3、scikit-learn 1.7.2、pytest 8.4.2。
- 固定模型配置未修改；未执行 baseline、正式数据集、代理训练或边界搜索。

## 待决定事项 002 — 交易年度概率字段

位置：规范第 27–28 节，co2_trade_year_probability / storage_trade_year_probability。

已核查：第 27 节只列字段名，第 28 节给出按正交易流量年份加权的条件价格，但没有定义以上两项概率的分母。决策 001 仅定义均衡统计。

待明确两个字段是否均采用：

co2_trade_year_probability = (1/30) * sum_t sum_s Pr_t(s) * 1{q_u(t,s)>0}。

storage_trade_year_probability = (1/30) * sum_t sum_s Pr_t(s) * 1{q_s(t,s)>0}。

交易事件口径也待明确：对无相应内部交易的模式（JV 的 storage、SOE 的 CO2/storage），是结构性 NaN，还是按物理利用/封存流量计算上述概率？这会改变指标的经济含义，不能用已有的价格适用矩阵自动推定物理流量指标的适用性。

问题以一个统计定义选择提交：A 为平均年度正物理流量概率、三模式均适用；B 为平均年度实际内部交易概率、无相应内部交易时结构性 NaN；C 为用户另行给出公式和适用模式。

当前暂停所有研究计算；未执行其余求解模块与正式 Gate。已有专项测试及配置保留。

## 2026-09-20：用户决策 002 已解决

用户附件明确选择 B，给出内部交易概率、实际成交指示、状态×动作权重、价格共用分母及结构性 NaN 适用矩阵。实现于 TransactionAccumulator，补充记录见 docs/USER_DECISIONS.md。

## 2026-09-20：阶段成果 003 — 核心求解器与专项测试

已实现固定经济参数、物理概率 CRR 树、Nash 议价、三模式利润、不可逆投资与建设滞后、pure/mixed Nash、确定性 tie-break、后向求解及独立前向概率传播。

新增两年手算案例及三模式 baseline 一致性测试。局部命令 python -m pytest -q -p no:cacheprovider：37 passed in 2.15s，exit=0。这是实现阶段检查，非完整正式 Gate 1。

正式数据集代码按每 128 个 scenario 保存检查点；六维 Sobol、split、HGBR 及阈值均使用规范固定值。并行只用于独立 scenario 调度。README、方法、议价、参数来源、代理协议及 RL note 已建立。

没有旧 RL 产物可核查；没有 Git 仓库，因此 Git SHA 将标为不可用，不虚构 commit。未创建或改写旧 RL 目录。


Gate 1 COMPILE_TESTS_CONFIG: PASS. {"compileall": {"exit_code": 0, "stdout": "", "stderr": ""}, "pytest": {"exit_code": 0, "stdout": "..................................................                       [100%]\n50 passed in 1.88s\n", "stderr": ""}}


Gate 2 BASELINE: PASS. {"mode_count": 3, "all_solver_status_OK": true}


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 75d61f4ac9037b50128719ff26c7c66045c126cf9119e1da9a60f3516ca49072.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash a135436461e50316afb71f1755eb792cefdd3d68656e6aebecf13158aa1161cb.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash d3a754009c584a1cdb8288089efe73d90667592653b9afa8348181e4265979ad.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 52fcd80fc911ab7011bdcc71dc8b6159bdbf76d93ce86ad7d8ecb0ddaec4691a.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 340c574350eb5f7cf01dc9ec6bc322e77d02c4ff58771ca03c2e29cc487375d2.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash 04a9e671dbf857fa380828e5206a58e6fd76f5950f4b4ed7921c5fffbc175723.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash a183071fdfaaa6d5c4aa8a85a2516c3816194ba20f397faa3cdc3f1b4ddcbec1.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash b505d4847b010713ca19439bf80448c82905d91b2375f4096d82dfad89222688.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash a33ed3d90d8a4dbd3290cdc4aeb67fd3ac5da9db499260383f3635cb488fb2a8.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash a41b7d7c54cfcec9ad140f81e6fc5adc5232ca8cab6a1afc9b6d5521eee00a99.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 5daa76a77c3449a1afe9b143c804513e2dfcf0a6f86d0bf05b915840eb022295.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 368532e1785bbebb15a1d2bbb8f56ad1432c1809ae9fd4e87add0d990f65fda3.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash 1d5df4a6c9cc33ae7558c6a9e7670bfcacfe2d30849042ab5a362d7659750c9e.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash d10d6caf16d9be373b63f2091fb3ca9e2770970e3ad87416c7c138d106a01bd6.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 69873989458891150f9ed0ff3d1d995f47113a91cfef3c8be67d667e83f2c879.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 51851c54ebebdd1ac4f93e8a08c70dcd2b4881209ce20ea402b6ef7ab5c4e246.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash f31c398f3ae20935b0a19226d3b79ea1b0c04e4208bfd1b624e288fde0e0c5cf.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 659e72a3c8b90835a466129a00072d2dd1a691b89b6b1120e68b827908dbde62.


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash f04e37dff707e0e27fa945252730cc8a65e5b62d3b1337584ae510177e32e1c9.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 1dbf91e2fe91dd52f87d5b913dcd1bbef8993c38a1d6426dc759e83e22bb2def.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash 542bbb2f0cf537cb4d401808daa8fb49bd01100e3d170336d494c0c462319cbc.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 9180cb3626824fd4b2bac87b137626f484e325f0fd77af1f4383f650d35ba07f.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash 482749a7e460fe84fa8c3d166da64d7e93bf82221ad179b4a30c64dff525cd01.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 508baecbd080d11aff4d3b56f1e4cf6cd29aaf306b6deac422696f3cad14645a.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 67140f83f09c19a854e08000b2fbbdad819b0d41af51edcf315c6584697aba11.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 0092b81590cfd50f23e156e1cf88cd05eb97d8deb558c2092a56ab3951549da0.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash b0cf2762c8a72035eeb43b4e87e4115218729ade190252385b5efecefa8b879e.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash df94a16636af47aeb711ec0f3c986bbdbc933ef19b6adf4d9627f584b3760396.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 9968b51c19fef00e88b1e783ff977e71034ad32cb271423193ff89f6b451c6bd.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash bd9d953f82e6f5cbf64d8407a2f9978911d767c2f0ed3f3b5fa78019668e20ff.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 66783c575723f8d7dcf033a52cec9eebb038ee3c274006329ba040ff07a9f4bb.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 819a8b50ce19c78e0bddcfba75e9633b9c925325e16e41eb962f66df4d6de2fb.


Gate 3 EXACT_DATASET: PASS. {"scenario_count": 4096, "row_count": 12288}


Gate 4 EXACT_INTEGRITY: PASS. {"solver_OK": 12288, "failed_solves": 0, "nonfinite_mandatory": 0, "probability_mass_failures": 0, "dynamic_accounting_failures": 0}


Gate 5 SURROGATE_FIT: PASS. {"models": 24}


Gate 6 SURROGATE_ACCURACY: PASS. {"gating_targets_passed": 24}


Gate 7 EXACT_VERIFIED_BOUNDARIES: PASS. {"rows": 61, "searches": 61}


## ALL_STAGES_COMPLETED

Final report: results/formal/FINAL_EXECUTION_REPORT.md

## 工程修复与独立归档

首次正式运行 Gate 1–7 全部通过，50 tests passed，4096×3 数据完整，24/24 代理 target 通过。61 项边界搜索保留 0 个 exact crossing，按固定规则丢弃 33 个 false brackets。此结果不能解释为整个参数区间不存在经济边界。

完整运行末尾代码审查发现成功后 --resume 会尝试重新创建已有最终报告。修复仅影响最终报告的恢复和完整性验证，不改变研究算法或参数。新增 completion.json 记录报告/manifest 哈希，恢复时验证后跳过已有报告；新增对应测试。

原始正式目录及源代码快照完整保存在 results/archive/run_a72a2305003f/，未删除或覆盖。因为 source hash 变化，未复用旧 exact 行，重新完整运行，遵守哈希一致才可 resume 的要求。最终报告补充 found=false 的解释限制，无扩大候选区间或替换搜索算法。

## Gate 1 重跑失败：停止等待用户决定

工程修复后的局部测试及正式 PRECHECK 均报告 50 passed、2 errors。两个错误均发生在新增 test_reproducibility.py 的 tmp_path fixture setup 阶段：pytest 尝试访问 C:/Users/pc/AppData/Local/Temp/ 下的 pytest-of-* 目录时出现 PermissionError / WinError 5。新增断言尚未执行，不能声称恢复修复已验证。

正式预检证据：results/formal/precheck_failure.json（compileall exit=0，pytest exit=1）。
停止报告：results/formal/EXECUTION_STOP_REPORT.md。
当前源码/配置与失败现场：results/formal/interrupted_reproducibility_manifest.json。

本轮失误记录：局部测试和正式入口被放在同一次工具编排中顺序调用，未先检查局部测试返回码，导致局部测试报错后仍启动了正式 PRECHECK。正式入口随后按 Gate 规则自行停止。未执行新版 baseline、dataset、surrogate 或 boundaries。今后必须先检查局部验证返回码再启动依赖步骤。

待决定：是否仅将 pytest 临时根目录设到项目内可写目录（工程环境修复，不改变测试断言、参数、算法、样本或 Gate），再用 --resume 重新预检并继续？未自动修改临时目录或绕过失败测试。

首轮运行的审计结论仍保留，适用于归档源码版本 a72a2305003f2fda42be7c509f5d71f13f98e28b82fe9d47735563f354e93c08：4096 场景、12288 行、24/24 代理 target 通过、16 主搜索和 45 补充搜索、61 found=false、33 false brackets；254 个已记录 artifact hashes 已独立复核一致。结果不能用来声称当前修改后的源码已完成正式验证。

## 2026-09-20：用户授权项目内临时目录修复；最小写入检查失败

已读取完整用户附件 8f2bc351-6663-4450-ba3a-6686d42ccdc1/已粘贴的文本.txt。授权仅限 pytest 测试运行环境；不改研究源码、模型配置、断言或 Gate。

写入前完整性核验：PASS。

- config SHA256：3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76。
- source_manifest_hash：2d53befd84c4ab357af40aa9c96a6f17ee6c959eb32c4af79196a68d8946eef0，与当前 formal_run_lock 和中断现场一致。
- 23 个源码文件逐一匹配中断 manifest。
- 12 个测试文件逐一匹配中断 manifest；未更改测试断言。
- git rev-parse HEAD 与 git status --short 均确认当前目录不是 Git 仓库，无法提供 Git SHA/worktree 状态。
- 项目不存在 .venv/Scripts/python.exe；检查使用原已记录的 D:/anaconda3/python.exe，未创建或切换 Python 环境。

在当前受限命令执行环境中运行：

```powershell
New-Item -ItemType Directory -Path '.pytest_tmp' -Force
& 'D:\anaconda3\python.exe' -c "from pathlib import Path; p=Path('.pytest_tmp'); p.mkdir(exist_ok=True); f=p/'write_test.txt'; f.write_text('ok',encoding='utf-8'); print(f.read_text(encoding='utf-8')); f.unlink()"
```

结果：exit code=1，未输出 ok。New-Item 返回 Access denied；Python 在 p.mkdir(exist_ok=True) 返回 PermissionError: [WinError 5]: '.pytest_tmp'，尚未执行 write_text。

按用户第 2 节明确要求“如果这里仍然出现 PermissionError：立即停止 LOCAL_PYTEST_TEMP_NOT_WRITABLE；不要继续 pytest”，当前停止。没有重跑 pytest/compileall/正式入口，没有修改 Windows ACL，没有使用管理员身份，没有跳过测试，没有覆盖正式结果。此记录不证明用户普通交互会话也不能写入该目录；已验证的是当前受限命令执行环境的写入失败。

本轮未完成 pytest.ini/.gitignore 设置；本地测试临时目录尚未通过可写性验证。正式 Gate 1 尚未重新通过，不能将归档结果标为当前版本通过。


## EXECUTION_STOPPED

Stage: PRECHECK

RuntimeError: GATE_PRECHECK_FAIL: pytest

No downstream stages executed; no parameter or gate changes.

## 2026-09-20：阶段成果 004 — 项目本地 pytest 环境恢复

最小写入检查输出 ok、exit=0。完整 pytest 52 passed in 2.04s，0 failed/0 errors/0 skipped；compileall exit=0。配置、23 个源码文件、12 个测试文件哈希全部与当前中断现场一致。新增 pytest.ini/.gitignore，标记 TEST_INFRASTRUCTURE_ONLY；未修改研究代码、断言、参数、模型、样本或 Gate。

事件详情见 docs/PYTEST_TEMPORARY_DIRECTORY_INCIDENT.md；可核验证据见 results/formal/test_infrastructure_recovery.json。当前 Git 不存在，继续如实标记不可用。当前 source hash 2d53befd84c4ab357af40aa9c96a6f17ee6c959eb32c4af79196a68d8946eef0 不同于首轮归档，不复用首轮研究产物。现在通过 run_full_protocol.py --resume 继续当前版本，正式研究阶段重新计算。


Gate 1 COMPILE_TESTS_CONFIG: PASS. {"compileall": {"exit_code": 0, "stdout": "", "stderr": ""}, "pytest": {"exit_code": 0, "stdout": "....................................................                     [100%]\n52 passed in 1.91s\n", "stderr": ""}}


Gate 2 BASELINE: PASS. {"mode_count": 3, "all_solver_status_OK": true}


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 75d61f4ac9037b50128719ff26c7c66045c126cf9119e1da9a60f3516ca49072.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash a135436461e50316afb71f1755eb792cefdd3d68656e6aebecf13158aa1161cb.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash d3a754009c584a1cdb8288089efe73d90667592653b9afa8348181e4265979ad.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 52fcd80fc911ab7011bdcc71dc8b6159bdbf76d93ce86ad7d8ecb0ddaec4691a.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 340c574350eb5f7cf01dc9ec6bc322e77d02c4ff58771ca03c2e29cc487375d2.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash 04a9e671dbf857fa380828e5206a58e6fd76f5950f4b4ed7921c5fffbc175723.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash a183071fdfaaa6d5c4aa8a85a2516c3816194ba20f397faa3cdc3f1b4ddcbec1.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash b505d4847b010713ca19439bf80448c82905d91b2375f4096d82dfad89222688.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash a33ed3d90d8a4dbd3290cdc4aeb67fd3ac5da9db499260383f3635cb488fb2a8.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash a41b7d7c54cfcec9ad140f81e6fc5adc5232ca8cab6a1afc9b6d5521eee00a99.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 5daa76a77c3449a1afe9b143c804513e2dfcf0a6f86d0bf05b915840eb022295.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 368532e1785bbebb15a1d2bbb8f56ad1432c1809ae9fd4e87add0d990f65fda3.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash 1d5df4a6c9cc33ae7558c6a9e7670bfcacfe2d30849042ab5a362d7659750c9e.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash d10d6caf16d9be373b63f2091fb3ca9e2770970e3ad87416c7c138d106a01bd6.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 69873989458891150f9ed0ff3d1d995f47113a91cfef3c8be67d667e83f2c879.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 51851c54ebebdd1ac4f93e8a08c70dcd2b4881209ce20ea402b6ef7ab5c4e246.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash f31c398f3ae20935b0a19226d3b79ea1b0c04e4208bfd1b624e288fde0e0c5cf.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 659e72a3c8b90835a466129a00072d2dd1a691b89b6b1120e68b827908dbde62.


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash f04e37dff707e0e27fa945252730cc8a65e5b62d3b1337584ae510177e32e1c9.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 1dbf91e2fe91dd52f87d5b913dcd1bbef8993c38a1d6426dc759e83e22bb2def.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash 542bbb2f0cf537cb4d401808daa8fb49bd01100e3d170336d494c0c462319cbc.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 9180cb3626824fd4b2bac87b137626f484e325f0fd77af1f4383f650d35ba07f.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash 482749a7e460fe84fa8c3d166da64d7e93bf82221ad179b4a30c64dff525cd01.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 508baecbd080d11aff4d3b56f1e4cf6cd29aaf306b6deac422696f3cad14645a.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 67140f83f09c19a854e08000b2fbbdad819b0d41af51edcf315c6584697aba11.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 0092b81590cfd50f23e156e1cf88cd05eb97d8deb558c2092a56ab3951549da0.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash b0cf2762c8a72035eeb43b4e87e4115218729ade190252385b5efecefa8b879e.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash df94a16636af47aeb711ec0f3c986bbdbc933ef19b6adf4d9627f584b3760396.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 9968b51c19fef00e88b1e783ff977e71034ad32cb271423193ff89f6b451c6bd.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash bd9d953f82e6f5cbf64d8407a2f9978911d767c2f0ed3f3b5fa78019668e20ff.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 66783c575723f8d7dcf033a52cec9eebb038ee3c274006329ba040ff07a9f4bb.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 819a8b50ce19c78e0bddcfba75e9633b9c925325e16e41eb962f66df4d6de2fb.


Gate 3 EXACT_DATASET: PASS. {"scenario_count": 4096, "row_count": 12288}


Gate 4 EXACT_INTEGRITY: PASS. {"solver_OK": 12288, "failed_solves": 0, "nonfinite_mandatory": 0, "probability_mass_failures": 0, "dynamic_accounting_failures": 0}


Gate 5 SURROGATE_FIT: PASS. {"models": 24}


Gate 6 SURROGATE_ACCURACY: PASS. {"gating_targets_passed": 24}


Gate 7 EXACT_VERIFIED_BOUNDARIES: PASS. {"rows": 61, "searches": 61}


## ALL_STAGES_COMPLETED

Final report: results/formal/FINAL_EXECUTION_REPORT.md


Gate 1 COMPILE_TESTS_CONFIG: PASS. {"compileall": {"exit_code": 0, "stdout": "", "stderr": ""}, "pytest": {"exit_code": 0, "stdout": "....................................................                     [100%]\n52 passed in 2.06s\n", "stderr": ""}}


Gate 2 BASELINE: PASS. {"mode_count": 3, "all_solver_status_OK": true}


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 75d61f4ac9037b50128719ff26c7c66045c126cf9119e1da9a60f3516ca49072.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash a135436461e50316afb71f1755eb792cefdd3d68656e6aebecf13158aa1161cb.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash d3a754009c584a1cdb8288089efe73d90667592653b9afa8348181e4265979ad.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 52fcd80fc911ab7011bdcc71dc8b6159bdbf76d93ce86ad7d8ecb0ddaec4691a.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 340c574350eb5f7cf01dc9ec6bc322e77d02c4ff58771ca03c2e29cc487375d2.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash 04a9e671dbf857fa380828e5206a58e6fd76f5950f4b4ed7921c5fffbc175723.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash a183071fdfaaa6d5c4aa8a85a2516c3816194ba20f397faa3cdc3f1b4ddcbec1.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash b505d4847b010713ca19439bf80448c82905d91b2375f4096d82dfad89222688.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash a33ed3d90d8a4dbd3290cdc4aeb67fd3ac5da9db499260383f3635cb488fb2a8.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash a41b7d7c54cfcec9ad140f81e6fc5adc5232ca8cab6a1afc9b6d5521eee00a99.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 5daa76a77c3449a1afe9b143c804513e2dfcf0a6f86d0bf05b915840eb022295.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 368532e1785bbebb15a1d2bbb8f56ad1432c1809ae9fd4e87add0d990f65fda3.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash 1d5df4a6c9cc33ae7558c6a9e7670bfcacfe2d30849042ab5a362d7659750c9e.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash d10d6caf16d9be373b63f2091fb3ca9e2770970e3ad87416c7c138d106a01bd6.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 69873989458891150f9ed0ff3d1d995f47113a91cfef3c8be67d667e83f2c879.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 51851c54ebebdd1ac4f93e8a08c70dcd2b4881209ce20ea402b6ef7ab5c4e246.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash f31c398f3ae20935b0a19226d3b79ea1b0c04e4208bfd1b624e288fde0e0c5cf.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 659e72a3c8b90835a466129a00072d2dd1a691b89b6b1120e68b827908dbde62.


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash f04e37dff707e0e27fa945252730cc8a65e5b62d3b1337584ae510177e32e1c9.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 1dbf91e2fe91dd52f87d5b913dcd1bbef8993c38a1d6426dc759e83e22bb2def.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash 542bbb2f0cf537cb4d401808daa8fb49bd01100e3d170336d494c0c462319cbc.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 9180cb3626824fd4b2bac87b137626f484e325f0fd77af1f4383f650d35ba07f.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash 482749a7e460fe84fa8c3d166da64d7e93bf82221ad179b4a30c64dff525cd01.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 508baecbd080d11aff4d3b56f1e4cf6cd29aaf306b6deac422696f3cad14645a.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 67140f83f09c19a854e08000b2fbbdad819b0d41af51edcf315c6584697aba11.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 0092b81590cfd50f23e156e1cf88cd05eb97d8deb558c2092a56ab3951549da0.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash b0cf2762c8a72035eeb43b4e87e4115218729ade190252385b5efecefa8b879e.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash df94a16636af47aeb711ec0f3c986bbdbc933ef19b6adf4d9627f584b3760396.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 9968b51c19fef00e88b1e783ff977e71034ad32cb271423193ff89f6b451c6bd.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash bd9d953f82e6f5cbf64d8407a2f9978911d767c2f0ed3f3b5fa78019668e20ff.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 66783c575723f8d7dcf033a52cec9eebb038ee3c274006329ba040ff07a9f4bb.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 819a8b50ce19c78e0bddcfba75e9633b9c925325e16e41eb962f66df4d6de2fb.


## EXECUTION_STOPPED

Stage: EXACT_DATASET

RuntimeError: FORMAL_ARTIFACT_ERROR: exact merged dataset

No downstream stages executed; no parameter or gate changes.

## 2026-09-20：阶段成果 005 — 当前源码完整正式运行通过

当前源码 hash 2d53befd84c4ab357af40aa9c96a6f17ee6c959eb32c4af79196a68d8946eef0；本轮重新计算 4096 scenarios × 3 modes = 12288 exact rows，未复用 source hash 不同的首轮归档。Gate 1–7 PASS，24/24 surrogate targets PASS，16 主搜索+45 补充搜索完成；61 found=false、33 surrogate false brackets。最终 compileall exit=0，pytest 52 passed in 2.10s、exit=0。报告已增加用户要求的 Pytest Temporary Directory Incident 一节。

## 2026-09-20：端到端 --resume 验证未通过

重新执行 run_full_protocol.py --resume，Gate 1/2 通过，32 个 chunks 全部通过校验，但合并 exact CSV 与 chunks 比较报 FORMAL_ARTIFACT_ERROR: exact merged dataset，exit=1。

只读诊断已唯一定位：mixed_equilibrium_state_probability、expected_mixed_equilibrium_years 两列在本数据集中全部为零；CSV 推断为 int64，Parquet 为 float64，pandas.DataFrame.equals 因 dtype 不同返回 False。两表均 12288 行，列顺序一致，逐单元格严格比较（对应 NaN 同位）不一致数为 0，solver_status 全部 OK。恢复过程中原有产物修改数为 0；正式 manifest 的 258 个 artifact hashes 全部匹配。

证据：results/formal/resume_verification_failure.json、RESUME_FAILURE_REPORT.md。正式报告状态已如实标注 FORMAL_RUN_COMPLETED; RESUME_VERIFICATION_FAILED，completion.json 同步记录整体 STOP_FOR_USER_DECISION 及报告哈希。没有修改研究结果来规避失败。

当前授权仅允许 pytest 测试运行环境修复，未修改 src/dataset.py、任何研究源码或测试断言来绕过这次拒绝。待用户决定是否授权仅修复序列化 dtype 的严格比较路径并增加回归测试。不得放宽数值比较、哈希校验或任何 Gate；源码变更后的 artifact 复用/重算仍严格按原规范处理。未继续执行依赖该恢复成功的步骤。


## 2026-09-20：用户授权继续修复 resume

旧运行和源码快照已完整保存在 results/archive/run_2d53befd84c4/。src/dataset.py 仅在合并 CSV 恢复时按验证过的 chunks dtype 显式读取，继续用 DataFrame.equals 严格比较，不舍入、不用近似容差。新增测试覆盖全零浮点列、一个 ULP 的真实差异、行顺序和结构性 NaN，53 passed in 2.16s。src/protocol.py 仅自动纳入用户要求的临时目录事件文档，避免手工补报告。配置及其余研究源码哈希全部不变。源码整体 hash 变化，因此重新计算正式阶段，不强行复用旧 artifacts。


Gate 1 COMPILE_TESTS_CONFIG: PASS. {"compileall": {"exit_code": 0, "stdout": "", "stderr": ""}, "pytest": {"exit_code": 0, "stdout": ".....................................................                    [100%]\n53 passed in 1.99s\n", "stderr": ""}}


Gate 2 BASELINE: PASS. {"mode_count": 3, "all_solver_status_OK": true}


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 75d61f4ac9037b50128719ff26c7c66045c126cf9119e1da9a60f3516ca49072.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash a135436461e50316afb71f1755eb792cefdd3d68656e6aebecf13158aa1161cb.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash d3a754009c584a1cdb8288089efe73d90667592653b9afa8348181e4265979ad.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 52fcd80fc911ab7011bdcc71dc8b6159bdbf76d93ce86ad7d8ecb0ddaec4691a.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 340c574350eb5f7cf01dc9ec6bc322e77d02c4ff58771ca03c2e29cc487375d2.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash 04a9e671dbf857fa380828e5206a58e6fd76f5950f4b4ed7921c5fffbc175723.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash a183071fdfaaa6d5c4aa8a85a2516c3816194ba20f397faa3cdc3f1b4ddcbec1.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash b505d4847b010713ca19439bf80448c82905d91b2375f4096d82dfad89222688.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash a33ed3d90d8a4dbd3290cdc4aeb67fd3ac5da9db499260383f3635cb488fb2a8.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash a41b7d7c54cfcec9ad140f81e6fc5adc5232ca8cab6a1afc9b6d5521eee00a99.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 5daa76a77c3449a1afe9b143c804513e2dfcf0a6f86d0bf05b915840eb022295.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 368532e1785bbebb15a1d2bbb8f56ad1432c1809ae9fd4e87add0d990f65fda3.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash 1d5df4a6c9cc33ae7558c6a9e7670bfcacfe2d30849042ab5a362d7659750c9e.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash d10d6caf16d9be373b63f2091fb3ca9e2770970e3ad87416c7c138d106a01bd6.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 69873989458891150f9ed0ff3d1d995f47113a91cfef3c8be67d667e83f2c879.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 51851c54ebebdd1ac4f93e8a08c70dcd2b4881209ce20ea402b6ef7ab5c4e246.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash f31c398f3ae20935b0a19226d3b79ea1b0c04e4208bfd1b624e288fde0e0c5cf.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 659e72a3c8b90835a466129a00072d2dd1a691b89b6b1120e68b827908dbde62.


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash f04e37dff707e0e27fa945252730cc8a65e5b62d3b1337584ae510177e32e1c9.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 1dbf91e2fe91dd52f87d5b913dcd1bbef8993c38a1d6426dc759e83e22bb2def.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash 542bbb2f0cf537cb4d401808daa8fb49bd01100e3d170336d494c0c462319cbc.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 9180cb3626824fd4b2bac87b137626f484e325f0fd77af1f4383f650d35ba07f.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash 482749a7e460fe84fa8c3d166da64d7e93bf82221ad179b4a30c64dff525cd01.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 508baecbd080d11aff4d3b56f1e4cf6cd29aaf306b6deac422696f3cad14645a.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 67140f83f09c19a854e08000b2fbbdad819b0d41af51edcf315c6584697aba11.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 0092b81590cfd50f23e156e1cf88cd05eb97d8deb558c2092a56ab3951549da0.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash b0cf2762c8a72035eeb43b4e87e4115218729ade190252385b5efecefa8b879e.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash df94a16636af47aeb711ec0f3c986bbdbc933ef19b6adf4d9627f584b3760396.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 9968b51c19fef00e88b1e783ff977e71034ad32cb271423193ff89f6b451c6bd.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash bd9d953f82e6f5cbf64d8407a2f9978911d767c2f0ed3f3b5fa78019668e20ff.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 66783c575723f8d7dcf033a52cec9eebb038ee3c274006329ba040ff07a9f4bb.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 819a8b50ce19c78e0bddcfba75e9633b9c925325e16e41eb962f66df4d6de2fb.


Gate 3 EXACT_DATASET: PASS. {"scenario_count": 4096, "row_count": 12288}


Gate 4 EXACT_INTEGRITY: PASS. {"solver_OK": 12288, "failed_solves": 0, "nonfinite_mandatory": 0, "probability_mass_failures": 0, "dynamic_accounting_failures": 0}


Gate 5 SURROGATE_FIT: PASS. {"models": 24}


Gate 6 SURROGATE_ACCURACY: PASS. {"gating_targets_passed": 24}


Gate 7 EXACT_VERIFIED_BOUNDARIES: PASS. {"rows": 61, "searches": 61}


## ALL_STAGES_COMPLETED

Final report: results/formal/FINAL_EXECUTION_REPORT.md


Gate 1 COMPILE_TESTS_CONFIG: PASS. {"compileall": {"exit_code": 0, "stdout": "", "stderr": ""}, "pytest": {"exit_code": 0, "stdout": ".....................................................                    [100%]\n53 passed in 1.97s\n", "stderr": ""}}


Gate 2 BASELINE: PASS. {"mode_count": 3, "all_solver_status_OK": true}


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 75d61f4ac9037b50128719ff26c7c66045c126cf9119e1da9a60f3516ca49072.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash a135436461e50316afb71f1755eb792cefdd3d68656e6aebecf13158aa1161cb.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash d3a754009c584a1cdb8288089efe73d90667592653b9afa8348181e4265979ad.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 52fcd80fc911ab7011bdcc71dc8b6159bdbf76d93ce86ad7d8ecb0ddaec4691a.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 340c574350eb5f7cf01dc9ec6bc322e77d02c4ff58771ca03c2e29cc487375d2.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash 04a9e671dbf857fa380828e5206a58e6fd76f5950f4b4ed7921c5fffbc175723.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash a183071fdfaaa6d5c4aa8a85a2516c3816194ba20f397faa3cdc3f1b4ddcbec1.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash b505d4847b010713ca19439bf80448c82905d91b2375f4096d82dfad89222688.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash a33ed3d90d8a4dbd3290cdc4aeb67fd3ac5da9db499260383f3635cb488fb2a8.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash a41b7d7c54cfcec9ad140f81e6fc5adc5232ca8cab6a1afc9b6d5521eee00a99.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 5daa76a77c3449a1afe9b143c804513e2dfcf0a6f86d0bf05b915840eb022295.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 368532e1785bbebb15a1d2bbb8f56ad1432c1809ae9fd4e87add0d990f65fda3.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash 1d5df4a6c9cc33ae7558c6a9e7670bfcacfe2d30849042ab5a362d7659750c9e.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash d10d6caf16d9be373b63f2091fb3ca9e2770970e3ad87416c7c138d106a01bd6.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 69873989458891150f9ed0ff3d1d995f47113a91cfef3c8be67d667e83f2c879.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 51851c54ebebdd1ac4f93e8a08c70dcd2b4881209ce20ea402b6ef7ab5c4e246.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash f31c398f3ae20935b0a19226d3b79ea1b0c04e4208bfd1b624e288fde0e0c5cf.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 659e72a3c8b90835a466129a00072d2dd1a691b89b6b1120e68b827908dbde62.


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash f04e37dff707e0e27fa945252730cc8a65e5b62d3b1337584ae510177e32e1c9.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 1dbf91e2fe91dd52f87d5b913dcd1bbef8993c38a1d6426dc759e83e22bb2def.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash 542bbb2f0cf537cb4d401808daa8fb49bd01100e3d170336d494c0c462319cbc.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 9180cb3626824fd4b2bac87b137626f484e325f0fd77af1f4383f650d35ba07f.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash 482749a7e460fe84fa8c3d166da64d7e93bf82221ad179b4a30c64dff525cd01.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 508baecbd080d11aff4d3b56f1e4cf6cd29aaf306b6deac422696f3cad14645a.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 67140f83f09c19a854e08000b2fbbdad819b0d41af51edcf315c6584697aba11.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 0092b81590cfd50f23e156e1cf88cd05eb97d8deb558c2092a56ab3951549da0.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash b0cf2762c8a72035eeb43b4e87e4115218729ade190252385b5efecefa8b879e.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash df94a16636af47aeb711ec0f3c986bbdbc933ef19b6adf4d9627f584b3760396.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 9968b51c19fef00e88b1e783ff977e71034ad32cb271423193ff89f6b451c6bd.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash bd9d953f82e6f5cbf64d8407a2f9978911d767c2f0ed3f3b5fa78019668e20ff.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 66783c575723f8d7dcf033a52cec9eebb038ee3c274006329ba040ff07a9f4bb.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 819a8b50ce19c78e0bddcfba75e9633b9c925325e16e41eb962f66df4d6de2fb.


Gate 3 EXACT_DATASET: PASS. {"scenario_count": 4096, "row_count": 12288}


Gate 4 EXACT_INTEGRITY: PASS. {"solver_OK": 12288, "failed_solves": 0, "nonfinite_mandatory": 0, "probability_mass_failures": 0, "dynamic_accounting_failures": 0}


Gate 5 SURROGATE_FIT: PASS. {"models": 24}


Gate 6 SURROGATE_ACCURACY: PASS. {"gating_targets_passed": 24}


Gate 7 EXACT_VERIFIED_BOUNDARIES: PASS. {"rows": 61, "searches": 61}


## ALL_STAGES_COMPLETED

Final report: results/formal/FINAL_EXECUTION_REPORT.md


## 2026-09-20：最终验收 — 正式全流程及完整 resume 均通过

当前源码 1d8388dd180a3b528d8a7fe66fdee6fb8886d5a28c760b9aec3e1ea86e439d0b 正式运行 exit=0，Gate 1–7 PASS，最终 53 tests passed。实际完整 --resume 再运行 exit=0，模型指标重算严格一致、全部检查点与边界结果通过身份/哈希验证、最终报告成功复用。恢复前后 257 个正式文件逐字节 SHA256 全部相同；没有覆盖 exact 行、模型、metrics、边界或报告。证据见 results/resume_verification_PASS.json 和 results/resume_before_1d8388dd.json。

4096 scenarios、12288 exact rows、0 solver failures、24/24 surrogate targets PASS；16 主搜索+45 补充搜索完成，61 found=false、33 false brackets，未保留精确 crossing。该结果不证明整个区间不存在经济边界；未擅自拓宽候选区间或改变搜索算法。临时目录事件已由正式入口自动纳入报告。旧 RL 项目与正式结果均未修改。最终状态 ALL_STAGES_COMPLETED。


## 2026-09-20：新阶段规范接收与 Git 前置检查

已完整阅读真实数据校准/边界 V2/同步投资/论文前最终化规范第 0–69 节，规范 SHA256：ffbdbdd883211bfb0a0e330f163c6ea2ff515a5a362c0f1dd2cc01f430fddba8。本阶段与已完成的方法验证版本区分，不复用旧 exact/models/boundaries 为实证结果。

已核验当前 config/source identity、正式 manifest 全部 artifact 哈希、最终报告和 completion 哈希一致。依新规范第 1 节仅新增 results/formal/RUN_CLASSIFICATION.json，标记 METHOD_VALIDATION_RUN；已有正式文件未改写。

Git 版本 2.53.0.windows.3。git config --get user.name 和 user.email 均 exit=1、空值，当前目录不是 Git 仓库。依第 4 节 Git identity 缺失立即停止；未 git init、未伪造姓名邮箱、未提交、未修改全局 Git 配置。

新阶段状态 STOP_FOR_USER_DECISION，待用户提供此项目提交使用的 user.name 和 user.email。旧方法验证运行仍是 ALL_STAGES_COMPLETED；新 source-backed 阶段尚未开始来源审计/碳价校准/新配置/求解/代理/V2 边界。


## 新阶段：Git identity 已由用户提供

用户确认仅本地工作，提交名 1VVVVVV1、邮箱 1817512522@qq.com。已初始化本地 Git 并仅写入仓库级 identity，无 remote、未上传。目录所有权来自旧沙箱，Git 命令使用单次 -c safe.directory 指定已确认项目路径，不修改全局信任或 ACL。已有正式产物哈希和研究源码 hash 核验一致。当前按指定 commit message 冻结已验证源码、测试、配置、文档及小型摘要，之后开始来源审计。


## 2026-09-20：来源审计阶段成果及停止点

本地冻结提交 4f34c2ba31dc3167e4bbfbd67d2a371c6a0d9a6f 已完成，无 remote、未上传。文献 API 预检通过；Crossref 部分查询 429 后转单 DOI/OpenAlex。已识别泰州、Carbon Neutrality、运输、Engineering 等文献，详见 docs/SOURCE_CATALOG.md。Engineering 原文核实 50–60 CNY/t 是其他 CCUS 的注入成本，按授权可取 55 作为 proxy；未将它解释为全链条成本。初步 registry 仅含此已支持值及 5 个明确模型假设，未填未验证参数。

STOP_FOR_USER_DECISION：运输市场价格基准 125 CNY/t 尚无已核实 Grade A/A- 实際收费原文依据，原指定运输论文的 DOI 已双源核实但正文访问受阻，Elsevier API 仅返回书目信息。未将 0.26×距离推为收费，未假定距离或加成。依据新规范第 11/21 节暂停，等待来源或用户研究决定。其他未完成项在 SOURCE_AUDIT.md 中逐项列明，不声称已穷尽检索。

原始证据 16 个文件及 SHA256 保存于 results/source_backed_formal/source_audit/evidence_manifest.json。尚未采集官方碳价序列、冻结 source-backed config、实现或运行新正式求解、代理、V2 边界与同步诊断。旧 results/formal/ 既有文件均未改动，仅按新规范新增 RUN_CLASSIFICATION.json。


## 2026-09-20：运输定价补充授权已落实

用户将 transport_market_price=125 重新定位为 MODEL_ASSUMPTION，paper_use 为 Internal transport-service transfer-price benchmark；[75,200] 为 DESIGN_RANGE_ASSUMPTION。这两项不再是 unresolved empirical parameter。registry 已更新。用户给定 0.2584 CNY/(tCO2 km) 仅登记为候选经验管道系数，明确原文数值尚未独立核验，不代表总运输成本已闭环。未假设距离、未换算总成本、未改动经济源码或旧 config。继续其余来源审计。


## 2026-09-20：运输补充审计与新停止点

- 9 行参数 registry 已核对：125 为 MODEL_ASSUMPTION；[75,200] 为 DESIGN_RANGE_ASSUMPTION；0.2584 仅为待原文核实的候选系数。未计算运输总成本。
- 追加 S06 管道成本论文的 Crossref/OpenAlex 双源书目信息，S07 EOR 经济论文及公开版本线索。原文访问失败如实保存，未把验证页、摘要或元数据认作数值证据。
- 新停止原因：缺少可对应本模型规模和资产边界的源—汇项目、距离及 U 端利用路线。不能任取距离，不能跨项目拼接 CAPEX/收益或自行缩放。
- 本轮新增 STOP_FOR_USER_DECISION_transport_scope.json；历史 tariff 停止记录保留且已在当前审计说明中标明被用户决定取代。
- 验证：CSV 固定 19 列、9 行；用户指定的分类和文字一致；冻结配置 SHA256 未变；git diff 确认 src、tests、原模型配置及既有 formal 文件无已跟踪改动。此次仅审计文档/证据更新，无需重跑经济测试。
- 当前未执行：新 source-backed config、官方碳价校准及后续正式计算。阶段完成情况不能标记为全流程完成。


## 2026-09-20：齐鲁—胜利授权归档及原文核验

- 完整保存用户决定，新增 USER_DECISIONS 决策 004；不再询问项目、U 路线或距离选择。
- 三篇指定论文完成双源书目交叉核对，响应、失败及哈希保存在 source_audit/eor_anchor/。Elsevier 仅元数据；Wei PDF 403、OSTI 超时、FULL 接口 429。无关搜索结果和验证码页未作为来源。
- U CAPEX/O&M 方程、同项目输入及增量油/CO2 比率仍未形成原文证据链。按用户要求，在可核验原文之前不猜公式、不登记为已验证参数、不编写虚构成本模型。
- 新停止点为全文/项目输入缺失，需可读原文表格；109 km 官方核验仍待完成，但不就既定选择重新询问。未运行正式 12288 行。
- 校验冻结配置 SHA256 未变，研究源码/测试/旧 formal 无已跟踪修改。本轮只新增来源证据及审计文档，不需要运行经济求解测试。


## 2026-09-20：Yuan PDF 核验、距离原文与捕集 OPEX 性质修正

- 已读取用户 PDF，提取 8 页文本，视觉核验成本表和情景假设页。正式年份 2023；不采用文件名 2024，不将其 20 年/10%/200 km/100 元数值替代模型参数。
- 本地同目录权威报告原文支持 109 km，registry 增至 10 行，列数仍为 19；108 km 在建条目的差异及业主交叉核验待办明确记录。
- 自主网上取得 Carbon Neutrality HTML 全文，核实 240 为在建泰州预计 OPEX。未将预测错标为实测，也未擅自采纳为新假设。
- Wei、Li、Miao 下载继续受限；原始请求/失败和内容有效性检查均保存。没有把返回 200 的验证码或 404 页判为成功。
- 已检查文献下载配置：无已保存图书馆入口。需用户提供实际入口网址才能转合法机构全文访问；不再要求其逐篇下载，不使用聊天中出现过的凭据。
- SOURCE_AUDIT 未通过，eor_cost_calibration.py 和正式计算未启动。此次变更仅审计/registry/证据，冻结配置和研究源码未改动。
- 文本提取输出首次遇终端 GBK 编码错误；PNG 已成功生成并读取，后续文本用 UTF-8 输出完成。此为输出编码问题，不影响 PDF 原文件或证据内容。


## 2026-09-20：用户指定 ScienceDirect 入口后浏览器核验

已直接打开 Wei 2015 的 ScienceDirect 文章页。当前仅 Codex 内置浏览器可用，未连接 Chrome；页面实际显示 Are you a robot? / Cloudflare 正在验证。尚未获取文章正文或 PDF，不把访问验证页当成下载成功。等待页面自动验证结果，不操作验证码，不修改模型或正式配置。


## 2026-09-20：Wei 原文读取成功、18 行 registry 及新来源冲突

- 浏览器自动验证通过，Wei HTML 全文可读；PDF 仍在验证页，未宣称 PDF 已下载。完整导出接口不支持，保存的是原表数值和冲突段落的结构化核验摘录。
- 原 Table 4 八项参照已登记为 MODEL_ASSUMPTION，registry 19 列/18 行；不改变正式 30 年、折现率、Nash 内生价格。
- Table 1 举升费 1 USD/STB 对正文 0.25 USD/STB；公式（7）、（9）、（12）显示/系数疑点。没有替作者修公式，没有自选数值，没有编写臆测成本模块。
- Li 2022 当前会话显示需要机构访问；未购买。
- 新停止文件 STOP_FOR_USER_DECISION_wei_conflicts.json；历史访问失败文件保留为历史。冻结配置与研究源码/测试/旧正式结果未改动。

## 2026-09-20：统一来源冲突规则落实

- 归档用户规则 docs/USER_SOURCE_CONFLICT_RULES.txt，更新 Wei 公式审计和 SOURCE_AUDIT。
- 参数注册表新增 cost_boundary、source_conflict_status，共21列19行。1 USD/STB 为 OPEX_ONLY；0.25 不参与正式计算。
- 检查 src/economics.py：投资时直接扣除 CAPEX；src 无 CRF 调用。公式12保留参考，不擅自修正。
- 公式7/9未实现；继续寻找明确直接成本，不强行完整复刻 Wei。
- 原方法验证结果及求解代码未修改；SOURCE_AUDIT 未通过，正式计算尚未开始。

## 2026-09-20：直接项目成本来源补充与核验

已下载 Lu2025 同项目捕集端全文XML（125091字节），保存DOI匹配与表12/16/17摘录；发现业主驱油封存投资披露线索，但未完成原件表格/资产边界核验，不写入正式配置。详情 docs/QILU_DIRECT_COST_FOLLOWUP.md。

验证：注册表19行21列；两新增字段枚举、fluid pumping=1.0及冲突标记通过。冻结配置SHA256保持3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76；git diff确认src、tests和原配置无修改。本轮仅审计与记录，不运行无关求解测试。

当前必须用户决定：依据此前齐鲁—胜利决定第10节，统一经济折现率8%或12%不能自行选择；两者均应透明标记MODEL_ASSUMPTION。30年不改。停止记录 source_audit/STOP_FOR_USER_DECISION_discount_rate.json；此暂停不是未使用Wei公式导致的Gate失败。正式source-backed配置、12288行数据、33代理目标、61边界V2仍未执行。

## 2026-09-20 决策006：FORMAL UNIFIED DISCOUNT RATE DECISION — 8%

完整授权见 docs/USER_UNIFIED_DISCOUNT_DECISION.txt。simulation.economic_discount_rate=0.08，MODEL_ASSUMPTION；所有主体、模式、commit-now、边界和代理目标统一 gamma=1/1.08。30年继续保留。决策依据为 integrated CCUS system scope consistency，不是为提高NPV。Wei12%保留REFERENCE_ONLY_CO2_EOR，Yuan10%保留REFERENCE_ONLY_COAL_CCUS；不平均、不做折现率敏感性分析。

IEA2020网页检索确认8%/30年，但其具体适用段落为制氢成本比较，不能表述为所有CCUS实际融资率或全链统一寿命。继续取得原始PDF定位页码。历史 STOP_FOR_USER_DECISION_discount_rate.json 由本授权取代，保留审计轨迹；SOURCE_AUDIT仍未通过。

### IEA与官方碳价入口核验结果

S15：IEA2020官方PDF已下载（14417258字节，SHA256 98357d3403375b2aa2f25dc061c3fce39b03719d65d6d6f155962802435aa187）。PDF第75页/印刷第74页图2.14注释经文字及页面图像核验，明确8%与30年；其范围是不同制氢路线成本比较。两个正式参数登记MODEL_ASSUMPTION、Grade A基准，不宣称实测融资成本。

上海环交所每日概况官方目录已保存。2021年目录提供历史分页；本轮2026年目录响应PublishDate为2026-08-14，未覆盖校准日。不能将该目录完整性或第三方收盘数据当作官方完整序列。尚未生成P0/mu/sigma或填补任何缺失数据。

## 当前阶段核查与研究设计停止点

注册表22行21列，8%、30年、Wei12%/Yuan10%参照行及枚举检查通过；旧配置哈希未变。IEA PDF页面证据已保存。

新发现的映射问题详见 docs/EOR_FLOW_MAPPING_AUDIT.md：现有模型xi表示EOR与独立封存两条互斥流量的分配，不能从EOR伴生封存事实直接推出xi=.20或1。前者缺经验依据，后者会使独立封存议价/补贴通道恒零。按新规范第3/7节及用户禁止擅改模型/参数要求，暂停依赖该值的正式校准并请用户决定。折现率问题不再询问。其余来源审核尚未全部完成，任何单项决定不等于总Gate通过。

## Stylized downstream CO2 routing versus EOR-associated storage

用户决策007：保留xi=0.20及现有双流结构，MODEL_ASSUMPTION；完整授权见 docs/USER_DOWNSTREAM_ROUTING_DECISION.txt。其含义为 baseline routing share of captured CO2 allocated to the CO2-utilization/EOR commercial route, with the remainder allocated to a dedicated geological-storage route。20/80是本研究结构假设，不是齐鲁—胜利实测分流、物理利用效率、EOR封存率或全国统计比例。

q_u是EOR路径，q_s是独立地质封存路径，实际Q=q_u+q_s。EOR-associated storage is embedded in the reduced-form abatement/value treatment and is not counted as a second physical flow。eta是reduced-form effective net-abatement proxy，统一表示捕集链残余排放及两路净减排效应；其数值仍须单独审计。

storage_subsidy仅用于q_s，是独立封存政策工具；TRANSFER的storage-service bargaining也仅用于q_s。q_u仅参与CO2销售议价与EOR经济活动。JV/SOE公式保持原样，交易未匹配时实际流量仍按原逻辑处理。齐鲁—胜利仅为物理源汇、EOR路线、运输距离及EOR技术经济证据锚点。

正确论文表述：A baseline routing share of 20% is assumed for the utilization/EOR pathway, while the remaining 80% is assigned to a dedicated geological-storage pathway. This split is a structural model assumption rather than an observed feature of the Qilu–Shengli project.

历史STOP_FOR_USER_DECISION_utilization_fraction.json已由本授权解决，保留历史文件供追溯。该假设不导致来源Gate失败；继续其余来源审计，不改变求解器、状态、流量、议价或补贴公式。

## 2026-09-20：双流决定、完整测试及新增原始证据

新增tests/test_downstream_routing.py五个测试案例：三模式0.10+0.40=.50；无独立封存时EOR不触发storage支付/补贴；独立封存费用转移及补贴仅按.40计入。重点核算测试10项通过，完整pytest58项通过（8.01秒）。未改src或冻结配置，也未覆写旧formal结果。

S13业主债券报告已下载并视觉核验表4.3/4.4及后页，解决先前访问限制。总投资3.4115/10.63亿元及年度能力披露保留为文献参照，不冒充匹配本模型的CAPEX。注册表现26行21列。

官方碳价目录采集58页（请求均成功），发现863个唯一日报URL：2021年114，2022–2025各150，2026年149，最近2026-08-14。页数/覆盖不足以证明完整历史序列；仅保存检索目录，未填补、平滑或校准。目录和哈希见routing_followup/carbon_catalog/catalog_manifest.json。

当前需要研究决定为U CAPEX资产范围及跨容量映射（详见docs/U_CAPEX_MAPPING_DECISION.md）。工程总投资不能自动按Q_bar或xi缩放，亦不代表独立封存渠道投资为零。根据新规范第3节第3项停止依赖该参数的正式实现；本停止点不是对已授权xi=.20重新提问。

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


## 2026-09-20：U CAPEX实现验证、运输原文闭环及后续审计

完整pytest已由此前58项扩为78项并全部通过（2.58秒）：U CAPEX新增17项，运输资源成本核算新增3项。此前新增CAPEX测试曾因Windows默认编码读JSON失败，显式UTF-8后完整75项通过；随后新增运输测试的最新完整结果为78项。测试在隔离配置下验证已批准值，不代表尚未完成的source-backed正式运行。三模式资本支付、乘数、xi独立性、不可逆单次投资、运输/封存成本独立性以及内部运输支付抵消均通过。

冻结model_config.game.json SHA256仍为3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76。对照results/resume_before_1d8388dd.json，旧formal的257个文件逐一哈希一致。未改动态求解器；验证摘要见post_u_capex/validation.json。

S03出版商HTML原文表2确认：设备0.2163、维护0.0319、电力0.0102，合计0.2584 CNY/(tCO2 km)，因此cost_boundary=LEVELIZED_CAPEX_PLUS_OPEX。原情景为20年、8%、2022价格、250km和60万吨/年。按既有用户授权登记0.2584×109=28.1656 CNY/tCO2，DERIVED_FROM_EMPIRICAL；这是有情景条件的文献成本基准，不是实测纯OPEX或统一收费。源模型压缩站及电力已计入；最终捕集压缩资产仍需核对重叠。没有额外新增T资本支出，125仍为内部支付MODEL_ASSUMPTION。注册表现31行21列，已批准输入集合更新，完整正式配置仍未生成。

S08 Li2022第4节及表2–7、S09 Miao2025第3节及表1–3已从出版商HTML读取并保存原文摘录；未宣称取得PDF。Li规划15年新捕集10.68 Mt、增量油2.97 Mt，油量/CO2分母及固定费、回收再注入量必须统一；旧780及94.1654不沿用。Miao净减排核算不包含采出油后续燃烧，不把其CROI或净减排总量自动写成eta。

S01正确书目链接https://academic.oup.com/ce/article/9/4/15/8071291已确认，浏览器仍连接超时，不能声称核实450 million CNY。官方行情查询页https://shyx.cneeex.com/qdata.html?1785740461457可读，2026-09-18综合价格行情收盘95.63元/吨；该单日快照已存档。历史目录至8月14日不代表数据终点，未把不完整目录校准成GBM，也未自动拼接不同价格定义。

新研究停止点：EOR固定O&M及年际变化如何跨容量映射到本模型恒定成本参数。详见docs/EOR_OPERATING_COST_MAPPING_DECISION.md；依据新规范第3节第3/8项，不擅自将固定费吨均化或缩放。建议生命周期累计EOR运营费用/累计新CO2映射，须用户审定其成本发生方式。PIPELINE_EXCLUDED及U CAPEX无需重新决定。来源Gate未通过，正式12288行、33代理目标和61项V2尚未启动。


## 2026-09-20 决策010：EOR两部制生命周期映射

用户原文归档docs/USER_EOR_TWO_PART_OPEX_DECISION.txt。全成本吨均化提案明确不采用；历史STOP_FOR_USER_DECISION_eor_opex_mapping.json已由本授权解决。固定EOR年费按基准fresh支路能力缩放，并在x_U=1后每年发生，包括q_u=0；只有变动费生命周期吨均化后乘q_u。基准缩放冻结后xi变化不自动改固定费。总U固定费仍待独立封存/共享成本审计，不提前填零。

新增docs/EOR_OPEX_COMPONENT_CROSSWALK.md和source_audit/eor_opex_component_crosswalk.csv（24行，12必需字段）。Li2022为主；Miao重复组件不相加。式3已核实资本、固定运营、变动运营和税分列。10.68Mt可作为累计fresh分母，平均0.712Mt/年，对0.10Mt/年模型基准的缩放因子0.1404494382022472。费用仍缺完整井设施计费基数及2019美元到人民币的来源核验；不套用Miao三项条件合计，不使用当前汇率或通胀升级。

src/eor_cost_calibration.py实现独立两部制函数；新增19测试覆盖成本发生、零流量负担、xi冻结、回收只入成本、资本/其他路径排除及Li/Miao去重。完整pytest97 passed in2.48s。所有合成测试值仅为验证，不进入正式参数。新增6条Li文献模型输入注册记录，当前37行21列；正式EOR fixed component和unit cost仍不填猜测值。

新停止点为Fig5年度原始数值可得性：出版商图像已视觉核对，15年四条曲线双轴无逐点标签；表格引用图5，数据声明Data will be made available on request。文字累计油吨数不能直接替代逐年桶数。图像数字化需要承认估读误差并获得研究授权；没有擅自估点、调整曲线满足合计或联系作者。详见STOP_FOR_USER_DECISION_eor_annual_data.json。两部制规则和U CAPEX均不再询问，GATE_SOURCE_AUDIT未通过，正式12288行未启动。


## 2026-09-20 决策011：最小必要图像数字化

授权归档docs/USER_LI_FIG5_DIGITIZATION_DECISION.txt。纠正先前“必须完整15年路径”的前提：线性变动费只依赖累计F/R/B；F=10.68Mt来自正文，fixed缩放不依赖图形。出版商高分辨率原JPEG已下载1712×954/278131bytes，并记录SHA256、日期和URL。

完成右轴15个油产量marker坐标、逐点上下界及累计值，约20.8million bbl；不采用无来源桶吨换算、不向2.97Mt强制校正。回收曲线第11年完全被绿色marker遮挡，替代注入曲线第5年也遮挡中心，未推断隐藏点或插值。触发本次决定第22节C/E，新STOP仅为遮挡点处置，不重新询问数字化授权。

输出位于source_audit/li_fig5_digitization/，包括原图、metadata、points、uncertainty、totals及LI_FIG5_DIGITIZATION_AUDIT.md。R_total/正式费用尚未生成；新增轴转换和累计费用函数及9项测试，完整106项通过（2.20秒）。两部制固定费用仍需井设施基数/货币口径等来源审计，总SOURCE_AUDIT_GATE未通过，12288行未启动。


## 2026-09-20 决策012：固定4:1 EOR收益映射

归档docs/USER_EOR_FIXED_RATIO_DECISION.txt；正式ratio=4.0 t fresh CO2/t incremental oil，MODEL_ASSUMPTION。新校准函数实现Q_oil=q_u/4及P_o=P_oil(CNY/t-oil)/4。现有求解器q_u为Mt/年，吨制接口显式×1e6，基准25,000t-oil/年；B_u=P_o-c_u公式不变。已批准输入集合增加ratio，未填未经审计的正式油价或P_o。

Fig5油曲线/正文2.97Mt退出正式收益校准，旧文件不删除；新classification.json单独记录用途变化。两部制成本不变，R_total仍进入回收和再注入电耗，不设0、不以4:1消去。剩余遮挡停止点按本次第12节改为EOR_OPEX_DATA_GAP，收益图像依赖已解除。详见docs/EOR_FIXED_RATIO_REVENUE_AUDIT.md及STOP_FOR_USER_DECISION_eor_opex_data_gap.json。

新增9项收益测试，完整115项通过（7.60秒）。原Outcome包含NaN导致初始相等断言失败，修复测试比较方式后通过；没有求解器改动。原formal257文件及冻结config哈希复核一致。Source audit仍未通过，12288行未启动。


## 2026-09-20 决策013：固定回收比rho_R=1.0

归档docs/USER_EOR_RECYCLE_RATIO_DECISION.txt；fixed lifecycle-average回收比1.0为MODEL_ASSUMPTION，写入approved inputs。R=q_u、I=2q_u仅内部处理工作量，不增交易/碳收益/外运/产油，4:1收益不变。所有LiCO2精细数字化终止，历史文件保留并由新classification标为REFERENCE_ONLY_NOT_USED_IN_FORMAL_RECYCLE_CALIBRATION。原Fig5回收点OPEX数据停止解除。

MIT原报告PDF及Abuov2022全文XML已下载/核验：MIT PDF41/印刷37节3.4.4参照1.1，Abuov gross15.77/net7.96/recycle7.81，均只为文献支持，不改正式1.0。20.4+38=58.4kWh/t fresh，×0.085=4.964USD/t为CO2电费分量，不是完整OPEX。国家统计局2019汇率6.8985检索核验，未做价格年通胀升级。

新增11案例，完整126项通过（2.57秒），旧formal257文件及冻结config哈希一致。动态求解器未修改。

新停止项：Li表4/5的新井、逐井维护费的资本基数不明确，不能自动采用Miao整项资本百分比合计。条件整项计算10.9536million USD/year尚未采用；详见docs/EOR_RECYCLE_RATIO_AUDIT.md。需审定是否允许整项资本代理基数。Source audit未通过，完整正式费用/12288行未启动。


## 2026-09-21 决策014：正式 EOR 简化成本（覆盖此前两部制映射）

正式 c_u=15×6.8974=103.461 CNY/t fresh CO2，MODEL_ASSUMPTION、A-，以 Guo et al. (2020), DOI 10.1016/j.petrol.2019.106720 的 O&M benchmark 为依据。国家统计局2020统计公报已独立核实汇率6.8974；Guo表1的15目前来自用户明确决定，独立表格核验继续。该来源的注入量口径迁移到本模型 fresh CO2 分母属于明确的模型假设，不是齐鲁观测。

EOR-specific fixed OPEX=0；Li/Miao逐井维护费、10.9536 million USD/year和4.964 USD/t电费均不叠加。rho=1仅保留技术工作量解释，4:1收益不变。q_u为Mt时，q_u×103.461直接得到million CNY。共享U CAPEX、运输和q_s储存成本独立计费；EOR固定分量为0不代表未经审计的其他平台费用已被确定。

Li/Miao组件表及历史工具保留为REFERENCE_ONLY_NOT_USED_IN_FORMAL_EOR_OPEX。解除EOR_FIXED_MAINTENANCE_BASE及相关井资本基数/固定费聚合停止项。今后标量来源优先直接代表值，不为设备级拆分停工；仅按本次用户决定第15节A–D及原规范Gate失败规则停下询问。SOURCE_AUDIT仍在进行，未冻结正式配置或启动12288行。

决策014验证：完整137项测试通过（8.37秒）；原formal257文件及冻结配置哈希不变。NBS2020汇率已核验，Guo原文HTTP403/浏览器读取超时，15 USD/t表格独立核验状态诚实保留待完成，不重新询问用户已批准的标量选择。

继续审计发现：泰州政府2025-12-07正式报道总投资3.85亿元，形成385 million CNY捕集项目资本候选，尚未写入正式输入；不是沿用未经核实的450。Carbon Neutrality原文明确240为建设期预期运营成本，可作为标量OPEX benchmark，不能称已实现实测成本。待核验项仍含油价、净减排比例、储存成本口径和完整官方碳价序列。证据及验证结果见source_audit/eor_reduced_form/。


## 2026-09-21 Guo原文独立核验完成及归因更正

出版商全文表1确认h=15 USD/tCO2，式2.9支持源端新鲜捕集量对应注入量，脚注7说明CO2回收费用包含在EOR运营费中。式2.7另列固定F，式2.8因其在原文运营优化中恒定而删除。当前模型存在投资进入决策，不能以该代数处理证明固定费为零。严格保留用户批准的103.461及EOR fixed=0，但后者明确标记为用户简化假设，不声称所有固定费被原文h覆盖。此前原文访问阻塞已解除；没有更改算法或增加工程拆分。证据：source_audit/eor_reduced_form/guo_original_verification.md。


## 2026-09-21 剩余标量校准推进

按最新简化原则与原规范第9/10节，将capture OPEX=240（MODEL_ASSUMPTION；Carbon Neutrality节3.2.4建设期预期运营成本）及eta=0.70（DERIVED_FROM_EMPIRICAL；Dong等JCP2025 DOI10.1016/j.jclepro.2024.144557出版商highlight约30%衍生排放抵消）加入已批准输入。eta仅reduced-form代理，不是ETS核证比例。Crossref确认卷486/144557；不是误用捕集率。两项均无需工程重建。未采用208总成本叠加。官方碳价分页缺口已定位：第10页以后跳到www.cneeex.com/zcms/ui/catalog/...动态页面，原先只抓静态目录不能说明完整性。


## 2026-09-21 NETL捕集资本原件核验

已下载并逐页定位NETL托管Tao2023报告，第9页图像核验右侧泰州50万吨/年Investment RMB385Million。正式已批准输入增加C CAPEX=385 million CNY，EMPIRICAL/A；同容量，无外推。同页总成本约30USD/t仅参考，不叠加240运营成本。PDF哈希及图像保存在scalar_followup/netl_verification.json、netl_page9.png。原冻结配置未修改。

官方COMCEA逐日接口恢复下载，已落盘响应复用。部分code401对应法定休市日，须与官方holiday表逐项核对，不能将其直接当网络失败或缺失交易日。完整性审计尚未完成，未校准GBM或启动正式数据集。


## 2026-09-21 注入成本标量与GBM实现

按规范第13节及最新标量校准原则，Engineering2024原文other CCUS注入成本50–60取中点55CNY/t，进入q_s流量成本。55仅injection-cost proxy，不宣称全国full-chain成本；原文未分资本/运营，registry的OPEX_ONLY明确为本模型会计归属，不是文献已证明的工程拆分。不另造storage CAPEX或资本回收费。

新增src/carbon_calibration.py按日历时间实现指定GBM公式，无平滑、裁剪或补价。新增7项公式/输入测试，完整144项通过（9.90s）。完整性审计工具在逐日下载未齐时拒绝导出校准。当前INCOMPLETE是采集过程状态，不是已提交正式Gate失败；正式GBM尚未生成。


## 2026-09-21 正式油价单位闭环

依据用户最新标量来源优先级，Wei2015中国陆上EOR的90USD/bbl代表值优先于另选单一年份业主实测价格。中国石化2020 SEC原始披露CONVERSION段确认国产原油7.1bbl/t（非炼油7.35）；NBS2020FX6.8974，得到4407.43860CNY/t-oil，除用户固定4得到1101.85965CNY/t fresh CO2。整个跨年份代表值映射标MODEL_ASSUMPTION，不声称统一实测价格年，不做未授权通胀升级，不是当前市场价。1902为2020部门实现价格，2029为外部销售价格，口径不同且受疫情价格下跌影响，仅参考。正式收益不依赖Fig5。证据哈希见scalar_followup/oil_revenue_verification.json。


## 2026-09-21 GATE_SOURCE_AUDIT PASS

官方1257条收盘价覆盖2021-07-16至2026-09-18，1351个工作日请求中的94日由官方休市表解释；2025-10-13 API缺项用同交易所公告原值57.15补齐来源，不插值。未解决日期0。P0=95.63，mu=0.16886265073995846，sigma=0.3106155387941257，CSV SHA256=a5e60f21e0c065a4c3ef361274c7dfbc8a8d1664ee133cad979286462494000e。三个规定校准产物已生成。来源Gate PASS，新增model_config.source_backed.json，原game配置及formal257文件不动。下一阶段仍须新增COMMIT_NOW、同步诊断、BoundaryV2代码/测试和正式代码冻结；12288行未启动，不声称全流程完成。


## 2026-09-21 source-profile实现预检STOP

新增COMMIT_NOW、同步前向统计、1001点exact BoundaryV2函数及测试；默认配置159passed（2.50s），新source配置相关19passed（0.83s）。尚未完成主入口/正式代码冻结。

TRANSFER在carbon_scale=6.25触发STATIC_ACCOUNTING_FAILURE=2.3283064365386963e-10>1e-10。误差恰为当前利润规模的1ULP；只读诊断math.fsum两边均1708392.8310323984、差0。尚未修改浮点实现或阈值，按用户Gate失败停止规则暂停后续流程，请用户决定是否只修复静态会计求和。详见SOURCE_PROFILE_PREFLIGHT_STOP.md和source_audit/static_accounting_endpoint_failure.json。正式12288行、33代理与61V2搜索未执行。


## 2026-09-22 授权fsum最小修复及再次预检

经济静态账相关多项求和改math.fsum，保留所有项及符号、乘法/议价/均衡/动态算法、参数、域和严格1e-10阈值。两个回归覆盖原聚合案例及主体利润求和案例；完整161passed（2.32s），source相关21passed（0.74s）。基准、下端点三模式均通过；TRANSFER上端点通过，max static error7.275957614183426e-12。

JV上端点仍FAIL：pool与application分别舍入再fsum为1708392.8310323982，直接资源账fsum为1708392.8310323984，差2.3283064365386963e-10。不同于原案例，已用fsum仍非0，未按授权条件豁免。已停止，待确认是否允许进一步处理JV中间金额舍入；正式12288行、代理、BoundaryV2未启动。详情FSUM_REPAIR_PREFLIGHT_STOP_20260922.md及source_audit/fsum_full_preflight_20260922.json。


## 2026-09-22 用户批准静态会计100元绝对误差预算

用户明确“不超过100元忽略”。source-backed静态会计预算统一为error<=100/1e6=0.0001million CNY，阶段计算和dataset完整性验证共用同一函数。保留math.fsum及实际误差，不修改利润、参数、设计域、动态/概率/代理阈值。method-validation仍严格<1e-10。新增99/100/超过100元及非有限值/负值测试。

完整170项通过（2.30s）；source基准与carbon_scale上下端点共9案例全部通过，含dataset.validate_rows。最大静态差额0.00023283064365386963元，未清零；最大动态误差1.4551915228366852e-11，仍满足原1e-8。source相关30项通过。此前静态Gate STOP由本决策解除，正式12288行尚未启动，仍需完成主入口及代码冻结等规定步骤。


## 2026-09-22 正式入口完成，准备冻结

新增run_source_backed_protocol.py，来源/官方序列重算验证、独立source配置、COMMIT_NOW9个目标、同步诊断、exact数据、33代理目标、61项1001点exact边界及哈希resume串联完成。172tests通过（2.52s），compileall通过。正式代理保持既定HGB和划分/阈值；commit-now使用价值类0.98/0.05门槛。新增边界与同步定义文档；阶段动作概率质量为30年累计量，不误称路径概率。原formal及全部来源原件保留本地，生成产物由哈希manifest审计，不上传。下一步本地Git冻结后启动正式入口。


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 71cbebb3adbb1eb8a3e1cb0869e4d29a68a635feaac5645fc080e2895029a2f6.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash 6b903a16d9b14553e24c6f5fdd8162aa90e646914e857a6767b8bd315ab42484.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash db70a6a502a5159e1d881d4dc7a5dd7f321e519c70fe1fe376a906653996505d.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 8c62e76bc4010b0cc44aaf98727ae1f5125ee69df763bf3ff4aecbf3abad133c.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 0011035b9838610066b5b04e5d4fb7de66e4ce83509ba5aed8bf74a9eb99f512.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash c9864468cdfc8707c7ac2334af3f550de3202dd489678b1730f380603263204c.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash d13567452d3cb19510d94d8b9dfea99732b2235b2b84fce01c0d510f9246e196.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash 959487405c0e78a95fd1bd6bc8fe8a203e92582b02f26f61ae93d0e6d1bf845a.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash 2cd0ae2522ff738f5bc2fad23cde0c6e9947acf435dab021240d6860a5063e40.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash 7fcd9f64996f185adc0f4a03f0fd7df0334ee39ac221906135aeab868858a90f.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 864925d8411b9c0fc4c3a1ea8d6e933384872e1f0281f36fe00811806451dfea.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 56228a3008169596dca13aaf0e4733fa4129e3b5664cb549c8e31ae12bba5580.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash ee69223c88a80add1f246e6383296dfccf4a3f05e813bbdd27c39e21e64481cd.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash 7c808258a9b16ae24b4db9ba7c9e2ea448628b4749a0999a2a4c4e8ad1690737.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 4f310d3eac663d8f72e4bd8115792920af816c46382271869820bc8e7d452340.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 35d1f52a43278a0f83a0c8d00d2b779f47c0fcf9d3bde89779e9a9fcd976ce8a.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash 53ed8ff461175bc5f3e652234eedbdf5a0753db71671e3c631275e27c556bbfe.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 7fd7804dc090ceb8adbb1856b2dc9820827a2bac3060d5999f5dd9145097127f.


## 2026-09-22 正式基准与冻结Gate通过

Git冻结bc0d0fe4d2fff35a32caae1e74f87e1ea74f0786；SOURCE_AUDIT、CARBON_CALIBRATION、CONFIG_FREEZE、BASELINE及SYNCHRONIZATION_DIAGNOSTIC Gate均PASS。正式启动前172tests及source30tests通过。基准单位million CNY：

         mode  system_npv  commit_now_system_npv  invest_prob_C  invest_prob_U
     TRANSFER 3885.186380            3871.460794       0.853660       0.853660
JOINT_VENTURE 3894.578561            3324.675920       0.930814       0.934506
  STATE_OWNED 3896.293879            3324.675920       0.918044       0.918044

基准同步判定TRANSFER=true、JV=false、SOE=true；仅为基准，最终全样本判定在exact完成后计算。JV的C/U投资概率差非零，未为制造差异改模型。所有正式结果写source_backed_formal，旧formal未复用。


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash 9021459435a76a89262b11d06c4d0b7321d20865407073ad9ea516ba46ee8898.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 6e6b07df71540f5c3a8d9dc967fa2d96f259a4b78e6a6f504915d7b865d090e9.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash e881eb792194be550ec599a86d52b9a0e5351ce70fb479739c6bc371c3182046.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 502dfb52476f4d05136c11bea18a2e8d20b15d89d66529b617b00b49f0590eb4.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash c421d0396ca92c7ae5b5752e581ccddb4789c9a43d23cfd2ae78bda5b7a78372.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 5d8d6a72aef8511ff96b45990570bfbc1462355d1995cca63a1e13ec4701ac2c.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 621c481ac4bf932b0aacf17797fad1c6505279eb6033401515fc1406aa52d943.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 805737bfd10da17b6acc32a9c5798dd255b0d2c210ddc79536046f8545491868.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash c87f3a0a4c8ff72368e9cf6d8749e864098084a5cbda04c9e106c37e96c7bdb6.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash d0a200e49291fafc84e0e2ac15c513f4dfa354608a7f89cfb720ba9773c16062.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 4be1af8424d0204fa9dd04d906903cc27b1fb1b17cd49d001991c34f4db7974d.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash a3fc6f51afdf996caa917e3dca6e70eb6bab16f6a384d463a054a20d9ca82d3a.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 92d14eb5adc6f18aae17aac6266cb91ac1eef670d0d9594ec3246f8ebdb953a6.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 8101471fb919c382ba3de3e9342cf0cca14698c1cc0d49dd8e5086091a1f2c23.


## 2026-09-22 正式exact与代理Gate通过

4096×3=12288行完成，solver_failures=0，EXACT_DATASET_GATE及EXACT_INTEGRITY_GATE PASS。全样本最大静态误差0.00023283064365386963CNY，最大动态误差7.275957614183427e-11，最大概率质量误差4.440892098500625e-16。33/33代理目标通过固定门槛：TRANSFER14、JV13、SOE6；未调参、裁剪或删target。

全样本同步TRANSFER=true、JV=false、SOE=true。JV最大投资概率差0.010815727580516077、最大条件投资年差2.258908099821208；均按原公式报告。已进入61项1001点exact-first BoundaryV2，边界结果尚待完成。


Exact checkpoint 0000: 128/4096 scenarios; chunk validated, hash 71cbebb3adbb1eb8a3e1cb0869e4d29a68a635feaac5645fc080e2895029a2f6.


Exact checkpoint 0001: 256/4096 scenarios; chunk validated, hash 6b903a16d9b14553e24c6f5fdd8162aa90e646914e857a6767b8bd315ab42484.


Exact checkpoint 0002: 384/4096 scenarios; chunk validated, hash db70a6a502a5159e1d881d4dc7a5dd7f321e519c70fe1fe376a906653996505d.


Exact checkpoint 0003: 512/4096 scenarios; chunk validated, hash 8c62e76bc4010b0cc44aaf98727ae1f5125ee69df763bf3ff4aecbf3abad133c.


Exact checkpoint 0004: 640/4096 scenarios; chunk validated, hash 0011035b9838610066b5b04e5d4fb7de66e4ce83509ba5aed8bf74a9eb99f512.


Exact checkpoint 0005: 768/4096 scenarios; chunk validated, hash c9864468cdfc8707c7ac2334af3f550de3202dd489678b1730f380603263204c.


Exact checkpoint 0006: 896/4096 scenarios; chunk validated, hash d13567452d3cb19510d94d8b9dfea99732b2235b2b84fce01c0d510f9246e196.


Exact checkpoint 0007: 1024/4096 scenarios; chunk validated, hash 959487405c0e78a95fd1bd6bc8fe8a203e92582b02f26f61ae93d0e6d1bf845a.


Exact checkpoint 0008: 1152/4096 scenarios; chunk validated, hash 2cd0ae2522ff738f5bc2fad23cde0c6e9947acf435dab021240d6860a5063e40.


Exact checkpoint 0009: 1280/4096 scenarios; chunk validated, hash 7fcd9f64996f185adc0f4a03f0fd7df0334ee39ac221906135aeab868858a90f.


Exact checkpoint 0010: 1408/4096 scenarios; chunk validated, hash 864925d8411b9c0fc4c3a1ea8d6e933384872e1f0281f36fe00811806451dfea.


Exact checkpoint 0011: 1536/4096 scenarios; chunk validated, hash 56228a3008169596dca13aaf0e4733fa4129e3b5664cb549c8e31ae12bba5580.


Exact checkpoint 0012: 1664/4096 scenarios; chunk validated, hash ee69223c88a80add1f246e6383296dfccf4a3f05e813bbdd27c39e21e64481cd.


Exact checkpoint 0013: 1792/4096 scenarios; chunk validated, hash 7c808258a9b16ae24b4db9ba7c9e2ea448628b4749a0999a2a4c4e8ad1690737.


Exact checkpoint 0014: 1920/4096 scenarios; chunk validated, hash 4f310d3eac663d8f72e4bd8115792920af816c46382271869820bc8e7d452340.


Exact checkpoint 0015: 2048/4096 scenarios; chunk validated, hash 35d1f52a43278a0f83a0c8d00d2b779f47c0fcf9d3bde89779e9a9fcd976ce8a.


Exact checkpoint 0016: 2176/4096 scenarios; chunk validated, hash 53ed8ff461175bc5f3e652234eedbdf5a0753db71671e3c631275e27c556bbfe.


Exact checkpoint 0017: 2304/4096 scenarios; chunk validated, hash 7fd7804dc090ceb8adbb1856b2dc9820827a2bac3060d5999f5dd9145097127f.


Exact checkpoint 0018: 2432/4096 scenarios; chunk validated, hash 9021459435a76a89262b11d06c4d0b7321d20865407073ad9ea516ba46ee8898.


Exact checkpoint 0019: 2560/4096 scenarios; chunk validated, hash 6e6b07df71540f5c3a8d9dc967fa2d96f259a4b78e6a6f504915d7b865d090e9.


Exact checkpoint 0020: 2688/4096 scenarios; chunk validated, hash e881eb792194be550ec599a86d52b9a0e5351ce70fb479739c6bc371c3182046.


Exact checkpoint 0021: 2816/4096 scenarios; chunk validated, hash 502dfb52476f4d05136c11bea18a2e8d20b15d89d66529b617b00b49f0590eb4.


Exact checkpoint 0022: 2944/4096 scenarios; chunk validated, hash c421d0396ca92c7ae5b5752e581ccddb4789c9a43d23cfd2ae78bda5b7a78372.


Exact checkpoint 0023: 3072/4096 scenarios; chunk validated, hash 5d8d6a72aef8511ff96b45990570bfbc1462355d1995cca63a1e13ec4701ac2c.


Exact checkpoint 0024: 3200/4096 scenarios; chunk validated, hash 621c481ac4bf932b0aacf17797fad1c6505279eb6033401515fc1406aa52d943.


Exact checkpoint 0025: 3328/4096 scenarios; chunk validated, hash 805737bfd10da17b6acc32a9c5798dd255b0d2c210ddc79536046f8545491868.


Exact checkpoint 0026: 3456/4096 scenarios; chunk validated, hash c87f3a0a4c8ff72368e9cf6d8749e864098084a5cbda04c9e106c37e96c7bdb6.


Exact checkpoint 0027: 3584/4096 scenarios; chunk validated, hash d0a200e49291fafc84e0e2ac15c513f4dfa354608a7f89cfb720ba9773c16062.


Exact checkpoint 0028: 3712/4096 scenarios; chunk validated, hash 4be1af8424d0204fa9dd04d906903cc27b1fb1b17cd49d001991c34f4db7974d.


Exact checkpoint 0029: 3840/4096 scenarios; chunk validated, hash a3fc6f51afdf996caa917e3dca6e70eb6bab16f6a384d463a054a20d9ca82d3a.


Exact checkpoint 0030: 3968/4096 scenarios; chunk validated, hash 92d14eb5adc6f18aae17aac6266cb91ac1eef670d0d9594ec3246f8ebdb953a6.


Exact checkpoint 0031: 4096/4096 scenarios; chunk validated, hash 8101471fb919c382ba3de3e9342cf0cca14698c1cc0d49dd8e5086091a1f2c23.


## 2026-09-22 SOURCE_BACKED_ALL_STAGES_COMPLETED

正式4096情景、12288行、solver failures0；33/33代理通过；61项V2完成，found0、found=false61、jump0、exact-root/level0、multiple-root0。每项均基于规定1001点exact网格，found=false不等于全域不存在边界，不扩大domain。最终完整172tests与source30tests通过。

完整run_source_backed_protocol.py --resume已通过：1862个正式目录产物哈希不变。最终旧formal257文件及原game配置哈希再次一致，旧RL未修改。completion.json=ALL_STAGES_COMPLETED。正式报告results/source_backed_formal/FINAL_EXECUTION_REPORT.md；复现manifest及resume_validation.json均已保存。Git冻结bc0d0fe4d2fff35a32caae1e74f87e1ea74f0786。所有工作仅本地，未上传。

## 2026-09-22 论文结果解释层完成

按正式身份 bc0d0fe4d2fff35a32caae1e74f87e1ea74f0786，仅读取 FINAL_EXECUTION_REPORT、baseline、exact_dataset、同步诊断和 Boundary V2 1001点网格，建立独立 paper_analysis/20260922 层。未修改正式模型、配置、均衡规则、代理设定或 results/source_backed_formal/ 文件。

已生成 PAPER_RESULTS_INTERPRETATION.md、baseline/commit-now/option value 表、JV 同步与参数分位表、61项 Boundary V2 分单位 proximity 排名表，以及3张论文核心图。分析确认：TRANSFER/JV 动态值为所选均衡系统价值，option_value 在联合情景中可为负，不能统称为非负集中式最优期权；baseline JV 非同步为 U-only 第20年先建、C-only 第21/23/26年跟随。碳价尺度和 U CAPEX 是 JV 非同步质量的主要描述性关联变量，transport_market_price 在既定域内关联接近零。

分析输入哈希、正式目录前后快照和 4096情景/12288行/61边界/18个1001点网格审计保存于 paper_analysis/20260922/audit。分析脚本在运行前验证 reproducibility manifest、正式配置与 Git 身份，运行后验证正式目录哈希未改变。Boundary proximity 按 NPV、概率和价格分开排名；61个 found=false 仅解释为规定网格和 domain 内未检测到 crossing。
