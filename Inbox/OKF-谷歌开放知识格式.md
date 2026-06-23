---
tags: [research, agent, knowledge-format]
type: research-note
status: open
topic: "OKF（Open Knowledge Format）：谷歌的 LLM-wiki 互操作标准"
created: "2026-06-23"
updated: "2026-06-23"
wiki-topic: "开放知识格式"
compiled: false
digested:
triage:
sinks: []
source:
  - "Google Cloud Blog: How the Open Knowledge Format can improve data sharing（2026-06）"
  - "GitHub: GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md（v0.1）"
  - "MarkTechPost / Search Engine Journal 报道（2026-06-16）"
---

# OKF：谷歌的开放知识格式

> 一句话：谷歌云把「给 AI agent 喂结构化上下文」这件事，定成了一个不绑平台的开放格式——**一堆带 YAML frontmatter 的 markdown 文件，互相用 markdown 链接连成图**。说白了，就是把我这套 `wiki/` 干的事写成了行业标准。

## 困惑与问题

- OKF 到底规定了什么、没规定什么？跟我的 auto-wiki `wiki/` 有多像、差在哪？
- 它跟刚 ingest 的 OAG / 决策中心架构是什么关系？
- 我要不要让 `wiki/` 跟 OKF 兼容（能导出/被 agent 直接吃）？

## 已知信息（它是什么）

谷歌云 2026-06 发布，v0.1，开源在 GitHub（`GoogleCloudPlatform/knowledge-catalog`）。定位是**格式不是平台、不是服务**：不绑云、不绑数据库、不绑模型商、不需要 SDK 或账号就能读写。源头是 Karpathy 说的「LLM-wiki」——人维护个人 wiki 会因为交叉引用太烦而放弃，但 LLM 不嫌烦、一遍能改 15 个文件，所以让 agent 来维护 wiki 正合适。

## 研究过程

### 发现 1 — 格式本体（极简）

- **bundle**＝分发单位＝一个目录树，全是 `.md`。保留文件：`index.md`（目录/渐进披露，可选）、`log.md`（变更史，可选）。
- **concept**＝一个 `.md` 文件。**ID = 文件相对路径去掉 `.md`**（`tables/users.md` → `tables/users`）。
- **frontmatter**：唯一必填是 `type`（自由字符串，无中央注册表，消费方要容忍未知 type）。推荐 `title / description / resource(URI) / tags / timestamp(ISO8601)`。允许任意扩展字段，消费方必须保留不认识的字段、不许拒读。
- **正文**：鼓励用结构化 markdown（标题/列表/表格/代码块）而非散文。软约定章节：`# Schema`、`# Examples`、`# Citations`（外部来源放编号引用）。
- **版本**：根 `index.md` 里写 `okf_version: "0.1"`；`major.minor`，消费方尽力消费不要因版本未知拒读。

### 发现 2 — 关系是「无类型」的（关键差异点）

> A 文件里有一条指向 B 的 markdown 链接 = 断言「A 和 B 有关系」。**具体什么关系（父子/引用/join/依赖）靠周围散文表达，链接本身不带类型。** 整个目录因此成为一张有向图。**断链是允许的**——可能代表「还没写的知识」。

链接两种写法：绝对（`/` 开头，从 bundle 根算，推荐，稳定）/ 相对路径。

### 发现 3 — 设计三原则 + 非目标

- **最小武断**：只强制一个 `type`，其余全交给生产者。「spec 定的是互操作界面，不是内容模型」。
- **生产者/消费者解耦**：人手写的 bundle 能被 agent 吃；导出管道生成的能被可视化器浏览；一个 LLM 合成的能被另一个 LLM 查询。
- **格式非平台**：开放标准，价值来自多少方说这门语言，不来自谁拥有它。
- **非目标**：不定死 type 分类法；不规定存储/服务/查询基础设施；不取代 Avro/Protobuf/OpenAPI（**引用**它们，不吞并）。
- **优雅降级**：缺字段、未知 type、未知 key、断链、缺 `index.md` 全部合规。

### 发现 4 — 参考实现（产/消两端各一个）

- **生产端**：enrichment agent 遍历 BigQuery 数据集，给每张表/视图起草一个 OKF concept，再跑第二遍 LLM 爬权威文档、补 citations / schema / join 路径。
- **消费端**：单文件静态 HTML 可视化器，把任意 bundle 变成交互图，无后端、数据不出页。
- 样例 bundle：GA4 电商 / StackOverflow / Bitcoin 公共数据集。
- 谷歌云 Knowledge Catalog 已能 ingest OKF 并喂给自家 agent。

## OKF vs 我的 auto-wiki（这才是重点）

同一个母题（LLM 维护的 wiki / 心智模型的「名词层」），我的实现**严格得多**，OKF **宽松得多**：

| 维度 | OKF v0.1 | tech_air auto-wiki |
|---|---|---|
| 载体 | 目录 + `.md` + YAML frontmatter | 一样 |
| 目录/历史文件 | `index.md` + `log.md` | hub（`领域中文名.md`）+ `log.md`（思路一致，hub 不叫 index） |
| 链接 | markdown 链接，**无类型**，关系靠散文 | `[[wikilink]]` + **受控关系词表**（typed，`relations[]` 双写 data.db） |
| 节点类型 | 只强制 `type`，自由字符串 | 7 种判据严格（实体/概念/事件/分析/来源…） |
| 数值/时序 | 留在 markdown 表格里 | **不进页，进双时态 `data.db`**（T0-T5 六档 + 退役不删除） |
| 断链 | 合规（= 待写） | lint 当问题报 |
| 哲学 | 互操作优先，最小武断 | 严谨优先（决策平台要可溯源/可时间旅行） |

**判断**：OKF 是「互操作下限」，我的库是「严谨上限」。两者不冲突——我的 `wiki/` 几乎是 OKF 的超集，**导出成 OKF 基本是降维投影**（typed 边塌成无类型链接、data.db 数值塞回 markdown 表）。

## 关联 OAG（接上一篇）

OKF 正好补在 [[OAG决策平台范式]] 的 **Data / 名词层（语义）** 那一柱：它是「给 agent 喂 curated context」的标准容器。但 OKF **只管名词**——没有 Logic（逻辑绑定/工具）、没有 Action（写回/沙盒）、没有决策血缘。所以 OKF ⊂ OAG：OKF 是 Palantir 本体「语义层」的一个开放、轻量、不绑平台的平替；OAG 在它之上还要逻辑和行动两柱。

## 结论与行动

- **结论**：OKF = LLM-wiki 的开放互操作标准，谷歌主推、v0.1、极简。我这套库本来就在干这事且更严，OKF 给了我一个「对外说话的格式」和一个「别人的 agent 能直接吃我的知识」的通道。
- **下一步可选**：
  1. ingest 进 `wiki/agent`：建 `开放知识格式`(OKF) 节点（原理/标准类）+ `alternative_to` 或对比边连 [[本体增强生成]]/[[Palantir 本体]]，落一篇 `分析/OKF vs auto-wiki`。
  2. 工程实验：写个小导出器 `wiki/{domain}` → OKF bundle（hub→index.md、relations[] 降成链接、data.db 数值回填 markdown 表、加 okf_version），验证「我的库能被任意 OKF 消费者吃」。
  3. 反向借鉴：OKF 的 `# Schema/# Examples/# Citations` 软章节、`resource` URI 字段，值得考虑吸收进我的 wiki-format。
