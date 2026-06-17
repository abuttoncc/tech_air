---
title: LangGraph
type: entity
subtype: instrument
created: 2026-06-17
updated: 2026-06-17
aliases: [langgraph]
sources: [2026-06-17-ablemind-able-alilab]
confidence: high
relations:
  - {target: 状态化执行, type: implements}
  - {target: PostgreSQL, type: built_on}
  - {target: 智能体, type: classified_as}
tags: [实体, 技术]
---

# LangGraph

LangChain 生态里把 LLM agent 建模为**有向图状态机**的编排框架：节点是计算步骤（模型调用、工具调用、子图），边是状态转移，整张图在一个可序列化的 state 上运行。相比线性的 prompt orchestration，它把「多轮、分支、循环、中断恢复」收进图的执行模型里，因此能承载 [[状态化执行]]。

在 ablemind 里，LangGraph 是整个 Agent 的底座：主 agent 由 [[deepagents]] 在其上构建，图编译时挂上 checkpointer 与 store。它的持久化后端是可插拔的，ablemind 选用 [[PostgreSQL]]（`AsyncPostgresSaver` / `AsyncPostgresStore`）承载 checkpoint 与长期记忆——这条 `built_on` 边即「智能体能力 → 依赖的底层数据技术」的跨域映射。它还支持本地 in-process 与远程 LangGraph Agent Server 两种运行时。

## 关联

- **实现**：[[状态化执行]]（implements）—— 图在可序列化 state 上跑，天然支持 checkpoint
- **持久化依赖**：[[PostgreSQL]]（built_on，跨域 → data）—— checkpointer / store 后端
- **被构建于其上**：[[deepagents]] —— 高阶 agent harness
- **分类**：智能体（classified_as）
