---
title: 智能体核心 · 代码走查（Wave 1）
type: resource
created: 2026-06-19
updated: 2026-06-19
tags: [学习, 代码走查, ablemind, 智能体工程]
related: ["[[智能体核心-学习要点（Wave1）]]", "[[ablemind-知识提炼]]"]
---

# 智能体核心 · 代码走查（Wave 1）

> 配套 [[智能体核心-学习要点（Wave1）]] 的"第二步：回代码"。所有 `文件:行号` 指 `/Users/jameslee/ablemind/able-alilab`，在仓库里可点开对照。
> 怎么用：开着 ablemind，顺着每个主题的"调用链"往下读，对照"必看代码"，最后照"自己 trace"走一遍。

## 一条请求的全景（五主题怎么串起来）

```
启动期：server.py lifespan → init_persistence()（建 PG checkpointer/store，全局单例）
构建期：build_agent() → build_runtime_assets()（装配资产，含 middleware 栈 + checkpointer）
        → create_agent_from_assets() → deepagents.create_deep_agent()（图编译，挂上 checkpointer）
运行期：adapter.run() → build_pipeline()（接上 PersistenceTap）
        → LangGraphAdapter 消费图事件 → 中间件富化/旁路 → StreamWriter 序列化 → SSE 到浏览器
模型层：每次 model call 经 RouterChatModel（供应商中立 + 推理内容回传处理）
```

主题 A=构建期、B=启动期落盘、C=中间件栈、D=运行期出流、E=模型层。下面逐个拆。

---

## 主题 A · 框架栈：构建一个 agent（装配 ≠ 编译）

**调用链**：
```
graph.py:76  build_agent()
  └─ runtime_assets.py:92  build_runtime_assets()        # 收集资产
       └─ assembly.py:527  _agent_common_setup()         # checkpointer = get_checkpointer()
       └─ assembly.py:562  build_middleware_stack()       # 见主题 C
  └─ runtime_assets.py:587 create_agent_from_assets()     # 编译
       └─ runtime_assets.py:629 deepagents.create_deep_agent(**kwargs)
```

**必看代码**：

`runtime_assets.py:25` —— RuntimeAssets 是"装配好但还没编译"的数据容器：
```python
@dataclass
class RuntimeAssets:
    model: Any
    tools: list[Any]
    subagents: list[Any]
    checkpointer: Any        # ← 状态持久化
    store: Any               # ← 记忆存储
    middleware: list[Any]
    identity_files: list[str]
    system_prompt: str
```

`runtime_assets.py:587` —— 编译只是把资产喂给 deepagents，checkpointer 此刻才挂上图：
```python
def create_agent_from_assets(assets: RuntimeAssets) -> Any:
    from deepagents import create_deep_agent
    kwargs = dict(
        model=assets.model, tools=assets.tools, middleware=assets.middleware,
        checkpointer=assets.checkpointer,   # ← 状态化执行从这里进图
        store=assets.store, subagents=assets.subagents, name="dpagt-main",
    )
    agent = create_deep_agent(**kwargs)
    return agent
```

**看懂了什么**：build 拆成两步——`build_runtime_assets`（收集）→ `create_agent_from_assets`（编译）。解耦的好处：QueryExecutor 等下游能**先检查/改 assets 再编译**，能在中间插权限/限流中间件，缓存键按"资产组合"而非图实例分层。这就是 wiki 里 [[deepagents]] →built_on→ [[LangGraph]] 的代码现场。

**自己 trace**：`graph.py:76` → `runtime_assets.py:92` →（资产从哪来）`assembly.py:527` →（编译）`runtime_assets.py:629`。

---

## 主题 B · 状态化执行：checkpoint 到底怎么落盘

**调用链**：`server.py` lifespan 启动 → `persistence.py:79 init_persistence()` → 全局 `_checkpointer` → `get_checkpointer()` 被 assembly 取用。

**必看代码**：

`persistence.py:79` —— 这段把"状态化执行"落到实处，注意 TCP keepalive 的注释（这是 SSE 卡死的真实根因）：
```python
# TCP keepalive：旧 idle=60+interval=10×5=110s 检测死连接 → SSE 卡死根因
# 新 idle=15+interval=5×3=30s，对齐 tcp_user_timeout
_keepalive_defaults = {"keepalives": "1", "keepalives_idle": "15",
    "keepalives_interval": "5", "keepalives_count": "3", "tcp_user_timeout": "15000"}
...
_cp_pool = AsyncConnectionPool(db_url, min_size=1, max_size=5,
    max_idle=300, max_lifetime=1800, reconnect_timeout=10, ...)
_checkpointer = AsyncPostgresSaver(conn=_cp_pool)
await _checkpointer.setup()
```

`persistence.py:164` —— 全局单例访问器，整个系统靠这两个函数拿到落盘能力：
```python
def get_checkpointer() -> AsyncPostgresSaver | None: return _checkpointer
def get_store() -> AsyncPostgresStore | None: return _store
```

