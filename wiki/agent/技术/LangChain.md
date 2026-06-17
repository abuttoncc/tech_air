---
title: LangChain
type: entity
subtype: instrument
created: 2026-06-17
updated: 2026-06-17
aliases: [langchain, langchain-core]
sources: [2026-06-17-ablemind-able-alilab]
confidence: high
relations:
  - {target: 智能体, type: classified_as}
tags: [实体, 技术]
---

# LangChain

LLM 应用开发的基础框架与生态，提供模型抽象、消息/工具规范、以及把横切能力挂在模型/工具调用周围的**中间件机制**（`AgentMiddleware`、`@wrap_model_call` 等钩子）。[[LangGraph]] 是其图编排子项目，[[deepagents]] 又建在 LangGraph 之上——三者构成 ablemind 后端的同一技术栈底座。

ablemind 的 [[中间件分层编排]] 正是建立在 LangChain 的中间件原语之上：用 LangChain 的 wrap 钩子实现重试/降级/模型选择/记忆/技能过滤等一长串中间件，再用声明式注册表组织它们的顺序。

## 关联

- **生态子项目**：[[LangGraph]]（← built_on）
- **中间件机制被其上构建**：[[中间件分层编排]]（← built_on）
- **分类**：智能体（classified_as）
