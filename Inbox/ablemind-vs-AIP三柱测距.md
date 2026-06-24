---
tags: [research, analysis, agent, ablemind, palantir]
type: analysis-note
status: crystallizing
topic: "ablemind vs Palantir AIP — 决策平台三柱测距"
created: "2026-06-23"
updated: "2026-06-23"
wiki-topic: "本体增强生成"
compiled: false        # 待决定是否 ingest 进 wiki/agent/分析
source:
  - "ablemind / able-alilab 代码库（一手）：dpagt/docs/spec/ontology-mem.md（ratified）· dpagt/docs/plans/2026-05-25-ontology-mem.md · dpagt/docs/spec/runtime/{ontology-constraint-sot,decision-signals,sensor-validation,hitl-persistence}.md"
  - "Palantir: Connecting AI to Decisions with the Palantir Ontology（Akshay Krishnaswamy，一手）= wiki/agent/来源/2024-01-05-palantir-connecting-ai-to-decisions"
  - "Palantir Engineering Blog: Building with AIP — Logic Tools / Data Tools for RAG-OAG"
  - "PPT: Palantir_AIP_Logic_Architecture.pdf（philo_air/ref/）"
  - "母本范式：[[OAG范式-维护心智模型实现决策平台]]"
---

# ablemind vs Palantir AIP — 决策平台三柱测距

> 一手核查（读了 ablemind 的 ratified spec + plan 原文，非二手猜测）。结论先行：**ablemind 不是"接近"这个架构，在认知/本体/治理层它已经独立造出了同一个架构，某些纪律比 AIP 公开材料还细。** 真缺口只有逻辑柱一条是硬欠债，另两条是产品定位选择。

## 0. 纠错（对上一轮判断的自我修正）

上一轮我基于 spec **索引一句话**判 ablemind 本体"距离中等、是护栏小本体"——**错**。读了 `ontology-mem.md`（ratified）+ 829 行 plan 后：它是 V1 八阶段（S1–S8）全上线的**生产级 OAG 实现**，FIBO 对齐、候选审核、双时态、Dream 自治整理俱全。教训已落 tech_air CLAUDE.md「检索纪律」：结构问 expand/db，**内容审计必须读原文**，别从索引摘要下判断。

## 1. 题眼：ablemind 自己的一句话就是 OAG

`ontology-mem` plan 的 TL;DR：
> Right brain discovers. Left brain accepts. **SQL stores facts. Graph stores meaning. Vector finds evidence. Rules control promotion.**
> 两条设计决策：① Proposed content is not canonical（route-before-store）② **Boundary > capacity**（识别更多概念不是目标）。

## 2. 三柱 + 治理 测距总表（带 spec 证据）

| AIP/OAG 要素 | ablemind 现状 | 距离 | 一手证据 |
|---|---|---|---|
| **本体 / 名词层** | Neo4j 语义图：`Concept/Entity/Company/Index/Fund/Methodology/ActionType/ExternalAnchor/DistinctionRule` + `IS_A/SAME_AS/NOT_SAME_AS/DERIVED_FROM/APPEARS_IN/ALIGNED_TO_FIBO/SUPPORTED_BY/SUPERSEDED_BY`；**FIBO 对齐**、每节点带 `source` provenance | **近** | `merge_verified_node`；ali-lab 现状 65 fibo_validated + 34 cn_ext + 8 workspace_primitive |
| **OAG 越过 RAG** | 检索 **Neo4j-first**：concepts/constraints → facts → vector → memory，5 层并发带预算；"vector 分不清 净利润≠归母净利润，只有结构图能" | **= 已跨过那条线** | `MUST-context-bundle-neo4j-first`；`context_assembler.py` 5 层；dogfood 实证 conv `b4c58dab` |
| **数值不进本体** | period+数值 → `fact_observations`（time-indexed），**绝不**进 Neo4j；Entity 节点只许 9 个身份白名单属性（ticker/exchange/isin/lei…） | **= 同一条规则** | `MUST-NOT-promote-time-bound-numbers-to-ontology` + `MUST-NOT-store-time-bound-on-entity-node` |
| **候选收口（只投不直写）** | `candidate_reviews` 状态机 `proposed→routed→conflict_checked→needs_review\|verified→promoted`；无任何直写正典的旁路 | **= 同一个 gate** | `MUST-route-before-store` + `MUST-NOT-bypass-review` |
| **矛盾检测（lint）** | `conflict_detector` V2，16/16 测试，5 规则；挡 `NetProfit SAME_AS 归母净利润`；verify 端 HTTP 409 unless override | **近** | S3；`knowledge/conflict_detector.py` |
| **退役不删除 + 双时态** | discard 留 90 天、`demote` 不删、`SUPERSEDED_BY`；`valid_from/valid_to/recorded_at` 已写 | **近**（time-travel 查询未实现） | `SHOULD-archive-not-delete`；plan「bi-temporal lite — written, not yet query-walked」 |
| **外部权威锚定** | 概念对齐 **FIBO**（金融业务本体），`ALIGNED_TO_FIBO` 边 → `:ExternalAnchor` URI stub；本地只存"探索地图"非 FIBO 副本 | **AIP 没强调这层，ablemind 更细** | `MUST-record-fibo-logical-path`、`fibo_mcp_client` |
| **自治整理 routine** | **Dream** 离线右脑整理 agent，读对话/工具/run，**只产候选**走同一管道；每 run ≤5 候选，必带 evidence_refs + why_long_term | **近**（cron 待 P2，现手动触发） | S7；`knowledge/dream.py`；`MUST-NOT-bypass-review` |
| **人审 / 护栏** | hitl 中断持久化 + `sensor-validation`（**shadow-before-flip 影子闸** + 调增益前置闸 + 4 维状态含 "ontology unvalidated"）+ multi-tenant fail-closed | **= 或更严** | `hitl-persistence.md`、`sensor-validation.md`、`ontology-constraint-sot` `MUST-shadow-before-flip-match-surface` |
| **决策血缘 / 学习闭环** | `knowledge_actions`/`review_decisions`/`message_events` 单表 replay+audit；6 类 decision signal（worker_terminal/controller/tool_outcome/final_answer/context_candidate/main_decision）| **仪表已建，学习用途待接** | `decision-signals.md`：**目前仅 1/6（worker_terminal）真 emit**，其余 middleware 在但未写表 |
| **逻辑柱（绑定模型）** | 逻辑 = LLM 推理 + MCP 工具 + 控制信号；`DERIVED_FROM` 只是**语义定义边**（NetMargin=NetProfit/Revenue），非可执行模型绑定 | **远** | 无 ModelOps / AutoML / Model-Adapter；plan 无量化模型生命周期 |
| **行动柱（写回外部系统）** | 写回**只到自己的知识图**（candidate→Neo4j），不写 ERP/组合/PMS；`ActionType` 标签 P1+ 规划中 | **最远（但是产品选择）** | plan：`ActionType — action semantics (P1+)` |

