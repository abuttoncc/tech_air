# Tech Air — 项目说明（给 Agent 读的指令文件）

Obsidian 个人**技术学习**知识库，主题是**智能体工程（Agent Engineering）**及其全栈基底（前后端 / 数据库 / 存储 / 容器 / 服务器 / CICD）。与 `valu_air`（金融投研）、`philo_air`（哲学）同范式、同引擎（见第五节 burrow-core）。**两层架构**：

- **PARA 工作层**（人写人看，按行动/时效组织）：学习笔记、踩坑、实践项目、日记。
- **知识本体层 `wiki/`**（编译产物，按**领域 domain** 组织）：结构化本体，进 git、进 Obsidian 图谱。

**编译方向单向**：`Inbox(学习散文) → /auto-wiki ingest → wiki(结构化本体)`。wiki 只反向被 `recall` 消费。**严谨用在已结晶的知识（wiki），不用在正在结晶的学习笔记（Inbox）。**

> 权威真相源是每个领域的 `wiki/{domain}/_ontology.md`（v2 本体契约），母本是 `wiki/agent/_ontology.md`。`ingest`/`recall` 前先读它 + `wiki/_index.md` 路由。

---

## 一、PARA 工作层

| 文件夹 | 用途 |
|--------|------|
| `00-Dashboard/` | 仪表盘（dataviewjs，引擎来自 burrow-core，勿手改） |
| `01-Projects/` | 活跃实践项目（搭一个 agent / 部署一套服务，有目标和 deadline） |
| `02-Areas/` | 持续跟进的技术方向 |
| `03-Resources/` | 文档/教程/速查 |
| `04-Archive/` | 已完成/归档 |
| `05-Daily/` | 每日笔记 |
| `06-Templates/` | 模板 |
| `07-QA/` | 问答库（动态问题=时间序列，append-only） |
| `08-Ops/` | 陋居自动化层：agent 契约 / run 记录 / 审核队列 / 审批账本 |
| `09-Attachments/` | 附件 |
| `Inbox/` | 收集箱：学习散文、踩坑记录、研究课题，每条独立文件 |

学习在 Inbox 用研究笔记模板写「困惑 / 目标 / 思路 / 线索」，学透后用 `/auto-wiki ingest` 编译进 `wiki/`。

---

## 二、知识本体层 `wiki/` — auto-wiki v2

引擎在 `.claude/skills/auto-wiki/`，脚本在其 `references/`（`schema.py` 校验、`store.py` 操作 `data.db`、`expand.py` 图谱遍历、`new_domain.py` 建域）。**这些 .py 由 burrow-core 同步，勿手改**（见第五节）。

### 四个域 × 两个方向

`wiki/{domain}/`，扁平并列（不做 `wiki/{方向}/{域}/` 两层，以免破坏 `data.db` 路径假设）。`direction` 是 `meta.yaml` 字段。

| 方向 | 域 | 中心实体 | 范围 |
|---|---|---|---|
| 智能体 | `wiki/agent/` | 智能体工程 | Agent 框架 / RAG / 编排 / 记忆 / 工具调用 / 评测（**母本域**）|
| 全栈 | `wiki/web/` | 全栈应用 | 前端 + 后端 |
| 全栈 | `wiki/data/` | 数据层 | 数据库 + 存储 |
| 全栈 | `wiki/infra/` | 运行时基础设施 | 容器 + 服务器 + CICD |

**路由**：`wiki/_index.md` 是自动生成的域注册表（`new_domain.py --reindex` 扫 `meta.yaml` 重建）。`ingest`/`recall` 第 0 步先读它，按关键词命中域；横跨多域则双写 + 跨域连边。

**跨域驱动边**：智能体工程构建在全栈技术之上。agent 用签名边 `built_on`（agent 节点 → web/data/infra 节点，跨域）表达「智能体能力 → 依赖的底层技术」；同一专名物（如 PostgreSQL、Docker）全库只建一次，另一域连边引用（单一中文/英文 slug 全库唯一）。

**继承式本体**：引擎是公共底座，`agent` 是母本，新域 `_ontology.md` 只声明自己特有的类型判据 + 关系词，其余沿用 agent 母本。建新域一条命令：
```
python .claude/skills/auto-wiki/references/new_domain.py <name> \
  --direction <方向> --central <中心实体> --hub <中文名> --desc "<范围>" \
  --types "技术,原理,模式,事件,分析,来源" --keywords "kw1,kw2,..."
```

### 节点类型与判据：实体 vs 概念

> **核心判据**：能用手指指向「就是这一个」、明年同名还指同一个 → **实体（individual）**；必须先讲一段机理/定义才懂 → **概念（class）**。

| 类型 | 子目录 | 实体/概念 | 例子 |
|---|---|---|---|
| 技术/工具 | `技术/` | 实体 | LangGraph、PostgreSQL、Docker、React、Kubernetes、FastAPI、Redis |
| 原理/机制 | `原理/` | 概念 | RAG、反向传播、MVCC、一致性哈希、事件循环、向量检索、共识算法 |
| 模式/架构 | `模式/` | 概念 | 多智能体编排、微服务、CQRS、Sidecar、Event Sourcing、ReAct |
| 事件 | `事件/` | 事件 | 2025-xx-某框架 v2 发布、某里程碑 |
| 分析 | `分析/` | 派生视图 | 「RAG 全景」「容器编排对比」（研究课题，删了不影响本体）|
| 来源 | `来源/` | 来源 | 官方文档 / 论文 / talk / 博客 |

