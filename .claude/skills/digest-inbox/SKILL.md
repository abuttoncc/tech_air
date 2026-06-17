---
name: digest-inbox
version: 0.1.0
description: |
  收集箱消化编排器：扫 Inbox 未消化的散文，逐篇分诊（结晶 / 参考 / 速朽），
  把结构化碎片编译进 wiki、把耐用散文路由到 PARA 归宿、给每篇打 compiled 标记，
  闭合「Inbox → 编译/归档 → 标记」这一环，让 Inbox 不再当熵的蓄水池。

  触发词：消化inbox、排空inbox、整理收集箱、清收集箱、digest inbox、drain inbox、
  /digest-inbox、消化一下、处理收集箱、归档收集箱。

  本 skill 是编排器，不自己实现 ingest —— 委托 auto-wiki；路由/标记/扫描自理。
  设计原则：检测自动、合并守闸；源文件不移动只打标；ingest 守 auto-wiki 全套纪律。
---

# 收集箱消化 (digest-inbox)

> 用户说「消化 inbox / 排空收集箱」时触发，或被轮询定时器 headless 调起。把 `Inbox/` 里
> **未消化的散文**逐篇跑标准流水线，沉淀进它该去的地方，然后打标，让收集箱回到"空"。

## 核心理念

- **降熵发生在消化那一刻**：Inbox 是高熵进料的隔离区，未消化的 Inbox = 熵的新房间。这个 skill 是那台「泵」——把进料压成低熵存量（wiki 节点 / PARA 归宿），再把进料标记为已处理。
- **双 sink，不是只进 wiki**：一篇散文消化后分三股 —— ①结构化碎片 → `wiki/{domain}/`（委托 auto-wiki ingest）；②耐用散文本身 → PARA 归宿（02-Areas / 03-Resources / 01-Projects / 04-Archive）；③速朽碎片 → 不强行本体化，只抽硬数据。
- **源文件 immutable，不移动只打标**：移动文件会断 wikilink 与溯源链。消化完只在 frontmatter 写 `compiled: true` / `digested` / `sinks` / `triage`，文件留在原地（除非用户显式要求归档到 04-Archive）。"已消化 vs 未消化"靠标记区分，不靠文件夹位置。
- **检测自动、合并守闸**：扫描/分诊/备草稿可以自动；但**写进 wiki 的那一步走 auto-wiki 全套纪律**（schema 校验 / 退役不删除 / 不编造），冲突项浮给人工。绝不盲目 auto-merge 污染低熵存量。
- **幂等可重跑**：已 `compiled: true` 且 `updated ≤ digested` 的跳过（对齐 SHA256-skip 思想，用 mtime/updated 近似）；笔记被改过（`updated > digested`）才重新消化。

## 执行流程

### Step 0 — 扫描与判定待消化
- 列 `Inbox/*.md`，**排除** `README.md`、`plan.md`，以及 frontmatter `type: capture` 的。
- **待消化判据**：缺 `compiled: true` —— 或 —— `updated` 晚于 `digested`（改过）。
- 读每篇 frontmatter（`tags` / `type` / `status` / `topic` / `wiki-topic` / `created` / `updated`）+ 正文要点。
- **先把待消化清单 + 各自 created 年龄报给用户**（被定时器调起时写进 digest 日志），再动手。

### Step 1 — 逐篇分诊（这是补上的关键裁判）
给每篇定一个 `triage`，决定它怎么消化：

| triage | 判据 | 怎么处理 |
|---|---|---|
| **crystallize** | 含耐用、可结构化的知识（机制/实体/指标/事件/关系），通常 `wiki-topic` 已填或可定 | ①auto-wiki ingest 进 wiki ②耐用散文路由到 PARA ③打标 |
| **reference** | 耐用散文但不是本体料（话术底稿 / 清单 / 资源整理 / 研判稿） | 只路由到 PARA（03-Resources / 02-Areas / 01-Projects），不 ingest wiki；打标 |
| **ephemeral** | 盘中即时思考 / 当日速记 / 高时效低沉淀 | **只抽硬数据**（数值→data.db、事件→events，经 auto-wiki），其余不强行本体化；打 `triage: ephemeral`，留 Inbox 或经确认移 04-Archive |

> 分诊存疑时（耐用 or 速朽分不清）→ 默认 `reference`（保住散文、不污染 wiki），并在汇报里标"待人工复核 triage"。

