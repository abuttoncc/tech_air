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

## 与 bin/structure-lint.sh 的关系

- `bin/structure-lint.sh`：轻量、纯确定性，launchd 每周一拉起做健康巡检。
- `graph/`：完整决策回路（含 research + 人审 + 候选收口）。lint 节点逻辑与 shell 版一致，但多了缺口补全和人审闸。

**想让 launchd 改拉 graph**：把 plist 的 ProgramArguments 换成
`$PY 08-Ops/graph/run.py start --thread weekly-$(date +%F)` 即可（dry-run 安全；要 live 跑 research 需先验证无头 claude 在 launchd 环境可用）。

## 扩展（下一批节点）

- `answer`（答题员）：扫 07-QA 到期动态问题，每题 recall→复盘→推演→追加答案。
- `pulse`（心跳员）：沿跨域 built_on 边走，产今日启发束 → `08-Ops/pulse/{date}.md`。
- `digest`（分诊员）：扫 Inbox 未消化散文分诊。

都按同样范式接：确定性的进工具节点，要推理的进 LLM 节点（壳调 claude），写正典的一律过 `gate` 人审。
