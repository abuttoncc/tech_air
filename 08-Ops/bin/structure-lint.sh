#!/bin/bash
# 结构巡检员 · lint —— 无人值守自动化（routine: 08-Ops/routines/结构巡检员.md）
# kind: tool / 纯代码无大脑：只跑 schema.py + expand.py --scan，只产报告不写本体。
# 被 launchd 拉起（com.techair.structure-lint.plist）；也可手动 bash 直接跑。
set -uo pipefail

# --- 定位库根（脚本在 <vault>/08-Ops/bin/ 下）---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$VAULT" || exit 1

REF="$VAULT/.claude/skills/auto-wiki/references"
RUNS="$VAULT/08-Ops/runs"
DOMAINS=(agent web data infra)

# --- python3：launchd 的 PATH 很裸，写死 homebrew python（pydantic 在此环境）---
PY="/opt/homebrew/opt/python@3.12/bin/python3.12"
[ -x "$PY" ] || PY="$(command -v python3)"

DATE="$(date +%Y-%m-%d)"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
OUT="$RUNS/${DATE}-结构巡检.md"
mkdir -p "$RUNS"

# --- 引擎①：schema.py 逐域校验（断链/越界边/frontmatter）---
schema_block=""
fail_total=0
pass_total=0
for d in "${DOMAINS[@]}"; do
  res="$("$PY" "$REF/schema.py" "$VAULT/wiki/$d" 2>&1)"
  # 末行 Result / Total 摘要
  summary="$(printf '%s\n' "$res" | grep -E 'Total:|Result:' | tr '\n' ' ' | sed 's/  */ /g')"
  [ -z "$summary" ] && summary="(无页面或无输出)"
  if printf '%s' "$res" | grep -q 'Failed: [1-9]'; then
    fcount="$(printf '%s' "$res" | grep -oE 'Failed: [0-9]+' | grep -oE '[0-9]+' | tail -1)"
    fail_total=$((fail_total + fcount))
  fi
  pcount="$(printf '%s' "$res" | grep -oE 'Passed: [0-9]+' | grep -oE '[0-9]+' | tail -1)"
  [ -n "$pcount" ] && pass_total=$((pass_total + pcount))
  schema_block+="- **$d**: $summary"$'\n'
done

# --- 引擎②：expand.py --scan 全库结构空洞 ---
scan_out="$("$PY" "$REF/expand.py" --scan --vault "$VAULT" 2>&1)"
real_holes="$(printf '%s' "$scan_out" | grep -oE '真洞 [0-9]+' | grep -oE '[0-9]+' | head -1)"
[ -z "$real_holes" ] && real_holes="?"

# --- 结论 ---
if [ "$fail_total" -gt 0 ]; then
  RESULT="FAIL"
elif [ "$real_holes" != "0" ] && [ "$real_holes" != "?" ]; then
  RESULT="WARN"
else
  RESULT="PASS"
fi

# --- 写 run 记录（append-only，每日一份）---
{
  echo "---"
  echo "type: run"
  echo "routine: lint"
  echo "name: 结构巡检员"
  echo "date: \"$DATE\""
  echo "trigger: launchd"
  echo "result: $RESULT"
  echo "---"
  echo ""
  echo "# 结构巡检 · $DATE"
  echo ""
  echo "> $TS · 无人值守 · 纯代码（schema.py + expand.py --scan）· 只产报告不写本体"
  echo ""
  echo "## 引擎① schema.py — 断链 / 越界关系边 / frontmatter"
  echo ""
  printf '%s' "$schema_block"
  echo ""
  echo "全库：通过 $pass_total · 失败 $fail_total"
  echo ""
  echo "## 引擎② expand.py --scan — 结构空洞（孤儿/挂件/仅taxonomy）"
  echo ""
  echo '```'
  printf '%s\n' "$scan_out"
  echo '```'
  echo ""
  echo "## 结论：$RESULT"
  echo ""
  case "$RESULT" in
    PASS) echo "- 本体结构健康：无校验失败、无真洞。" ;;
    WARN) echo "- 校验全过，但有 **$real_holes 个真洞**（孤儿/挂件节点）→ 派研究员织入边。" ;;
    FAIL) echo "- ⚠️ 有 **$fail_total 处校验失败**（断链/越界边/frontmatter 违规）→ 需人工修。" ;;
  esac
} > "$OUT"

# --- 滚动日志（一行一条，给 Dashboard / 巡查用）---
echo -e "${DATE}\t${RESULT}\tpass=${pass_total}\tfail=${fail_total}\tholes=${real_holes}" >> "$RUNS/_log.tsv"

echo "[structure-lint] $TS → $RESULT (pass=$pass_total fail=$fail_total holes=$real_holes) → $OUT"
exit 0