**看懂了什么**：[[状态化执行]] 这个抽象，落地就是 `AsyncPostgresSaver`——LangGraph 每个 step 后内部调 `checkpointer.put(config, values, ...)` 写 PG、`get(config)` 恢复。`DATABASE_URL` 没配就降级到内存（优雅降级）。这就是 [[LangGraph]] →built_on→ [[PostgreSQL]] 那条跨域边的代码现场。

**自己 trace**：`server.py` 找 `await init_persistence()` → `persistence.py:79` 看连接池与 keepalive → `persistence.py:164` 看单例 → 回 `assembly.py:527` 看谁取用。

---

## 主题 C · 中间件分层编排：能力是"装配"出来的

**调用链**：`middleware.yaml`（声明顺序）→ `middleware_registry.py:545 build_middleware_stack()`（读 yaml + 调工厂）→ 产出实例栈 → 进 `create_deep_agent(middleware=...)`。

**必看代码**：

`middleware.yaml:33` —— "顺序 + 装哪些"一目了然（基础设施层）：
```yaml
stack:
  - name: hitl                          # MUST 首位（中断是框架级控制流）
  - name: tool_budget_actionable_hint
  - name: model_retry
    config: { max_retries: 2, backoff_factor: 2.0 }
  - name: tool_retry
  - name: model_call_limit              # MUST 在 retry 后（limit 只数成功的 call）
```

`middleware_registry.py:545` —— 注册表按 yaml 顺序调工厂，工厂返回 1 个 / list / None：
```python
def build_middleware_stack(ctx: MiddlewareBuildContext, path=None) -> list:
    for entry in load_stack_config(path):           # load 时 fail-loud 拒未注册/重复
        if not entry.get("enabled", True): continue
        mw = REGISTRY[entry["name"]](ctx, **(entry.get("config") or {}))
        if mw is None: continue
        if isinstance(mw, list): stack.extend(m for m in mw if m)  # fan-out
        else: stack.append(mw)
    return stack
```

`middleware_registry.py:316`（节选）—— 一个工厂可 fan-out 多实例（PII 每类一个）：
```python
def _pii(ctx, **cfg):
    if os.environ.get("PII_GUARD_ENABLED", "on") in ("off","0","false"): return None
    rules = [("email", None), ("credit_card", None),
             ("id_card_cn", r"(?<!\d)\d{17}[\dXx](?!\d)")]   # 中国身份证
    return [PIIMiddleware(t, strategy=strategy, detector=d, ...) for t, d in rules]
```

**看懂了什么**：① 改 agent 行为只动 `middleware.yaml`，不碰 Python 主循环；② 顺序有契约（`dpagt/docs/spec/middleware/chain-order.md` 的 MUST：hitl 必首、retry 在 limit 前…），还有 `tests/spec/test_middleware_chain_order.py` 自动校验；③ 执行时 `abefore_model` 按列表正序、`aafter_model` 反序——这点最容易看漏。这就是 [[中间件分层编排]] 的现场。

**自己 trace**：`middleware.yaml` 看声明 → `middleware_registry.py:545` 看怎么物化 → 挑一个工厂（如 `_hitl` / `_pii`）看签名 → `chain-order.md` 看为什么这个顺序。

---

## 主题 D · 协议桥接管道：输出怎么到浏览器（单点守门）

**调用链（三层）**：
```
LangGraphAdapter.stream()  消费图的 astream（messages/updates/custom/tasks 四通道）
  → 统一事件 UiProtocolEvent（TextDelta/ToolCall/Finish/Error/DataChannel）
  → 中间件链 StatusEnricher（注进度）/ PersistenceTap（旁路写库）
  → StreamWriter.write_events()  序列化成 AI SDK v6 SSE + 生命周期保证
  → sse_helpers QueuedStream  keepalive + 断连不杀生产者
```

**必看代码**：

`schemas.py:32`（节选）—— FinishEvent 用 Literal 锁死六个合法值，且 usage 不进 SSE（AI SDK v6 严格校验）：
```python
class FinishEvent(BaseModel):
    finishReason: Literal["stop","length","error","tool-calls","content-filter","other"]
    def to_sse(self) -> str:
        return _sse({"type": "finish", "finishReason": self.finishReason})  # 不带 usage
```

`writer.py:56`（节选）—— StreamWriter 是**有状态守门人**：text-start/end 配对、恰好一个 finish、异常也补全：
```python
if isinstance(ui_event, FinishEvent):
    self.has_finish = True
    yield self._close_text()        # 先闭合开放的 text
    yield ui_event.to_sse()
...
finally:                            # 即使异常
    yield self._close_text()
    if not self.has_finish:         # 没 finish 自动补 finish(error)
        yield FinishEvent(finishReason="error").to_sse()
    yield SSE_DONE                  # [DONE] 必须最后
```

`sse_helpers.py:38`（节选）—— 断连不杀生产者（保证 PersistenceTap 一定执行），空闲发 keepalive 防中间件超时：
```python
except asyncio.TimeoutError:
    yield ": keepalive\n\n"   # 前端忽略，但字节在线上重置 Cloudflare/nginx 计时器
```

