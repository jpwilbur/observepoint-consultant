# Web governance frameworks — ObservePoint's published checklists + the report library that operationalizes them

Load this when the user wants to run or understand an ObservePoint **Web Governance Framework** — an expert-validated checklist for a specific governance goal (validate a Google Analytics / Adobe Analytics / Adobe Experience Platform implementation, or stand up CIPA-compliance monitoring) — **or** when they want to **build a report** and you should reach for a pre-built template instead of authoring one from scratch.

A framework is ObservePoint's opinionated answer to "how do I do X well." It bundles three things: a set of named **checks** grouped into policy categories, a recommended **run cadence**, and the **pre-built reports** that make each check observable. This file owns the framework construct and the framework→report mapping. It does not own the mechanics of editing/scheduling/charting a report (that's `account-and-program`), the depth of analytics validation (`tag-and-analytics-quality`), or CIPA legal-evidence framing (`litigation-defense`).

**The frameworks are published and still evolving — the help-doc articles are the source of truth.** Link the customer to the article for the current, complete framework; this file is the operating summary. The library is expanding; treat anything not listed here as "check the hub article."

Hub article: https://help.observepoint.com/en/articles/13657336-observepoint-web-governance-frameworks

## Contents

1. [The template-first reporting path](#1-the-template-first-reporting-path)
2. [Standard operating cadence](#2-standard-operating-cadence)
3. [Analytics implementation frameworks (GA / Adobe Analytics / AEP)](#3-analytics-implementation-frameworks-ga--adobe-analytics--aep)
4. [CIPA compliance framework](#4-cipa-compliance-framework)
5. [Boundaries](#5-boundaries)

## 1. The template-first reporting path

Every framework check maps to a report — and ObservePoint pre-built the reports for you. There is a **library of ObservePoint-managed report templates** (100+, organized by use case) covering exactly these checks: broken tags, missing tags, duplicate tags, missing identity cookies, missing data layer, query-params-lost-on-redirect, CIPA wiretap risk, and many more. **Do not build these from scratch. Clone the template.**

The path, every time:

1. `list_report_templates` — search the library for the check you need. Filter by `search` (e.g. "broken google analytics", "data layer", "CIPA"), `gridEntityType` (`pages`, `tags`, `cookies`, `tag_variables`, `browser_logs`, `network_requests`, `links`), or `useCase` ("privacy", "tag governance", "page performance"). (Report-template `gridEntityType` values are underscored — `tag_variables`, `web_audit_runs` — not the hyphenated `entityType` that `query_report` uses.)
2. Match the template **by name** and confirm it in the returned list. Template IDs are assigned by the platform and change over time — **never assume an ID; read it from the live list.**
3. `create_report_from_template` with the chosen template's id — clones it into the account as an editable saved report. Run `dryRun:true` first to preview; the report is created `private` by default. It's a WRITE — confirm with the user before committing.
4. Customize / schedule / chart the cloned report — those mechanics live in `account-and-program`.

This is the **first** thing to try whenever someone asks for a report that matches a framework check. Build-from-scratch (discover columns → query → save) is the fallback for genuinely bespoke reports with no template. The live tool list is the source of truth; if `list_report_templates` / `create_report_from_template` aren't loaded in your session, the same library is in the ObservePoint UI under report templates. See `references/mcp-tools.md`.

## 2. Standard operating cadence

Every framework recommends the same monitoring rhythm. Translate it into ObservePoint audit schedules:

| Frequency | Scope | Goal | In ObservePoint |
|---|---|---|---|
| Daily | 10–100 critical pages | Confirm coverage holds | A scheduled daily audit of the key pages |
| Every deployment | 10–15% sample | Catch regressions before release | An audit run wired into the release pipeline — a **CI/CD gate** (see `automation-and-testing`) |
| Quarterly | 100% of pages | Total coverage | A full-site audit on a quarterly schedule |

Setting up the schedules and the account structure behind them is `account-and-program`'s job; wiring the every-deploy run into CI/CD is `automation-and-testing`'s.

## 3. Analytics implementation frameworks (GA / Adobe Analytics / AEP)

Three frameworks — **Google Analytics Implementation**, **Adobe Analytics Implementation**, and **Adobe Experience Platform (AEP) Implementation** — share one check spine because they ask the same questions of three different platforms. For each check, find the matching template with the `search` hint shown (substitute the platform name).

| Policy | Check | Report to clone (search hint) |
|---|---|---|
| Tag Health | Tags return a success (200) status | "broken `<platform>` tags" |
| Tag Health | No console errors tied to the tag | "`<platform>` browser console errors" |
| Tag Health | No console warnings tied to the tag | "`<platform>` browser console warnings" |
| Tag Health | Tag loads in under 500 ms | "`<platform>` load times over 500" |
| Tag Implementation | Every page fires the tag | "pages missing `<platform>`" |
| Tag Implementation | Data goes to the correct ID | GA: "measurement IDs by domain"; Adobe: "report suite IDs … domain" |
| Tag Implementation | Tag is not duplicated | "duplicate `<platform>` tags" |
| Tag Implementation | Tag fires before LCP | "`<platform>` tags firing after LCP" |
| Tag Implementation | Values are ASCII-only | "`<platform>` capturing non-ASCII" |
| Identity | Identity cookie present on every page | GA: "missing _ga cookies"; Adobe Analytics: "missing AMCV cookies"; AEP: "missing kndctr_ cookies" |
| Data Layer | Data layer object present | "pages missing data layer" |
| Page Behavior | Query parameters survive redirects | "lose query parameters after redirects" |
| Privacy | Tag honors consent; no PII/PHI | consent proof → `privacy-compliance`; PII → `scan_audit_pii` |

Platform articles (source of truth):

- Google Analytics — https://help.observepoint.com/en/articles/13688039-google-analytics-implementation-framework
- Adobe Analytics — https://help.observepoint.com/en/articles/13657294-adobe-analytics-implementation-framework
- Adobe Experience Platform — https://help.observepoint.com/en/articles/14111777-adobe-experience-platform-aep-implementation-framework

**How the advisor work splits.** `tag-and-analytics-quality` owns *why* each check matters and how to validate the data deeply (the `WHEN … EXPECT` Rules, data-layer timing, value integrity). This file owns *which framework the check belongs to and which report proves it*. The consent checks ("honors consent", "no PII/PHI") are `privacy-compliance` / PII-scanning work.

The frameworks also recommend governance documents — a Business Requirements Document, a Technical Specifications Document, a Measurement Plan, and a Taxonomy Guide. Point the customer to the article; templated deliverables live in `references/consulting-deliverables.md`.

## 4. CIPA compliance framework

The **CIPA Compliance** framework operationalizes California Invasion of Privacy Act exposure — **Penal Code §631** (routing a user's communications through a third party before consent is litigated as an unauthorized wiretap) and **§632.7** (real-time recording disclosure). Its policy spine:

- **Notice & Prior Consent** — wiretap-risk tags (session replay, behavioral recording, advertising, web analytics, chat) must be **suppressed until affirmative opt-in**; real-time recording disclosure must be clear.
- **Chat & Form Governance** — live-chat text not captured until submitted; no leakage while a form is being filled.
- **Piggybacking & Secondary Interceptions** — no unmapped secondary scripts spawned by an authorized vendor.

**The report + the audit it depends on.** The "Pages with CIPA Non-Compliance Risk" template (currently flagged experimental in the platform) flags pages where wiretap-risk tags execute in the **default consent state**. It is meaningful **only against an audit configured with a California geolocation and no pre-audit actions** — i.e. the default, pre-consent state, with no "Reject All" / CMP click before the scan. If that audit doesn't exist, the report has nothing correct to read; set it up first (→ `account-and-program`; the Default/Opt-Out/GPC pattern is `privacy-compliance`). Supporting inventories surface the same way — `list_report_templates` with `useCase:"tag governance"`, or `search` for "tag inventory", "chat", and "session replay" — to maintain the tag/account, chat-tag, and session-replay inventories the framework calls for.

CIPA article (source of truth): https://help.observepoint.com/en/articles/15261445-cipa-compliance-framework

**Where this goes next.** Turning these findings into evidence for outside counsel is `litigation-defense`. Whether a tag is *correctly consent-gated* in general (Consent Mode v2, CMP behavior) is `privacy-compliance`. This file gets you the framework, the report, and the audit prerequisite.

## 5. Boundaries

- **Report CRUD, schema discovery, scheduling, charting** → `account-and-program`. This file says *which* template to clone; that advisor is *how* to shape, save, schedule, and chart whatever report you land on.
- **Deep analytics validation** (`WHEN … EXPECT` Rules, data-layer timing, value integrity, the GA4/Adobe contracts) → `tag-and-analytics-quality`.
- **Consent proof** (does Reject-All block the tag, Consent Mode v2, CMP behavior) and **privacy-law mapping** → `privacy-compliance`.
- **CIPA / wiretap evidence for counsel** → `litigation-defense`.
- **CI/CD wiring** of the every-deploy audit → `automation-and-testing`.
- **The live MCP tool list + never-invent rule** → `references/mcp-tools.md`. The runtime tool list always overrides this file; clone reports by template **name**, never a memorized ID.

*Last verified: 2026-06-12*
