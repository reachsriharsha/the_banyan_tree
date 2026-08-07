#!/usr/bin/env python3
"""Import Claude Desktop cowork sessions into the vault's sessions/ folder.

Reads local-agent-mode-sessions metadata (local_<id>.json) + transcripts
(local_<id>/audit.jsonl) and writes sessions/session-YYYY-MM-DD-HH-MM-<id8>.md
in the same markdown format as the CLI-synced sessions, with
`source: claude-desktop` frontmatter so origin stays distinguishable.

Idempotent: skips sessions whose target file already exists.
Re-run any time:  python3 analytics/import_desktop_sessions.py
"""

import glob
import json
import os
from datetime import datetime, timezone

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSIONS_DIR = os.path.join(VAULT, "sessions")
DESKTOP_ROOT = os.path.expanduser(
    "~/Library/Application Support/Claude/local-agent-mode-sessions"
)


def to_local(iso_utc: str) -> datetime:
    """'2026-05-14T06:38:13.974Z' (UTC) -> local datetime."""
    dt = datetime.fromisoformat(iso_utc.replace("Z", "+00:00"))
    return dt.astimezone()


def text_of(content) -> str:
    """Extract human text from a message content (str or block list)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [b.get("text", "") for b in content if b.get("type") == "text"]
        return "\n".join(p for p in parts if p).strip()
    return ""


def convert(meta_path: str) -> str | None:
    meta = json.load(open(meta_path))
    session_dir = meta_path[: -len(".json")]
    audit = os.path.join(session_dir, "audit.jsonl")
    if not os.path.isfile(audit):
        return None

    created = datetime.fromtimestamp(meta["createdAt"] / 1000).astimezone()
    sid = meta.get("cliSessionId") or os.path.basename(session_dir)[len("local_"):]
    fname = f"session-{created.strftime('%Y-%m-%d-%H-%M')}-{sid[:8]}.md"
    target = os.path.join(SESSIONS_DIR, fname)
    if os.path.exists(target):
        return None  # already imported

    lines = [
        "---",
        "type: session",
        "source: claude-desktop",
        f"title: {meta.get('title', 'Untitled')}",
        f"model: {meta.get('model', '')}",
        f"session_id: {sid}",
        "---",
    ]

    for raw in open(audit):
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue
        role = d.get("type")
        if role not in ("user", "assistant"):
            continue
        text = text_of(d.get("message", {}).get("content"))
        if not text:
            continue  # tool_use / tool_result / thinking-only entries
        ts = d.get("_audit_timestamp")
        stamp = to_local(ts).strftime("%Y-%m-%dT%H:%M:%S") if ts else "?"
        heading = "User" if role == "user" else "Assistant"
        lines += ["", f"## {heading} ({stamp})", "", text, "", "---"]

    with open(target, "w") as f:
        f.write("\n".join(lines) + "\n")
    return fname


def main():
    metas = sorted(glob.glob(os.path.join(DESKTOP_ROOT, "*", "*", "local_*.json")))
    written = []
    for m in metas:
        name = convert(m)
        if name:
            written.append(name)
    print(f"imported {len(written)} of {len(metas)} desktop sessions")
    for n in written:
        print(f"  + {n}")


if __name__ == "__main__":
    main()
