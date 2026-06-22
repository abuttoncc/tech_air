"""
tech_air 决策平台 · LangGraph 编排核心
============================================
把 08-Ops/routines/ 的 routine 编成一张图来跑，对齐「实现决策平台」骨架三条铁律：
  1. 决策长在心智模型上  —— lint 节点直接读 wiki 本体 + data.db
  2. 可解释是信任前提    —— 每个节点往 state.trace 追加 X-Ray 轨迹，落 runs/
  3. 人是最后的闸        —— gate 节点用 interrupt() 暂停等人审，候选只投不直写正典

节点分工：
  · 确定性工具节点（lint / commit / record）：纯 python，零 LLM、零 API。
  · LLM 节点（research）：壳调 headless `claude -p`，复用 Claude Code 登录，默认 dry-run。
"""
from __future__ import annotations

import operator
import re
import subprocess
from pathlib import Path
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt

# --- 路径锚点（本文件在 <vault>/08-Ops/graph/）---
VAULT = Path(__file__).resolve().parents[2]
REF = VAULT / ".claude" / "skills" / "auto-wiki" / "references"
WIKI = VAULT / "wiki"
RUNS = VAULT / "08-Ops" / "runs"
REVIEW = VAULT / "08-Ops" / "review"
DOMAINS = ["agent", "web", "data", "infra"]

PY = "/opt/homebrew/opt/python@3.12/bin/python3.12"
if not Path(PY).exists():
    PY = "python3"


# ============================================================
# 共享状态
# ============================================================
class OpsState(TypedDict, total=False):
    run_id: str
    date: str
    dry_run: bool
    lint_result: str          # PASS / WARN / FAIL
    lint_summary: str
    holes: int                # 结构空洞（真洞）数
    passed: int
    failed: int
    needs_work: bool
    candidates: list          # 研究员产出的候选（proposed，不直写正典）
    approved: bool
    decision: str
    trace: Annotated[list, operator.add]   # X-Ray 思维链，append-only


# ============================================================
# 辅助
# ============================================================
def _run(cmd: list[str], timeout: int = 120) -> str:
    p = subprocess.run(cmd, cwd=str(VAULT), capture_output=True, text=True, timeout=timeout)
    return (p.stdout or "") + (p.stderr or "")


def _claude(prompt: str, timeout: int = 600) -> str:
    """壳调 headless claude（复用 Claude Code 登录，无需 API key）。"""
    p = subprocess.run(["claude", "-p", prompt], cwd=str(VAULT),
                       capture_output=True, text=True, timeout=timeout)
    return (p.stdout or "").strip() or (p.stderr or "").strip()


# ============================================================
# 节点
# ============================================================
def node_lint(state: OpsState) -> dict:
    """确定性工具节点：schema.py 逐域校验 + expand.py --scan 扫结构空洞。"""
    passed = failed = 0
    lines = []
    for d in DOMAINS:
        out = _run([PY, str(REF / "schema.py"), str(WIKI / d)])
        m_p = re.search(r"Passed:\s*(\d+)", out)
        m_f = re.search(r"Failed:\s*(\d+)", out)
        p = int(m_p.group(1)) if m_p else 0
        f = int(m_f.group(1)) if m_f else 0
        passed += p
        failed += f
        lines.append(f"{d}: pass={p} fail={f}")

    scan = _run([PY, str(REF / "expand.py"), "--scan", "--vault", str(VAULT)])
    m_h = re.search(r"真洞\s*(\d+)", scan)
    holes = int(m_h.group(1)) if m_h else 0

    result = "FAIL" if failed else ("WARN" if holes else "PASS")
    summary = f"{result} · 通过 {passed} 失败 {failed} 真洞 {holes} · " + " | ".join(lines)
    return {
        "lint_result": result, "lint_summary": summary,
        "holes": holes, "passed": passed, "failed": failed,
        "needs_work": result != "PASS",
        "trace": [f"① lint → {summary}"],
    }


def route_after_lint(state: OpsState) -> str:
    return "research" if state.get("needs_work") else "record"


def node_research(state: OpsState) -> dict:
    """LLM 节点：针对缺口产出候选（只投候选不写正典）。默认 dry-run 不调 claude。"""
    summary = state.get("lint_summary", "")
    if state.get("dry_run", True):
        cand = {"type": "研究候选", "status": "proposed",
                "desc": f"[dry-run] 针对「{state.get('lint_result')}」的织入边/补全候选（未调用 claude）"}
        return {"candidates": [cand],
                "trace": [f"② research(dry-run) → 产出 1 条候选"]}
    prompt = (f"你是 tech_air 的研究员 routine（deep-dive）。结构巡检结果：{summary}。"
              f"请按 auto-wiki 找缺口并产出候选织入边/补全清单，"
              f"严守『只产候选不写正典、搜不到明示未能补全』。输出简明 markdown 清单。")
    out = _claude(prompt)
    cand = {"type": "研究候选", "status": "proposed", "desc": out[:4000]}
    return {"candidates": [cand],
            "trace": [f"② research(live) → claude 产出候选 {len(out)} 字"]}


