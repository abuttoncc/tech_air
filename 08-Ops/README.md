# 08-Ops · 陋居自动化层

人做深度学习与全局掌控，「当 X 发生 → 做 Y」的模式化劳动交给受契约约束的 agent（routine）。

| 落点 | 内容 |
|---|---|
| `routines/` | agent 契约（分诊员/答题员/研究员/结构巡检员/编译裁决员/心跳员），契约=trigger/scope/budget/escalation，**改契约=改权限** |
| `runs/` | 无人值守 run 记录 |
| `review/` | 审核队列：高危写入候选卡（pending → approved/rejected） |
| `pulse/` | 今日启发束（心跳员产出，沿跨域 built_on 边走） |
| `审批账本.md` | 信任账本：每类写入 streak/threshold/state + 审计日志 |

**高危写入 gate**：`newnode` / `xedge`(跨域 built_on 边) / `t0-merge` 可连续批准升为自动；`retire` 与 `disputed` 永久人工。
**模式区分**：交互会话当场问用户、裁决即记账；无人值守一律落 `review/` 候选。
