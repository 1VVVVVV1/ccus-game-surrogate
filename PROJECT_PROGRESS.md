# CCUS 项目进程与核查记录

## 当前状态

ALL_STAGES_COMPLETED — 当前源码正式全流程及完整 --resume 均 exit=0；Gate 1–7 全通过，53 tests passed，4096 场景/12288 行/0 求解失败，24/24 代理 target 通过。完整恢复前后全部 257 个正式文件哈希相同。61 项边界搜索完成，未保留精确 crossing（不等于证明经济边界不存在）。最终证据见文末与 results/resume_verification_PASS.json。

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
