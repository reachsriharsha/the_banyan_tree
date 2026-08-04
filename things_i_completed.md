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
