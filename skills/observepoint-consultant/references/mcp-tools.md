# MCP tools — the ObservePoint MCP server

The ObservePoint MCP server wraps the platform's REST API with an opinionated, expert-aware tool surface. It's currently in development and not yet generally available. A small group of internal users has access today; broader release is expected in the coming months. The skill auto-detects `mcp__ObservePoint__*` tools at runtime — when they're present, prefer them over raw REST.

This file is the working reference for those tools. When the server reaches GA, this becomes the day-one guide for everyone.

## Contents

- [Rules of engagement](#rules-of-engagement)
- [What the server is](#what-the-server-is)
- [How discovery works](#how-discovery-works)
- [How to verify this catalog against your live server](#how-to-verify-this-catalog-against-your-live-server)
- [Tool families](#tool-families)
  - [Discovery and account](#discovery-and-account)
  - [Audits](#audits--the-bread-and-butter)
  - [Audit configuration](#audit-configuration)
  - [Audit run data and reports](#audit-run-data-and-reports)
  - [Page-level inspection](#page-level-inspection)
  - [Journeys](#journeys)
  - [Action-sets](#action-sets--reusable-journey-sequences)
  - [Rules](#rules)
  - [Alerts](#alerts)
  - [Consent categories and CMP integration](#consent-categories-and-cmp-integration)
  - [Folders, sub-folders, labels](#folders-sub-folders-labels)
  - [Scheduling](#scheduling)
  - [Locations and geo](#locations-and-geo)
  - [Grid reports](#grid-reports)
  - [Exports](#exports)
  - [PII scanning](#pii-scanning) *(new)*
  - [Cross-audit comparison](#cross-audit-comparison) *(new)*
  - [Anomalies, drift, coverage](#anomalies-drift-coverage) *(new)*
  - [Analysis primitives](#analysis-primitives) *(new)*
  - [Inventory and data shape](#inventory-and-data-shape) *(new)*
  - [Selector verification](#selector-verification) *(new)*
  - [Bulk operations](#bulk-operations) *(new)*
  - [Site Census](#site-census) *(new, admin)*
  - [HAR Analyzer](#har-analyzer) *(new)*
  - [Account governance and event log](#account-governance-and-event-log) *(new)*
  - [Escape hatches](#escape-hatches)
- [Safety gates encoded in the wrappers](#safety-gates-encoded-in-the-wrappers)
- [Common patterns](#common-patterns)
- [When to use `op_api_call`](#when-to-use-op_api_call)
- [Knowledge-only mode](#knowledge-only-mode)
- [What changes at GA](#what-changes-at-ga)

## Rules of engagement

Three rules. They are absolute.

1. **Never invent a tool name.** Only call tools that appear in your available-tools list. If you're not certain a tool exists, don't pretend it does. The catalog below is current as of the `Last verified` date, but the server is under active development — your runtime catalog is the source of truth.

2. **Prefer the wrapper over the raw API.** The MCP server's typed tools encode behavior the raw API doesn't: schedule sanitization, selector-type rewriting, safety gates, two-step mutation patterns, PII masking, scope-aware drift detection. When you call `build_schedule` instead of constructing an RRULE by hand, the wrapper validates and normalizes; when you call `update_journey_actions`, the wrapper enforces selector-evidence requirements. Bypassing wrappers with `op_api_call` discards those protections.

3. **When a wrapper refuses, the wrapper is right.** The safety gates exist because the underlying API will happily accept malformed input. If `update_journey_actions` refuses because a selector lacks evidence, the right answer is to verify the selector — not to switch to `op_api_call` to slip it past.

## What the server is

- **160+ tools** spanning every ObservePoint product surface — audits, journeys, action-sets, rules, alerts, consent categories, CMP integration, grid reports, scheduling, exports, plus newer surfaces: PII scanning, consent-state comparison, anomaly detection, **charting** (`add_report_chart`), report templates, **bulk operations**, **Site Census** scoping (admin), the **HAR Analyzer**, and account-governance / event-log / admin-impersonation tools.
- **Wraps both v2 and v3** of the ObservePoint REST API. v2 for CRUD; v3 for reporting and advanced features.
- **One escape hatch**: `op_api_call` for endpoints without a typed wrapper. See `get_api_docs` for the full endpoint list.
- **One self-describing call**: `get_api_docs` returns the entire endpoint reference, including which wrappers exist for which endpoints.

## How discovery works

Each turn, check whether tools prefixed `mcp__ObservePoint__` are in your available tools.

- **Tools present** — prefer them. Name the specific tool in your reply so the user can audit (`"Calling \`mcp__ObservePoint__list_audits\` to find the audit for example.com..."`).
- **Tools absent** — fall back to the REST recipes the `automation-and-testing` skill owns. Tell the user the MCP server isn't loaded in this session. Don't construct fake tool calls.

## How to verify this catalog against your live server

This file is hand-curated and drifts as the MCP server evolves. To check whether the catalog matches your live server:

1. Call `mcp__ObservePoint__get_api_docs` in any Claude session that has the MCP server loaded. The output is the authoritative endpoint reference.
2. Look at the system reminder listing your available tools (or run `claude mcp list` in Claude Code). Tool names prefixed `mcp__ObservePoint__` are what's actually loaded.
3. If you find a tool in your runtime that isn't in this file, or a tool documented here that isn't in your runtime, that's drift — open a PR refreshing this file, or rely on your runtime catalog and ignore the doc for that tool.

A quarterly refresh of this file is the recommended cadence (or per-MCP-server-release, whichever is sooner). See `CONTRIBUTING.md`.

## Tool families

The catalog is large. Group by family before reaching for any individual tool.

### Discovery and account

Use these to understand the customer's environment before doing anything.

| Tool | Use when |
|---|---|
| `get_account` | Need account-level info, plan tier, usage caps |
| `list_users` | Show who has access |
| `get_usage_overview`, `get_usage_summary`, `get_usage_trends` | Capacity planning, budget conversations |
| `whoami` | Confirm which account/identity the session is currently acting as. **Call FIRST** on any "my account"/"our account" task — the connector is one long-lived session shared across conversations, so a prior task may have left an impersonation active. |
| `find_account` | Admin: locate a customer account by name/id. |
| `find_item` | Admin: resolve an audit / journey / run ID to the ACCOUNT that owns it (the "item finder") — paste any numeric id (or partial) and get account, folder, domain, latest run. Substring-matches; prefers an exact id, lists candidates when several match. |
| `login_as_account` | Admin: impersonate into an account — reads work immediately, **writes are BLOCKED until `confirm_account_plan`**. Persists until you switch / `stop_impersonation` / idle auto-revert. |
| `confirm_account_plan` | Admin: **arms writes** for the impersonated account — call ONLY after telling the user which account + intent and getting an explicit "proceed." Re-confirm for each distinct piece of work. |
| `stop_impersonation` | Admin: return to your own admin account. |

**Admin impersonation doctrine.** The connector is ONE long-lived session shared across conversations. Start any account task with `whoami`; if it shows an impersonation you didn't expect, surface it rather than assume. Lifecycle: `login_as_account` (reads only) → tell the user the account + plan → on explicit approval `confirm_account_plan` (arms writes) → work → `stop_impersonation`. A wrong-account write lands in real customer data — treat the gate as load-bearing.

### Audits — the bread and butter

`list_audits` is usually call number one. Almost every audit-related task starts by finding the right audit ID.

| Tool | Use when |
|---|---|
| `list_audits` | Discover audit IDs. Supports `search` (substring on name + URL), `folderId`, paging. Fetches the full list once and filters client-side. |
| `get_audit` | Full config of one audit |
| `get_audit_summary`, `get_audit_health` | Quick health-check views |
| `query_audit_configs` | Filter audits by attributes (location, frequency, etc.) |
| `create_audit` | Create a new audit |
| `update_audit` | Modify an existing audit |
| `delete_audit` | Tear down |
| `run_audit` | Trigger a run now |
| `stop_audit` | Stop an active run |
| `get_audit_runs`, `check_run_status` | Run history + live status |
| `compare_audit_runs` | Regression detection between two runs |
| `reprocess_audit_rules` | **Re-evaluate an existing run's rules/reports WITHOUT re-crawling** — near-instant, consumes NO page-scan quota. The correct cheap follow-up after `update_audit_rules` ("reprocess" vs a full "re-run"). Audits only; journeys have no reprocess path — use `run_journey`. |
| `get_audits_status` | Compact run-status across a SET of audits (folder / domain / id list) — see [Account governance](#account-governance-and-event-log). |

### Audit configuration

Each audit has multiple configurable surfaces.

| Tool | Use when |
|---|---|
| `get_audit_filters` / `update_audit_filters` | URL include/exclude patterns |
| `get_audit_rules` / `update_audit_rules` | Tag & Variable Rules attached to the audit |
| `get_pre_audit_actions` / `update_pre_audit_actions` | Steps that run ONCE before the crawl (login, CMP opt-in/out) |
| `get_on_page_actions` / `update_on_page_actions` | Steps that run on EACH crawled page |
| `get_blocking_configuration` / `update_blocking_configuration` | Block third-party cookies, etc. |

The pre-audit-action wrapper supports `privacyoptin` and `privacyoptout` action types that auto-invoke a supported CMP's accept/reject SDK without manual selectors. Combine with `list_supported_cmps` to know which CMPs qualify.

### Audit run data and reports

After a run completes, the data and report endpoints are how you actually consume results.

| Tool | Use when |
|---|---|
| `get_audit_page_summary` | Per-page pass/fail summary |
| `get_tag_inventory` | What tags fire, where |
| `get_cookie_inventory` | What cookies are set, where |
| `get_cookie_privacy_report` | Cookies categorized by consent compliance |
| `get_request_privacy_report` | Vendor / geo data flow |
| `get_tag_health` | Tag uptime and reliability |
| `get_browser_logs` | Console errors and warnings |
| `get_request_domains` | Distinct domains receiving data |
| `get_geo_locations` | Geographic distribution of those domains |
| `get_file_changes` | What changed since the last run |
| `query_cookies` | Powerful query against the cookie dataset |

### Page-level inspection

When debugging a specific page rather than the whole audit:

| Tool | Use when |
|---|---|
| `get_page_info` | Page metadata + status |
| `get_page_tags` | Tags firing on this page |
| `get_page_cookies` | Cookies set on this page |
| `get_page_requests` | Full network log |
| `get_page_screenshot` | Visual capture URL |
| `get_page_console_logs` | Browser console for this page |

### Journeys

Multi-step interaction validation.

| Tool | Use when |
|---|---|
| `list_journeys`, `get_journey` | Discover and inspect |
| `get_journey_actions` | Read the step sequence |
| `get_journey_rules` | Rules attached to the journey |
| `create_journey`, `update_journey`, `update_journey_actions` | Mutate (subject to the safety gates below) |
| `delete_journey` | Tear down |
| `design_journey` | The smart-construction wrapper |
| `diagnose_journey` | Smart diagnosis of failed journeys |
| `run_journey` | Trigger a run |
| `get_journey_runs` | Run history |
| `get_run_action_outcomes` | Diagnostic per-step results (the only sensible way to inspect a journey run — the raw `/results` endpoint is 3+ MB) |
| `get_journey_console_errors` | Browser-console errors captured during a journey run |
| `get_journey_run_rule_results` | Rule pass/fail breakdown for a specific journey run |
| `update_journey_rules` | Assign rules to a journey at the JOURNEY level and/or per-ACTION (step) level. Event rules (`view_item`, `purchase`…) usually belong on the STEP that fires them, not journey-wide. `dryRun` previews. Write counterpart to `get_journey_rules`. |
| `stop_journey` | Stop a running journey scan (needs the specific `runId`, or finds the latest in-progress run). Tolerates "nothing running." |
| `analyze_journey_failures` | **Fleet-wide** journey-failure analysis in two aggregated grid calls — the failure-reason vocabulary + top culprit journeys over a window. Use THIS for "which journeys are failing across the account, and why" instead of iterating per-journey (infeasible at ~1000 journeys). For a single run's drill-down use `get_run_action_outcomes`. |

### Action-sets — reusable journey sequences

Action-sets are reusable named sequences referenced from multiple journeys or pre-audit-actions.

| Tool | Use when |
|---|---|
| `list_actionsets`, `get_actionset` | Discover |
| `create_actionset`, `update_actionset_actions` | Mutate |
| `delete_actionset` | Tear down (breaks any journey referencing it) |
| `find_actionset_references` | "What journeys use this action-set?" before deleting |

### Rules

Tag & Variable Rules — the `WHEN/EXPECT` validation primitive.

| Tool | Use when |
|---|---|
| `list_rules`, `get_rule` | Discover |
| `create_rule`, `update_rule`, `delete_rule` | Manage |
| `find_rule_references` | "What audits / journeys use this Rule?" before deleting |

Pair with `update_audit_rules` or `update_journey` equivalents to actually attach the Rule to an audit/journey.

### Alerts

Routed notifications for failing Rules or threshold breaches.

| Tool | Use when |
|---|---|
| `list_alerts`, `get_alert` | Discover |
| `get_alert_metric_types` | Which metrics support alerts |
| `create_alert`, `update_alert`, `delete_alert` | Manage |
| `get_run_alerts` | Alerts triggered on a specific run |

Alert bodies have two distinct scope fields: `assignments` (which audits/journeys), and `filtersV0` (which pages within each run count). Old wrappers conflated them; current versions expose both.

### Consent categories and CMP integration

The privacy-validation primitive. Consent categories classify cookies / tags / request-domains and attach to audits.

| Tool | Use when |
|---|---|
| `list_consent_categories`, `get_consent_category` | Discover |
| `create_consent_category`, `update_consent_category`, `delete_consent_category` | Manage |
| `add_consent_category_cookies` / `remove_consent_category_cookies` | Membership management |
| `add_consent_category_tags` / `remove_consent_category_tags` | Membership management |
| `add_consent_category_request_domains` / `remove_consent_category_request_domains` | Membership management |
| `add_consent_category_label` / `remove_consent_category_label` / `get_consent_category_labels` | Per-category label management |
| `get_audit_consent_categories`, `set_audit_consent_categories`, `add_audit_consent_categories`, `remove_audit_consent_categories` | Attach / detach from audits |
| `detect_cmp` | Which CMP is on a given page |
| `list_supported_cmps` | Which CMPs have native opt-in/out support |
| `start_onetrust_consent_category_import` → `poll_onetrust_consent_category_import` → `sync_onetrust_consent_categories` | Three-step OneTrust import (see safety gates) |
| `check_compliance_status` | Status of a compliance setup |
| `setup_compliance_monitoring` | **One-shot CCPA / privacy setup** — see below |
| `get_compliance_guide` | The MCP server's own opinionated guidance |

**Important: `setup_compliance_monitoring` for CCPA creates THREE audits, not one.** From the server's instructions:

> CCPA/CPRA compliance requires three audits per domain, not one. When a user asks to set up CCPA audits, use `setup_compliance_monitoring` with regulation "ccpa" — it automatically creates: (1) Default Audit (baseline, all consent categories), (2) Opt-Out Audit (pre-audit CMP "Reject All" click, Strictly Necessary categories only), (3) GPC Audit (gpcEnabled + blockThirdPartyCookies, Strictly Necessary categories only). Never assign non-essential consent categories to the Opt-Out or GPC audits.

This is the cleanest CCPA setup path. Don't reinvent it manually.

**`sync_onetrust_consent_categories` is the third step in the OneTrust importer** — and it's idempotent. Earlier versions of the importer created consent categories without the full CMP identity, so re-imports orphaned them. The current `sync_onetrust_consent_categories` always writes the full identity (`cmpVendor`, `oneTrustCookieGroupDomain`, `oneTrustCookieGroupGeo`, `oneTrustCookieGroupId`, `sourceUrl`) so a re-import updates in place. Always run with `dryRun: true` first.

### Folders, sub-folders, labels

Organization primitives.

| Tool | Use when |
|---|---|
| `list_folders`, `create_folder` | Top-level organization |
| `delete_folder` | Remove a folder (must be empty) |
| `get_folder_contents` | What's inside a folder |
| `list_subfolders`, `create_subfolder`, `delete_subfolder` | Domain-level grouping |
| `get_subfolder`, `update_subfolder` | Inspect / rename a sub-folder |
| `list_labels`, `create_label`, `update_label`, `delete_label` | Tagging audits/journeys for filtering |
| `get_audit_labels`, `set_audit_labels` | Per-audit label management |
| `get_journey_labels`, `add_journey_label`, `remove_journey_label` | Per-journey label management |
| `get_saved_report_labels`, `set_saved_report_labels` | Per-report label management |
| `list_tags` | The known tag DEFINITIONS (vendor catalog), not user labels |

### Scheduling

Surprisingly deep. The wrapper does substantially more than the REST API.

| Tool | Use when |
|---|---|
| `list_schedule_presets` | Canonical preset names ("weekly", "business-days", "monthly", etc.) |
| `get_audit_frequencies` | Allowed frequency values |
| `list_timezones` | IANA names with region grouping + DC-location cross-reference |
| `build_schedule` | **Take this over manual RRULE construction.** Takes a preset name, validates the timezone, emits a complete schedule block ready to drop into `create_audit` / `update_audit` / `create_journey` / `update_journey`. Warns when the timezone's recommended datacenter disagrees with the audit's `location`. |
| `describe_recurrence_rule` | Validate / human-readable a custom RRULE |
| `get_schedule_calendar` | What's scheduled when |

RRULE composition has fiddly rules (`WKST=SU` first, explicit `INTERVAL=N`, signed ordinals in positional `BYDAY`, IANA timezone in `tzId`, no `Z`/offset in `dtStart`). `build_schedule` knows all of them. Use it.

### Locations and geo

| Tool | Use when |
|---|---|
| `get_geo_locations` | Geo distribution of audit results |
| `list_locations` | Available datacenter locations + region grouping |

### Grid reports

Custom dashboards built on the v3 grid-reporting API.

| Tool | Use when |
|---|---|
| `get_report_schema` | **Call FIRST** to discover column names for an entity type, before building a report. Supports a `search` parameter to filter columns by keyword. |
| `query_report` | Run an ad-hoc query against grid data |
| `list_saved_reports`, `get_saved_report` | Discover existing saved reports |
| `create_saved_report` | Build a new saved report (chart, table, etc.) |
| `update_saved_report`, `delete_saved_report` | Manage |
| `add_report_chart` | **Charting (now in the MCP).** Add a chart "view" tab to an EXISTING saved report without resending the whole body. Types: area / bar / column / line (+ `-stacked`, `-stacked-100`), pie, donut. The category + each series reference report columns via `columnRef` — they MUST match columns already in the report's query, so call `get_saved_report` first. WRITE — confirm before adding. |
| `remove_report_chart` | Remove a chart from a saved report by `title`, internal `name`, or 0-based `index` (`get_saved_report` first). WRITE. |
| `list_report_templates` | List ObservePoint-published report "library" templates; filter by `search` / `gridEntityType` / `useCase`. |
| `create_report_from_template` | Clone a template into the account as an editable saved report (`dryRun:true` first; created `private` by default). |

Entity types supported: `web-audit-runs`, `web-journey-runs`, `pages`, `cookies`, `tags`, `accessibility-issues`, `links`, `tag-variables`, `network-requests`, `browser-logs`, `rules`.

When users say "reports," "grid reports," "custom reports," or "dashboards," they mean these.

### Exports

| Tool | Use when |
|---|---|
| `list_exports` | What exports are running or recent |
| `export_report` | Create an export of a grid report |
| `get_export_status` | Poll completion |

### PII scanning

Detect PII / personal data being collected on the site. Both wrappers MASK raw values in output — the report tells you the leak path without echoing the literal.

| Tool | Use when |
|---|---|
| `scan_audit_pii` | Site-wide PII scan over an audit run. Checks tag-variable values, cookie values, request query strings. Uses three detection modes: REGEX (email + your `customRegex`; numeric patterns off by default to avoid false positives on analytics IDs), OP-STATIC-IP (visitor IP equals ObservePoint's egress IP), and severity weighting by destination (first-party data layer = governance smell; same value to a third-party domain = active leak). |
| `scan_journey_pii` | Per-journey-run PII scan. Adds a CANARY mode on top of the audit version: any literal typed via the journey's `input` / `maskedinput` steps appearing downstream in tags/cookies/requests/POST-bodies = definitive collection, zero false positives. The strongest signal. |

Healthcare-tracking and CIPA-style litigation defense both lean heavily on these. See the `litigation-defense` skill for the evidence patterns.

### Cross-audit comparison

Diff two runs or two consent-state audits. Privacy / consent-leak work depends on these.

| Tool | Use when |
|---|---|
| `compare_consent_states` | **The canonical consent-leak diagnostic.** Diff the tag set between two consent-state audits on the same domain — "what tags fire on Accept-All but not Reject-All?" Auto-discovers audit pairs by domain + state name (`default` / `opt-out` / `gpc`); recognizes the audit-naming patterns from `setup_compliance_monitoring`. Override with explicit audit IDs for finer control. |
| `compare_cookie_set` | Diff the cookie set between two audit runs (or two audits). |
| `compare_domain_set` | Diff the request-domain set between two runs / audits. |
| `compare_tag_set` | Diff the tag set between two runs / audits. |
| `compare_audit_runs` | Pre-existing higher-level regression diff between two runs of the same audit. |

### Anomalies, drift, coverage

For "what changed?" and "what slipped past?" workflows.

| Tool | Use when |
|---|---|
| `find_anomalies` | Detect runs where a metric jumped suddenly vs the prior run. **Scope-aware** — when a run's page count changes ≥20% vs prior, raw deltas aren't comparable, so the wrapper normalizes to a per-page rate and labels the run "scope-change" rather than a hard anomaly. Default threshold is ±25% over a 10-run lookback. Metric taxonomy: tags / cookies / pages / request-domains / broken-pages / pages-with-browser-errors. |
| `get_metric_trend` | Time-series of a metric across recent runs. Companion to `find_anomalies`. |
| `find_coverage_gaps` | What's missing — pages without expected tags, domains never seen, etc. |
| `find_first_observed` | When something was first seen in the audit history. Useful for "when did this vendor appear?" |
| `find_rare_observations` | Low-frequency findings worth a look. |

### Analysis primitives

Higher-level diagnostics built on the raw `get_*` data tools. Use these when you want the wrapper to do the interpretation rather than pull raw data and analyze yourself.

| Tool | Use when |
|---|---|
| `analyze_journey_cookies` | Cookie analysis for a journey run with context — what set them, on which step, at which URL. |
| `analyze_journey_requests` | Request analysis for a journey run — third-party calls, status codes, payload size patterns. |
| `analyze_journey_tags` | Tag firing analysis for a journey run. |
| `analyze_rule_results` | Rule pass/fail interpretation across runs. |

### Inventory and data shape

| Tool | Use when |
|---|---|
| `get_inventory` | Cross-audit inventory roll-up. |
| `correlate_pages` | Cross-page correlation — what loads with what. |
| `profile_variable` | Profile the values a tag-variable takes across pages. Useful for finding outliers or unexpected data. |
| `get_pages_without_tag` | Pages where a specific tag doesn't fire. The "should be everywhere but isn't" workflow. |

### Selector verification

| Tool | Use when |
|---|---|
| `verify_selectors` | Verify a CSS / XPath / ID selector resolves to exactly one element on a page. Pairs with the selector-evidence gate documented under "Safety gates" below. |

### Bulk operations

Create / update / delete / assign many objects of ONE entity type in a single call. Supported entities: `audit`, `label`, `rule`, `consent-category`, `alert`, `folder`. Continue-on-error — created ids + failed rows are reported so you re-run only the failures.

| Tool | Use when |
|---|---|
| `bulk_describe` | **Call FIRST.** With an `entity`, returns the item shape per op (create/update/delete/assign); without, lists the registered entities. |
| `bulk_create` | Create many from shared `defaults` + terse `items[]` overrides (max 500/call). Some entities take relational fields on create (rule/consent-category `assignToAuditIds`; consent-category `cookies`/`tags`). `dryRun:true` first. |
| `bulk_update` | Patch many by `id` (read-modify-write per id); `defaults` is a shared patch. |
| `bulk_delete` | Delete many by id. **Two-step:** `dryRun:true` to preview, then `dryRun:false` AND `confirm:true` to execute. Destructive; max 500. |
| `bulk_assign` | Attach rules / consent-categories to a set of audits. `mode`: `add` (union, default — does not clobber), `remove`, `replace` (set EXACTLY — removes others). Serial by default (concurrency 1) to avoid lost-update races. |

Lost-update caution: `bulk_create` with `assignToAuditIds` and `bulk_assign` both do per-audit read-modify-write. If multiple items target the SAME audit in one call, keep `concurrency:1` or attach afterward.

### Site Census

The internal large-scale crawler that sizes a domain's real page count for audit / licence scoping. **Admin-only — impersonate the central census account first** (`login_as_account`). This is the engine behind contract page-count scoping.

| Tool | Use when |
|---|---|
| `list_site_censuses` | List censuses (server-side `search` by name; `runningOnly`). Shows crawl completeness per census. |
| `create_site_censuses` | Create (auto-starts unless `autoStart:false`) from `items[]` + `defaults`. `dryRun:true` previews. |
| `update_site_censuses` | Read-modify-write patch by id (`dryRun` previews). |
| `delete_site_censuses` | Delete by id — `dryRun:true` first; permanent. |
| `start_site_census` | Start OR resume a census by id (resume keeps crawling an under-crawled one). |
| `size_site_census` | Estimate page count from the Links grid: classifies query-param spirals, rolls up a URL-based total and a spiral-adjusted total, rates crawl completeness. The defensible scoping number. |
| `sample_site_census_pages` | Pull a few REAL example URLs per host (spirals + top-N by real-page count) as evidence the count isn't junk — never fabricates URLs. |

### HAR Analyzer

Run Tag & Variable Rules against captured traffic (a `.har` from Charles, mitmproxy, Fiddler, or DevTools), including a mobile app's capture — the supported path for native-app validation given the no-native-mobile limitation. A HAR "configuration" (a.k.a. "device") groups uploaded sessions and carries the rules applied to every upload.

| Tool | Use when |
|---|---|
| `summarize_har_file` | **Local, read-only.** Parse a local `.har` → entry count, top hosts, capture window, recognizable vendors (GA4/Adobe/Meta/Segment/OneTrust…). Pre-upload sanity check, or a standalone look when the account doesn't license the Analyzer. Uploads nothing. |
| `list_har_configs` | List HAR configurations; the id is the `configId` for the tools below. |
| `create_har_config` | Create a configuration (requires a `folderId` — use `list_folders`). Attach rules afterward. WRITE. |
| `update_har_config_rules` | Full-replace the rule set applied to every FUTURE upload (bare rule-ID array, same contract as `update_audit_rules`; re-upload to re-score). `dryRun` previews. WRITE. |
| `upload_har_file` | Upload 1–15 local `.har` files (≤300 MB each) → validate → upload → process → poll. Returns the run id + rule rollup. **The HAR content is sent to ObservePoint (transits its S3 bucket)** — same as a UI upload; confirm with the user. WRITE. |
| `get_har_run_status` | Poll a run (16 = processing, 30 = completed); omit `runId` to list a config's recent sessions. |
| `get_har_run_results` | Processed results, summarized: sections `tags` / `rules` / `requests` / `actions` / `all`; `verboseRequests` for the raw per-request log. |

### Account governance and event log

| Tool | Use when |
|---|---|
| `get_account_health` | Account-health digest: the most problematic audits across the account (or a folder / audit-id `scope`), ranked by a weighted severity score over failed runs, triggered alerts, rule failures, broken pages (unapproved cookies as tiebreaker). The fast "what's broken right now?" read. |
| `get_audits_status` | Compact run-status for a SET of audits (by `folderId`, sub-folder `domainId`, or explicit `auditIds`) — one terse row each (state, pagesScanned, lastRun) + a state tally. No-run audits show "queued" rather than vanishing. Watch a `bulk_create` batch move queued → running → completed. |
| `query_user_events` | Account event log — who created/deleted/updated which item and when. **Attribution only** (THAT it changed + WHEN; no before/after diff). Server-side `itemType`/`eventType`; client-side `userId`/`itemId`/`since`/`until`. |
| `review_account_access` | Access review — who can access the account, flagging admins, never-logged-in, and stale users (no login within `staleDays`, default 90). |
| `get_user` | A single user by id — role/permissions, email, last login. |

### Escape hatches

| Tool | Use when |
|---|---|
| `get_api_docs` | Find an endpoint not covered by a typed wrapper |
| `op_api_call` | Call any endpoint by URL. **Bypasses safety gates** — use only when no wrapper exists. |

## Safety gates encoded in the wrappers

The MCP server's wrappers enforce constraints the raw REST API does not. Understanding these matters — when a wrapper refuses, the right response is to fix the request, not to bypass with `op_api_call`.

### Selector evidence gate

`create_journey`, `update_journey_actions`, `create_actionset`, and `update_actionset_actions` refuse to write selector-bearing actions (`click`, `input`, `maskedinput`, `select`, `check`, `uncheck`, `enteriframe`) when any new or changed selector lacks a `selector.evidence` block captured live via Claude for Chrome.

Required evidence shape:
```
{
  verifiedAt: ISO timestamp (≤ 6h old),
  verifiedVia: "claude-for-chrome",
  matchCount: 1,
  pageUrl: <URL>,
  observedAttributes: { id?, "data-testid"?, "aria-label"?, role?, name?, text?, ... }
}
```

The wrapper diffs incoming selectors against the current saved version per-action; only genuinely new or changed selectors need evidence. Deleting actions, patching `waitDuration`, etc. pass through with no evidence required.

If you can't verify via Claude for Chrome, the wrapper makes you stop and switch sessions. Do not work around this — selectors written without evidence break the moment the page changes. `verify_selectors` is the companion tool for sanity-checking that a selector resolves.

### Journey-shape gate

`create_journey` and `update_journey_actions` refuse journeys whose action list reduces to 2+ `navto` steps with zero interactive steps (click / input / etc.). A journey simulates a real human using the site — it's for verifying data flowing through user gestures, not for loading URLs. Loading URLs in sequence is what `create_audit` is for.

| Shape | Verdict |
|---|---|
| 1 navto + 0+ interactive | OK (ping check or start URL + gestures) |
| 0 navto + 1+ interactive | OK (start URL is implicit) |
| 2+ navto + 0 interactive | **REFUSED** (audit-in-disguise) |
| 2+ navto + 1+ interactive | Soft warning |

### Watch-usage gate

`create_journey`, `update_journey_actions`, `create_actionset`, and `update_actionset_actions` refuse 2+ `watch` steps. `watch` is for video playback or side-loading content, not generic "wait N seconds." For between-step buffers, use `waitDuration` on the action itself — every action supports it.

### Three-step OneTrust import

`start_onetrust_consent_category_import` returns import-request IDs and the list of cookies the CMP detected. `poll_onetrust_consent_category_import` shows what will be committed. `sync_onetrust_consent_categories` performs the create / update / delete commit — idempotently, so re-imports update in place rather than orphaning. Run `sync_onetrust_consent_categories` with `dryRun: true` first to preview the plan, then again with `dryRun: false` after the user confirms. The wrapper deliberately does NOT collapse this into one step — committing cookie-to-category mappings without showing the user what's about to happen is exactly the failure mode the dryRun pattern exists to prevent.

### Schedule sanitization

The schedule object has read-only computed fields (`description`, `presetType`) the GET returns but the PUT/POST rejects. The wrapper strips them automatically via `sanitizeScheduleForWrite` when you pass a GET response back as a write body. The raw API will reject the body if you don't.

### Selector-type rewriting

The audit/journey backend natively accepts only `selectorType: "css"`, `"id"`, `"xpath"`. The MCP wrappers transparently rewrite `"text"` → xpath `//*[normalize-space()='value']`, `"ariaLabel"` → css `[aria-label='value']`, `"name"` → css `[name='value']`. This normalization is applied to the full merged body, so legacy data is normalized too.

### Scope-aware anomaly detection

`find_anomalies` doesn't flag a run as a hard anomaly when the page count changed ≥20% vs the prior run — a 10-page homepage scan next to a 1,006-page crawl makes raw deltas meaningless. Instead it labels the run "scope-change" and shows the per-page rate so you can decide whether the normalized change is real drift. This prevents the classic false alarm where a scan-size change masquerades as a tag spike.

### PII masking

`scan_audit_pii` and `scan_journey_pii` never echo raw PII. Findings are reported as "leak path X collected a value matching pattern Y" with the value masked. This is deliberate — the report can land in a ticket or evidence pack without leaking the very data the scan was looking for.

## Common patterns

Walk users through these step sequences rather than reaching for individual tools.

**"What's on site X?"**
```
list_audits(search="X") → pick audit
get_audit_runs(auditId) → pick latest completed run
get_tag_inventory(auditId, runId)  // and/or get_cookie_inventory
```

**"Set up CCPA compliance for example.com"**
```
setup_compliance_monitoring(regulation="ccpa", domain="example.com")
// One call creates three audits per the wrapper's CCPA pattern.
```

**"Does our Reject All actually block tracking?"**
```
compare_consent_states(domain="example.com", leftState="default", rightState="opt-out")
// Auto-discovers the audit pair, returns only-on-default tags that should NOT fire on opt-out.
```

**"Scan for PII leaks on the patient portal"**
```
list_audits(search="patient-portal") → pick audit
scan_audit_pii(auditId, customRegex=[{name: "MRN", pattern: "MRN-\\d{8}"}])
// PII findings are masked; report tells you what leaked and to which destination domain.
```

**"What changed since last release?"**
```
find_anomalies(auditId, metric="tags", thresholdPct=25, lookbackRuns=10)
// Returns runs where the tag count jumped beyond the threshold, scope-normalized.
```

**"Sync OneTrust consent categories"**
```
start_onetrust_consent_category_import(cmpProvider="ONE_TRUST", sourceUrl=..., locales=[...])
poll_onetrust_consent_category_import(importRequestIds=[...])    // shows what was detected
sync_onetrust_consent_categories(importRequestIds=[...], dryRun=true)   // preview plan
// User confirms the plan
sync_onetrust_consent_categories(importRequestIds=[...], dryRun=false)  // commit
```

**"Build a release-gate audit"**
```
list_audits(search="staging") → pick or create_audit
run_audit(auditId)
check_run_status(auditId, runId) → poll
get_run_alerts(auditId, runId) → block release if alerts > 0
```

**"Custom report on broken pages"**
```
get_report_schema(entityType="pages", search="status")  // discover columns
create_saved_report(entityType="pages", filters={...}, columns=[...])
```

**"Schedule the audit weekly"**
```
build_schedule(presetName="weekly", tzId="America/Los_Angeles", startTime="09:00")
// Returns a complete schedule block.
update_audit(auditId, schedule=<that block>)
```

**"Diagnose this failed journey"**
```
diagnose_journey(journeyId, runId)  // smart wrapper
// or:
get_journey_runs(journeyId) → get_run_action_outcomes(runId)
// avoid the raw /results endpoint — it's 3+ MB
```

**"Which audits / journeys use this Rule?" (before deleting)**
```
find_rule_references(ruleId)
// Same pattern: find_actionset_references(actionSetId) before deleting an action-set.
```

**"Reprocess rules after I changed them" (no re-crawl, no quota)**
```
update_audit_rules(auditId, ruleIds=[...])
reprocess_audit_rules(auditId)   // re-scores the existing run in place — near-instant
```

**"Validate the mobile app's tags from a capture"**
```
summarize_har_file(filePath="/abs/capture.har")        // local sanity check, uploads nothing
list_har_configs() → create_har_config(name=..., folderId=...) if none
update_har_config_rules(configId, ruleIds=[...])        // rules to score every upload
upload_har_file(configId, filePaths=["/abs/capture.har"])  // sends the HAR to OP — confirm first
get_har_run_results(configId, runId, section="rules")
```

**"Create 30 audits from a list"**
```
bulk_describe(entity="audit", op="create")              // get the item shape
bulk_create(entity="audit", defaults={...}, items=[...], dryRun=true)   // preview
bulk_create(entity="audit", defaults={...}, items=[...])                // execute
get_audits_status(folderId=...)                         // watch queued → running → completed
```

**"Add a chart to a saved report"**
```
get_saved_report(reportId)        // see the report's columns (the columnRef targets)
add_report_chart(reportId, chart={type:"column", title:"Tags by audit", categoryColumn:{...}, series:[{...}]})
```

**"Size example.com for a contract" (admin)**
```
whoami                                  // confirm identity; impersonate the census account if needed
create_site_censuses(items=[{domain:"example.com", startingUrls:[...]}])
size_site_census(censusId=...)          // URL total + spiral-adjusted total + completeness
sample_site_census_pages(censusId=...)  // real example URLs as evidence
```

## When to use `op_api_call`

The escape hatch. Use it only when:

- No typed wrapper covers the operation.
- You need a raw response shape that the wrapper transforms.

Be aware: `op_api_call` bypasses every safety gate above. The wrappers exist for reasons; reach for them first.

## Knowledge-only mode

If no `mcp__ObservePoint__*` tools are present in your available tools, the user hasn't installed the MCP server (or doesn't have access — it's not yet generally available).

In that mode:

- Answer from the REST recipes the `automation-and-testing` skill owns.
- Walk the user through the equivalent REST calls.
- Mention that the MCP server is in development and will substantially simplify the same workflow when available.
- Don't invent tool calls. Don't reference `mcp__ObservePoint__*` as if it's loaded.

## What changes at GA

When the MCP server reaches generally available status:

- The README's install section moves from "internal users only" to public install steps.
- The plugin may ship a `.mcp.json` that auto-bootstraps the server on install (decided in v0.2.0 to NOT ship one pre-GA; the public release revisits this).
- This file's `Last verified` date updates with whatever wrapper changes shipped.

Watch the changelog and the server's own `get_api_docs` for the source of truth.

---

*Last verified: 2026-06-10*