三分铁律：**数值/benchmark 进 data.db 不建节点** · **关系是边不是页** · **分类标签（智能体/前端/后端/数据库/存储/容器/服务器/CICD）是 `classified_as` 边不建页**。

### 受控关系词表（边非页，越界边被 lint 拒绝）

`depends_on`(技术→技术，运行/构建依赖) · `built_on`(技术→技术/原理，基于…构建；**跨域签名边** agent→全栈) · `implements`(技术→原理/模式) · `instance_of`(技术→模式) · `part_of`(组成) · `alternative_to`(技术↔技术，同类替代/竞品) · `runs_on`(技术→技术，运行于…之上) · `classified_as`(技术→层标签) · `created_by`/`changed_by`(→事件) · `references`(分析/来源→任意，溯源)。

双写：页面 `frontmatter.relations[]`（给 Obsidian 连边）+ `data.db relations 表`（给查询/校验），两者一致。

### 6 档时间模型 + 退役不删除（同引擎）

T0 观测值（data_points）· T1 状态/制度态（facts 拉链）· T2 耐用逻辑（机制页 + durability）· T3 实体/近永久关系（relations 带时态）· T4 事件（append-only）· T5 类型公理（_ontology + DB CHECK）。

> 例：「某框架当前推荐的编排方式 = X」是 **T1**（facts，被版本事件切换）；「某 benchmark 某次测得 = 12ms」是 **T0**（data_points）。

**退役不删除**：覆盖原值只允许 T0 同 period 纠错；T1/T2/T3 的任何变化都是「旧行封 `valid_to` + 插新行」，永不 DELETE，追溯到一个 T4 事件页。

### data.db（每域一个，双时态，SQLite，由 store.py 操作）

核心表 `data_points`(T0) / `facts`(T1+T2) / `events`(T4) / `relations`(T3 带时态)。**命名纪律**：单一 slug = 文件名 = `[[wikilink]]` = `data.db` 主键，跨来源去重靠 `aliases:`。运行产物 `data.db-wal/-shm` 不入库。

### 五个模式（auto-wiki skill）

`recall`（加载本体上下文）· `ingest`（编译源材料→建/合并节点→写时间表→退役协议→校验）· `query`（单次取答）· `lint`（断链/越界边/矛盾/覆盖率）· `deep-dive`（lint 找缺口 + ingest 填充）。

---

## 三、编译生命周期

① Inbox 用研究笔记模板写困惑/目标/思路 → ② 调 MCP / web / 官方文档 / 论文取材 → ③ `ingest`：先读 `_index` 路由命中域 → 查 canonical 合并 or 按决策树建节点 → 定 6 档时间档写表 → 补受控关系边 → 退役协议 → 落 `分析/` + 更新 Hub + `log.md` → `schema.py` 校验 → 刷新 `position_encoding.py` + `--report` → ④ Obsidian Graph / `_report.html` 呈现知识网。

---

## 四、MCP / 取材通道

智能体工程取材走：`context7`（库/框架文档）· web 搜索 / arxiv（论文）· `follow-builders`（AI builder 动态，只用其 fetch 产出，不用 digest/telegram 投递）· 官方 docs。`.mcp.json` 按需加项目级 server。**金融 MCP（gangtise/juzi/ablemind/fibo）不适用本库**。

---

## 五、burrow-core 共享引擎（关键）

Dashboard（`00-Dashboard/Dashboard.md` + `.obsidian/snippets/dashboard.css`）与 auto-wiki python 引擎（`references/{schema,store,position_encoding,expand,new_domain}.py`）**不是本库手写的**，来自父目录的 `burrow-core` 包（`pip install`，与 valu_air/philo_air 共享）。

- 个性化全在 `.burrow/config.json`（title/order/labels/navOntology/features/relations/new_domain）。
- 改**引擎/布局**：改 `burrow-core/burrow/core/`，在父目录跑 `burrow sync --all`。**别手改本库的 Dashboard.md / 那些 .py**（文件头标了「勿手改」，会被下次 sync 覆盖）。
- 改**本库个性**：改 `.burrow/config.json`，跑 `burrow sync tech_air`。

---

## 六、同步约定

- `.claude/`（skill 引擎）+ `wiki/`（本体）+ `.burrow/`（配置）进 git，别人 pull 即得；仅 `.claude/settings.local.json` 排除。
- `wiki/` 必须可见（非 dotfolder），进 Obsidian Graph。`obsidian-git` 自动提交推送。
- 数值/海量行情不进 wiki；data.db-wal/-shm 不入库。

---

## 七、陋居自动化层（08-Ops）

人做深度学习与全局掌控，「当 X 发生 → 做 Y」的模式化劳动交给受契约约束的 agent（routine）。原则：产出收口（无人值守只投候选不直写正典）· 捕获免费晋升收紧 · 连续批准升级一次驳回降级 · 确定性优先。`routines/` agent 契约 · `runs/` 运行记录 · `review/` 审核队列 · `审批账本.md` 信任账本 · `pulse/` 今日启发束（心跳员产出）。高危写入 gate：`newnode`/`xedge`(跨域 built_on 边)/`t0-merge` 可升自动；`retire`/`disputed` 永久人工。
