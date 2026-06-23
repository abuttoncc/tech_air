---
title: Palantir 本体
type: entity
subtype: instrument
created: 2026-06-23
updated: 2026-06-23
aliases: [Palantir Ontology, Ontology, Palantir AIP, AIP]
sources: [2024-01-05-palantir-connecting-ai-to-decisions]
confidence: high
relations:
  - {target: 决策中心架构, type: implements}
  - {target: 本体增强生成, type: implements}
  - {target: 逻辑绑定, type: implements}
  - {target: 写回模式, type: implements}
  - {target: 沙盒情景, type: implements}
  - {target: 决策血缘, type: implements}
  - {target: 智能体, type: classified_as}
tags: [实体, 工具]
---

# Palantir 本体

Palantir AIP / Foundry 的运营层，把企业的数据、逻辑、行动整合进一个以决策为中心、随组织实时演化的统一模型，让人和 AI 在同一套运营底座上查询、推理、行动。它是 [[决策中心架构]] 的工业级实现样板，也是本库 OAG 范式的母本来源（提炼见 [[OAG决策平台范式]]）。

落到能力：以 [[本体增强生成]] 锚定 LLM；以 [[逻辑绑定]] 把异构逻辑 surfaced as tools；以 [[沙盒情景]] + [[写回模式]] 安全落地行动；以 [[决策血缘]] 把决策捕获成可学习的燃料。所有 AI 活动受与人类相同的安全策略管控。

## 关联
- **实现（implements）**：[[决策中心架构]] · [[本体增强生成]] · [[逻辑绑定]] · [[写回模式]] · [[沙盒情景]] · [[决策血缘]]
- **分类**：智能体（classified_as）
