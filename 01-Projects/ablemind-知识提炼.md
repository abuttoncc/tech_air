---
title: 从 ablemind 提炼智能体工程 — 研究选题盘点（syllabus）
type: project
status: active
created: 2026-06-17
source: /Users/jameslee/ablemind/able-alilab
tags: [project, ablemind, syllabus, backlog]
---

# 从 ablemind 提炼智能体工程 — 选题盘点

> **目标**：把生产级金融研究 Agent SaaS `ablemind`（able-alilab）当源材料，逐个薄切片地把其中**耐用的智能体工程知识**编译进 `wiki/`（agent 母本 + web/data/infra 三域），冷启动这张知识图谱。
>
> **这是研究 backlog，不是结论**。每个单元学透后才 `/auto-wiki ingest`，建完节点回来勾掉。

## 四条纪律（每次 ingest 都守）

1. **`graphify-out/` 是源不是产物**：able-alilab 里那个 `graphify-out/`（21MB 代码图）只当**代码导航器**定位实现；产物是 `wiki/` 里的概念节点。
2. **agent 母本先行，按 `built_on` 向外拉**：先在 agent 域立中心节点，再把 web/data/infra 节点作为 `built_on`/`runs_on` 的靶子拉进来。同一专名物（FastAPI、PostgreSQL、Docker…）**全库只建一次**，别域连边引用。
3. **一次一薄切片**：绝不把整仓倒进 ingest。一个 ingest = 一个学透的单元。
4. **取材三路**：① `graphify-out` 定位代码 → ② `context7`/官方 docs 取框架原理（LangGraph / AI SDK v6 / deepagents）→ ③ **ablemind 自己的 `dpagt/docs/spec/`**（已结晶的 invariants，本体金矿，见文末）。

## 取材地图（able-alilab 里东西在哪）

| 区域 | 路径 | 装什么 |
|---|---|---|
| 后端 Agent 内核 | `dpagt/backend_dp/kernel/{agent,middleware,runtime}/` | 图构建、40+ middleware、deepagents 适配 |
| 流式管道 | `dpagt/backend_dp/orchestration/streaming/` + `packages/protocol_bridge/` | Protocol Bridge Pipeline |
| 共享包 | `packages/{protocol_bridge,llm_router,conversation_kit,im_bridge,attachment_router}/` | 可复用抽象，多含 `tests/spec/` |
| 前端 | `dpagt/frontend_dp/` + `uipack/` | AI SDK v6 / Zustand / ai-elements |
| 沙箱/部署 | `dpagt/sandbox_service/` + `dpagt/deploy/` | 三模式沙箱、docker-compose、Nginx/PM2/Casdoor/Infisical |
| **已结晶契约** | `dpagt/docs/spec/`（`INDEX.md`）+ `docs/agent-contract.md` | invariants / ADR，最高本体价值 |

---

## 选题 backlog（14 单元，分 4 波）

> 节点类型：**实体**=技术/工具（指得到的那一个）· **概念**=原理/机制 · **模式**=架构/范式。优先级 P0 最高。

### Wave 1 — agent 母本心脏（先立中心，跑通跨域边）

| # | 选题 | 域 | 节点类型 | 取材 | 会建的跨域 `built_on`/`runs_on` 边 | 优先级 |
|---|---|---|---|---|---|---|
| U1 | **LangGraph + deepagents 状态化 Agent 图构建** | agent | LangGraph·deepagents=实体；状态化执行=概念 | `kernel/agent/{graph,assembly,runtime_assets}.py`；context7 LangGraph | →FastAPI(web)、→PostgreSQL(data,checkpoint)、→Docker 沙箱(infra) | **P0** |
| U2 | **Protocol Bridge Pipeline（Source→Adapter→Middleware→SSE）** | agent | 模式 | `orchestration/streaming/`、`packages/protocol_bridge/`（有 `tests/spec`） | runs_on→AI SDK v6 SSE(web)、built_on→PostgreSQL(PersistenceTap,data) | **P0** |
| U3 | **Middleware 分层与声明式编排** | agent | 模式（基础设施型 vs 功能型双层） | `kernel/agent/middleware_registry.py`、`config/system/middleware.yaml`、spec `middleware/chain-order.md` | implements→LangChain middleware | **P0** |
| U4 | **llm_router 供应商中立路由 + thinking round-trip** | agent | LLMRouter=实体；推理内容生命周期=概念 | `packages/llm_router/`、`REASONING_ROUNDTRIP_NOTES.md`（war story） | alternative_to 各供应商；built_on→DashScope/OpenAI 等 | **P0** |

### Wave 2 — 状态 · 隔离 · 记忆（耐用底座，桥到 data）

| # | 选题 | 域 | 节点类型 | 取材 | 跨域边 | 优先级 |
|---|---|---|---|---|---|---|
| U5 | **ExecutionContext 四层线程隔离 + 多租户** | agent×data | 概念 | `models/execution.py`、spec `invariants/multi-tenant.md` | built_on→PostgreSQL(WHERE user_id) | P1 |
| U6 | **Checkpoint/Store 状态化记忆持久化** | agent×data | 概念；PostgreSQL/pgvector=实体 | `data/storage/persistence.py`（TCP keepalive 调优） | built_on→PostgreSQL、→pgvector 向量检索 | P1 |
| U7 | **事件溯源式持久化（message_events 无损日志）** | data | 概念（Event Sourcing 变体） | `packages/conversation_kit/persistence.py`、spec `runtime/message-events-persistence.md` | — | P1 |
| U8 | **Worker 生命周期 + decision signals 多智能体编排** | agent | 模式 | `kernel/middleware/worker_lifecycle.py`、spec `orchestrator/task-orchestrator.md`（**ratified**）、`runtime/decision-signals.md` | built_on→PostgreSQL(task_runs)、→Redis Streams | P1 |