def node_gate(state: OpsState) -> dict:
    """人审闸（铁律 3）：有候选则 interrupt() 暂停，等人 approve/reject。"""
    cands = state.get("candidates", [])
    if not cands:
        return {"approved": True, "decision": "无候选",
                "trace": ["③ gate → 无候选，跳过"]}
    decision = interrupt({
        "type": "审批请求",
        "gate": "newnode / xedge（跨域 built_on 边）",
        "candidates": [c["desc"] for c in cands],
        "提示": "批准 → 候选写入 review 队列（不直写正典）。resume 传 approve / reject。",
    })
    ok = str(decision).strip().lower() in ("approve", "approved", "y", "yes", "批准", "通过")
    return {"approved": ok, "decision": str(decision),
            "trace": [f"③ gate → 人审：{decision} → {'批准' if ok else '驳回'}"]}


def node_commit(state: OpsState) -> dict:
    """确定性节点：批准的候选入 review 队列（产出收口：只投候选不直写正典）。"""
    if not state.get("approved"):
        return {"trace": ["④ commit → 未批准，候选丢弃（一次驳回 streak 清零，见审批账本）"]}
    cands = state.get("candidates", [])
    REVIEW.mkdir(parents=True, exist_ok=True)
    path = REVIEW / f"{state['date']}-{state['run_id']}.md"
    body = ["---", "type: review-candidate", f"date: \"{state['date']}\"",
            f"run_id: {state['run_id']}", "status: pending-human-merge", "---", "",
            f"# 候选 · {state['date']} · {state['run_id']}", ""]
    for i, c in enumerate(cands, 1):
        body.append(f"## 候选 {i}（{c.get('type')}）\n\n{c.get('desc')}\n")
    path.write_text("\n".join(body), encoding="utf-8")
    return {"trace": [f"④ commit → {len(cands)} 条候选入 review 队列：{path.name}"]}


def node_record(state: OpsState) -> dict:
    """确定性节点：把整条 X-Ray 轨迹落 runs/（铁律 2 可解释）。"""
    RUNS.mkdir(parents=True, exist_ok=True)
    path = RUNS / f"{state['date']}-graph-{state['run_id']}.md"
    result = state.get("lint_result", "?")
    trace = state.get("trace", [])
    body = ["---", "type: run", "engine: langgraph", f"date: \"{state['date']}\"",
            f"run_id: {state['run_id']}", f"result: {result}",
            f"approved: {state.get('approved', '—')}", "---", "",
            f"# 决策平台运行 · {state['date']} · {state['run_id']}", "",
            f"> LangGraph 编排 · 结果 {result} · {'dry-run' if state.get('dry_run', True) else 'live'}", "",
            "## X-Ray 思维链（节点轨迹）", ""]
    body += [f"{i}. {t}" for i, t in enumerate(trace, 1)]
    body += ["", f"## 结论：{result}", "",
             f"- 校验：通过 {state.get('passed', 0)} · 失败 {state.get('failed', 0)} · 真洞 {state.get('holes', 0)}",
             f"- 人审：{state.get('decision', '—')}"]
    path.write_text("\n".join(body), encoding="utf-8")
    line = f"{state['date']}\t{state['run_id']}\t{result}\tapproved={state.get('approved','-')}"
    (RUNS / "_graph_log.tsv").open("a", encoding="utf-8").write(line + "\n")
    return {"trace": [f"⑤ record → 运行记录已写 {path.name}"]}


# ============================================================
# 组图
# ============================================================
def build_graph(checkpointer=None):
    g = StateGraph(OpsState)
    g.add_node("lint", node_lint)
    g.add_node("research", node_research)
    g.add_node("gate", node_gate)
    g.add_node("commit", node_commit)
    g.add_node("record", node_record)

    g.add_edge(START, "lint")
    g.add_conditional_edges("lint", route_after_lint,
                            {"research": "research", "record": "record"})
    g.add_edge("research", "gate")
    g.add_edge("gate", "commit")
    g.add_edge("commit", "record")
    g.add_edge("record", END)
    return g.compile(checkpointer=checkpointer)
