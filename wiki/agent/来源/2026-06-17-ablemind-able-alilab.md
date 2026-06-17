---
title: 2026-06-17-ablemind-able-alilab
type: source
created: 2026-06-17
updated: 2026-06-17
sources: []
confidence: high
source_type: 一手
source_origin: ablemind / able-alilab 代码库（abuttoncc/ablework）
source_date: 2026-06-17
source_url: ""
tags: [来源, 一手来源]
---

# ablemind（able-alilab）代码库

生产级**金融研究 Agent SaaS**，面向 ~50 用户的多租户系统。一手来源 = 代码库本身（本地工作副本 `able-alilab`，远端 `able-dpagt`，GitHub `abuttoncc/ablework`）。本页是 tech_air 从 ablemind 提炼智能体工程知识的 **canonical 源**，U1–U14 全部 ingest 共用本页溯源。

## 系统概览

- **后端**：FastAPI + LangGraph（Python 3.12），主执行链 = 本地 [[LangGraph]] Agent（经 [[deepagents]] 构建）+ MCP 工具链 + Protocol Bridge Pipeline → AI SDK v6 SSE。
- **前端**：Vite + React Router + AI SDK v6（TS）+ ai-elements + Zustand。
- **数据**：[[PostgreSQL]]（pgvector）承载 checkpoint/store 持久化与 conversation/message/runs 多租户持久化。
- **运行时**：三层沙箱（Docker · bwrap · direct）、Casdoor 认证、Infisical 密钥、Nginx/PM2、docker-compose。
- **已结晶契约**：`dpagt/docs/spec/` 18+ 个带 invariants 的 spec（含 ratified 的 task-orchestrator / ontology-mem / multi-tenant）。

## U1 取材范围（LangGraph + deepagents 状态化 Agent 图构建）

- 代码：`dpagt/backend_dp/kernel/agent/{graph,assembly,runtime_assets}.py`、`kernel/runtime/deepagents_adapter.py`、`data/storage/persistence.py`（AsyncPostgresSaver / AsyncPostgresStore + TCP keepalive 调优）。
- 要点：用 `deepagents.create_deep_agent()` 在 LangGraph 上构建主 agent（身份文件拼接、MCP 工具异步加载、planning/filesystem 中间件、subagents）；RuntimeAssets 把「资产装配」与「图编译」解耦；checkpoint/store 持久化到 PostgreSQL，支持本地 in-process 与远程 LangGraph Agent Server 两种运行时。
- 代码地图导航：`graphify-out/`（AST 级，仅作定位用）。

> 忠实摘要，不可变。后续单元（Protocol Bridge / Middleware / 沙箱 / 多租户 …）继续引用本页。
