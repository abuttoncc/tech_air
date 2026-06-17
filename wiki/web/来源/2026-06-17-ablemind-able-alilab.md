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

# ablemind（able-alilab）代码库 — web 域视角

同一份一手来源（代码库本身）在 web 域的承载页（跨域双写，slug 与 agent/data 域一致）。完整系统概览见 agent 域同名来源页。

## web 域取材范围

- **前端**：Vite + React Router + [[AI SDK v6]]（TS）+ ai-elements 组件库 + Zustand 状态管理。
- **流式接缝**：前端 `useChat()` 经 [[SSE]] 消费后端 [[协议桥接管道]] 产出的 AI SDK v6 事件流；`UIMessage.parts[]` 承载 text/reasoning/tool/data-* 分片。
- 代码：`packages/protocol_bridge/`（pipeline/schemas/sse_helpers/writer，含 tests/spec）、`dpagt/backend_dp/orchestration/streaming/`、`dpagt/frontend_dp/lib/hooks/use-chat-*.ts`、`dpagt/docs/spec/protocol/sse-events.md`。

> 忠实摘要，不可变。U2 落 AI SDK v6 / SSE 两节点；前端 store/事件路由细节留待 U12/U13。
