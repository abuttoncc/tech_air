#!/usr/bin/env python3
"""
tech_air 决策平台 · LangGraph CLI
=================================
  python3 run.py start [--live] [--thread ID]   启动一次运行（默认 dry-run）
  python3 run.py approve --thread ID [--reject]  恢复被人审中断的运行
  python3 run.py show    --thread ID             查看某次运行的最终状态
  python3 run.py graph                           打印图拓扑（mermaid）

状态进 SQLite checkpointer（checkpoints.sqlite），可中断、可恢复、可追溯。
"""
import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import build_graph, VAULT  # noqa: E402

from langgraph.checkpoint.sqlite import SqliteSaver  # noqa: E402
from langgraph.types import Command  # noqa: E402

CKPT = Path(__file__).resolve().parent / "checkpoints.sqlite"


def _saver():
    conn = sqlite3.connect(str(CKPT), check_same_thread=False)
    return SqliteSaver(conn)


def _cfg(thread: str):
    return {"configurable": {"thread_id": thread}}


def _show_interrupt(result):
    intr = result.get("__interrupt__")
    if not intr:
        return False
    payload = intr[0].value if isinstance(intr, (list, tuple)) else intr
    print("\n⏸  运行已暂停，等待人审（铁律 3：人是最后的闸）")
    print("─" * 56)
    for k, v in payload.items():
        if isinstance(v, list):
            print(f"  {k}:")
            for item in v:
                print(f"    - {item}")
        else:
            print(f"  {k}: {v}")
    print("─" * 56)
    return True


def cmd_start(args):
    thread = args.thread or "run-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    date = datetime.now().strftime("%Y-%m-%d")
    graph = build_graph(_saver())
    state = {"run_id": thread, "date": date, "dry_run": not args.live, "trace": []}
    print(f"▶ 启动运行 thread={thread} · {'LIVE' if args.live else 'dry-run'}")
    result = graph.invoke(state, _cfg(thread))
    if _show_interrupt(result):
        print(f"\n→ 审批：python3 run.py approve --thread {thread}   （驳回加 --reject）")
        return
    _print_done(graph, thread)


def cmd_approve(args):
    decision = "reject" if args.reject else "approve"
    graph = build_graph(_saver())
    print(f"▶ 恢复运行 thread={args.thread} · 人审决定={decision}")
    result = graph.invoke(Command(resume=decision), _cfg(args.thread))
    if _show_interrupt(result):
        return
    _print_done(graph, args.thread)


def _print_done(graph, thread):
    snap = graph.get_state(_cfg(thread))
    s = snap.values
    print(f"\n✅ 运行完成 · 结果 {s.get('lint_result')} · 人审 {s.get('decision', '—')}")
    print("\nX-Ray 思维链：")
    for t in s.get("trace", []):
        print(f"  {t}")


def cmd_show(args):
    graph = build_graph(_saver())
    snap = graph.get_state(_cfg(args.thread))
    if not snap.values:
        print(f"无此 thread：{args.thread}")
        return
    s = snap.values
    print(f"thread={args.thread} · result={s.get('lint_result')} · approved={s.get('approved')}")
    print(f"下一步节点：{snap.next or '（已结束）'}")
    print("\nX-Ray 思维链：")
    for t in s.get("trace", []):
        print(f"  {t}")


def cmd_graph(args):
    graph = build_graph(None)
    try:
        print(graph.get_graph().draw_mermaid())
    except Exception as e:
        print("（mermaid 渲染失败，打印节点/边）", e)
        g = graph.get_graph()
        print("nodes:", [n for n in g.nodes])


def cmd_health(args):
    """纯程序快查（供 hook 调用）：只跑确定性 lint 节点，一行健康摘要，不写状态、不调 LLM。"""
    from pipeline import node_lint
    try:
        r = node_lint({})
        print(f"[wiki health] {r['lint_result']} · pass={r['passed']} "
              f"fail={r['failed']} holes={r['holes']}")
    except Exception as e:
        print(f"[wiki health] SKIP ({e})")


def main():
    ap = argparse.ArgumentParser(description="tech_air 决策平台 LangGraph CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("start"); p.add_argument("--live", action="store_true")
    p.add_argument("--thread"); p.set_defaults(fn=cmd_start)

    p = sub.add_parser("approve"); p.add_argument("--thread", required=True)
    p.add_argument("--reject", action="store_true"); p.set_defaults(fn=cmd_approve)

    p = sub.add_parser("show"); p.add_argument("--thread", required=True)
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("graph"); p.set_defaults(fn=cmd_graph)

    p = sub.add_parser("health"); p.set_defaults(fn=cmd_health)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
