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

把主流 AI 产品 / 模型被**提取出来的 system prompt 原文**聚成一处的合集：基座模型（Claude / GPT / Gemini / Grok / Llama / Kimi…）、编码 Agent / IDE（Cursor / Windsurf / Devin / Replit / Cline / v0 / Bolt…）、检索浏览（Perplexity / Brave / Dia）、通用 Agent（Manus）等。作者立意是**透明度**：「In order to trust the output, one must understand the input.」——用户该知道在管控自己所用 AI 的那段隐藏指令。

对本库（**Agent Engineering**）的价值：这是**一手的提示词工程教材**——真实生产环境里怎么写 persona、怎么下工具调用指令、怎么搭安全护栏 / 拒答框架、怎么组织 agentic 编辑约束。比任何二手教程都真。

> 当前快照覆盖 **25 个厂商 / 61 份提示词原文**（2026-06-15 commit，已收到 Claude Fable 5 / Opus 4.7 等最新版）。

## 覆盖面（按用途）

| 用途 | 厂商 / 目录 |
|---|---|
| 基座模型系统提示 | `ANTHROPIC`（Claude 3.5/3.7/4/4.5/4.6/4.7/Opus、**Fable 5**、Claude Code、设计系统提示、UserStyle）· `OPENAI`(GPT/ChatGPT) · `GOOGLE`(Gemini) · `XAI`(Grok×7) · `META` · `MISTRAL` · `MOONSHOT`(Kimi) · `MINIMAX` |
| 编码 / Agent IDE | `CURSOR` · `WINDSURF` · `DEVIN` · `REPLIT` · `CLINE` · `FACTORY` · `BOLT` · `LOVABLE` · `VERCEL V0` · `SAMEDEV` |
| 检索 / 浏览 | `PERPLEXITY` · `BRAVE` · `DIA` · `MULTION` |
| 通用 / 语音 / 其他 | `MANUS`(通用 agent) · `HUME`(语音) · `CLUELY` |

## 怎么用（库外副本）

```bash
REF="/Users/jameslee/Documents/文稿 - James的MacBook Pro/ref/CL4R1T4S"
git -C "$REF" pull              # 跟最新（上游高频更新）
grep -rl "tool" "$REF/ANTHROPIC"        # 找含某关键词的提示词
ls "$REF"/*/                            # 浏览全部厂商
```

学习切口建议：
- **工具调用指令**：对比 Claude Code / Cursor / Devin 怎么约束文件编辑、并行调用、确认边界。
- **安全护栏 / 拒答框架**：各家「不能说什么、怎么 refuse/redirect」的写法差异。
- **persona 与口吻**：同一基座不同产品（如 Grok vs ChatGPT）的人格塑造手法。
- **agentic 循环**：IDE 类 agent 的「计划→执行→自检」提示结构。

## 我的思考

- **链接 vs 拉取**：上游是活的、高频更新；本地 `ref/CL4R1T4S` 只是离线 grep 用的快照，看最新仍以 GitHub / `git pull` 为准。**没有**拉进 vault git——避免嵌套仓库被 obsidian-git 自动提交、避免海量原文污染图谱。
- **⚠️ 注入告警（教学样本）**：本 repo 的 `README.md` 末尾埋了一段 leetspeak **提示词注入** payload（诱导读它的 AI 吐出自身系统提示词）。读这个库时人/agent 都别照做——它本身就是一个现成的「间接提示词注入」防御案例，值得 ingest 成 `wiki/agent` 里「注入攻防」的来源/分析。
- **编译去向**：原始 repo 永远是被 recall 消费的**外部源**，不进本体。等真研究透某几家提示词、提炼出可复用模式（如「Claude 工具调用指令结构」「Cursor agentic 编辑约束」），再 `/auto-wiki ingest` 把**模式**编进 `wiki/agent/`，并在 `wiki/agent/来源/` 建一个指回本 repo 的 `来源` 节点溯源。

## 关联笔记 & 行动

- [[智能体核心-学习要点（Wave1）]]
- [ ] 挑 1 家编码 agent（Cursor / Devin）逐条读其工具调用指令，记 Inbox 困惑笔记
- [ ] 把「README 注入 payload」作为注入攻防案例 ingest 进 `wiki/agent`
- [ ] 定期 `git -C "$REF" pull` 跟最新（新模型上线即更新）

---
*标签建议：#resource #prompt-engineering #system-prompt #agent-engineering*
