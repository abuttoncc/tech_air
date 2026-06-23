---
title: 2024-01-05-palantir-connecting-ai-to-decisions
type: source
created: 2026-06-23
updated: 2026-06-23
sources: []
confidence: high
source_type: 一手
source_origin: Palantir（Akshay Krishnaswamy, Chief Architect）
source_date: 2024-01-05
source_url: https://blog.palantir.com/connecting-ai-to-decisions-with-the-palantir-ontology-c73f7b0a1a72
aliases: [Connecting AI to Decisions with the Palantir Ontology, 用帕兰提尔本体连接AI与决策]
tags: [来源, 一手来源]
---

# Connecting AI to Decisions with the Palantir Ontology

Palantir 首席架构师 Akshay Krishnaswamy 的本体范式入门（2024-01-05）。本地存档 `09-Attachments/Palantir-Connecting-AI-to-Decisions-with-the-Ontology.pdf`。核心论点忠实摘要：

- **决策中心，非数据中心**：本体建模的对象是「决策」不是「数据」。传统数据/分析架构不捕获决策背后的推理，也不捕获决策落地的动作，故学不会、接不进 AI。
- **决策三要素**：数据（做决策的信息）· 逻辑（评估决策的过程）· 行动（决策的执行）。本体把三者合进一个随组织实时演化的统一模型。
- **名词 vs 动词**：数据元素是企业的「名词」（语义层 semantic 的对象与关系）；行动是「动词」（动能层 kinetic 的真实执行）。每条工作流是名词 + 动词凑成的完整句子。
- **数据·相关性**：AI 时代主要矛盾是 relevance 而非清洗统一。最关键的是「决策数据」与端到端「决策溯源 decision lineage」——某决策何时、基于哪版数据、经哪个应用做出，自动捕获，供人与 AI 取用。
- **逻辑·逻辑绑定**：异构逻辑资产（CRM/ERP 业务逻辑、ML 模型、优化/模拟算法）经「逻辑绑定 logic binding」统一成接口，作为「工具」补足 LLM 的非确定性推理。OAG 越过 RAG 只接数据的天花板，让 LLM 经可扩展工具范式同时接触数据/逻辑/行动三类原语。
- **行动·安全写回**：模拟结果先打包成「本体情景 Scenario」（沙盒子集）安全推演，确认再 commit。协作模型分三权——探索 / 暂存待审 / 提交落地。写回例程按系统定制（仓储 API、ERP 原生连接器、生产计划平文件异步）。护栏给 AI 划可行边界，自由度可放可收，copilot 像渐放权的新团队成员。
- **决策中心学习**：数据/逻辑/行动全连进本体后，端到端决策溯源成为微调训练燃料；隐性「部落知识」被蒸馏成 principles 在 LLM prompt 时调用，即「用 AI 改进 AI 的应用」。
- **案例**：虚构医疗器械厂 Titan Industries 遭遇关键原料断供，用调优 copilot「Disruption Bot」跨数据源扫描、查过往复盘、调重分配模型，提出新方案、落沙盒情景推演、交人终审，再按系统分别写回。

> 本页是原文忠实摘要，不可变。范式提炼见 [[OAG决策平台范式]]。
