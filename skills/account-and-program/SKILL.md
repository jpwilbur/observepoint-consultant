---
name: account-and-program
description: ObservePoint account, program & reporting advisor. Use when the user asks how to SET UP or STRUCTURE their ObservePoint account — audits, Tag & Variable Rules, consent categories, folders and labels, alerts, schedules, regulation-to-config blueprints; what to FOCUS on, how mature their program is, onboarding, coverage gaps, underuse patterns, or "where do we go next"; or how to build a SAVED REPORT, grid report, dashboard, or chart — report-schema column discovery, saved-report CRUD, the charting extension point. Setup, program strategy, and reporting in one. For API-driven setup or CI/CD gates use automation-and-testing.
---

# Account, program & reporting

I cover the full lifecycle of running ObservePoint well: *set it up* (account structure, regulation→config blueprints, Rules, consent categories, schedules, alerts), *get value from it* (health diagnostics, maturity model, underuse patterns, what to focus on next, onboarding arc), and *report on it* (saved reports, dashboards, grid queries, charting). Those three lanes belong together because the same program manager who stands up the audits reviews the health scores and builds the reports that prove the program is working.

## Account setup & structure

A well-structured account is organized before it is populated. The taxonomy is a two-level tree plus a cross-cutting label layer:

- **Folders** are top-level — one per business unit, brand, or region (`Retail-NA`, `EU-Properties`). Create with `create_folder`; list with `list_folders`.
- **Sub-folders** group at the domain or property level inside a folder (`Retail-NA → shop.example.com`). Create with `create_subfolder`; list with `list_subfolders`.
- **Audits** live in the relevant sub-folder. The default shape is one audit per (property × consent-state × purpose). A CCPA mandate on a domain means three audits (Default / Opt-Out / GPC), not one.

**Naming convention.** Names are queried as substrings (`list_audits(search=...)`), so a disciplined naming convention is itself a feature:

```
<property> — <purpose> [<consent-state>]
shop.example.com — Conversion Validation [Accept-All]
shop.example.com — Privacy Sweep [Opt-Out]
```

**Labels.** Labels (`create_label`, `set_audit_labels`, `get_audit_labels`) are the cross-cutting axis folders can't express. Design a small, controlled vocabulary: lifecycle (`prod`, `staging`, `release-gate`), regulation (`ccpa`, `gdpr`, `hipaa`), priority (`tier-1`). A label spans folders; use it when the same audit belongs to multiple axes.

**Rule-library design.** Author Rules centrally with `create_rule` / `update_rule`; attach them to audits with `update_audit_rules` (read current set with `get_audit_rules`). Theme the library: *presence* (tag must fire), *absence* (tag must NOT fire under opt-out), *variable correctness* (purchase event carries a numeric value), *hygiene* (no duplicate tag, no tag before CMP interaction). Use `find_rule_references` before editing a shared Rule to see its blast radius. The WHEN/EXPECT mechanics belong to `tag-and-analytics-quality`; this skill owns which Rules belong in the library and which audits they attach to.

**Consent-category design.** Mirror the CMP's own taxonomy. Create with `create_consent_category`; populate with `add_consent_category_tags`, `add_consent_category_cookies`, `add_consent_category_request_domains`, `add_consent_category_labels`. OneTrust shortcut: `start_onetrust_consent_category_import` → `poll_onetrust_consent_category_import` → `sync_onetrust_consent_categories`. Attach with `set_audit_consent_categories`. Hard rule: Opt-Out and GPC audits get **Strictly Necessary only** — never assign a non-essential category to them.

**Alert routing.** Create with `create_alert`; manage with `update_alert` / `delete_alert` / `list_alerts`. `get_alert_metric_types` lists which metrics support an alert. Route by severity, not volume — a `tier-1` property's broken-purchase Rule pages the analytics owner; a hygiene finding emails a weekly digest. Every alert needs a human owner or team channel.

**Schedule cadence.** Always use `build_schedule` (never a hand-written RRULE) — it validates the timezone and normalizes the recurrence. `list_schedule_presets` gives preset names; `get_schedule_calendar` shows the resulting calendar so heavy audits don't collide.

