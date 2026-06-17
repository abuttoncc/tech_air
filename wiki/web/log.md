# 全栈应用领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-06-17
- 域创建（new_domain.py 脚手架）。待首次 ingest。

## 2026-06-17 — ingest U2（web 域首次落地，被 agent 引用）
- Source: 来源/2026-06-17-ablemind-able-alilab（一手·代码库，web 域视角）
- Created: 技术/AI SDK v6, 原理/SSE, 来源/2026-06-17-ablemind-able-alilab
- Relations: AI SDK v6→SSE built_on; AI SDK v6→前端 classified_as；被 agent 域 协议桥接管道 经 built_on 跨域引用（边存于 agent/data.db）
- data.db: pages 3, relations 2
- Conflicts: (无)