## 3. 三个真缺口——只有一个是硬欠债

**① 本体的"种类"不同：知识语义本体 vs 运营对象本体。**
ablemind 建模金融**含义**（概念/指标定义/公司身份/区分规则）；AIP 还建模**活的运营对象**（这一张订单、实时库存状态）+ 挂对象上的动作。
→ **对研究型产品，知识本体就是对的种类，运营对象层很可能本就不需要。** 这条多半不该补。

**② 逻辑柱：推理+MCP vs 绑定的确定性模型 + 生命周期。**（← **唯一硬欠债**）
没有把估值/盈利预测/筛选这类**确定性金融模型**做成带 ModelOps 的逻辑工具。`DERIVED_FROM` 是语义边不是可执行绑定。
→ 与定位一致的真缺口：要让 LLM 指挥家有"算得准的量化后端"，这柱得补。

**③ 行动柱：写回知识图 vs 写回外部运营系统。**
但 **"候选→审核→提交 + 人审闸"这个 PATTERN ablemind 已经有了**（用在知识图上）。把它接到外部系统（组合/下单/PMS）才是缺的。
→ 首先是产品问题：ablemind 要不要成为会动手改外部系统的东西？研究助手不该有这柱；要做执行就把现成 gate pattern 延伸过去。

## 4. 元洞察：同一个架构，三个独立实例

| 实例 | 本体/名词 | 事实层 | 候选收口 | 退役 | 自治 routine |
|---|---|---|---|---|---|
| **ablemind ontology-mem** | Neo4j 语义图（FIBO 锚） | `fact_observations` | `candidate_reviews` 状态机 | demote + 90 天留存 | Dream |
| **tech_air auto-wiki** | wiki 节点 + Neo4j-free data.db | `data_points`/`facts` | 候选 → review → commit | 退役不删除 + 双时态 | 心跳员/研究员 |
| **Palantir AIP/OAG** | Ontology（运营对象） | facts 层 | Scenario 三权分立 | 双时态 | （Foundry 管道） |

**三者是同一模式的三个独立实例。** 这个收敛本身证明：这不是 Palantir 营销话术，是个承重架构。而且 **ablemind 比 AIP 公开材料理解得更深**——plan 里那条三模型（Claude+Codex+Gemini）共识「**boundary > capacity**，防 false growth（概念数涨但 hit-rate 不涨、用户纠错不减、bundle 不缩）」，AIP 博客根本没讲到这层。

## 5. 若要往 AIP-operational 收敛（按杠杆排序）

1. **补逻辑柱（最该做）**：把 1–2 个确定性金融模型（估值/盈利预测）封成 MCP 工具或 LangGraph 子图，挂 ModelOps-lite 三层（建模目标/资产/适配器），让 `inspect_context` 之后能接"算"。
2. **激活已有学习闭环**：`decision-signals` 把剩下 5/6 信号真 emit 到 `message_events` + 上 P0 的 hit-rate 看板 + 30 天 auto-demote——已设计好，只差落地。
3. **行动柱按需**：仅当产品要"执行"时，把 candidate→review→commit 的 gate 延伸到外部系统；否则别建。

## 6. 关联与待结晶

- 若 ingest 进 `wiki/agent/分析/`：本篇作 analysis 页，`references` 边连 [[Palantir 本体]] / [[本体增强生成]] / [[决策中心架构]] / [[写回模式]] / [[沙盒情景]] / [[决策血缘]]。
- 可考虑新节点：`技术/` [[ModelOps]]（ablemind 缺、AIP 有，逻辑柱缺口的载体）；ablemind 侧若要建实体，单独起 ablemind 来源页已存在（`来源/2026-06-17-ablemind-able-alilab`）。
- 母本范式见 [[OAG范式-维护心智模型实现决策平台]]。

## 结论

- **认知/本体/治理层：ablemind ≈ AIP，治理（影子闸/sensor-validation）更严。**
- **三个缺口里两个是产品选择**（运营对象本体、外部写回），**一个是真欠债**（确定性模型当逻辑工具 + ModelOps）。
- 下一步若深挖：逻辑柱怎么补（ModelOps-lite for 金融模型）最有价值。
