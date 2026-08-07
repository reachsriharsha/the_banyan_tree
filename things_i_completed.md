---

Session (2026-08-07 05:14) — clone_repo.sh backup script (qmd://sessions/session-2026-08-07-05-14-8ce0a896.md)

**Project:** _(standalone tooling — repo `/Users/swbs/src/backup`)_

- Wrote `clone_repo.sh`: takes a git URL, creates a `yyyy_mm_dd_hhmmss_<repo_name>` directory, and clones into it
- Derives repo name from the URL (strips trailing `.git`), timestamps via `date +%Y_%m_%d_%H%M%S`, uses `set -euo pipefail` for fail-fast + usage error when the arg is missing

---

Session (2026-08-05 19:41) — Ad-hoc invoicing shipped; duplicate-warning pipeline started (qmd://sessions/session-2026-08-05-19-41-6ad2b173.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Shipped `m3_19_adhoc_student_invoice` end-to-end (spec PR #324, impl PR #325, FAQ PR #327 — all merged): `POST /invoices/manual` (XOR student_ids/section_id targeting), `POST /invoices/{id}/cancel`, nullable `Invoice.description`, `list_invoices` join fix, frontend dialog; unit 409/409 and api 630/630 pass
- Wrote `docs/housekeeping/db-connection-pooling.md` (database-per-tenant QueuePool analysis, DigitalOcean 22-connection exhaustion math, PgBouncer transaction-mode fix + NullPool/`prepare_threshold=None` changes)
- Wrote `docs/housekeeping/small-institution-support.md` — decision record for dance/art/camp schools (season-as-academic-year, one-student-row-per-discipline, ad-hoc invoicing as the only code change needed)
- Root-caused 39 api failures to `dev_db recreate` run without `--seed` (not a regression); fixed e2e `e1` (admin→parent role switch missing session reset) with a one-line `clearCookies()`
- Created shared `.claude/settings.json` permission allowlist (+ local `/tmp` allows) in the akshara repo
- Locked scope for `m2_03_duplicate_student_warning` (live debounced name+DOB check, red-bar UX, 409 + `acknowledge_duplicate` backstop) and started `/ship`: spec PR #329 merged (tracker Specced)
- In progress at session end: Phase 2 (build) of duplicate-warning not yet merged; e2e webhook 422 flake handed to user

---

Session (2026-08-05 14:54) — Students pagination + Attendance nav investigation (qmd://sessions/session-2026-08-05-14-54-fcbcd0e0.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Analysis only (no code changed, per request)
- Confirmed the admin Students page uses cursor/keyset pagination (25/page, limit capped at 200) via TanStack `useInfiniteQuery` "Load more" — not a fetch-all
- Flagged CSV export (`/students/export`) as the only fetch-everything path worth confirming it streams
- Diagnosed the core confusion: the "Attendance" nav item routes to `HolidayCalendarPage` (m5_01), not an attendance view; recommended renaming it to "Holidays"
- Mapped the 3 attendance nav entries to real destinations (Holiday Calendar / Mark Attendance / Attendance Register), gated by distinct RBAC perms
- Suggested (not implemented) a server-side total-count for "1–25 of N" display

---

Session (2026-08-05 14:48) — Shipped 3 platform-console features via /ship (qmd://sessions/session-2026-08-05-14-48-5b2d3977.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Shipped `m8_11_platform_console` (spec PR #318, impl #319, FAQ #320 — merged): new left nav, Home dashboard stat cards (Total/Active/Suspended/Pending-erase), redesigned tenants table, tenant detail page with cross-DB `SchoolSettings` read; added `admin_email`/`admin_phone` to `TenantOut` + `GET /platform/tenants/{slug}`
- Shipped `m8_12_console_preselect` (spec #321, impl #322, FAQ #323 — merged): SMS page reads `?tenant=<slug>` preselect, Feature Flags "showing overrides for X" banner + presets, unit-tested `preselect.ts`
- Shipped `m5_07_attendance_colors` (spec #326, impl #328 — merged; FAQ skipped): shared `attendance/status.ts`, exception-first color-coding on monthly register with legend + color-blind-safe letters
- Investigated red e2e gate: confirmed `m3_19 e2` + `m3_10 e2` fail deterministically (HTTP 422 webhook) on clean main — pre-existing payment-webhook regression from the m3_19 fees merge, independent of the attendance change; `m2_09 e2` is the known `Date.now()` flake; flagged webhook regression to user (deferred)
- All three at tracker Merged, `RELEASE_NOTES.md` regenerated

---

Session (2026-08-05 05:39) — Disable Communication nav for teachers (RBAC) (qmd://sessions/session-2026-08-05-05-39-1310467c.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Fixed a teacher over-grant: dropped `communication:read` + `communication:send` from the teacher role in `backend/app/authz/catalog.py` (hides the nav item and closes the API together, no frontend change)
- Flipped 4 tests asserting teacher access to assert denial (`m1_09 u1`, `m4_06 a9`, `m4_02 a8`, `m4_05 a9`); added E2E regression spec `teacher/sidebar-scope.spec.ts`
- Ran full `run_all.sh` (caught 2 regressions the static search missed), re-ran clean; backend 5/5, api 27/27, e2e green
- Ran a tracker-drift audit (0 total/passing drift across 84 rows); bumped `m1_09_*` rows `e:7/7 → 8/8` in a separate `chore(tracker)` commit
- Opened/merged PR #317; updated spec docs + FAQ; saved a memory note to run the full API suite on RBAC-role changes

---

Session (2026-08-05 05:29) — DLT/SMS template system analysis (qmd://sessions/session-2026-08-05-05-29-203e344e.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Analysis/discussion only (no code changed, per request)
- Determined DLT template registration is super-admin only; school admins can't see or perform it
- Documented that template bodies live in code (`TEMPLATE_CATALOG` in `communication/catalog.py`); changing one needs a code change + PR + `app.templates_sync` CLI
- Established what's editable today: super admin sets per-school DLT template id + lifecycle status (draft→approved→active→disabled); activation without a DLT id → 422
- Key finding: the requested "assign a template to a school" already exists as a backend dark feature (`GET/PUT/DELETE /api/v1/communication/notification-map`, school-admin `settings:update` gated) but has no UI
- Surfaced open product questions (move template creation to a super-admin UI? who owns mapping overrides?) — parked

---

Session (2026-08-04 15:13) — SwimAcademy MVP built, dockerized, poolside UX (qmd://sessions/session-2026-08-04-15-13-b09feb68.md)

**Project:** [[projects/swimmer progress tracker/Requirements|Swimmer Progress Tracker]] _(repo `cadencelanes`)_

- Built the full SwimAcademy MVP from spec in one shot: FastAPI + SQLAlchemy 2.x backend, two-DB pattern (`control.db` + per-club `club_{id}.db`, 10 tables seeded with 5 styles / 7 events), phone+OTP JWT auth, RBAC, and all spec endpoints (club register/approval, coaches, student CRUD, sessions w/ auto-attendance, timings w/ auto personal-best, notes, assessments, computed progress report)
- Built a React + Vite + Tailwind v4 + Recharts frontend (16 pages)
- Packaged into a single Docker image via `./run.sh` (26-check smoke test), later migrated to docker-compose on an isolated bridge network with a restart policy; switched storage to a host bind mount for backup visibility
- Made session types dynamic (keeps the one-per-type-per-day constraint); confirmed assistant coaches can create sessions
- Rebuilt Timings into a poolside quick-entry tool (auto-detected session, tap-chip style/distance, present-swimmers Enter flow, inline PB feedback); added exact age (y/m/d) display
- Added missing UI forms for coach notes + skill assessments; added a Coach/Analytics mode switch with a poolside bottom-tab home
- Created reusable `seed_demo.py` + `DEMO_SCHOOL.md`; reseeded a category-based demo (24 students, 44 sessions over 4 weeks, ~160 timings, a competition session, assessments)

---

Session (2026-08-04 07:00) — Staff bulk import: XLSX migration + error visibility (qmd://sessions/session-2026-08-04-07-00-e63a3269.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Diagnosed the original import failure as a delimiter mismatch (parser split `subjects` on `;` but the CSV used commas; "Art" ≠ seeded "Art & Craft")
- Migrated staff import CSV→XLSX: `build_import_template_xlsx()` + `_parse_import_xlsx()` (openpyxl read-only, 10MB/1000-row guards, header check, numeric coercion); rewrote the frontend to a single validate-then-commit Import button
- Added staff-import logging (`import.started`, per-row `row_failed`, `completed` now fires on dry-run); registered events in `log-schema.md`
- Fixed a real bug: `row_failed` log used the reserved LogRecord attr `message` (would 500 every failing row) → renamed to `reason`
- Fixed a cryptic 422: backend `_handle_problem` now logs a `request.problem` event; frontend surfaces `error.detail` instead of the bare status
- Added tests (a11/a12 on real xlsx, a15 title-row 422, e2e e3/e4); updated the m2_10 spec set + FAQ
- Shipped via 5 merged PRs (#312 feature, #314 error visibility, #313/#315/#316 tracker); `run_all.sh --fast` passed (609 api tests)

---

Session (2026-08-04 05:55) — SMS-only absence notification investigation (qmd://sessions/session-2026-08-04-05-55-e8347bb0.md)

**Project:** [[projects/akshara/README_Akshara|Akshara]]

- Investigation only (no code changed)
- Documented the absence-SMS architecture: channel-agnostic port-adapter in `communication/` + `attendance/service.py` `notify_absences()` trigger; dedup via `AbsenceNotificationMark`, cancels on correction
- Confirmed SMS is not deliverable yet (`PendingSender` placeholder, no real provider wired)
- Confirmed there's no auto-dispatch — messages drained only by the manual/cron CLI `python -m app.messages_dispatch <tenant>` (or `--all`)
- Answered how to send SMS only: disable other templates (recommended) / per-tenant `notification_mappings` override / edit `DEFAULT_MAP`; provided SQL
- Noted template-management UI is scheduled under US-M4-01 (Sprint 13) but only the read endpoint has landed

---

Session (2026-07-23) — E2E Flake Analysis

[[projects/akshara/README_Akshara|Akshara]]

**Work:** E2E test failure analysis for m3_08 receipt PDF generation
- Analyzed 1 failed + 2 skipped tests in receipt-download.spec.ts
- Root cause identified: PNG fixture (1x1 transparent LA-mode PNG from school-settings spec) embedded in PDF crashes WeasyPrint + Pillow 12.2 when specs overlap in fullyParallel mode
- Race condition: m7_02 e2 uploads logo, m3_08 e1 generates receipt with embedded logo, then m7_02 e2 deletes it — collision window ~500ms
- Not a regression; deterministic failure only when timing aligns
- Found hardcoded PNG fixture in test/e2e/specs/admin/school-settings.spec.ts:9-12
- Documented 3 candidate fixes (swap PNG format, isolate test state, harden backend validation)

**Output:** Analysis documented in memory; no code changes needed yet

---

Session 1 — March 28, 6:33 AM (qmd://sessions/session-2026-03-28-06-33-0e6673a3.md)

Mailreeper: Email Rule Engine

**Project:** [[projects/autolife/README|Autolife Toolkit]]

- Built a subject-based rule engine for mailreeper
- YAML-driven rules to delete or label emails by subject match
- Added --dry-run, --days, --all-mail CLI flags
- Rules run before expense parsing; deleted emails are excluded from parsing
- Daily report now includes an "Email Rules Applied" section

---

Session 2 — March 28, 8:48 AM to late night (qmd://sessions/session-2026-03-28-08-48-2957a080.md)

Repo Restructuring

**Project:** [[projects/autolife/README|Autolife Toolkit]]

- Moved README.md and CLAUDE.md into mailreeper/
- Created new root-level docs describing autolife as a multi-tool automation toolkit

Zerodha Holdings Tool

**Project:** [[projects/ai_investment_analysis/README|AI Investment Analysis]]

- Built Kite Connect OAuth with local callback server (WSL-aware via cmd.exe)
- Debugged browser login redirect issues
- Built headless login using credentials + TOTP (pyotp) for cron
- Debugged 403 to headers fix to password quoting to TOTP to /connect/finish failure to pivoted enctoken approach (using Kite web API directly instead of SDK)
- Holdings download to CSV/JSON with portfolio summary
- Built HoldingsAnalyzer — categorizes stocks by drawdown (5%/10%/15% buckets), sends color-coded email

Security

**Project:** [[projects/autolife/README|Autolife Toolkit]]

- Created SECURITY.md — GPG encryption guide for storing Zerodha credentials

---

Session 3 — March 29 (current session, not yet exported)

Portfolio Analyzer Integration

**Project:** [[projects/ai_investment_analysis/README|AI Investment Analysis]]

- Renamed portfolio_automation to portfolio_analyzer
- Merged dependencies into root pyproject.toml
- Built CSV column bridge (write_zerodha_console_csv) mapping Kite API fields to Zerodha Console format
- Updated run_weekly.py to auto-download holdings from Zerodha (no manual CSV)
- Created email_report.py — Gmail-friendly email builder with inline styles + CID-embedded chart images (separate from the interactive HTML report)
- Added send_mime_email() to mailreeper for multipart MIME support

Cron Setup

**Project:** [[projects/autolife/README|Autolife Toolkit]]

- Created wrapper scripts: run_zerodha_holdings.sh, run_portfolio_analyzer.sh
- Analyzed cron compatibility for all 3 tools
- Set schedules: Mailreeper daily 4 AM, Zerodha weekdays 4 PM, Portfolio Analyzer Friday 6 PM
- Centralized cron docs in root README with GPG and plaintext options

---

Session Summary — 2026-03-29

Plugin-Autodev (Claude Code Plugin)

**Project:** [[projects/pi_dev_cursor_ollama/README|Pi Dev / Cursor + Ollama]], [[projects/agentic_study/lc-deep_agents|Agent Study]]

Built a two-agent autonomous development system with composable sub-agents.

Key decisions:

- Architecture: Composable agents in a single plugin (Approach C) — Atlas + Vulcan + spawnable sub-agents
- Specs as code: Specs go through branch, PR, review, merge — same as implementation code
- Feature IDs: feat*<domain>*<NNN> format (Atlas suggests, human confirms), also used as GitHub labels for bug traceability
- Single tracking file: docs/tracking/features.md — one table, all features at a glance
- Two-commit pattern: Every PR merge = merge commit + tracking update commit on main
- Clean sandbox: Both agents always start from fresh git pull origin main
- Sub-agents are read-only: They produce markdown, primary agent commits

Files created (12):

| File | Purpose |
|---|---|
| .claude-plugin/plugin.json | Plugin manifest |
| DESIGN.md | All design decisions and architecture |
| README.md | Installation, usage, conventions |
| conventions.md | Single source of truth for naming/paths/status |
| agents/atlas.md | Planner agent |
| agents/vulcan.md | Builder agent |
| agents/doc-writer.md | Documentation sub-agent (read-only) |
| skills/atlas/SKILL.md | Atlas slash command |
| skills/vulcan/SKILL.md | Vulcan slash command |
| hooks/update-tracker.sh | Post-merge tracking updates |
| scripts/init-feature.sh | Create spec directory structure, |
| scripts/next-feature-id.sh | Suggest next feature ID |

Validation fixes applied:

- Moved manifest to .claude-plugin/plugin.json
- Restructured skills into subdirectories (skills/atlas/SKILL.md)
- Fixed hooks schema to standard matcher + hooks array format
- Replaced jq dependency with gh --jq built-in
- Fixed tools to allowed-tools in doc-writer frontmatter

Still pending:

- End-to-end test of /atlas flow on a real feature
- End-to-end test of /vulcan flow on a specced feature
- Plugin not yet committed to git
- Future agents: Minerva (reviewer), customer-docs, log-analyzer (with version/label awareness)

---

Session Summary — 2026-05-27

**Project:** [[projects/akshara/README_Akshara|Akshara]]

Bug Fix

- DB seeding fix: dev_db.py was failing on recreate --seed due to SQLAlchemy inserting child rows before parent rows (nullable FK ordering issue). Fixed by adding _add_in_order() helper that flushes after each row.

US-M1-03 — Client Logger + Shipping Endpoint (3 pts) — Shipped

Full four-skill lifecycle:
- Vishwakarma — spec PR #3 (merged)
- Nala — impl PR #4 (merged). Frontend global error handler (window.onerror / onunhandledrejection) with batched shipping (2s / 10-entry cap). Backend POST /api/v1/platform/client-logs + dev-only trace endpoint. 5 unit + 6 API tests.
- Vyasa — impl notes + changelog
- Gargi — FAQ PR #5 (merged)

US-M1-05 — Tenant DB Template + Provisioning CLI (8 pts) — Shipped

Full four-skill lifecycle:
- Vishwakarma — spec PR #6 (merged)
- Nala — impl PR #7 (merged). New tenancy/service.py with provision_tenant() (idempotent, rollback on failure), upgrade_all_tenants(). CLI subcommands tenant-init and tenant-upgrade-all. 2 unit + 7 API integration tests.
- Vyasa — impl notes + changelog
- Gargi — FAQ PR #8 (open, pending merge)

Tracker State:

| Feature | Status |
|---|---|
| m3_03_late_fee_rules | Merged (prior) |
| m1_03_client_logger | Merged |
| m1_05_tenant_db_template | Merged |

Next Up

- US-M1-06 — Tenant context middleware + per-tenant session factory (depends on M1-05)

---

Session Summary — 2026-05-29

**Project:** [[projects/akshara/README_Akshara|Akshara]]

Tenancy Delivery Milestone:

- Shipped 3 tenancy features end-to-end on 2026-05-28 via the spec to build to doc to FAQ workflow:
   - m1_05_tenant_db_template
   - m1_06_tenant_context
   - m1_07_tenant_onboarding
- All three features merged with unit + API tests, implementation notes, changelog, and user FAQ coverage (PRs #6 through #14).
- m1_07 delivered full create-tenant flow:
   - super-admin-gated POST/GET /api/v1/platform/tenants
   - provisioning saga
   - platform Tenants UI (TanStack Query + RHF + zod)
   - end-to-end coverage

Testing, Debugging, and Reliability:

- Started manual GUI testing for tenant creation on 2026-05-29 and hit a 401.
- Diagnosed 401 root cause as missing or mismatched platform-admin token and confirmed backend reads os.environ directly (no dotenv loader).
- Added AKSHARA_LOG_FORMAT=text dev log toggle for human-readable local debugging logs with unit tests (PR #15, merged).
- Backfilled real test counts for m1_05, m1_06, and m1_07 in the tracker and committed to main.
- Root-caused create-tenant 500: make_tenant_dsn used str(url), masking password as *** and breaking per-tenant DB auth.
- Fixed DSN rendering with render_as_string(hide_password=False) and added regression test asserting password is preserved (PR #17, merged).
- Verified end-to-end fix: real POST /api/v1/platform/tenants returns 201, tenant appears in list, and throwaway tenant was cleaned up.

Security and Secrets Handling:

- Hardened secret handling (PR #16):
   - start_api_server.sh now sources gitignored backend/.env
   - added backend/.env.example
   - tracked e2e package-lock.json
   - removed plaintext token from versioned script
- Rotated dev super-admin token across backend/.env and frontend/.env and kept values aligned without committing secrets.
- Logged security concern in MVP plan section 14: tenants.dsn currently stores DB password in cleartext, marked for dedicated design discussion.

Projects and Tooling:

**Project:** [[projects/pi_dev_cursor_ollama/README|Pi Dev / Cursor + Ollama]]
- Worked on local setup of pi.dev coding agent and Cursor with Ollama.
- Model choice as of 2026-05-29: qwen 3.6.

**Project:** [[projects/openclaw_exploration/README|OpenClaw Exploration]]
- Bought OpenClaw on 2026-05-28; use case is not finalized yet — moved into an exploration project.

**Project:** [[projects/m5stack_sarvam_voice_agent/README|M5Stack Sarvam Voice Agent]], [[projects/akshara/README_Akshara|Akshara]]
- Added a new hardware project after receiving M5Stack Stick S3: build a voice agent using Sarvam models.
