# 智能体工程领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-06-17
- 域创建（new_domain.py 脚手架）。待首次 ingest。

## 2026-06-17 — ingest U1（LangGraph + deepagents 状态化 Agent 图构建）
- Source: 来源/2026-06-17-ablemind-able-alilab（一手·代码库）
- Created: 技术/LangGraph, 技术/deepagents, 原理/状态化执行, 来源/2026-06-17-ablemind-able-alilab
- Relations: deepagents→LangGraph built_on; LangGraph→状态化执行 implements; LangGraph→PostgreSQL built_on（跨域 agent→data 签名边）; LangGraph/deepagents→智能体 classified_as
- data.db: pages 4, relations 5（无 T0/T1/T4）
- Conflicts: (无)
- 范围说明: 原计划的 FastAPI(web)/Docker(infra) 两个 built_on 靶子未建——图构建本身不准确依赖二者，FastAPI 留待 SSE 服务单元、Docker 留待 U9 沙箱单元，避免越界边。

## 2026-06-17 — ingest U2（Protocol Bridge Pipeline）
- Source: 来源/2026-06-17-ablemind-able-alilab（复用 U1 来源页）
- Created: 模式/协议桥接管道
- Relations: 协议桥接管道→AI SDK v6 built_on（跨域 agent→web）; 协议桥接管道→PostgreSQL built_on（跨域 agent→data，PersistenceTap）
- data.db: pages 5（+1）, relations 7（+2）
- Conflicts: (无)
- 关联说明: 主要事件源 [[LangGraph]] 在正文以散文连接（无合适受控边表达"下游消费"，不强建）。

## 2026-06-17 — ingest U3（中间件分层编排）
- Source: 来源/2026-06-17-ablemind-able-alilab（复用）
- Created: 技术/LangChain, 模式/中间件分层编排
- Updated: 技术/deepagents（+implements 中间件分层编排）, 技术/LangGraph（+built_on LangChain）
- Relations: LangGraph→LangChain built_on; 中间件分层编排→LangChain built_on; deepagents→中间件分层编排 implements; LangChain→智能体 classified_as
- data.db: pages 7（+2）, relations 11（+4）
- Conflicts: (无)
- 说明: 纯 agent 域，无跨域边；引入 LangChain 作生态底座，把 LangGraph/中间件模式锚定到统一框架。

## 2026-06-18 — ingest U4（供应商中立路由 + 推理内容回传）｜Wave 1 封顶
- Source: 来源/2026-06-17-ablemind-able-alilab（复用）
- Created: 模式/供应商中立路由, 原理/推理内容回传
- Relations: 供应商中立路由→LangChain built_on; 推理内容回传→LangChain built_on
- data.db: pages 9（+2）, relations 13（+2）
- Conflicts: (无)
- 说明: 纯 agent 域。LLM 供应商实体节点（DashScope/OpenAI 等）暂不建——保持"供应商中立"为抽象模式，避免堆 6 个 provider 页。war story 的具体数值（fold +%、事故 conv）留在来源 NOTES，正文只引述结论（不伪造 T0 period）。

## 2026-06-23 — ingest U5（OAG 决策中心范式）｜Wave 2 起
- Source: 来源/2024-01-05-palantir-connecting-ai-to-decisions（Palantir 首席架构师，一手；母本散文 Inbox/OAG范式-维护心智模型实现决策平台.md；PDF 存档 09-Attachments/）
- Created 原理(3): 检索增强生成(RAG), 本体增强生成(OAG), 决策血缘
- Created 模式(6): 决策中心架构, 工具调用编排, 逻辑绑定, 沙盒情景, 写回模式, 人在回路
- Created 技术(1): Palantir 本体
- Created 分析(1): OAG决策平台范式
- Relations(+15): 本体增强生成→检索增强生成 built_on; 决策中心架构→本体增强生成 built_on; {工具调用编排,写回模式,沙盒情景,人在回路,决策血缘}→决策中心架构 part_of; 逻辑绑定→工具调用编排 part_of; Palantir 本体→{决策中心架构,本体增强生成,逻辑绑定,写回模式,沙盒情景,决策血缘} implements; Palantir 本体→智能体 classified_as
- data.db: pages 21（+12）, relations 28（+15）; DataPoints/Facts/Events 0（本篇无 T0 数值/T1 状态翻转/T4 事件）
- Schema: 21/21 PASSED
- Conflicts: (无)
- 说明: 纯 agent 域。analysis 的 references 边只写 frontmatter（不进语义图/data.db，遵 references 不进语义图规则）。跨域 built_on 边本轮暂缺——OAG 范式不直接锚到现有全栈节点(PostgreSQL/AI SDK v6/SSE)，不硬建 Docker/HuggingFace 凑边。补齐了母本笔记欠的 Action 一柱（写回/沙盒/人在回路）与决策中心学习（决策血缘）。

## 2026-06-24 — ingest（声明式 agent 定义）
- Source: 来源/2026-06-24-langchain-deepagents-docs（LangChain Deep Agents 官方文档，一手）
- Created 模式(1): 声明式智能体定义 —— agent 是声明式文件不是代码：dict/AGENTS.md 描述「是什么」，引擎跑循环；声明式优先、代码兜底（CompiledSubAgent 塞 LangGraph 图）
- Created 来源(1): 2026-06-24-langchain-deepagents-docs
- Updated: 技术/deepagents（+implements→声明式智能体定义，正文补 AGENTS.md/字典声明）；hub 智能体工程（模式 9→10、来源 2→3、结构图 deepagents 行）
- Relations(+1): deepagents→声明式智能体定义 implements
- data.db: pages 23（+2）, relations 29（+1）; DataPoints/Facts/Events 0（纯概念，无 T0/T1/T4）
- Schema: 23/23 PASSED; 位置编码 26 节点重算; _report.html 重建
- Conflicts: (无)
- 说明: 与既有 模式/中间件分层编排 相邻但不同——后者讲「能力」声明式装配，本节点讲「整个 agent 身份」声明式描述，prose 互链不强建越界边。未对 LangGraph/子agent编排 建 typed 边（对照关系无受控词，子agent编排 无节点），仅 prose 引用避免断链。
