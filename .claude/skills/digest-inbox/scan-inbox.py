#!/usr/bin/env python3
"""Inbox 待消化预检 —— 纯 stdlib，零依赖。

轮询定时器的「便宜检测层」：扫 Inbox 散文，判定哪些未消化（缺 compiled:true，
或 updated 晚于 digested = 改过需重消化）。有未消化才值得唤醒 claude 跑 ingest。

用法:
  python3 scan-inbox.py            # 打印 JSON（count / oldest_days / items），调试用
  python3 scan-inbox.py --count    # 只打印待消化篇数（runner 用，便宜）
  VAULT=/path python3 scan-inbox.py  # 覆盖库根；默认从脚本位置上溯 4 层

退出码: 0=无待消化 / 10=有待消化（方便 shell 直接判断）。
"""
import sys, os, re, json, glob
from datetime import date, datetime

# 脚本在 .claude/skills/digest-inbox/ 下 → 库根上溯 4 层；可被 VAULT 环境变量覆盖
VAULT = os.environ.get(
    "VAULT",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
)
INBOX = os.path.join(VAULT, "Inbox")
SKIP_NAMES = {"README", "plan"}        # 导航/规划文件，非研究散文


def frontmatter(path):
    """最小 frontmatter 解析（扁平 key: value），不依赖 pyyaml。"""
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
    except OSError:
        return {}
    if not txt.startswith("---"):
        return {}
    end = txt.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in txt[3:end].splitlines():
        m = re.match(r"\s*([A-Za-z0-9_-]+)\s*:\s*(.*)", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip("\"'")
    return fm


def parse_date(s):
    if not s:
        return None
    s = str(s).strip().strip("\"'")
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def scan():
    pending = []
    for path in sorted(glob.glob(os.path.join(INBOX, "*.md"))):
        name = os.path.splitext(os.path.basename(path))[0]
        if name in SKIP_NAMES:
            continue
        fm = frontmatter(path)
        if fm.get("type") == "capture":          # 收集箱 README 之类
            continue
        compiled = str(fm.get("compiled", "")).lower() in ("true", "yes", "1")
        updated = parse_date(fm.get("updated"))
        digested = parse_date(fm.get("digested"))
        # 待消化 = 没消化过，或消化后又被改动（updated 晚于 digested）
        is_pending = (not compiled) or (updated and digested and updated > digested)
        if is_pending:
            created = parse_date(fm.get("created"))
            age = (date.today() - created).days if created else None
            pending.append({"name": name, "age_days": age,
                            "wiki_topic": fm.get("wiki-topic", "")})
    oldest = max((p["age_days"] for p in pending if p["age_days"] is not None),
                 default=None)
    return {"count": len(pending), "oldest_days": oldest, "items": pending}


def main():
    result = scan()
    if "--count" in sys.argv:
        print(result["count"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(10 if result["count"] else 0)


if __name__ == "__main__":
    main()
