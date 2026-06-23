---
description: 驱动决策平台 LangGraph（08-Ops/graph）—— 跑/审批/查健康，由智能体管理
argument-hint: run [--live] | approve <thread> [--reject] | show <thread> | health | status
---

把 `08-Ops/graph/` 的 LangGraph 决策平台交给你（智能体）来管理。**自动化只走两种形态：确定性程序（图的工具节点）或 LLM 调用（图的 research 节点壳调 claude）——不碰 OS cron/shell 那套。**

统一用 `PY=/opt/homebrew/opt/python@3.12/bin/python3.12`，工作目录 `08-Ops/graph/`。参数：$ARGUMENTS（缺省 = `status`）。

## 子命令

### run [--live]
启动一次决策回路：`lint → (非PASS) research → gate人审 → commit候选 → record`。
- 默认 **dry-run**（research 节点不调 claude，只产占位候选），先验证回路。
- 加 `--live` 才真壳调 `claude -p` 跑 research。
- thread 自动生成（`run-<时间戳>`）。
- 跑：`$PY run.py start [--live]`。
- **若返回「⏸ 运行已暂停」**：说明命中 gate 人审（铁律 3：人是最后的闸）。把审批载荷（候选清单）原样转述给用户，等用户裁决，不要自己批。用户说批准/驳回后再走 `approve`。

### approve <thread> [--reject]
恢复被人审中断的运行：`$PY run.py approve --thread <thread>`（驳回加 `--reject`）。
- 批准 → 候选写入 `08-Ops/review/` 队列（`pending-human-merge`，**只投候选不直写正典**）。
- 驳回 → 候选丢弃（按审批账本：一次驳回 streak 清零）。
- 跑完按结果在 `08-Ops/审批账本.md` 的审计日志 append 一行（手动维护那本账）。

### show <thread>
查某次运行的最终状态 + X-Ray 思维链（跨进程从 SQLite 读）：`$PY run.py show --thread <thread>`。

### health
纯程序快查库健康度（只跑确定性 lint，不写状态、不调 LLM）：`$PY run.py health`。
一行摘要：`[wiki health] PASS/WARN/FAIL · pass/fail/holes`。

### status（缺省）
读 `08-Ops/runs/_graph_log.tsv` 末几行 + 跑一次 `health`，汇报：最近几次图运行结果、当前库健康、review 队列里有没有待人工合并的候选（`ls 08-Ops/review/`）。

## 纪律
- **决策不旁路本体**：lint 直接读 `wiki/` + `data.db`。
- **可解释**：每次运行的 X-Ray 轨迹都落 `08-Ops/runs/{date}-graph-{thread}.md`，要追溯直接读。
- **人是闸**：任何写正典的动作必须经 gate 人审；你只转述候选、不替用户拍板。
- 汇报口径：跑了什么、结果、X-Ray 关键几步、有没有待人审/待合并项。git 交给 obsidian-git，不手动 push。
