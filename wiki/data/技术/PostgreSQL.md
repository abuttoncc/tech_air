---
title: PostgreSQL
type: entity
subtype: instrument
created: 2026-06-17
updated: 2026-06-17
aliases: [Postgres, PG, pgvector]
sources: [2026-06-17-ablemind-able-alilab]
confidence: high
relations:
  - {target: 数据库, type: classified_as}
tags: [实体, 技术]
---

# PostgreSQL

开源关系型数据库，以 ACID 事务、丰富索引与可扩展类型著称；`pgvector` 扩展使其同时承担向量检索，省去单独的向量库。

在 ablemind 里，PostgreSQL 是单实例（pgvector 镜像）数据底座，身兼两职：① 作为 [[LangGraph]] checkpointer / store 的持久化后端，落盘 agent 的 [[状态化执行]] 状态（checkpoint + 长期记忆）；② 承载 conversation / message / message_events / runs / task_runs 等多租户业务表。连接层为 WAN 稳定性做了 TCP keepalive 与连接池调优。

作为本库 data 域节点，它是 agent 域 [[LangGraph]] 经 `built_on` 边引用的**跨域靶子**——同一专名物全库只建一次。

## 关联

- **被依赖（跨域）**：[[LangGraph]] →built_on→ 本节点（agent → data）
- **分类**：数据库（classified_as）
