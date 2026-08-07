# Akshara (School Management)

## Goal
- Build and ship the Akshara school management MVP through small, test-backed milestones.

## Current Status
- Active project with sustained delivery across late May 2026.
- Major school-management modules shipped in parallel waves.
- E2E reliability hardening completed; remaining action is to branch and open PR for pending test-only fix in working tree.

## Linked Daily Updates

### June 2026
- [[daily/2026/06/2026-06-03|2026-06-03]] — Payment sandbox learning (card payments, Razorpay)
- [[daily/2026/06/2026-06-11|2026-06-11]] — UPI payment learning module
- [[daily/2026/06/2026-06-14|2026-06-14]] — UPI sandbox debugging
- [[daily/2026/06/2026-06-22|2026-06-22]] — Card/UPI payment debugging

### July 2026
- [[daily/2026/07/2026-07-03|2026-07-03]] — Feature planning M3-01 (fee heads)
- [[daily/2026/07/2026-07-06|2026-07-06]] — M3-03 audit + M3-04 (concessions) spec
- [[daily/2026/07/2026-07-09|2026-07-09]] — Seed data audit & refresh
- [[daily/2026/07/2026-07-10|2026-07-10]] — WeasyPrint DYLD fix + DB schema doc
- [[daily/2026/07/2026-07-11|2026-07-11]] — Parent RBAC over-grant analysis & fix spec
- [[daily/2026/07/2026-07-15|2026-07-15]] — DYLD error analysis + DB connection architecture
- [[daily/2026/07/2026-07-18|2026-07-18]] — Seed setup Q + API documentation
- [[daily/2026/07/2026-07-19|2026-07-19]] — Super admin bug + onboarding guide design
- [[daily/2026/07/2026-07-20|2026-07-20]] — School settings UI tabs restructuring
- [[daily/2026/07/2026-07-21|2026-07-21]] — Academic year status + staff phone sync + Docker secondary env
- [[daily/2026/07/2026-07-22|2026-07-22]] — Employee ID validation + TCO calculator
- [[daily/2026/07/2026-07-23|2026-07-23]] — E2E flake analysis (m3_08 receipt PDF)

## Linked Sessions

### August 2026
- [[sessions/session-2026-08-04-05-55-e8347bb0|2026-08-04 05:55]] — SMS-only absence notification investigation (analysis)
- [[sessions/session-2026-08-04-07-00-e63a3269|2026-08-04 07:00]] — Staff bulk import: XLSX migration + error visibility (PRs #312–#316)
- [[sessions/session-2026-08-05-05-29-203e344e|2026-08-05 05:29]] — DLT/SMS template system analysis (analysis)
- [[sessions/session-2026-08-05-05-39-1310467c|2026-08-05 05:39]] — Disable Communication nav for teachers, RBAC (PR #317)
- [[sessions/session-2026-08-05-14-48-5b2d3977|2026-08-05 14:48]] — 3 platform-console features via /ship (PRs #318–#328)
- [[sessions/session-2026-08-05-14-54-fcbcd0e0|2026-08-05 14:54]] — Students pagination + Attendance-nav investigation (analysis)
- [[sessions/session-2026-08-05-19-41-6ad2b173|2026-08-05 19:41]] — Ad-hoc invoicing shipped (PRs #324/#325/#327); duplicate-warning /ship started (PR #329)

## Delivery Highlights (2026-05-30 to 2026-05-31)
- M1-10 Audit log infra (per-tenant audit_events).
- M2-01 Academic year management.
- M2-02 Class and Section setup.
- M2-03 Student profile CRUD.
- M2-04 Student list (search/filter/pagination).
- M2-10 Staff CRUD + bulk import + class/subject mapping.
- M5-01 Holiday calendar.
- M7-02 School settings (profile, logo, letterhead, signature).

## Notes
- Parallel /ship wave planned and executed on 2026-05-30.
- M7-02 crossed midnight and completed on 2026-05-31.
- Student E2E failures on 2026-05-31 were due to shared test-state drift, not feature regressions.

## Latest Updates (2026-07-23)
- E2E flake in m3_08 receipt PDF analyzed: WeasyPrint 69 + Pillow 12.2 fail on 1×1 LA-mode PNG (from m7_02 school-settings fixture) when embedded as data URI
- Race condition identified: m7_02 e2 uploads/deletes logo in ~500ms window, m3_08 e1 receipt generate can collide and embed broken image
- Candidates to fix: swap PNG format to RGBA, isolate test tenant state, or validate/re-encode uploaded assets in backend

## Next Actions
- Decide on E2E flake fix strategy (PNG format / test isolation / backend hardening)
- Continue module delivery with the same spec -> implementation -> FAQ merge discipline.
