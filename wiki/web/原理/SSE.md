---
title: SSE
type: concept
created: 2026-06-17
updated: 2026-06-17
aliases: [Server-Sent Events, 服务器推送事件, text/event-stream]
sources: [2026-06-17-ablemind-able-alilab]
confidence: high
durability: high
preconditions: [单向 服务器→客户端 流式推送, HTTP 长连接]
falsifiable_by: [若改用 WebSocket 双向通道或短轮询]
relations: []
tags: [概念, 原理]
---

# SSE（Server-Sent Events）

基于 HTTP 的**单向服务器→客户端流式推送**机制（MIME `text/event-stream`）：服务端在一条长连接上持续 push 事件，客户端按行解析。相比 WebSocket 的双向全双工，它更轻、天然走 HTTP 基础设施、自带断线重连语义，是 LLM token 逐字流式输出的常用选择。

在 ablemind 里，主对话链路用 SSE（POST endpoint）承载 [[AI SDK v6]] 的事件协议，配合 keep-alive 注释帧防代理超时、用 ring-buffer + `since_seq` 支持移动端断连重连。它是 [[协议桥接管道]] 最末端的输出传输层。

## 关联

- **承载于其上的协议**：[[AI SDK v6]]（← built_on）
- **作为管道输出层**：[[协议桥接管道]]
