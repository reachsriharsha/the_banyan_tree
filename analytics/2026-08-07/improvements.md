# Improvement Suggestions

One entry per review. Each suggestion carries the metric that tests it, so the
next monthly snapshot (`analysis-YYYY-MM-DD.md`) can score it objectively.
Review cadence: monthly — next review due **2026-09-07**.

---

## Baseline review — 2026-08-07

Source: [[analytics/2026-08-07/analysis|analysis 2026-08-07]] · charts: `analytics/2026-08-07/index.html`

### What's already working (keep doing)

- **Analyze-first discipline.** 20 sessions (18%) are explicit "don't change
  code" investigations, and they visibly feed the shipping sessions that follow
  (e.g. SMS-architecture analysis on Aug 4–5 mornings → RBAC fix and console
  features shipped the same evenings). This is a genuinely good loop.
- **Dawn shift.** 27% of activity lands 05:00–09:59, and those sessions skew
  analysis/planning while evenings skew shipping. The split matches energy to
  task type — keep it.
- **One-shot side projects.** The Swim Tracker MVP went spec→dockerized app in
  a single 2.2h session. Scoping small enough to finish in one sitting is why
  side projects don't linger half-done.

### Suggestions

1. **Close analysis sessions with a written decision.**
   Several analysis sessions ended "parked" (e2e webhook 422 deferred, DLT
   template ownership question parked, attendance-nav rename only recommended).
   Parked items have no home, so they resurface as re-investigations.
   *Action:* end every analysis session by writing the decision or next action
   into the project note's "Next Actions".
   *Measure next month:* count of parked items that got resolved vs re-investigated.

2. **Weekend load is the real peak — decide if that's intentional.**
   Sat (1,280) and Sun (1,373) are the two heaviest message days; peak cell is
   **Sun 17:00**. Weekdays average ~816. If weekends are your deep-work slots
   by choice, fine — but it's worth confirming it's a choice, not a backlog spillover.
   *Measure next month:* weekend share of messages (baseline: **40%**).

3. **Cap marathon sessions.**
   14 sessions ran ≥ 4h active; the longest was 9.3h (Akshara, Aug 1). The Aug 5
   19:41 marathon is also the one that ended with work still in flight
   (duplicate-warning Phase 2 unfinished). Long sessions correlate with loose ends.
   *Action:* at ~3h, either ship what's done or write a handoff note and stop.
   *Measure next month:* sessions ≥ 4h (baseline: **14**); sessions ending with
   unfinished in-flight work.

4. **Portfolio concentration: 78% Akshara.**
   Healthy while Akshara is the priority — but the Desktop "analyst" habit
   stopped: last investing session was **Jun 30**, and M5Stack Voice has had
   10 minutes total. If those still matter, give them a recurring slot; if not,
   archive them so the project list reflects reality.
   *Measure next month:* investing sessions since Jun 30 (baseline: **0**);
   Akshara share (baseline: **78%**).

5. **PR cadence is bursty — smooth the trough weeks.**
   71 PR-mentions in W22 and 56 in W28 against several zero weeks. Bursts are
   fine for /ship waves, but the zero weeks in between include working weeks.
   *Measure next month:* number of active weeks with ≥1 PR (baseline: 10 of 25).

6. **Automate the vault sync.**
   `sessions/.sync-hashes` implies a manual sync step, and Desktop sessions were
   invisible to the vault until today's import. The pipeline is now 3 commands —
   worth a single script or launchd job so the data is always current.
   *Action:* wrap `import_desktop_sessions.py + extract.py + report.py` in one
   entry point; run it weekly.
   *Measure next month:* days between newest session file and newest sync.

### Metrics scorecard to re-check on 2026-09-07

| Metric | 2026-08-07 baseline | 2026-09-07 |
|---|---|---|
| Weekend share of messages | 40% | |
| Sessions ≥ 4h active | 14 | |
| Analysis sessions ending with written decision | ad-hoc | |
| Investing sessions in the month | 0 (since Jun 30) | |
| Akshara time share | 78% | |
| Active weeks with ≥1 PR | 10 / 25 | |
| Parked items resolved | — | |

---

*Before each review, run `./analytics/refresh.sh` — it creates a fresh
`analytics/YYYY-MM-DD/` snapshot (charts + data + report); older snapshots stay
frozen for comparison.*
