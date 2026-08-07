#!/bin/bash
# Refresh work-pattern analytics into a frozen, dated snapshot folder:
#   analytics/YYYY-MM-DD/{index.html, data.js, analysis.md}
# Reusable scripts stay in analytics/; every run's folder is self-contained,
# so older snapshots remain viewable forever.
# Usage: ./analytics/refresh.sh
set -euo pipefail
cd "$(dirname "$0")"
DIR="$(date +%F)"
mkdir -p "$DIR"
python3 import_desktop_sessions.py
python3 extract.py "$DIR"
python3 report.py "$DIR"
cp index.template.html "$DIR/index.html"
echo "done — snapshot in analytics/$DIR/ (open index.html for charts, analysis.md for the report)"
