---
title: 智能体核心 · 学习要点（Wave 1）
type: resource
created: 2026-06-18
updated: 2026-06-18
tags: [学习, 智能体工程, ablemind, 学习要点]
related: ["[[ablemind-知识提炼]]", "[[智能体工程]]"]
---

# 智能体核心 · 学习要点（Wave 1）

> 学习对象：从 ablemind 提炼进 `wiki/agent` 的 9 个节点（框架栈 + 5 个模式/原理）。
> 这份不是知识本身（知识在 wiki 节点里），是**怎么学透它们的路线 + 自测**。

## 怎么用这份要点

每个主题三步走：
1. **读 wiki 节点**（已结晶的精炼版，5 分钟建立骨架）。
2. **回 ablemind 读源码/spec**（"去读什么"那一栏，把骨架填成血肉，亲手 trace 一条具体路径）。
3. **答自测题**（能讲出来 = 懂了；讲不出 = 回去读）。学习中的困惑/顿悟随手丢进 `Inbox/`，将来 ingest 回 wiki。

**优先级**：⭐ 标记的是"必须先懂"的承重墙；🔥 是三个 war story（工程智慧密度最高，最值得啃）。

## 学完 Wave 1 你应该能做到

- 画出 `LangChain → LangGraph → deepagents` 三层栈，并说清每层各加了什么、为什么要分层。
- 解释一个 agent "持续工作"靠什么撑住（状态化执行 → checkpoint → PostgreSQL）。
- 说出 agent 能力是"装配"出来的：能描述如何加一个中间件、顺序由谁决定。
- 从一个 LangGraph 事件 trace 到浏览器渲染，并说清"为什么所有输出必经一条管道"。
- 复述 thinking round-trip 两个坑，并解释"推理内容为什么必须和答案内容分开"。

---

## 主题 A ⭐ 框架栈：LangChain → LangGraph → deepagents

- **一句话**：三层地基，越往上越"开箱即用"，越往下越"可控"。
- **必懂的为什么**：为什么不直接用 LangChain？为什么要"图"而不是"链"？
  - LangChain = 原语层（模型抽象、消息/工具规范、中间件钩子）。
  - LangGraph = **有状态图编排**：节点=步骤、边=状态转移；图能表达分支/循环/中断恢复，链不能。
  - deepagents = 固执的脚手架：planning / filesystem / subagents / memory 预接好。
- **核心洞见**：每上一层是用"可控性"换"省事"。知道何时该往下钻一层，是会用这套栈的关键。
- **去读什么**：`kernel/agent/{graph,assembly,runtime_assets}.py`、`kernel/runtime/deepagents_adapter.py`。重点看 RuntimeAssets 怎么把"资产装配"和"图编译"解耦。
- **自测**：① deepagents 帮你省了什么、又藏了什么？② 如果要自定义一个 LangGraph 没有的执行流，你从哪层下手？
- **wiki**：[[LangChain]] · [[LangGraph]] · [[deepagents]]

## 主题 B ⭐ 状态化执行：agent 凭什么"持续工作"

- **一句话**：把执行状态序列化落盘，agent 才从"会聊天"变成"接得住任务"。
- **必懂的为什么**：多轮累积、中断恢复（HITL/断连）、进程重启不丢——这三件事都要靠状态持久化。
- **核心洞见**：这是"研究助手 vs 聊天模型"的分水岭，也是 T2 定义性逻辑（只要还想跨轮持续工作，它就成立）。
- **去读什么**：`data/storage/persistence.py`（AsyncPostgresSaver / AsyncPostgresStore + 为 WAN 调的 TCP keepalive）。
- **自测**：① 一轮对话结束时，到底什么被写进了 checkpoint？② 用户刷新页面重连，状态怎么续上？
- **wiki**：[[状态化执行]] →（落盘）→ [[PostgreSQL]]

## 主题 C ⭐ 中间件分层编排：能力是"装配"出来的

- **一句话**：把 agent 能力拆成可插拔中间件栈，按声明顺序组合。
- **必懂的为什么**：
  - **双层**：基础设施型（重试/降级/调用上限/模型选择）管健壮性 vs 功能型（记忆/技能过滤/PII脱敏/预算）加能力。
  - **声明式**：yaml 管"顺序+装哪些"，工厂管"怎么构造"。
