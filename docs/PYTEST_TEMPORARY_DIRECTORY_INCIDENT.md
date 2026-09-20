## Pytest Temporary Directory Incident

- 原始错误：Windows default temp PermissionError / WinError 5。
- 原错误发生于两个恢复测试的 tmp_path fixture setup；尚未进入测试断言。
- 在受限执行环境中，项目内目录的第一次最小写入检查也失败；用户随后解除文件系统限制并授权重试。
- 重试 .pytest_tmp 最小写入检查：输出 ok，exit code=0。
- 解决方式：project-local --basetemp=.pytest_tmp；pytest.ini 设置 addopts=-p no:cacheprovider --basetemp=.pytest_tmp，.gitignore 忽略 .pytest_tmp/ 和 .pytest_cache/。
- 分类：TEST_INFRASTRUCTURE_ONLY。未修改 Windows ACL，未启动管理员会话，未修改测试断言、研究参数或 Gate，未 skip/xfail 测试。
- 修复后完整命令：D:/anaconda3/python.exe -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp。
- 完整结果：52 passed in 2.04s，failed=0、errors=0、skipped=0、exit code=0。
- compileall：D:/anaconda3/python.exe -m compileall -q .，exit code=0。
- 项目未提供 .venv/Scripts/python.exe，因此继续使用原先已记录的 Python 3.13.9 环境 D:/anaconda3/python.exe，没有切换依赖版本。
- config SHA256：3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76。
- source_manifest_hash：2d53befd84c4ab357af40aa9c96a6f17ee6c959eb32c4af79196a68d8946eef0。
- 23 个源码文件、12 个测试文件逐一匹配上次中断 manifest，无研究源码或测试变更。
- Git SHA / worktree status：当前目录不是 Git 仓库，命令返回 128，不虚构 Git commit。
- 先前失败记录仍保留供审计；不能将历史失败记录误作本次修复后的测试结果。
