---
title: OAG决策平台范式
type: analysis
created: 2026-06-23
updated: 2026-06-23
sources: [2024-01-05-palantir-connecting-ai-to-decisions]
confidence: high
relations:
  - {target: 决策中心架构, type: references}
  - {target: 本体增强生成, type: references}
  - {target: 检索增强生成, type: references}
  - {target: 工具调用编排, type: references}
  - {target: 逻辑绑定, type: references}
  - {target: 沙盒情景, type: references}
  - {target: 写回模式, type: references}
  - {target: 人在回路, type: references}
  - {target: 决策血缘, type: references}
  - {target: Palantir 本体, type: references}
tags: [分析]
---

# OAG 决策平台范式

> 派生视图：把 Palantir 的决策中心范式从产品话术里抽出来，提炼成做「决策平台」反复套用的骨架。源 [[2024-01-05-palantir-connecting-ai-to-decisions]]；母本散文在 `Inbox/OAG范式-维护心智模型实现决策平台.md`。

## 一句话

维护一个跟领域真实运转同构的**心智模型**（名词：世界是什么样），并在它之上实现一个能算、能推、能建议、能落地的**决策平台**（动词：那我该怎么办）。

## 三支柱

- **Data**——[[本体增强生成]]（built_on [[检索增强生成]]）锚定运营真相，避免幻觉。
- **Logic**——[[逻辑绑定]] 把异构逻辑统一成工具，[[工具调用编排]] 让 LLM 当指挥家、确定性工具负责精确计算。
- **Action**——[[写回模式]]（三权分立 + 按系统写回）落地，[[沙盒情景]] 先彩排，[[人在回路]] 守闸。

闭环：[[决策血缘]] 把每个决策捕获成可微调的训练燃料，部落知识蒸馏成 principles 反哺 LLM。整套由 [[Palantir 本体]] 工业级实现。

## 镜像 tech_air

这套库本身就是同一个骨架的实例：`wiki/` + 双时态 `data.db` = 心智模型（名词层）；auto-wiki 引擎 = 逻辑工具；`08-Ops/` 的 candidate→review→commit + 高危 gate = 行动回路（[[写回模式]] 三权分立）；`runs/` + `log.md` = [[决策血缘]]；「只投候选不直写正典」= AI 自由度可放可收。Palantir 把决策推回 ERP，我把候选推回 wiki 正典。