**看懂了什么**：为什么"所有输出必经管道"——只有 `StreamWriter` 能生成 SSE，于是 text/reasoning 生命周期配对、恰好一个 finish、error 不在 finish 后，全在**一个地方**保证，而不是散在各路由靠纪律。spec `protocol/sse-events.md` 的几条 MUST 都能在这里找到落点。这就是 [[协议桥接管道]] 的现场，它 →built_on→ [[AI SDK v6]] / [[PostgreSQL]]。

**自己 trace（最高回报的一条）**：挑一个工具调用，从 `LangGraphAdapter.stream`（adapter.py，四通道分发）→ `StatusEnricher`（注 data-agent-progress）→ `PersistenceTap`（dispatch_event 写库）→ `writer.py` 看 ToolCall 怎么变成 `tool-input-start/delta/available` 三行 SSE → 最后 FinishEvent → `[DONE]`。能 trace 通，Wave 1 骨架就握住了。

---

## 主题 E · 供应商中立路由 + 推理内容回传（🔥 war story）

**调用链**：
```
RouterChatModel._agenerate()（langchain_model.py:458）
  → config.py get_model_config()  取 thinking_roundtrip + provider
  → router.py:206 chat_completion() → PROVIDER_FACTORIES[type] 建 provider
  → AnthropicCompat / OpenAICompat 按 thinking_roundtrip 决定是否 strip reasoning
  → 回 _convert_messages() 出站时把 reasoning 从 content 摘回
```

**必看代码**：

`router.py:99` —— 供应商工厂注册表（OpenAI / Anthropic 协议分流就在这）：
```python
PROVIDER_FACTORIES = {
    "openai_compatible": _create_openai_compatible, "qwen": _create_qwen,
    "ollama": _create_ollama, "anthropic_compat": _create_anthropic_compat,
    "dashscope_responses": _create_dashscope_responses,
}
```

`config.py:357` —— 🔥 **空签名网关 fail-loud**（war story ②的防御）：
```python
def _validate_thinking_roundtrip(models):
    # 背景(conv e0e452ad)：空签名网关上 keep 回灌历史 thinking 会被逐字重展
    #   → 确定性工具复读死循环（write_todos ×6 → 400）
    for m in models.values():
        p = providers.get(m.provider)
        if p.provider_type != "anthropic_compat": continue
        if p.options.get("thinking_signature") != "empty": continue
        if m.supports_thinking and m.capabilities.get("thinking_roundtrip") not in ("keep","strip"):
            offenders.append(m.name)
    if offenders:
        raise ValueError(f"...必须显式声明 thinking_roundtrip(keep|strip): {offenders}")
```

`langchain_model.py:370` —— 🔥 **fold-fix**（war story ①的修复：出站把 reasoning 从 content 摘回）：
```python
# reasoning 永远是独立字段，绝不留在 content。入站为显示可临时折进 content，
# 出站必须摘回，否则 reasoning 双发 + 无签名网关当文本重展 → 思考膨胀
out_content = msg.content
if additional.get("_content_from_reasoning"):
    out_content = ""                       # ← 摘回
router_messages.append(RouterChatMessage(
    role="assistant", content=out_content, tool_calls=tool_calls,
    thinking_blocks=thinking_blocks, reasoning_content=reasoning_content))  # reasoning 独立走
```

`test_reasoning_content_roundtrip.py:52` —— 不变量断言：出站 content 绝不等于 reasoning_content：
```python
out = _model()._convert_messages([msg])
assert not (out[0].content and out[0].content == out[0].reasoning_content)
```

**🔥 两个 war story（学习要点里那两个，这里是代码现场）**：
1. **fold 膨胀**：reasoning 并入 content → 每轮历史把推理正文重塞进输入，多轮复利膨胀（NOTES 实测 6 轮 +55%）。修复=出站摘回（`langchain_model.py:370`），reasoning 只走独立字段。
2. **空签名回放死循环**：无 `thinking_signature` 的网关把历史 thinking 当文本重展 → 模型复读同一工具（真实事故 conv e0e452ad）。修复=加载期 fail-loud（`config.py:357`），强制显式声明 `keep|strip`，缺省即报错。

**看懂了什么**：三层防御——config 层（fail-loud 防埋坑）、model 层（fold-fix 防膨胀）、provider 层（strip 逃生阀）。这就是 [[供应商中立路由]] + [[推理内容回传]] 的现场。完整复盘读 `packages/llm_router/REASONING_ROUNDTRIP_NOTES.md`（"假设→A/B 实测→推翻"的方法论范例）。

**自己 trace**：`router.py:99` 看工厂分流 → `config.py:357` 看 fail-loud → `langchain_model.py:370` 看 fold-fix → 两个 spec 测试看不变量怎么钉死。

---

## 走查完之后

- 卡住或有顿悟 → 丢 `Inbox/`，下轮 ingest 原料。
- 真要内化：**主题 D 的"自己 trace"**（一个工具调用从图事件到 SSE）+ **主题 E 的两个 war story**（能复述根因和修复），是 Wave 1 性价比最高的两块。
- 想继续：Wave 2（U5–U8）会把多租户/记忆/事件溯源织进 data 域——那时再开一轮代码走查。