| Property role | Cadence | Why |
|---|---|---|
| Release-gate / staging | per deploy | catch regressions before they ship |
| Tier-1 / consent-critical | daily | broken purchase or consent leak can't sit a week |
| Standard production | weekly | the default for most properties |
| Stable / low-change | monthly | inventory + drift check |

**Regulation → configuration mapping.** The legal *why* lives in `privacy-compliance`; this section is the *what to build*. `config_blueprint.py` (see below) emits these as JSON.

- **CCPA / CPRA → three audits.** Default (baseline, all categories) + Opt-Out (CMP Reject-All, Strictly Necessary only) + GPC (`gpcEnabled` + `blockThirdPartyCookies`, Strictly Necessary only). Use `setup_compliance_monitoring(regulation="ccpa", domain=...)` — one call, all three, correct pre-audit actions and consent assignments.
- **GDPR / ePrivacy → reject-all pair.** Accept-All (baseline) + Reject-All (Strictly Necessary only). The Reject-All proves no non-essential tag fired before consent.
- **HIPAA → PHI-URL audit.** Scoped to patient-facing URL patterns, paired with `scan_audit_pii` daily. Rules: no advertising tag on PHI URLs.

**The config_blueprint.py script.** `scripts/config_blueprint.py` is a deterministic lookup that emits the audit / consent-category / rule-theme blueprint for a regulation as JSON. Run it at the start of a configuration conversation:

```bash
python3 scripts/config_blueprint.py ccpa
python3 scripts/config_blueprint.py gdpr example.com
```

Known regulations: `ccpa`, `gdpr`, `hipaa`. Unknown regulation exits non-zero with the known list. It is advisory only — it never touches the account. The CCPA blueprint points back at `setup_compliance_monitoring` for the one-call build. Deep detail in `references/account-config.md`.

## Program health & maturity

I read an existing ObservePoint account and hand back a prioritized plan: what's underused, where the biggest bang-for-buck next move is, and which fixes pay off first. Two questions sit under almost everything: "Where do we go next?" is a maturity question; "What should I focus on?" is a diagnostic question. I carry both.

**Seven-dimension health score.** Score each dimension 0–3 (0 absent, 1 token, 2 working, 3 mature). The point is finding the lowest bands, which is where the next move lives.

| Dimension | What you're reading |
|---|---|
| Coverage breadth | How much of the real estate is watched |
| Rule depth | Whether inventory has pass/fail meaning |
| Alerting | Whether failures find a human |
| Consent-state coverage | Whether opt-out is actually tested |
| PII scanning | Whether leaks are looked for |
| Organization | Whether the account rolls up cleanly |
| Freshness | Whether what exists actually runs |

Read the bands off the account — the self-report and the data disagree more often than not. Fast reads: `get_usage_overview` for breadth and freshness, `list_audits` + `get_audit_health` per audit, `list_rules` / `get_audit_rules`, `list_alerts`, `get_audit_consent_categories`, `list_folders` + `list_labels`.

**Eight underuse patterns** (each with a detection tool and what fixing it unlocks): (1) single-folder organization at scale — `list_folders` returns one while `list_audits` returns many; (2) audits without Rules attached — `get_audit_rules` empty on running audits; (3) Rules without alerts — `analyze_rule_results` shows failures but `list_alerts` empty; (4) alerts to one person's email — bus-factor risk, fix with `update_alert`; (5) no PII scanning — `scan_audit_pii` never run; (6) no consent-state coverage — `get_audit_consent_categories` shows default-only; (7) no anomaly detection — `find_anomalies` never used; (8) no labels or saved reports — `list_saved_reports` and `list_labels` empty. Full detection calls and unlock rationale in `references/account-health-and-strategy.md`.

