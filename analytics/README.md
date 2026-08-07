# Analytics

Work-pattern analytics from Claude session data (CLI + Desktop).

## Refresh

```bash
./analytics/refresh.sh
```

Creates a frozen snapshot in `analytics/YYYY-MM-DD/`:

- `index.html` — charts (open in browser)
- `analysis.md` — metrics report
- `data.js` — the data behind both

Old snapshots stay untouched — compare across months.
After each refresh, score the previous month in `improvements.md`.
