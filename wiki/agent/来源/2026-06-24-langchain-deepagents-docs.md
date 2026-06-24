---
title: LangChain Deep Agents 官方文档（subagents / code）
type: source
created: 2026-06-24
updated: 2026-06-24
sources: []
confidence: high
source_type: 一手
source_origin: docs.langchain.com/oss/python/deepagents
source_date: 2026-06-24
aliases: [deepagents docs, deep agents subagents doc, AGENTS.md spec]
---

# LangChain Deep Agents 官方文档（subagents / code）

deepagents 把「一个 agent 是什么」表达成**声明（数据）**而非**控制流（代码）**。摘自官方 docs 的关键事实：

## SubAgent 字典声明

`create_deep_agent(subagents=[...])` 的 `subagents` 接受一组**字典**，每个字典即一份 agent 规格说明书（`SubAgent` spec）：

| 字段 | 必填 | 含义 |
|---|---|---|
| `name` | 是 | 唯一标识，主 agent 调 `task()` 工具时用这个名字 |
| `description` | 是 | 干什么；主 agent 据此**决定何时把活派过来** |
| `system_prompt` | 是 | 给这个 subagent 的指令；自定义 subagent 必须自带，不继承主 agent |
| `tools` | 否 | 工具集，默认继承主 agent，指定则整体覆盖 |
| `model` | 否 | 覆盖主 agent 模型（`provider:model` 串或 chat model 对象） |
| `middleware` / `interrupt_on` / `skills` / `response_format` / `permissions` | 否 | 中间件 / 人审 / 技能 / 结构化输出 / 文件权限 |

例：
```python
research_subagent = {
    "name": "research-agent",
    "description": "Used to research more in depth questions",
    "system_prompt": "You are a great researcher",
    "tools": [internet_search],
    "model": "openai:gpt-5.5",
}
agent = create_deep_agent(model="google_genai:gemini-3.5-flash",
                          subagents=[research_subagent])
```

## AGENTS.md：subagent 即一个 markdown 文件

Deep Agents Code 把 subagent 定义成磁盘上的 markdown 文件，引擎自动发现：
```
.deepagents/agents/{name}/AGENTS.md          # 项目级
~/.deepagents/{agent}/agents/{name}/AGENTS.md # 用户级（项目级覆盖用户级）
```
frontmatter 写 `name` / `description` / 可选 `model`；**markdown 正文整段就是 `system_prompt`**。其它字段（tools/middleware/skills）经此法定义时不可配，继承主 agent，要全控制走 SDK。

## 代码兜底：CompiledSubAgent

复杂工作流时，subagent 也可以是 `CompiledSubAgent`——传一个**编译好的 LangGraph 图**（`runnable` 字段，须先 `.compile()`），由 `create_agent` 或自定义 graph API 构造。即「声明式优先、代码兜底」。

## 执行循环归引擎

agent 的运行循环、规划（`write_todos`）、文件系统（ls/read_file/write_file/edit_file）、子 agent 派发（`task`）、上下文压缩、人审，都是 deepagents 这个公共引擎内置的，对所有声明一视同仁。配置只声明「是什么」，「怎么跑」不写。
