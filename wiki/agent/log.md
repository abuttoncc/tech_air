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
