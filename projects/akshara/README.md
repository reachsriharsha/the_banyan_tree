# Akshara (School Management)

## Goal
- Build and ship the Akshara school management MVP through small, test-backed milestones.

## Current Status
- Active project with sustained delivery across late May 2026.
- Major school-management modules shipped in parallel waves.
- E2E reliability hardening completed; remaining action is to branch and open PR for pending test-only fix in working tree.

## Linked Daily Updates
- [[daily/2026/05/2026-05-30|2026-05-30]]
- [[daily/2026/05/2026-05-31|2026-05-31]]

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

## Next Actions
- Branch and open PR for the pending E2E-only fix currently in working tree on main.
- Continue module delivery with the same spec -> implementation -> FAQ merge discipline.
