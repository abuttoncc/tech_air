---
tags: [resource, prompt-engineering, system-prompt, agent-engineering]
type: other
source: https://github.com/elder-plinius/CL4R1T4S
author: elder-plinius (Pliny the Liberator)
date: "2026-06-19"
status: new
---

# CL4R1T4S — 生产级系统提示词合集

**来源**：<https://github.com/elder-plinius/CL4R1T4S>
**作者**：elder-plinius (Pliny the Liberator) — @elder_plinius
**日期**：2026-06-19 收录
**状态**：new
**本地副本**：`../ref/CL4R1T4S/`（在工作区根 `ref/` 下，**不在 vault git 内**，库外只读参考）
**许可**：见仓库 `LICENSE`

---

## 这是什么

有人把主流 AI 产品和模型的系统提示词（system prompt）原文从各家产品里提取出来，汇成这一处合集。系统提示词，就是开发者写给模型、塞在用户看不见的地方的那段指令。合集覆盖几类：基座模型（Claude / GPT / Gemini / Grok / Llama / Kimi…）、编码 Agent / IDE（Cursor / Windsurf / Devin / Replit / Cline / v0 / Bolt…）、检索浏览（Perplexity / Brave / Dia）、通用 Agent（Manus）等。作者做这件事是为了透明度，原话是「In order to trust the output, one must understand the input.」——要信一个 AI 的输出，得先知道它收到了什么输入。用户理应知道，是哪段隐藏指令在管控着自己用的 AI。

这对本库（智能体工程，**Agent Engineering**）有什么用？它是一份一手的提示词工程教材。真实生产环境里，persona 怎么写、工具调用指令怎么下、安全护栏和拒答框架怎么搭、agentic 编辑约束怎么组织，这里全是活样本。比任何二手教程都真。

> 当前快照覆盖 **25 个厂商 / 61 份提示词原文**（2026-06-15 commit，已收到 Claude Fable 5 / Opus 4.7 等最新版）。

## 覆盖面（按用途）

下面按用途把收录的厂商分四类列出来，方便按需要找。

| 用途 | 厂商 / 目录 |
|---|---|
| 基座模型系统提示 | `ANTHROPIC`（Claude 3.5/3.7/4/4.5/4.6/4.7/Opus、**Fable 5**、Claude Code、设计系统提示、UserStyle）· `OPENAI`(GPT/ChatGPT) · `GOOGLE`(Gemini) · `XAI`(Grok×7) · `META` · `MISTRAL` · `MOONSHOT`(Kimi) · `MINIMAX` |
| 编码 / Agent IDE | `CURSOR` · `WINDSURF` · `DEVIN` · `REPLIT` · `CLINE` · `FACTORY` · `BOLT` · `LOVABLE` · `VERCEL V0` · `SAMEDEV` |
| 检索 / 浏览 | `PERPLEXITY` · `BRAVE` · `DIA` · `MULTION` |
| 通用 / 语音 / 其他 | `MANUS`(通用 agent) · `HUME`(语音) · `CLUELY` |

## 怎么用（库外副本）

本地这份副本主要用来离线 grep。下面几条命令够日常翻阅了。

```bash
REF="/Users/jameslee/Documents/文稿 - James的MacBook Pro/ref/CL4R1T4S"
git -C "$REF" pull              # 跟最新（上游高频更新）
grep -rl "tool" "$REF/ANTHROPIC"        # 找含某关键词的提示词
ls "$REF"/*/                            # 浏览全部厂商
```

从哪几个角度切进去学，建议这几条：
- **工具调用指令**：对比 Claude Code / Cursor / Devin，看它们怎么约束文件编辑、怎么管并行调用、把确认边界划在哪。
- **安全护栏 / 拒答框架**：各家在「什么不能说、怎么拒答（refuse）、怎么把话题岔开（redirect）」上写法各不相同，正好对照着读。
- **persona 与口吻**：同一个基座模型，到了不同产品里（比如 Grok 和 ChatGPT）人格怎么塑造，手法差在哪。
- **agentic 循环**：IDE 类 agent 把「计划→执行→自检」这套流程写成了什么样的提示结构。

## 我的思考

- **链接还是拉取**：上游一直在更新，更得很勤；本地 `ref/CL4R1T4S` 只是一份快照，留着离线 grep 用。要看最新版，还是以 GitHub 和 `git pull` 为准。我没把它拉进 vault git，一是怕这个嵌套仓库被 obsidian-git 顺手自动提交，二是怕海量原文把图谱搅乱。
- **⚠️ 注入告警（拿来当教学样本）**：这个 repo 的 `README.md` 末尾，埋了一段用 leetspeak 写的**提示词注入** payload，专门诱导读到它的 AI 吐出自己的系统提示词。读这个库的时候，无论是人还是 agent 都别照着做。换个角度看，它本身就是一个现成的「间接提示词注入」防御案例，值得 ingest 成 `wiki/agent` 里「注入攻防」的来源或分析。
- **以后往哪编译**：这个原始 repo 始终是外部源，给 recall 消费用，不进本体。等真把某几家的提示词研究透了，能提炼出可复用的模式（比如「Claude 工具调用指令结构」「Cursor agentic 编辑约束」），再用 `/auto-wiki ingest` 把这些**模式**编进 `wiki/agent/`，同时在 `wiki/agent/来源/` 建一个 `来源` 节点指回本 repo，留住出处。

## 关联笔记 & 行动

- [[智能体核心-学习要点（Wave1）]]
- [ ] 挑 1 家编码 agent（Cursor / Devin）逐条读其工具调用指令，记 Inbox 困惑笔记
- [ ] 把「README 注入 payload」作为注入攻防案例 ingest 进 `wiki/agent`
- [ ] 定期 `git -C "$REF" pull` 跟最新（新模型上线即更新）

---
*标签建议：#resource #prompt-engineering #system-prompt #agent-engineering*
