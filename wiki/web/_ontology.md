---
title: 全栈应用领域本体契约
type: ontology
domain: web
direction: 全栈
created: '2026-06-17'
updated: '2026-06-17'
schema_version: "2.0"
central_entity: 全栈应用
tags: [ontology, contract]
---

# Tech Air · 全栈应用领域本体契约

> `wiki/web/` 的本体定义。与 [[wiki/agent/_ontology|agent 母本]] **共用同一套 6 档时间模型、退役不删除协议、三分铁律与受控关系词表**——本页只声明本域的**节点类型示例**。`ingest`/`recall` 前先读母本 + 本页。

## 0–1. 总原则与节点判据
全部同 [[wiki/agent/_ontology|agent 母本]]：三分铁律（数值进 data.db / 关系是边 / 标签是边）· 编译单向 · 退役不删除 · 「能指向就是这一个 → 实体；要讲机理才懂 → 概念」。

## 2. 节点类型（=目录=图谱着色）
| 类型 | 子目录 | 实体/概念 | 判据 | 例子 |
|---|---|---|---|---|
| 技术/工具 | `技术/` | 实体 | 有官方名/版本的前后端库、框架、运行时、协议 | React、Vue、Next.js、Node.js、FastAPI、Express、TypeScript、Vite、Tailwind |
| 原理/机制 | `原理/` | 概念 | 要先讲一段机理才懂的通用方法 | 事件循环、虚拟 DOM、SSR/CSR、响应式渲染、CORS、JWT 鉴权、HTTP 缓存 |
| 模式/架构 | `模式/` | 概念 | 可复用的设计/架构范式 | MVC、BFF、微前端、REST、GraphQL、组件化、状态管理 |
| 事件 | `事件/` | 事件 | 有日期+施动者 | 2024-xx-React 19 发布、Node 22 LTS |
| 分析 | `分析/` | 派生视图 | 研究课题页（删了不影响本体） | 「前端框架选型」「SSR 方案对比」 |
| 来源 | `来源/` | 来源 | 文档/规范/博客，只溯源 | MDN、框架官方文档 |

## 3. 受控关系词表
本域**无特有关系词**，全部沿用 [[wiki/agent/_ontology|agent 母本]]（depends_on / built_on / implements / instance_of / part_of / alternative_to / runs_on / classified_as / created_by / changed_by / references）。

## 4. 跨域连接
本域是智能体工程的**底层基底**：被 agent 域的节点用签名边 `built_on` 指入（如 agent 的「Web Agent」→built_on→ web 的 [[Next.js]]）。**同一专名物全库只建一次**——本域建页，agent 域连边引用。
