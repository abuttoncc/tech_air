# 08-Ops/graph —— 决策平台 · LangGraph 编排

把 `08-Ops/routines/` 的 routine 编成一张 **LangGraph** 来跑。这是「实现决策平台」骨架的程序化落地：图编排 = LLM 节点 + 确定性工具节点 + 人审中断。

## 图拓扑

```
START → lint ─┬─(PASS)──────────────→ record → END
              └─(WARN/FAIL)→ research → gate → commit → record → END
```

| 节点 | 类型 | 干什么 |
|---|---|---|
| `lint` | 确定性工具 | 跑 `schema.py` 逐域校验 + `expand.py --scan` 扫结构空洞。零 LLM。 |
| `research` | LLM | 针对缺口产候选（**只投候选不写正典**）。壳调 `claude -p`，默认 dry-run 不触发。 |
| `gate` | 人审中断 | `interrupt()` 暂停，等人 approve/reject。**人是最后的闸**。 |
| `commit` | 确定性工具 | 批准的候选写入 `08-Ops/review/` 队列（pending-human-merge）。 |
| `record` | 确定性工具 | 整条 X-Ray 思维链落 `08-Ops/runs/{date}-graph-{run_id}.md`。 |

## 三条铁律怎么落的

1. **决策长在心智模型上** —— `lint` 直接读 `wiki/` 本体 + `data.db`，不旁路。
2. **可解释是信任前提** —— 每个节点往 `state.trace` 追加轨迹，全程落 runs/（X-Ray）。
3. **人是最后的闸** —— `gate` 节点 `interrupt()` 暂停，候选只投 review 队列、不直写正典。

## 用法

```bash
PY=/opt/homebrew/opt/python@3.12/bin/python3.12

# 启动一次运行（默认 dry-run，不调 claude）
$PY run.py start --thread today

# 加 --live 才真的壳调 claude 跑 research 节点
$PY run.py start --thread today --live

# 若在 gate 暂停 → 人审恢复（驳回加 --reject）
$PY run.py approve --thread today
$PY run.py approve --thread today --reject

# 查看某次运行的最终状态 / X-Ray（跨进程，从 SQLite 读）
$PY run.py show --thread today

# 打印图拓扑（mermaid）
$PY run.py graph
```

## 后端与持久化

- **LLM 节点后端**：headless `claude -p`，复用 Claude Code 登录，**无需 ANTHROPIC_API_KEY**。换成 Anthropic API 只需改 `pipeline.py` 的 `_claude()`。
- **持久化**：`SqliteSaver` → `checkpoints.sqlite`。状态可中断、可恢复、可跨进程追溯。比照 `data.db-wal`，checkpoint 是运行态，**不入库**（已 gitignore）。

## 谁来触发：智能体管理，不靠 OS cron

自动化只走两种形态——**确定性程序**（图的工具节点）或 **LLM 调用**（research 节点壳调 claude）——统一收在这张图里，再以两种接口交给智能体管理：

| 接口 | 形态 | 触发时机 | 文件 |
|---|---|---|---|
| **工具** | slash 命令 `/ops` | 智能体/你主动调（run/approve/show/health/status） | `.claude/commands/ops.md` |
| **hook** | SessionStart | 每次开会话自动跑 `health`，把库健康度注入上下文 | `.claude/settings.json` |

- `/ops` 让智能体能驱动整张图（含人审中断的转述与恢复）。
- SessionStart hook 调 `run.py health --json`（纯确定性、不调 LLM、~1.5s），输出 `hookSpecificOutput.additionalContext`，会话一开就知道 wiki 健康。关掉就删 `.claude/settings.json` 里的 SessionStart 块。

## 与 launchd / bin 的关系（已退居冗余）

`bin/structure-lint.sh` + launchd（`com.techair.structure-lint`）是早先的 OS-cron 路径。现在触发已收回到智能体侧（tool + hook），launchd **冗余**，可保留作离线兜底，也可卸载：

```bash
launchctl unload ~/Library/LaunchAgents/com.techair.structure-lint.plist
```

## 扩展（下一批节点）

- `answer`（答题员）：扫 07-QA 到期动态问题，每题 recall→复盘→推演→追加答案。
- `pulse`（心跳员）：沿跨域 built_on 边走，产今日启发束 → `08-Ops/pulse/{date}.md`。
- `digest`（分诊员）：扫 Inbox 未消化散文分诊。

都按同样范式接：确定性的进工具节点，要推理的进 LLM 节点（壳调 claude），写正典的一律过 `gate` 人审。
