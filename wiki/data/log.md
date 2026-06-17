# 数据层领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-06-17
- 域创建（new_domain.py 脚手架）。待首次 ingest。

## 2026-06-17 — ingest U1（跨域双写：被 agent 域引用）
- Source: 来源/2026-06-17-ablemind-able-alilab（一手·代码库，data 域视角）
- Created: 技术/PostgreSQL, 来源/2026-06-17-ablemind-able-alilab
- Relations: PostgreSQL→数据库 classified_as；被 agent 域 LangGraph 经 built_on 跨域引用（边存于 agent/data.db）
- data.db: pages 2, relations 1
- Conflicts: (无)
