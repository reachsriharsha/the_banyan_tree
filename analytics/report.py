#!/usr/bin/env python3
"""Generate a markdown snapshot of work-pattern metrics from a run's data.js.

Writes <run-dir>/analysis.md next to that run's data.js. The run dir defaults
to analytics/<today>/ (each monthly run is its own frozen folder); pass a dir
to override:
    python3 analytics/report.py [analytics/2026-09-07]

Run after extract.py.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, date.today().isoformat())
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def hrs(m):
    return f"{m/60:.1f}h" if m >= 60 else f"{round(m)}m"


def load():
    raw = open(os.path.join(RUN_DIR, "data.js")).read()
    return json.loads(re.sub(r"^window\.WORKDATA = |;\s*$", "", raw))


def main():
    d = load()
    S = d["sessions"]
    out = []
    w = out.append

    total_min = sum(max(s["duration_min"], 1) for s in S)
    desktop = [s for s in S if s["source"] == "desktop"]
    prs = sorted({p for l in d["prs_by_week"].values() for p in l})
    tokens_out = sum(t.get("output", 0) for t in d["tokens_by_week"].values())

    w(f"# Work Pattern Analysis — {date.today().isoformat()}")
    w("")
    w(f"Frozen metrics snapshot generated from `data.js` "
      f"(extracted {d['generated_at'][:16].replace('T', ' ')}). "
      f"Compare against the next dated snapshot to measure change.")
    w("")

    # ---------------- headline
    w("## Headline")
    w("")
    w("| Metric | Value |")
    w("|---|---|")
    w(f"| Sessions | {len(S)} ({len(S)-len(desktop)} CLI / {len(desktop)} Desktop) |")
    w(f"| Active days | {len(d['calendar'])} |")
    w(f"| Time in session (gap-capped active) | {hrs(total_min)} |")
    w(f"| Distinct PRs mentioned as \"PR #N\" | {len(prs)} |")
    w(f"| Claude API turns (CLI) | {d['turn_count']:,} |")
    w(f"| Claude output tokens | {tokens_out:,} |")
    w(f"| Prompts typed (history) | {d['prompt_count']} |")
    w("")

    # ---------------- rhythm
    punch = d["punchcard"]
    total_msg = sum(sum(r) for r in punch) or 1
    def band(a, b):
        return sum(r[h] for r in punch for h in range(a, b + 1))
    peak_v, peak_d, peak_h = max(
        (v, di, hi) for di, r in enumerate(punch) for hi, v in enumerate(r))
    days = sorted(d["calendar"])
    best, cur, prev = 0, 0, None
    for day in days:
        t = datetime.fromisoformat(day).toordinal()
        cur = cur + 1 if prev is not None and t - prev == 1 else 1
        best = max(best, cur)
        prev = t
    biggest = max(d["calendar"].items(), key=lambda kv: kv[1])

    w("## Rhythm")
    w("")
    w(f"- Peak hour: **{peak_h:02d}:00 on {DOW[peak_d]}s** ({peak_v} messages)")
    w(f"- Dawn 05:00–09:59: **{band(5,9)/total_msg:.0%}** · "
      f"Midday 10:00–13:59: {band(10,13)/total_msg:.0%} · "
      f"Afternoon 14:00–18:59: {band(14,18)/total_msg:.0%} · "
      f"Evening 19:00–23:59: {band(19,23)/total_msg:.0%}")
    w(f"- Longest daily streak: **{best} days** · "
      f"Biggest day: **{biggest[0]}** ({hrs(biggest[1])})")
    per_dow = [sum(r) for r in punch]
    w("- Messages by weekday: " + " · ".join(
        f"{DOW[i]} {v}" for i, v in enumerate(per_dow)))
    w("")

    # ---------------- projects
    proj = defaultdict(lambda: [0, 0.0])
    for s in S:
        proj[s["project"]][0] += 1
        proj[s["project"]][1] += max(s["duration_min"], 1)
    w("## Projects")
    w("")
    w("| Project | Sessions | Time | Share |")
    w("|---|---:|---:|---:|")
    for p, (n, m) in sorted(proj.items(), key=lambda kv: -kv[1][1]):
        w(f"| {p} | {n} | {hrs(m)} | {m/total_min:.0%} |")
    w("")

    # ---------------- types & sources
    types = Counter(s["type"] for s in S)
    w("## Session types (heuristic)")
    w("")
    w("| Type | Sessions | Share |")
    w("|---|---:|---:|")
    for t in ("shipping", "building", "analysis", "discussion"):
        w(f"| {t} | {types.get(t,0)} | {types.get(t,0)/len(S):.0%} |")
    ship, ana = types.get("shipping", 0), max(types.get("analysis", 1), 1)
    w("")
    w(f"Shipping-to-analysis ratio: **{ship/ana:.1f}**")
    w("")

    months = defaultdict(lambda: [0, 0])
    for s in S:
        months[s["start"][:7]][0 if s["source"] != "desktop" else 1] += 1
    w("## Builder (CLI) vs Analyst (Desktop) by month")
    w("")
    w("| Month | CLI | Desktop |")
    w("|---|---:|---:|")
    for m in sorted(months):
        w(f"| {m} | {months[m][0]} | {months[m][1]} |")
    w("")

    # ---------------- durations
    durs = sorted(s["duration_min"] for s in S)
    med = durs[len(durs)//2]
    p90 = durs[int(len(durs)*0.9)]
    longest = max(S, key=lambda s: s["duration_min"])
    over4h = sum(1 for x in durs if x >= 240)
    w("## Session length")
    w("")
    w(f"- Median **{hrs(med)}** · p90 **{hrs(p90)}** · "
      f"longest **{hrs(longest['duration_min'])}** "
      f"({longest['project']}, {longest['start'][:10]})")
    w(f"- Sessions ≥ 4h active: **{over4h}**")
    w("")

    # ---------------- tools & tokens & prs
    w("## Top tools (CLI turns)")
    w("")
    w("| Tool | Calls |")
    w("|---|---:|")
    for name, v in list(d["tools"].items())[:10]:
        w(f"| {name} | {v:,} |")
    w("")

    w("## Weekly output")
    w("")
    w("| Week | Output tokens | PRs merged (mentions) |")
    w("|---|---:|---|")
    weeks = sorted(set(d["tokens_by_week"]) | set(d["prs_by_week"]))
    for wk in weeks:
        tok = d["tokens_by_week"].get(wk, {}).get("output", 0)
        pr = d["prs_by_week"].get(wk, [])
        w(f"| {wk} | {tok:,} | {len(pr)} |")
    w("")
    w("---")
    w("Regenerate pipeline: `./analytics/refresh.sh` "
      "(creates a fresh dated folder; this one stays frozen)")
    w("")

    target = os.path.join(RUN_DIR, "analysis.md")
    with open(target, "w") as f:
        f.write("\n".join(out))
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
