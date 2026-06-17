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

# ablemind（able-alilab）代码库 — data 域视角

同一份一手来源（代码库本身）在 data 域的承载页（跨域双写，slug 与 agent 域一致）。完整系统概览见 agent 域同名来源页。

## data 域取材范围

- **PostgreSQL（pgvector）单实例**：既是 [[LangGraph]] checkpoint/store 的持久化后端，又承载 conversation / message / message_events / runs / task_runs 多租户业务表。
- **多租户隔离**：所有跨租户查询带 `WHERE user_id`，`user_id NOT NULL` 无默认兜底。
- **事件溯源式持久化**：`message_events` append-only 事件日志，幂等键 + 冷刷新重放（U7）。
- 代码：`packages/conversation_kit/persistence.py`、`dpagt/backend_dp/data/storage/persistence.py`、`dpagt/deploy/docker-compose.prod.yml`。

> 忠实摘要，不可变。U1 仅落 [[PostgreSQL]] 作为 agent 跨域 `built_on` 靶子；多租户/事件溯源细节留待 U5/U7。
