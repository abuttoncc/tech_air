# 08-Ops/bin —— 无人值守自动化脚本

routine 契约在 `../routines/`，这里放真正被调度器拉起来的可执行脚本。

## 已上线

### structure-lint.sh —— 结构巡检员（lint）
- **干什么**：跑 `schema.py`（断链/越界边/frontmatter）+ `expand.py --scan`（结构空洞），逐域校验全库本体。
- **kind: tool / 纯代码无大脑**：确定性，零 LLM、零 API 成本、零 MCP 依赖。**只产报告不写本体**（最安全）。
- **产出**：`08-Ops/runs/{date}-结构巡检.md`（每日一份 run 记录）+ `08-Ops/runs/_log.tsv`（滚动一行一条）。
- **结果**：`PASS`（无失败无真洞）/ `WARN`（有孤儿挂件真洞 → 该派研究员织入边）/ `FAIL`（校验违规 → 人工修）。

## 调度（launchd）

plist：`~/Library/LaunchAgents/com.techair.structure-lint.plist`，**每周一 09:00** 跑一次周期健康巡检。

```bash
# 手动跑一次（不依赖调度器）
bash "08-Ops/bin/structure-lint.sh"

# 立即触发 launchd 任务（验证裸环境能跑）
launchctl start com.techair.structure-lint

# 查看是否已注册
launchctl list | grep techair

# 改了 plist 后重新加载
launchctl unload ~/Library/LaunchAgents/com.techair.structure-lint.plist
launchctl load -w ~/Library/LaunchAgents/com.techair.structure-lint.plist

# 关掉自动化
launchctl unload ~/Library/LaunchAgents/com.techair.structure-lint.plist
```

调度器日志：`08-Ops/runs/_launchd.log`。

## 注意
- 脚本写死了 homebrew python（`/opt/homebrew/opt/python@3.12/bin/python3.12`，pydantic 在此环境）。换 python 环境要同步改 `structure-lint.sh` 顶部的 `PY`。
- launchd 只在 Mac 开机/唤醒时跑；错过的时刻不补跑（设计如此，周期巡检不追时效）。
- 这是第一条上线的 routine（只读、零写入风险）。下一条若涉及写 wiki（答题员/研究员），需走 headless claude + ingest 闸门，且建议先验证 MCP 取数通道在无头环境可用。
