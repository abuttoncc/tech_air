---
title: deepagents
type: entity
subtype: instrument
created: 2026-06-17
updated: 2026-06-17
aliases: [deep agents, deepagents框架]
sources: [2026-06-17-ablemind-able-alilab]
confidence: high
relations:
  - {target: LangGraph, type: built_on}
  - {target: 中间件分层编排, type: implements}
  - {target: 智能体, type: classified_as}
tags: [实体, 技术]
---

# deepagents

构建在 [[LangGraph]] 之上的 **agent harness（脚手架）**：它把「能干活的深度 agent」常用的几样东西打包成可注入的中间件——规划（planning / todo）、文件系统、子智能体（subagents）、长期记忆——让上层只需声明配置，不必每次手搓图。

ablemind 用 `deepagents.create_deep_agent()` 构建主 agent：拼接身份文件（SOUL.md 进 system prompt）、异步加载 MCP 工具、挂 planning/filesystem 中间件、装配 subagents。它不自己管状态——状态与持久化交给底层的 [[LangGraph]] 图与 checkpointer。因此 deepagents 与 LangGraph 的关系是「高阶封装 built_on 底层框架」。

## 关联

- **构建于其上**：[[LangGraph]]（built_on）—— deepagents 是 LangGraph 的高阶封装
- **实现的模式**：[[中间件分层编排]]（implements）—— 以中间件组合方式装配 agent 能力
- **分类**：智能体（classified_as）
