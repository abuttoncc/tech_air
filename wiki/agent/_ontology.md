---
title: 智能体工程领域本体契约
type: ontology
domain: agent
direction: 智能体
created: '2026-06-17'
updated: '2026-06-17'
schema_version: "2.0"
central_entity: 智能体
tags: [ontology, contract]
---

# Tech Air · 智能体工程领域本体契约（母本）

> `wiki/agent/` 的本体定义，也是 **tech_air 全库的母本契约**——web/data/infra 三域共用本页的
> 6 档时间模型、退役不删除协议、三分铁律与受控关系词表，只在各自 `_ontology.md` 声明**本域特有**的补充。
> `ingest`/`recall` 前先读本页 + `wiki/_index.md` 路由。引擎规范见 `.claude/skills/auto-wiki/`（由 burrow-core 同步）。

## 0. 总原则
1. **节点 / 数据 / 边 三分**：数值/benchmark 绝不是节点（进 data.db）；关系是边不是页；分类标签是边不是页。
2. **编译单向**：`Inbox(学习散文) → ingest → wiki(本体)`。严谨只用在已结晶的知识。
3. **退役不删除**：T1/T2/T3 任何变化都是「旧行封 valid_to + 插新行」，永不 DELETE，必有 T4 事件盖章。

## 1. 节点判据
能用手指指向「就是这一个」、明年同名还指同一个（有官方名/版本号） → **实体**；
必须先讲一段机理/定义才听得懂的通用方法 → **概念**。
> 会骗你的直觉：「有没有数据/有没有配置项」不可靠——一个算法有参数也仍是概念。唯一可靠判据是「能不能指向那一个」。

## 2. 节点类型（=目录=图谱着色）
| 类型 | 子目录 | 实体/概念 | 判据 | 例子 |
|---|---|---|---|---|
| 技术/工具 | `技术/` | 实体 | 有官方名/版本的具体软件、库、框架、服务、协议 | LangGraph、LlamaIndex、Qdrant、OpenAI API、MCP、vLLM |
| 原理/机制 | `原理/` | 概念 | 要先讲一段机理才懂的通用方法/算法 | RAG、function calling、嵌入检索、上下文管理、推测解码、KV cache |
| 模式/架构 | `模式/` | 概念 | 可复用的设计/编排范式 | ReAct、Plan-and-Execute、多智能体编排、RAG 管道、工具路由、反思循环 |
| 事件 | `事件/` | 事件 | 有日期+施动者、发生即固定 | 2025-xx-某框架 v2 发布、某模型上线 |
| 分析 | `分析/` | 派生视图 | 研究课题页（删了不影响本体） | 「Agent 记忆方案全景」「RAG vs 长上下文」 |
| 来源 | `来源/` | 来源 | 官方文档/论文/talk/博客，只溯源 | 某框架 docs、某 arxiv 论文 |

## 3. 受控关系词表（边非页；`type` 不许自由文本，越界边被 lint 拒绝）
双写：页面 `frontmatter.relations[]` + `data.db relations 表`，两者一致。

| 关系 | 方向（from → to） | 语义 |
|---|---|---|
| `depends_on` | 技术 → 技术 | 运行/构建依赖（缺它跑不起来） |
| `built_on` | 技术 → 技术/原理（**跨域允许**） | 基于…构建。**本库签名边**：agent 节点 →built_on→ web/data/infra 节点 |
| `implements` | 技术 → 原理/模式 | 实现了某原理/模式 |
| `instance_of` | 技术 → 模式 | 是某模式的一个具体实例 |
| `part_of` | 技术→技术 / 原理→原理 | 组成部分 |
| `alternative_to` | 技术 ↔ 技术 | 同类替代 / 竞品 |
| `runs_on` | 技术 → 技术 | 部署/运行于…之上 |
| `classified_as` | 技术 → 层标签 | 贴层标签（智能体/前端/后端/数据库/存储/容器/服务器/CICD），按它分桶着色，不建页 |
| `created_by` / `changed_by` | 任意 → 事件 | 被某 T4 事件创建/变更 |
| `references` | 分析/来源 → 任意 | 溯源，不承载语义 |

## 4. 跨域连接（智能体工程 = 全栈技术的上层）
智能体系统构建在全栈技术之上。用签名边 **`built_on`**（agent 节点 → web/data/infra 节点，跨域）表达
「智能体能力 → 依赖的底层技术」（如 `向量记忆` →built_on→ `Qdrant`(data)；`Agent 服务` →built_on→ `Docker`(infra)）。
**同一专名物全库只建一次**（命名纪律：单一 slug 全库唯一），另一域连边引用，不重复建页。
