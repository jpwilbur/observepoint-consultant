# Reporting & charting — grid reports, saved reports, dashboards, charts

Load this when the user wants to **build a saved report, a grid report, a dashboard, or a chart** in ObservePoint — discovering which columns an entity exposes, querying grid data ad hoc, and assembling the saved artifacts a dashboard is made of. The grid is ObservePoint's cross-product reporting layer: one query surface that spans audit runs, journey runs, pages, cookies, tags, and more, so a question like "broken pages this week across every audit" is one report, not eleven.

This file owns the *mechanics* of building the report — the entity types, the column-discovery step, the query and save calls, and how saved reports roll up into a dashboard. It does **not** decide *which* metrics deserve a dashboard (that judgment comes from `references/account-health-and-strategy.md`) or the specifics of the accessibility-issues report (that's `accessibility`). Build the report here; let those references tell you what to put on it.

One discipline to flag up front: **charting is a brand-new ObservePoint feature that is not yet exposed through the MCP server.** This file documents it as an extension point using the same pre-GA discipline the codebase applies everywhere else — describe the anticipated capability, build the underlying saved report with the real tools that exist today, and never invent a charting tool name. See section 4.

## Contents

1. [Grid reporting — entities, schema discovery, querying](#1-grid-reporting--entities-schema-discovery-querying)
2. [Saved reports — create, list, inspect, update, delete](#2-saved-reports--create-list-inspect-update-delete)
3. [Dashboards — assembling saved reports](#3-dashboards--assembling-saved-reports)
4. [Charting — extension point (pending MCP support)](#4-charting--extension-point-pending-mcp-support)
5. [Worked examples](#5-worked-examples)
6. [Boundaries](#6-boundaries)

## 1. Grid reporting — entities, schema discovery, querying

The grid is the v3 reporting layer. A grid report is a query against one **entity type** — pick the entity, choose columns, apply filters, and the grid returns rows. The entity types the MCP server reports support:

| Entity type | One row is… |
|---|---|
| `web-audit-runs` | a single run of a Web Audit (run-level rollups — page count, alert count, duration) |
| `web-journey-runs` | a single run of a Journey |
| `pages` | one scanned page (status code, load time, on-page tag/cookie counts) |
| `cookies` | one cookie observation (name, domain, party, expiry, the page it set on) |
| `tags` | one tag observation (account/vendor, the page, the request) |
| `accessibility-issues` | one accessibility finding (rule, severity, element) — see `accessibility` for specifics |
| `links` | one link (status, source/target, broken vs. healthy) |
| `tag-variables` | one tag variable on one hit (the granular data-layer/parameter level) |
| `network-requests` | one network request (URL, domain, method, status) |
| `browser-logs` | one console / browser-log entry |
| `rules` | one Rule result (pass/fail against a run) |

**Always discover columns before you build.** Column names are not guessable across entities — the grid is wide, and the same concept (a status, a domain) is named differently per entity. The first call is always:

```
get_report_schema(entityType="pages", search="status")
```

The `search` parameter filters the column list by keyword, which is essential — a bare schema for `pages` or `network-requests` is long. Search `"status"` to find the status-code column, `"load"` for timing, `"domain"` for the request/cookie domain, `"tag"` for tag columns. Use the exact column names it returns; do not paraphrase them into the report.

**Query ad hoc with `query_report`.** Once you know the columns, run an exploratory query to see the shape of the data before you commit it to a saved report:

```
query_report(entityType="pages", filters={ "statusCode": { "gte": 400 } }, columns=["url", "statusCode", "auditName"])
```

`query_report` is the right tool for a one-off question ("show me the 4xx/5xx pages right now") and for sanity-checking filters before you save them. When the answer is something the user will want again — a recurring view, a dashboard tile — promote it to a saved report (section 2).

A note on filters and grouping: filters narrow the rows (a status threshold, a date window, a specific audit), and the entity you pick decides the grain — one row per page, per cookie, per tag observation. A "count by X" report (tag count by audit, cookie count by domain) is the same query grouped on the X column; the count is the aggregation of the rows that survive your filters. Confirm the grouping column exists in the schema (`get_report_schema` with the right `search` term) before you rely on it, and verify the row shape in `query_report` before you save.

## 2. Saved reports — create, list, inspect, update, delete

A **saved report** is a grid query persisted with a name, its entity type, its columns, and its filters, so it can be reopened, scheduled into a dashboard, and (once charting ships) visualized. The full CRUD surface:

| Tool | Use when |
|---|---|
| `create_saved_report` | Persist a grid query as a named, reusable report. Pass the `entityType`, the `columns` you discovered via `get_report_schema`, and the `filters`. |
| `list_saved_reports` | Discover what reports already exist. **Call this first** — most accounts already have reports; don't duplicate one. |
| `get_saved_report` | Inspect a saved report's full definition (entity, columns, filters) — read it before you change it. |
| `update_saved_report` | Mutate an existing report's columns or filters. Prefer this over delete-and-recreate so any dashboard reference and label survive. |
| `delete_saved_report` | Remove a report. Check `list_saved_reports` and confirm nothing depends on it first. |

**Build order, every time:**

1. `list_saved_reports` — does this report (or a near-match) already exist?
2. `get_report_schema(entityType=..., search=...)` — confirm the exact column names.
3. `query_report(...)` — sanity-check the filters return what you expect.
4. `create_saved_report(...)` — persist it with a clear, human name.
5. `get_saved_report(...)` — read it back to confirm the saved definition matches intent.

Naming matters: a saved report's name is what shows up in the dashboard picker and in `list_saved_reports`, so name it for the question it answers ("Broken pages — all audits, last 7 days"), not for the entity ("pages report 3").

**Organizing reports.** Saved reports carry labels, the same way audits and journeys do, so a team can group its governance reports, its privacy reports, and its accessibility reports. The label tools — `get_saved_report_labels` and `set_saved_report_labels` — live in the shared catalog under saved-report management; reach for them when the user wants reports filed under a label rather than scattered in one flat list. The label vocabulary itself (how labels are structured across the account) is covered in the account setup section of the `account-and-program` skill, not this file's.

## 3. Dashboards — assembling saved reports

A dashboard in ObservePoint is a layout of saved reports — each tile is a saved report rendered as a table (and, once charting ships, as a chart; see section 4). You build the dashboard from the bottom up: **each tile is a saved report you create first.** There is no "create dashboard" MCP tool; the dashboard composition lives in the ObservePoint UI today. The MCP-supported half of the workflow is the durable half — the saved reports — and that is where your tool calls go.

So the pattern for "build me a tag-governance dashboard" is:

1. Decide the tiles with the user (defer the *which-metrics* question to the program health section of `account-and-program`).
2. For each tile, build the saved report (section 2) — one `create_saved_report` per tile.
3. In the UI, drop those saved reports onto a dashboard and arrange the layout.

Because the tiles are saved reports, the dashboard stays live: re-running the underlying audits refreshes every tile, and `update_saved_report` on a tile's report updates it in place wherever it's used.

## 4. Charting — extension point (pending MCP support)

**Charting is a new ObservePoint feature. It is NOT yet exposed through the MCP server.** Treat it exactly the way this codebase treats every pre-GA capability (mirror the framing in `references/mcp-tools.md`): describe the anticipated capability, point at what exists today, and **never invent a tool name for it.**

**The anticipated capability.** Charting will let a saved report render as a visualization — a bar/line/pie/area chart over the report's grid data — instead of (or alongside) a flat table, with the chart type, the dimension/measure mapping, and the grouping configured on the saved report. A dashboard tile then shows the chart rather than rows. Conceptually it is a *presentation layer on top of a saved report*: the same grid query you already build, drawn as a picture.

**How it will slot in.** When the MCP server exposes charting, the natural shape is a chart specification carried on the existing saved-report surface — i.e., `create_saved_report` / `update_saved_report` gain chart-configuration fields, rather than a new top-level "create chart" tool. The grid query underneath is unchanged; only the render config is added. **Do not assume that shape is final and do not name a tool for it.** The runtime tool list is the source of truth; if a charting parameter or tool is not in your available tools, it does not exist yet.

**What to do today.** Build the chart's data foundation with the real tools that exist now:

1. `get_report_schema` → confirm the dimension and measure columns the chart will plot.
2. `query_report` → verify the data shape (the grouping you want to chart is actually present in the rows).
3. `create_saved_report` → persist that query as a saved report.
4. Tell the user the chart visualization itself is configured **in the ObservePoint UI** on that saved report today, and that programmatic charting via MCP is **pending exposure** — the saved report you just built is exactly what the chart will sit on when it lands.

**Follow-up, out of scope here.** "Expose charting via MCP" is an ObservePoint MCP-team task, not something this plugin can implement — the plugin documents and consumes the server, it does not build it. Flag it as that team's follow-up; don't fake it with `op_api_call` against an unstable endpoint, and don't reference a charting tool as if it were loaded.

## 5. Worked examples

**"Tag count by audit."** The user wants a report of how many tags each audit is firing.

1. `list_saved_reports` — check for an existing "tags by audit" report.
2. `get_report_schema(entityType="tags", search="audit")` — find the audit-name/ID column; `search="tag"` for the tag-identity column.
3. `query_report(entityType="tags", columns=["auditName", "tagName"], filters={...})` — confirm the rows group the way you expect (one row per tag observation; the count is the aggregation).
4. `create_saved_report(entityType="tags", columns=[...], filters={...})` named "Tag count by audit."
5. Charting note: a bar chart of *count of tags grouped by audit* is the obvious visualization. Build this saved report now; the bar chart is configured on it in the UI, pending MCP charting (section 4).

**"Broken pages this week."** The user wants every page returning a 4xx/5xx in the last seven days, across all audits.

1. `list_saved_reports` — avoid duplicating an existing broken-pages report.
2. `get_report_schema(entityType="pages", search="status")` — get the status-code column name; `search="url"` for the page URL.
3. `query_report(entityType="pages", filters={ "statusCode": { "gte": 400 }, /* last-7-days run filter */ }, columns=["url", "statusCode", "auditName"])` — eyeball the result.
4. `create_saved_report(...)` named "Broken pages — all audits, last 7 days."
5. Drop it onto the health dashboard as a tile (section 3). Defer *whether broken-page count is the right health metric* to the program health section of `account-and-program`.

## 6. Boundaries

- **Which metrics matter / what belongs on the dashboard** → program health section of `account-and-program`. This file builds whatever report you ask for; it does not decide that broken-page rate, tag duplication, or consent-leak count is the metric your account should watch. Account strategy lives there.
- **The accessibility-issues report specifics** → `accessibility`. The `accessibility-issues` entity is queryable here like any other, but which severities, WCAG criteria, and rules to surface — and how to prioritize them — is that skill's domain.
- **Charting tool calls** → nobody, yet. Charting is not in the MCP server (section 4). Build the saved report; configure the chart in the UI; treat MCP charting as a pending MCP-team follow-up.
- **The MCP tool catalog and the pre-GA discipline** → `references/mcp-tools.md` (shared). The grid/report tools are listed there under "Grid reports"; that file is the authority on what's GA, what's pending, and the never-invent-a-tool rule.

*Last verified: 2026-06-04*
