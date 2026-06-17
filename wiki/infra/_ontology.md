---
title: 基础设施领域本体契约
type: ontology
domain: infra
direction: 全栈
created: '2026-06-17'
updated: '2026-06-17'
schema_version: "2.0"
central_entity: 基础设施
tags: [ontology, contract]
---

# Tech Air · 基础设施领域本体契约

> `wiki/infra/` 的本体定义。与 [[wiki/agent/_ontology|agent 母本]] **共用同一套 6 档时间模型、退役不删除协议、三分铁律与受控关系词表**——本页只声明本域的**节点类型示例**。`ingest`/`recall` 前先读母本 + 本页。

## 0–1. 总原则与节点判据
全部同 [[wiki/agent/_ontology|agent 母本]]：三分铁律（数值进 data.db / 关系是边 / 标签是边）· 编译单向 · 退役不删除 · 「能指向就是这一个 → 实体；要讲机理才懂 → 概念」。

## 2. 节点类型（=目录=图谱着色）
| 类型 | 子目录 | 实体/概念 | 判据 | 例子 |
|---|---|---|---|---|
| 技术/工具 | `技术/` | 实体 | 有官方名/版本的容器、编排、服务器、CICD、可观测工具 | Docker、Kubernetes、Nginx、Containerd、GitHub Actions、ArgoCD、Terraform、Prometheus |
| 原理/机制 | `原理/` | 概念 | 运行时/部署的通用机理 | 容器隔离（namespace/cgroup）、反向代理、负载均衡、滚动更新、服务发现、声明式编排 |
| 模式/架构 | `模式/` | 概念 | 部署/运维范式 | 蓝绿部署、金丝雀发布、GitOps、Sidecar、不可变基础设施、微服务编排 |
| 事件 | `事件/` | 事件 | 有日期+施动者 | 2024-xx-Kubernetes 1.30 发布 |
| 分析 | `分析/` | 派生视图 | 研究课题页（删了不影响本体） | 「容器编排方案对比」「CICD 流水线设计」 |
| 来源 | `来源/` | 来源 | 文档/规范，只溯源 | 官方文档、CNCF |

## 3. 受控关系词表
本域**无特有关系词**，全部沿用 [[wiki/agent/_ontology|agent 母本]]（depends_on / built_on / implements / instance_of / part_of / alternative_to / runs_on / classified_as / created_by / changed_by / references）。

## 4. 跨域连接
本域是智能体工程的**底层基底**：被 agent 域的节点用签名边 `built_on` 指入（如 agent 的「Agent 服务」→built_on→ infra 的 [[Docker]]）。**同一专名物全库只建一次**——本域建页，agent 域连边引用。
