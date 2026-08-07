#!/usr/bin/env python3
"""Extract work-pattern analytics from all Claude data sources into data.js.

Sources:
  1. sessions/*.md            — vault transcripts (CLI-synced + claude-desktop imports)
  2. ~/.claude/usage.db       — per-turn tokens / models / tools (CLI)
  3. ~/.claude/projects/*.jsonl — raw CLI transcripts (fills usage.db gaps)
  4. ~/.claude/history.jsonl  — every prompt typed (timestamps + project)
  5. analytics/conversations.json — OPTIONAL claude.ai export (phase 2); folded in if present

Output: <run-dir>/data.js  (window.WORKDATA = {...}) consumed by that run's
index.html. The run dir defaults to analytics/<today>/ so each monthly run is
a frozen, self-contained snapshot; pass a dir to override:
    python3 analytics/extract.py [analytics/2026-09-07]
"""

import glob
import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAUDE = os.path.expanduser("~/.claude")
RUN_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    VAULT, "analytics", date.today().isoformat())
OUT = os.path.join(RUN_DIR, "data.js")

# ---------------------------------------------------------------- helpers

def local(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt  # already naive local
    return dt.astimezone().replace(tzinfo=None)


def parse_iso(s: str) -> datetime:
    return local(datetime.fromisoformat(s.replace("Z", "+00:00")))


def week_of(d: datetime) -> str:
    iso = d.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


PROJECT_MAP = [
    (r"akshara", "Akshara"),
    (r"cadencelanes", "Swim Tracker"),
    (r"banyan", "Second Brain"),
    (r"brain_clone", "Second Brain"),
    (r"autolife|/sa$|autolife_sa", "Autolife"),
    (r"educational_sa", "Autolife"),
    (r"ll_site", "LL Site"),
    (r"ay2627class5", "Class Tools"),
    (r"m5s3|m5stack", "M5Stack Voice"),
    (r"scenario-valuation|remj|ansec", "Investing"),
    (r"backup", "Tooling"),
    (r"daari", "Daari"),
    (r"edu-mgmt", "Edu Mgmt (early)"),
    (r"lc_test|plugin-autodev", "Tooling"),
    (r"minimalist-app", "Minimalist App"),
]

DESKTOP_CATEGORY = [
    (r"invest|stock|ipo|valuation|filing|company|financ", "Investing"),
    (r"langchain|job", "Job Research"),
    (r"slide|presentation", "Presentations"),
    (r"skill|agent", "AI Tooling"),
]


def project_name(path_or_title: str, source: str) -> str:
    s = (path_or_title or "").lower()
    rules = DESKTOP_CATEGORY if source == "desktop" else PROJECT_MAP
    for pat, name in rules:
        if re.search(pat, s):
            return name
    return "Other"


# ------------------------------------------------- 1. vault session files

SESSION_RE = re.compile(r"^## (User|Assistant) \((\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", re.M)

SHIP_HINTS = re.compile(r"PR #\d+|merged|opened.*pull request", re.I)
ANALYSIS_HINTS = re.compile(
    r"do ?n[o']t change (any )?code|no code change|analysis only|"
    r"just explain|investigation|clarif", re.I)
PR_RE = re.compile(r"PR ?#(\d+)|pull request #(\d+)", re.I)


def classify(user_text: str, full_text: str) -> str:
    if ANALYSIS_HINTS.search(user_text):
        return "analysis"
    if SHIP_HINTS.search(full_text):
        return "shipping"
    if re.search(r"\b(create|build|implement|fix|add|write|refactor)", user_text, re.I):
        return "building"
    return "discussion"


def parse_vault_sessions():
    sessions = []
    for path in sorted(glob.glob(os.path.join(VAULT, "sessions", "session-*.md"))):
        text = open(path, encoding="utf-8", errors="replace").read()
        fm = {}
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
        source = "desktop" if fm.get("source") == "claude-desktop" else "cli"
        stamps, user_chars, n_user, n_asst = [], 0, 0, 0
        user_texts = []
        for role, ts in SESSION_RE.findall(text):
            stamps.append(datetime.fromisoformat(ts))
        # walk messages for role stats
        parts = re.split(r"^## (User|Assistant) \([^)]*\)\s*$", text, flags=re.M)
        for i in range(1, len(parts) - 1, 2):
            body = parts[i + 1]
            if parts[i] == "User":
                n_user += 1
                user_chars += len(body.strip())
                user_texts.append(body)
            else:
                n_asst += 1
        if not stamps:
            continue
        stamps.sort()
        start, end = stamps[0], stamps[-1]
        # active minutes: gap-capped so a session resumed days later doesn't
        # count wall-clock idle time (cap inter-message gap at 30 min)
        active = 0.0
        day_minutes = Counter()
        for a, b in zip(stamps, stamps[1:]):
            gap = min((b - a).total_seconds() / 60, 30)
            active += gap
            day_minutes[a.strftime("%Y-%m-%d")] += gap
        active = max(round(active, 1), 1)
        if not day_minutes:
            day_minutes[start.strftime("%Y-%m-%d")] = 1
        user_blob = "\n".join(user_texts)
        prs = sorted({int(g) for tup in PR_RE.findall(text) for g in tup if g})
        proj_src = fm.get("title", "") if source == "desktop" else fm.get("project", "")
        sessions.append({
            "id": os.path.basename(path),
            "source": source,
            "project": project_name(proj_src, source),
            "raw_project": proj_src,
            "title": fm.get("title", ""),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "duration_min": active,
            "span_min": round((end - start).total_seconds() / 60, 1),
            "day_minutes": dict(day_minutes),
            "n_user": n_user,
            "n_assistant": n_asst,
            "user_chars": user_chars,
            "type": classify(user_blob, text),
            "prs": prs if SHIP_HINTS.search(text) else [],
            "stamps": [s.isoformat() for s in stamps],
        })
    return sessions


# ------------------------------------------------- 2+3. usage.db + raw jsonl

def parse_usage_and_raw():
    tokens_week = defaultdict(lambda: Counter())
    tools = Counter()
    models = Counter()
    turn_stamps = []
    seen_sessions = set()

    db = os.path.join(CLAUDE, "usage.db")
    if os.path.exists(db):
        con = sqlite3.connect(db)
        for sid, in con.execute("SELECT session_id FROM sessions"):
            seen_sessions.add(sid)
        for ts, model, i, o, cr, cc, tool in con.execute(
                "SELECT timestamp, model, input_tokens, output_tokens,"
                " cache_read_tokens, cache_creation_tokens, tool_name FROM turns"):
            try:
                d = parse_iso(ts)
            except (ValueError, TypeError):
                continue
            w = week_of(d)
            tokens_week[w]["input"] += i or 0
            tokens_week[w]["output"] += o or 0
            tokens_week[w]["cache_read"] += cr or 0
            turn_stamps.append(d.isoformat())
            if model:
                models[model] += 1
            if tool:
                tools[tool] += 1
        con.close()

    # raw jsonl for sessions usage.db hasn't processed yet
    for path in glob.glob(os.path.join(CLAUDE, "projects", "*", "*.jsonl")):
        sid = os.path.basename(path)[:-6]
        if sid in seen_sessions:
            continue
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            msg = d.get("message", {})
            u = msg.get("usage") or {}
            ts = d.get("timestamp")
            if not ts:
                continue
            try:
                dt = parse_iso(ts)
            except (ValueError, TypeError):
                continue
            w = week_of(dt)
            tokens_week[w]["input"] += u.get("input_tokens", 0)
            tokens_week[w]["output"] += u.get("output_tokens", 0)
            tokens_week[w]["cache_read"] += u.get("cache_read_input_tokens", 0)
            turn_stamps.append(dt.isoformat())
            if msg.get("model"):
                models[msg["model"]] += 1
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    tools[b.get("name", "?")] += 1
    return tokens_week, tools, models, turn_stamps


# ------------------------------------------------- 4. history.jsonl prompts

def parse_history():
    prompts = []
    path = os.path.join(CLAUDE, "history.jsonl")
    if not os.path.exists(path):
        return prompts
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
            dt = datetime.fromtimestamp(d["timestamp"] / 1000)
            prompts.append({
                "ts": dt.isoformat(),
                "project": project_name(d.get("project", ""), "cli"),
                "chars": len(d.get("display", "")),
            })
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    return prompts


# ------------------------------------------------- 5. optional claude.ai export

def parse_claude_ai_export():
    """Phase-2 hook: drop the claude.ai data-export conversations.json here."""
    path = os.path.join(VAULT, "analytics", "conversations.json")
    if not os.path.exists(path):
        return []
    convos = []
    try:
        data = json.load(open(path))
    except (json.JSONDecodeError, OSError):
        return []
    for c in data:
        msgs = c.get("chat_messages", [])
        stamps = []
        for m in msgs:
            ts = m.get("created_at")
            if ts:
                try:
                    stamps.append(parse_iso(ts))
                except ValueError:
                    pass
        if not stamps:
            continue
        convos.append({
            "id": c.get("uuid", ""),
            "source": "claude.ai",
            "title": c.get("name", ""),
            "project": project_name(c.get("name", ""), "desktop"),
            "start": min(stamps).isoformat(),
            "end": max(stamps).isoformat(),
            "n_messages": len(msgs),
        })
    return convos


# ------------------------------------------------- aggregate + emit

def main():
    sessions = parse_vault_sessions()
    tokens_week, tools, models, turn_stamps = parse_usage_and_raw()
    prompts = parse_history()
    chats = parse_claude_ai_export()

    # punchcard from every user-message timestamp in sessions
    punch = [[0] * 24 for _ in range(7)]
    calendar = Counter()   # date -> active minutes
    for s in sessions:
        for st in s["stamps"]:
            d = datetime.fromisoformat(st)
            punch[d.weekday()][d.hour] += 1
        for day, mins in s["day_minutes"].items():
            calendar[day] += max(mins, 1)

    weekly = defaultdict(lambda: defaultdict(float))  # week -> project -> minutes
    for s in sessions:
        w = week_of(datetime.fromisoformat(s["start"]))
        weekly[w][s["project"]] += max(s["duration_min"], 1)

    prs_week = defaultdict(set)
    for s in sessions:
        w = week_of(datetime.fromisoformat(s["start"]))
        for pr in s["prs"]:
            prs_week[w].add(pr)

    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "sessions": [{k: v for k, v in s.items() if k not in ("stamps", "day_minutes")}
                     for s in sessions],
        "turn_count": len(turn_stamps),
        "punchcard": punch,
        "calendar": dict(sorted(calendar.items())),
        "weekly_project_minutes": {w: dict(p) for w, p in sorted(weekly.items())},
        "tokens_by_week": {w: dict(c) for w, c in sorted(tokens_week.items())},
        "tools": dict(tools.most_common(20)),
        "models": dict(models.most_common()),
        "prs_by_week": {w: sorted(v) for w, v in sorted(prs_week.items())},
        "prompt_count": len(prompts),
        "prompt_chars": [p["chars"] for p in prompts],
        "claude_ai_chats": chats,
    }

    os.makedirs(RUN_DIR, exist_ok=True)
    with open(OUT, "w") as f:
        f.write("window.WORKDATA = ")
        json.dump(data, f, separators=(",", ":"))
        f.write(";\n")
    kb = os.path.getsize(OUT) // 1024
    print(f"wrote {OUT} ({kb} KB)")
    print(f"  sessions: {len(sessions)} ({sum(1 for s in sessions if s['source']=='desktop')} desktop)")
    print(f"  turn stamps: {len(turn_stamps)}, prompts: {len(prompts)}, chats: {len(chats)}")
    print(f"  types: {Counter(s['type'] for s in sessions)}")
    print(f"  projects: {Counter(s['project'] for s in sessions)}")


if __name__ == "__main__":
    main()
