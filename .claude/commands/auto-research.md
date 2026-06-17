---
description: 手动触发 auto research（morning=问答库例行 / evening=盘后板块数据）
argument-hint: morning | evening
---

按参数执行对应例行任务。参数：$ARGUMENTS（缺省视为 morning）。

## morning — 问答库例行

执行今日例行任务（daily-routine skill）：

1. 扫 `07-QA/`，只跑到期的动态问题：recall → 复盘上周期已发生 → 推演本周期情景 → 缺口 deep-dive → ingest 回 wiki → append 答案 → 回写 Daily。
2. 严守库内纪律：答案 append 不覆盖；ingest 走退役不删除协议；数值进 data.db 不进正文。
3. 需要人工决策或数据矛盾的地方不要猜，写进当天 `05-Daily` 的「待人工确认」小节。

## evening — 盘后板块数据

1. 用 ablemind-findata 拉今日申万一级 31 个行业指数的当日成交额与涨跌幅：先 `get_industry_overview(action=classify, level=L1, src=SW2021)` 拿指数代码，再对每个代码 `get_historical_data` 取当日。注意 amount 单位是万元；用 `get_market_summary` 的全市场总量做交叉验证（其 total 实际单位是千万元，文档标注的亿元不可信）。
2. 生成当日板块成交额排名表 + 一句话轮动结论，写进当天 `05-Daily` 笔记的「## 盘后数据」小节（当日 Daily 不存在则按 `06-Templates` 模板新建）。
3. 若排名揭示了值得沉淀的结构性变化（如某板块成交占比突破历史区间），按 auto-wiki ingest 协议把观测写进对应域；日常波动只留在 Daily，不进 wiki。
4. 若返回的 trade_date 不是今天，说明数据未落库，在 Daily 记一句「盘后数据未更新」后结束。
5. 若 07-QA 有到期动态问题，顺带按 daily-routine 处理。

## 收尾（两种模式通用）

会话内跑属**交互模式**（陋居纪律见 `08-Ops/README.md`）：高危写入（newnode/retire/disputed/xedge）当场问用户裁决并记审批账，不落候选；跑完更新对应 agent 契约（`08-Ops/routines/`）的 last-run / last-result，QA 答案回写 last-summary。

最后给出汇报：跑了什么、各自一句话结论、ingest 了什么、审批账本记了几笔、有什么待人工确认项。git 提交交给 obsidian-git 自动备份，不需要手动 push。