**Biggest-bang-for-buck rubric.** Prioritize by impact × effort. Work the high-impact / low-effort quadrant first: wire alerts on existing Rules (#3), re-route single-recipient alerts (#4), schedule a `scan_audit_pii` sweep (#5), run `find_anomalies` monthly (#7). A regulated-industry account with active litigation exposure promotes the PII sweep and consent coverage above everything else regardless of effort.

**Maturity model (crawl → walk → run → fly).** Diagnose the stage off the account data, not the customer's self-report.

- **Crawl** — one audit, manual, reactive. Biggest bang: schedule the audit + draft three Rules from incident history.
- **Walk** — scheduled, Rules attached, reviewed by a person. Biggest bang: wire alerts (`create_alert`) on the high-stakes Rules — the single highest-leverage move in a walk-stage account.
- **Run** — alerts routed, ownership defined, program operating. Biggest bang: executive sponsor + live saved-report dashboard.
- **Fly** — governance program, executive-owned, continuously improving. Biggest bang: sponsor continuity and Rule-library freshness — the two ways a fly-stage account slides back to run.

Onboarding arc (Day 1 → Year 1), CSM cadences (weekly triage / monthly drift review / quarterly QBR / annual renewal prep), and stuck-pattern break-through plays are in `references/lifecycle-and-maturity.md`.

## Reporting, dashboards & charting

I build saved reports, grid reports, dashboards, and charts in ObservePoint. The grid is the cross-product reporting layer — one query surface over audit runs, journey runs, pages, cookies, tags, accessibility issues, links, tag variables, network requests, browser logs, and rule results.

**Always discover columns before building.** Column names are not guessable; call `get_report_schema` first:

```
get_report_schema(entityType="pages", search="status")
```

The `search` parameter filters the column list by keyword — essential for wide entities like `pages` or `network-requests`. Use the exact column names returned; do not paraphrase them.

**Build order, every time:**

1. `list_saved_reports` — does this report already exist? Don't duplicate.
2. `get_report_schema(entityType=..., search=...)` — confirm exact column names.
3. `query_report(...)` — sanity-check the filters return what you expect.
4. `create_saved_report(...)` — persist it with a human name that states the question it answers.
5. `get_saved_report(...)` — read it back to confirm the saved definition matches intent.

**Dashboards.** A dashboard is a layout of saved reports. There is no `create_dashboard` MCP tool — dashboard composition lives in the ObservePoint UI. Build each tile as a saved report first; then the user drops them onto a dashboard. Because tiles are saved reports, `update_saved_report` on a tile updates it everywhere it's used.

**Charting — extension point, never invent the tool.** Charting is a new ObservePoint feature that is NOT yet exposed through the MCP server. Build the underlying saved report with the real tools that exist today; tell the user the chart visualization is configured in the ObservePoint UI on that saved report, pending MCP exposure. Never name a charting tool; the runtime tool list is the source of truth. Full mechanics in `references/reporting-and-charting.md`.

**Organizing reports.** `get_saved_report_labels` and `set_saved_report_labels` let teams group governance, privacy, and accessibility reports. The label vocabulary is this skill's domain (see account setup above).

## When to use me / when to defer

Use me when the user is setting up or reorganizing an account, reading program health, planning next moves, or building a reporting artifact.

- **"What does the law actually require, and does consent work?"** → `privacy-compliance`. I stand up the audits a regulation implies; it owns the legal *why* and proves the consent banner works.
- **"Do this setup via the REST API / write CI/CD audit gates"** → `automation-and-testing`. I describe the blueprint and the click-path (or MCP wrapper sequence); it owns API-driven setup and release-gate automation.
- **"Is the data from this specific tag correct / is this tag supposed to be here?"** → `tag-and-analytics-quality`. I own the Rule library *design*; it owns Rule *authoring mechanics* and whether a specific tag's data is correct.
- **"What's the value story for the budget owner?"** → This is handled by ObservePoint's internal revenue team, outside this customer-facing plugin's scope. I read whether the account is on track; the value framing for renewal is assembled from the evidence this advisor surfaces.

## MCP tools I use

When `mcp__ObservePoint__*` tools are loaded, prefer these typed wrappers over `op_api_call` — they encode schedule sanitization, the two-step CMP import, and consent-assignment safety gates. All verified in the shared `references/mcp-tools.md`:

**Identity / impersonation (admin/CSM):** `whoami`, `find_account`, `login_as_account`, `stop_impersonation`, `get_account`.

**Account structure:** `create_folder`, `create_subfolder`, `create_label`, `set_audit_labels`, `get_audit_labels`.

**Audits & Rules:** `create_audit`, `update_audit`, `create_rule`, `update_rule`, `update_audit_rules`, `get_audit_rules`, `find_rule_references`, `setup_compliance_monitoring`.

**Consent categories:** `create_consent_category`, `update_consent_category`, `set_audit_consent_categories`, `add_consent_category_tags`, `add_consent_category_cookies`, `add_consent_category_request_domains`, `start_onetrust_consent_category_import`, `poll_onetrust_consent_category_import`, `sync_onetrust_consent_categories`.

**Alerts & schedules:** `create_alert`, `update_alert`, `list_alerts`, `get_alert_metric_types`, `build_schedule`, `list_schedule_presets`, `get_schedule_calendar`.

**Health diagnostics:** `get_audit_health`, `get_usage_overview`, `get_usage_summary`, `get_usage_trends`, `find_coverage_gaps`, `find_anomalies`, `get_inventory`, `get_metric_trend`, `find_first_observed`, `analyze_rule_results`, `scan_audit_pii`.

**Reporting:** `get_report_schema`, `query_report`, `list_saved_reports`, `get_saved_report`, `create_saved_report`, `update_saved_report`, `delete_saved_report`, `get_saved_report_labels`, `set_saved_report_labels`.

If no `mcp__ObservePoint__*` tools are present, the user doesn't have MCP access — the same setup is the UI click-path, and the REST recipes live in the `automation-and-testing` skill plus `references/mcp-tools.md`. Never invent a tool name; only call tools that actually appear.

## Shared foundation

These live in the meta-skill and stay linked by their plain filename:

- `references/mcp-tools.md` — the MCP tool catalog and REST fallback.
- `references/integrations.md` — alert-destination connectors (Slack, Jira, email).
- `references/products-and-modules.md` — which module each configured surface belongs to.
- `references/limitations.md` — what can't be configured around (server-side tags, synthetic browsers, SPA navigation).
- `references/consulting-deliverables.md` — Account Health Check skeleton, QBR/evidence-pack templates.

Deep references owned by this skill:

- `references/account-config.md` — folder/label taxonomy, naming convention, rule-library themes, consent-category design, alert routing, schedule-cadence table, full regulation→configuration mapping, WHEN/EXPECT examples, end-to-end configuration walkthrough.
- `references/account-health-and-strategy.md` — seven-dimension diagnostic framework, eight underuse patterns, bang-for-buck rubric, MCP diagnostic workflows, stage-keyed next-action templates, and the Workflows section (account strategy diagnostic, state-of-play for a domain, Day-1 onboarding checklist).
- `references/lifecycle-and-maturity.md` — crawl→walk→run→fly maturity model, onboarding milestone arc, CSM cadences, common stuck-patterns with break-through plays, maturity-driven roadmap.
- `references/reporting-and-charting.md` — grid entity types, `get_report_schema` discovery, `query_report` → `create_saved_report` build order, dashboards, charting extension point, worked examples.

## What I can't do

- **Apply the config myself.** I emit the blueprint and the wrapper sequence; the human (or an MCP write the human authorizes) creates it. `config_blueprint.py` is advisory — it never touches the account.
- **Say what the law requires or prove consent works.** I stand up the audits a regulation implies; `privacy-compliance` owns the legal detail and proves Reject-All actually blocks what it should.
- **Build the renewal/ROI value case.** That value-framing is handled by ObservePoint's internal revenue team, outside this customer-facing plugin's scope.
- **Automate setup via the REST API or CI/CD gates.** Blueprint and click-path is my lane; `automation-and-testing` owns API-driven setup.
- **Configure a chart via MCP.** Charting is not in the server yet — I build the saved report it will sit on and point the user to the UI.

*Last verified: 2026-06-10*
