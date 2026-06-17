---
title: AI SDK v6
type: entity
subtype: instrument
created: 2026-06-17
updated: 2026-06-17
aliases: [Vercel AI SDK, ai-sdk, AI SDK]
sources: [2026-06-17-ablemind-able-alilab]
confidence: high
relations:
  - {target: SSE, type: built_on}
  - {target: 前端, type: classified_as}
tags: [实体, 技术]
---

# AI SDK v6

Vercel 出品的前端 AI 流式 SDK（v6 系），定义了一套以 `UIMessage.parts[]` 为核心的流式 UI 消息协议，并提供 `useChat()` 等 React hook 在客户端消费。parts 是一个灵活的分片类型系统——`text`、`reasoning`、`tool-invocation`、`source-url`、`data-*`（带类型判别符的元数据通道）——让"文本 + 推理 + 工具卡片 + 引用 + 进度"在同一条消息里有序呈现。

它的流式传输底座是 [[SSE]]（POST endpoint），并支持 `resume` 重连。在 ablemind 里，前端 `useChat()` 消费的正是 [[协议桥接管道]] 产出的 AI SDK v6 SSE 流——这条协议是后端 agent 与前端 UI 之间的契约接缝。

## 关联

- **流式传输底座**：[[SSE]]（built_on）
- **被其产出协议构建**：[[协议桥接管道]]（← built_on，agent 域）
- **分类**：前端（classified_as）