### Step 2 — crystallize：编译进 wiki（委托 auto-wiki）
1. **路由到域**：先读 `wiki/_index.md` 注册表，按关键词把材料命中到域（横跨多域则双写 + 跨域 `drives`/`references` 连边）。
2. **委托 auto-wiki ingest**：按 `ingest-protocol` —— 抽名词查 canonical（含 aliases）合并 or 建节点 → 6 档时间档写对应表 → 补/退役受控关系边 → 研报落 `分析/` → 更新 Hub + `log.md` → 跑 `schema.py` 校验。
3. **不编造**：数值查不到就留空标"待补"，不臆造（对齐 tech 域 06-08「data_points: 0，未编造」先例）。
4. 记下这篇贡献了哪些 wiki 节点/数值/边，填进 `sinks`。

### Step 3 — 路由耐用散文到 PARA 归宿
按信号选归宿（散文本身搬过去，或留原地只在 frontmatter 记 `sinks`；首批默认**只记 sinks 不搬文件**，搬动需用户确认）：

| 信号（tags / type / 内容） | PARA 归宿 |
|---|---|
| 持续跟踪的领域研判 / 投研主线 | `02-Areas/投资研究` |
| 客户话术 / FAQ / 清单 / 信息源 / 工具文档 | `03-Resources/` |
| 绑定明确目标+截止的工作 | `01-Projects/` |
| 已成稿、已 ingest、无后续动作的旧研究 | `04-Archive/`（仅在 crystallize 完成后） |
| 盘中速记等速朽 | 留 Inbox 或移 `05-Daily/` 当日附注 |

### Step 4 — 打标（回写 frontmatter，文件不动）
给消化完的 Inbox 笔记 frontmatter 写入：
```yaml
compiled: true
digested: <today>
triage: crystallize | reference | ephemeral
sinks: [wiki/macro, 03-Resources/投研信息源]   # 实际去向，逗号列出
status: digested                               # 原 open → digested
```
> **绝不删源散文**；"归档"= 打标（+ 经确认才移 04-Archive）。退役/纠错走 auto-wiki 协议，不在此 DELETE。

### Step 5 — 收尾
- 更新 `Inbox/README.md` 「## 待处理」清单：已消化的勾掉/移除。
- 追加一行到消化日志 `Inbox/.digest-log.md`（append-only：日期 · 篇名 · triage · sinks · 校验结果）。
- 若被 daily-routine / 定时器调起，把"本次消化 N 篇 + 去向"回写当天 `05-Daily/<today>.md`。

### Step 6 — 汇报
```
收集箱消化完成（as-of <today>）：
- 待消化 N 篇 → 已消化 M 篇，剩 K 篇（最老 X 天）
- crystallize：<篇> → wiki/<域> 新增/更新 <节点/数值/边>
- reference：<篇> → 路由到 <PARA 归宿>
- ephemeral：<篇> → 抽硬数据 <…>，散文留置
- 待人工：<triage 存疑 / wiki 冲突 / 待确认搬动>
```

## 防扩散与纪律

- **源 immutable**：默认不移动文件，只打标；搬到 04-Archive 必须用户确认。
- **合并守闸**：写 wiki 严格走 auto-wiki（schema 校验 + 退役不删除 + 不编造）；冲突浮人工，不静默覆盖。
- **幂等**：`compiled: true` 且未改动的跳过；改动过才重消化。
- **可控范围**：一次最多消化 N=8 篇，超出报"剩 K 篇待下轮"；ephemeral 只抽数据不强行建页。
- **分诊保守**：耐用/速朽分不清 → 默认 reference，保散文、不污 wiki。

## 与其它 skill / 工具的关系

| 职责 | 委托给 |
|---|---|
| ingest / recall / lint（写 wiki 本体） | `auto-wiki` |
| 扫描 / 分诊 / 路由 / 打标 / 日志 | 本 skill 自理 |
| 被每日例行串起来调用 | `daily-routine`（Step 之间插「消化 Inbox」） |
| 研报 / 指标 / 行情取材（crystallize 补数） | `gangtise-ultra` / `ablemind-findata` / `juzi-*` |
| 轮询触发（检测层） | launchd `com.airvault.inbox-scan`（见部署说明） |


## 陋居接线（08-Ops，2026-06-11 起）

- 委托 ingest 时遵守**产出收口**：无人值守上下文中高危写入（newnode/retire/disputed/xedge）按 `08-Ops/审批账本.md` 状态分流——auto 直写记账，其余落 `08-Ops/review/` 候选。
- 消化完成更新 `08-Ops/routines/分诊员.md` 的 `last-run` / `last-result`；无人值守跑时在 `08-Ops/runs/` 建 run 档。