- **核心洞见**：能力解耦成独立中间件 → 可独立增删、独立测试、按场景重排。改行为只动配置，不碰主循环。
- **去读什么**：`kernel/agent/middleware_registry.py`、`config/system/middleware.yaml`、spec `dpagt/docs/spec/middleware/chain-order.md`。
- **自测**：① 加一个新中间件要动哪几处？② 中间件顺序为什么有讲究、谁来保证？
- **wiki**：[[中间件分层编排]] →（建于）→ [[LangChain]]

## 主题 D ⭐ 协议桥接管道：输出怎么到达客户端

- **一句话**：Source → Adapter → Middleware → SSE，所有对客户端的输出必经这一条管道。
- **必懂的为什么**：单一管道才能在一处统一保证事件顺序、生命周期、持久化、断连恢复——否则全是事后补丁。
- **核心洞见**：行为被结晶成**可执行不变量**（FinishEvent 最后、ErrorEvent 不得在 Finish 后、`data-*` 必带类型判别符、reasoning 先于 text）。读 spec 比读代码更快抓住骨架。
- **去读什么**：`packages/protocol_bridge/`（pipeline / schemas / sse_helpers / writer + `tests/spec`）、spec `protocol/sse-events.md`。重点看 PersistenceTap（旁路写库）和 DeliveryTap（挂附件）。
- **自测**：① 把一个 LangGraph 事件 trace 到浏览器渲染，中间经过哪些层？② 为什么严禁在路由层手写 SSE 字符串？
- **wiki**：[[协议桥接管道]] →（输出/持久化）→ [[AI SDK v6]]、[[PostgreSQL]]；客户端侧 [[SSE]]

## 主题 E 模型接口层：供应商中立路由 + 推理内容回传

- **一句话**：多 LLM 供应商藏在统一接口后；其中最难的是历史推理内容怎么跨轮回传。
- **必懂的为什么**：选型/协议适配（OpenAI↔Anthropic 格式互转、tool_call_id 合成、usage 归一）/ 降级 / key 池。
- **核心洞见**：模型供应商应是**可替换的底层依赖**，不是写死的耦合。
- **去读什么**：`packages/llm_router/`（config / router / langchain_model / fallback）。
- **自测**：① RouterChatModel 为什么要做成 LangChain ChatModel？② 一次 429 之后发生了什么？
- **wiki**：[[供应商中立路由]] · [[推理内容回传]]

---

## 🔥 三个 war story（最值得啃的部分）

工程智慧密度最高的不是"功能怎么搭"，而是"踩了什么坑、为什么"。这三个要能给别人讲明白：

1. 🔥 **fold 膨胀**（[[推理内容回传]]）：把 reasoning 并入出站 `content`，会让每轮历史把推理正文重塞进输入 → 多轮输入暴涨。修复 = reasoning 与 content **结构上同级隔离**。
   - 教训：推理内容和答案内容是**两条生命周期**，不能混。
2. 🔥 **空签名回放死循环**（[[推理内容回传]]）：`thinking_signature` 为空的网关，若把历史 thinking 当普通文本回传，模型会当成新输入重读 → 工具复读死循环（真实事故）。修复 = fail-loud，必须显式声明 `thinking_roundtrip`。
   - 教训：跨供应商的隐式行为差异要**显式处理 + 出错即响**，不能静默兜底。
3. 🔥 **必经管道**（[[协议桥接管道]]）：任何绕过管道手写 SSE 的输出，都会让顺序/持久化/恢复失控。
   - 教训：横切关注点要**收口到单一通道**，用不变量约束，而不是靠纪律分散保证。
   - 延伸读：`REASONING_ROUNDTRIP_NOTES.md`（前两个坑的完整复盘，"假设→A/B 实测→推翻"的方法论范例）。

---

## 学完之后

- 困惑/顿悟随手写进 `Inbox/`（研究笔记模板：困惑/目标/思路/线索）——这些就是下一轮 `ingest` 的原料。
- 想继续往下学：Wave 2（[[ablemind-知识提炼]] 的 U5–U8）会把 **多租户隔离 / checkpoint 记忆 / 事件溯源** 织进 data 域；想看运行时就跳 U9 沙箱。
- 想验证理解：挑主题 D 的自测①，真的去仓库 trace 一遍一个事件的完整旅程——能 trace 通，说明 Wave 1 的骨架你已经握住了。
