# SOTA 模型接口需求 & 参考价格

> 数据源：OpenRouter `/api/v1/models` 实时 API，快照 **2026-06-22**
> 价格单位：USD / 百万 token（输入 in / 输出 out）

## 〇、接口协议对照

业界现在三种主流请求格式：**OpenAI Chat Completions**（事实标准，几乎所有家都兼容）、**OpenAI Responses API**（OpenAI 新的有状态/agent 格式）、**Anthropic Messages**（Claude 原生）。选型时只要确认目标模型支持你 SDK 用的那种格式即可。下表均已逐家核对官方文档（2026-06）。

| 厂商/平台 | 原生协议 | OpenAI Chat | OpenAI Responses | Anthropic Messages | Base URL |
|---|---|---|---|---|---|
| **OpenRouter**（聚合） | OpenAI Chat | ✅ 主推 | ✅ | ✅ `/messages` | `https://openrouter.ai/api/v1` |
| OpenAI | Chat + Responses | ✅ | ✅ 原生 | ❌ | `https://api.openai.com/v1` |
| Anthropic | Messages | ❌ | ❌ | ✅ 原生 | `https://api.anthropic.com/v1` |
| Google Gemini | `generateContent` | ✅ 官方兼容端点 | ❌ | ❌ | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| xAI Grok | OpenAI Chat | ✅ 原生 | ❌ | ✅ | `https://api.x.ai/v1` |
| DeepSeek | OpenAI Chat | ✅ | ❌ | ✅ | `https://api.deepseek.com` |
| Qwen / DashScope | 原生 + 兼容 | ✅ compatible-mode | ❌ | ✅ | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 智谱 GLM | 原生 + 兼容 | ✅ | ❌ | ✅ | `https://open.bigmodel.cn/api/paas/v4` |
| MiniMax | 原生 + 兼容 | ✅ | ❌ | ✅ | `https://api.minimax.io/v1` |
| Moonshot Kimi | OpenAI Chat | ✅ | ❌ | ✅ | `https://api.moonshot.cn/v1` |

要点：
- **走 OpenRouter 一把梭**：统一 OpenAI Chat 格式，换模型只改 `model` 字段，省去对接各家 SDK；代价是比直连原生贵几个点。Auth: `Bearer $OPENROUTER_API_KEY`，请求体 `model` = 下表 ID。
- **Responses API 目前只有 OpenAI 原生 + OpenRouter 转发**，别家都没有；要用 agent 长流程的有状态特性就直连 OpenAI 或走 OpenRouter。
- **Anthropic Messages 格式已是国产标配**（为接 Claude Code 普遍提供），各家 Anthropic 兼容 Base URL（配 `ANTHROPIC_BASE_URL` + `ANTHROPIC_API_KEY` 即可直接喂给 Claude Code）：
  - DeepSeek `https://api.deepseek.com/anthropic`（claude-opus→deepseek-v4-pro，claude-sonnet/haiku→deepseek-v4-flash）
  - 智谱 GLM `https://open.bigmodel.cn/api/anthropic`
  - MiniMax `https://api.minimax.io/anthropic`
  - Kimi `https://api.moonshot.cn/anthropic`
  - Qwen `https://dashscope-intl.aliyuncs.com/apps/anthropic`（仅新加坡区 key）
  - Grok：`https://api.x.ai` 同时兼容 OpenAI 与 Anthropic SDK
- **Gemini 没有 Anthropic 兼容**，但有官方 OpenAI 兼容端点；原生 `generateContent` 字段差别大（`contents`/`parts` vs `messages`），不想改代码就用它的 OpenAI 兼容端点。

## 一、旗舰 LLM（文本 + 视觉，第一梯队）

| 模型 | OpenRouter Model ID | 模态 | 上下文 | 输入 | 输出 |
|---|---|---|---|---|---|
| Claude Opus 4.8 | `anthropic/claude-opus-4.8` | text/image/file | 1M | $5.00 | $25.00 |
| GPT-5.5 | `openai/gpt-5.5` | text/image/file | 1.05M | $5.00 | $30.00 |
| GPT-5.4 | `openai/gpt-5.4` | text/image/file | 1.05M | $2.50 | $15.00 |
| Gemini 3.1 Pro | `google/gemini-3.1-pro-preview` | 全模态(含音视频) | 1M | $2.00 | $12.00 |
| Grok 4.3 | `x-ai/grok-4.3` | text/image | 1M | $1.25 | $2.50 |
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4.6` | text/image/file | 1M | $3.00 | $15.00 |

## 二、国产 LLM

| 模型 | OpenRouter Model ID | 模态 | 上下文 | 输入 | 输出 |
|---|---|---|---|---|---|
| Qwen3.7-Max | `qwen/qwen3.7-max` | text | 1M | $1.25 | $3.75 |
| GLM-5.2 | `z-ai/glm-5.2` | text | 1M | $1.00 | $4.00 |
| MiniMax M3 | `minimax/minimax-m3` | text/image/video | 1M | $0.30 | $1.20 |
| Kimi K2.6 | `moonshotai/kimi-k2.6` | text/image | 262K | $0.66 | $3.41 |

## 三、图像生成（OpenRouter 可直连的 image-output 模型）

| 模型 | OpenRouter Model ID | 模态 | 输入 | 输出 |
|---|---|---|---|---|
| GPT-5.4 Image 2 | `openai/gpt-5.4-image-2` | image/text/file | $8.00 | $15.00 |
| GPT-5 Image | `openai/gpt-5-image` | image/text/file | $10.00 | $10.00 |
| GPT-5 Image Mini | `openai/gpt-5-image-mini` | image/text/file | $2.50 | $2.00 |
| Gemini 3 Pro Image | `google/gemini-3-pro-image` | image/text | $2.00 | $12.00 |
| Gemini 3.1 Flash Image | `google/gemini-3.1-flash-image` | image/text | $0.50 | $3.00 |

> ⚠️ OpenRouter 主要是按 token 计费的 LLM/VLM。纯图像生成（Midjourney v7、Imagen 4 Ultra、FLUX.2 Pro、Ideogram v3、Seedream 5）多数**不在 OpenRouter**，需走各自原生 API 或 fal.ai / Replicate，且通常按**张数**计费。

## 四、视频生成（OpenRouter 暂未覆盖，走原生 API）

| 模型 | 渠道 | 参考价 |
|---|---|---|
| Google Veo 3.1 | Gemini API / Vertex AI | 按秒，4K 较贵 |
| Kling 3.0 | 快手 / fal.ai | 按秒，premium 里最便宜 |
| Seedance 2.0 | 字节 / fal.ai | ~$0.022/秒 |

---
注：价格按 OpenRouter default 路由取，部分模型有多家供应商、价格浮动；带 `-preview` 为预览版，可能变动。纯图像/视频生成计费逻辑是按张/秒而非 token。