### Wave 3 — 运行时与工具（能力扩展，桥到 infra）

| # | 选题 | 域 | 节点类型 | 取材 | 跨域边 | 优先级 |
|---|---|---|---|---|---|---|
| U9 | **沙箱三模式隔离（Docker · bwrap · direct）** | infra×agent | 模式；Docker·bubblewrap=实体 | `sandbox_service/server.py`、`capabilities/sandbox/{backend,paths}.py` | agent 工具执行 runs_on→沙箱；built_on→Docker | P1 |
| U10 | **MCP 工具链接入 + 运行时热重载** | agent | 概念；MCP=概念/协议 | `capabilities/tools/loader.py`、`kernel/agent/mcp_lifecycle.py` | built_on→langchain-mcp-adapters | P2 |
| U11 | **Thinking policy + tool preset 成本控制** | agent | 概念（二元决策，非档位） | `kernel/agent/{thinking_policy,tool_preset_policy}.py` | — | P2 |

### Wave 4 — 全栈承接面（web/infra 收口，补全四域）

| # | 选题 | 域 | 节点类型 | 取材 | 跨域边 | 优先级 |
|---|---|---|---|---|---|---|
| U12 | **AI SDK v6 SSE 流式消费（web↔agent 接缝）** | web | AI SDK v6·React=实体；SSE 流式消费=概念 | `frontend_dp/lib/hooks/use-chat-*.ts`、spec `protocol/sse-events.md` | 消费 agent 的 SSE 输出（与 U2 对接） | P2 |
| U13 | **Zustand 响应式 store + SSE 事件路由** | web | Zustand=实体；事件驱动状态=模式 | `frontend_dp/lib/stores/`、`lib/replay/dispatch.ts` | — | P2 |
| U14 | **部署栈：docker-compose / Nginx·PM2 / Casdoor / Infisical** | infra | 实体（各一节点）+ 编排=模式 | `dpagt/deploy/`、`.github/workflows/ci.yml` | runs_on 关系网 | P2 |

---

## 进度追踪

- [x] U1 LangGraph + deepagents 图构建 ✅ 2026-06-17（agent: LangGraph/deepagents/状态化执行 + 来源；data: PostgreSQL；跨域边 LangGraph→PostgreSQL built_on。FastAPI/Docker 按边准确性延后到 SSE 服务单元 / U9）
- [x] U2 Protocol Bridge Pipeline ✅ 2026-06-17（agent: 协议桥接管道；web 首次落地: AI SDK v6 + SSE + 来源；跨域边 协议桥接管道→AI SDK v6 / →PostgreSQL）
- [ ] U3 Middleware 分层与编排
- [ ] U4 llm_router + thinking round-trip
- [ ] U5 ExecutionContext 四层隔离 + 多租户
- [ ] U6 Checkpoint/Store 记忆持久化
- [ ] U7 message_events 事件溯源
- [ ] U8 Worker 生命周期 + decision signals
- [ ] U9 沙箱三模式隔离
- [ ] U10 MCP 工具链 + 热重载
- [ ] U11 thinking/tool preset 成本控制
- [ ] U12 AI SDK v6 SSE 消费
- [ ] U13 Zustand store + 事件路由
- [ ] U14 部署栈

## 已结晶素材专项（spec = 最高本体价值，优先消费）

ablemind 的 `dpagt/docs/spec/` 有 18+ 个带 Invariants 的契约，等于半成品本体：

- **ratified（强制，等于已定公理）**：`orchestrator/task-orchestrator.md`（U8）、`ontology-mem.md`、`invariants/multi-tenant.md`（U5）。
- **draft 但逻辑基本落地**：`protocol/sse-events.md`（U2/U12）、`runtime/hitl-persistence.md`、`runtime/message-events-persistence.md`（U7）、`runtime/decision-signals.md`（U8）、`runtime/frontend-consumable-state.md`、`middleware/commitment-closure.md`。

> **彩蛋单元（进阶 P3）**：ablemind 自带一套 `ontology-mem` 知识治理管线（route-before-store + 冲突检测 + Neo4j/Postgres 双存），和本库的 auto-wiki 是**同构对照** —— 学透它能反哺 tech_air 自身引擎设计。

## 下一步

- **U1+U2 已完成**（2026-06-17）：四域已起三域（agent/web/data），跨域 `built_on` 机器双向验证。当前图谱 — agent 5 节点、web 3 节点、data 2 节点。
- **下一刀候选**：① **U3 Middleware 分层编排**（继续夯实 agent 心脏，纯 agent 域，最快）；② **U5 ExecutionContext 多租户**（桥到 data，复用 PostgreSQL，开始织 data 域）。建议 U3 收尾 Wave 1 的 agent 心脏，再转 Wave 2。
- 之后按 Wave 顺序推进，每个 ingest 后回来勾进度。
- 经验记录：ingest 时严格按「边准确性」决定建不建跨域靶子，宁可延后也不建越界边（U1 的 FastAPI/Docker 即按此延后）。模式(concept)节点按 CLAUDE.md 签名边惯例可作 built_on 源（schema.py 仅警告，受控词表归 lint）。
