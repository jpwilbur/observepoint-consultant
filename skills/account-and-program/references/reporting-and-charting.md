# Reporting & charting — grid reports, saved reports, dashboards, charts

Load this when the user wants to **build a saved report, a grid report, a dashboard, or a chart** in ObservePoint — discovering which columns an entity exposes, querying grid data ad hoc, and assembling the saved artifacts a dashboard is made of. The grid is ObservePoint's cross-product reporting layer: one query surface that spans audit runs, journey runs, pages, cookies, tags, and more, so a question like "broken pages this week across every audit" is one report, not eleven.

This file owns the *mechanics* of building the report — the entity types, the column-discovery step, the query and save calls, and how saved reports roll up into a dashboard. It does **not** decide *which* metrics deserve a dashboard (that judgment comes from `references/account-health-and-strategy.md`) or the specifics of the accessibility-issues report (that's `accessibility`). Build the report here; let those references tell you what to put on it.

One note up front: **charting is now in the MCP server** — `add_report_chart` attaches a chart to an existing saved report and `remove_report_chart` removes one. A chart is a presentation layer over a saved report's existing query, so you build (or pick) the saved report first, then attach the chart referencing columns the report already selects. The runtime tool list stays the source of truth — never name a charting tool that isn't loaded. See section 4.

## Contents

1. [Grid reporting — entities, schema discovery, querying](#1-grid-reporting--entities-schema-discovery-querying)
2. [Saved reports — create, list, inspect, update, delete](#2-saved-reports--create-list-inspect-update-delete)
3. [Dashboards — assembling saved reports](#3-dashboards--assembling-saved-reports)
4. [Charting](#4-charting)
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

A **saved report** is a grid query persisted with a name, its entity type, its columns, and its filters, so it can be reopened, scheduled into a dashboard, and visualized as a chart (`add_report_chart`, section 4). The full CRUD surface:

| Tool | Use when |
|---|---|
| `create_saved_report` | Persist a grid query as a named, reusable report. Pass the `entityType`, the `columns` you discovered via `get_report_schema`, and the `filters`. |
| `list_saved_reports` | Discover what reports already exist. **Call this first** — most accounts already have reports; don't duplicate one. |
| `get_saved_report` | Inspect a saved report's full definition (entity, columns, filters) — read it before you change it. |
| `update_saved_report` | Mutate an existing report's columns or filters. Prefer this over delete-and-recreate so any dashboard reference and label survive. |
| `delete_saved_report` | Remove a report. Check `list_saved_reports` and confirm nothing depends on it first. |

**Build order, every time:**

1. `list_saved_reports` — does this report (or a near-match) already exist in the account? Don't duplicate it.
2. `list_report_templates` — is there a pre-built OP template for this? The library has 100+ templates organized by use case (filter by `search` / `gridEntityType` / `useCase`), including the analytics-implementation and CIPA framework report sets. If one matches, **clone it instead of building**: `create_report_from_template(templateId)` (run `dryRun:true` first; created `private` by default — it's a WRITE, confirm first). Match by name and read the id from the live list; never assume one. This is the fast path for any framework check — see `references/governance-frameworks.md`.
3. Only if no saved report and no template fits, build from scratch:
   1. `get_report_schema(entityType=..., search=...)` — confirm the exact column names.
   2. `query_report(...)` — sanity-check the filters return what you expect.
   3. `create_saved_report(...)` — persist it with a clear, human name.
   4. `get_saved_report(...)` — read it back to confirm the saved definition matches intent.

Naming matters: a saved report's name is what shows up in the dashboard picker and in `list_saved_reports`, so name it for the question it answers ("Broken pages — all audits, last 7 days"), not for the entity ("pages report 3").

**Organizing reports.** Saved reports carry labels, the same way audits and journeys do, so a team can group its governance reports, its privacy reports, and its accessibility reports. The label tools — `get_saved_report_labels` and `set_saved_report_labels` — live in the shared catalog under saved-report management; reach for them when the user wants reports filed under a label rather than scattered in one flat list. The label vocabulary itself (how labels are structured across the account) is covered in the account setup section of the `account-and-program` skill, not this file's.

## 3. Dashboards — assembling saved reports

A dashboard in ObservePoint is a layout of saved reports — each tile is a saved report rendered as a table or a chart (`add_report_chart`; see section 4). You build the dashboard from the bottom up: **each tile is a saved report you create first.** There is no "create dashboard" MCP tool; the dashboard composition lives in the ObservePoint UI today. The MCP-supported half of the workflow is the durable half — the saved reports — and that is where your tool calls go.

So the pattern for "build me a tag-governance dashboard" is:

1. Decide the tiles with the user (defer the *which-metrics* question to the program health section of `account-and-program`).
2. For each tile, build the saved report (section 2) — one `create_saved_report` per tile.
3. In the UI, drop those saved reports onto a dashboard and arrange the layout.

Because the tiles are saved reports, the dashboard stays live: re-running the underlying audits refreshes every tile, and `update_saved_report` on a tile's report updates it in place wherever it's used.

## 4. Charting

**Charting is now in the MCP server.** A saved report can carry one or more chart "view" tabs alongside its table, added with `add_report_chart` and removed with `remove_report_chart`. (This was previously a pending capability; it has shipped. Still: the runtime tool list is the source of truth — if `add_report_chart` isn't loaded in your session, don't reference it.)

**The model — a chart rides an existing report's query.** A chart does NOT run its own query; it's a presentation layer over the saved report's existing grid query. So you build (or pick) the saved report FIRST, then attach a chart whose category and series reference columns *already selected by that report's query*.

| Tool | Use when |
|---|---|
| `add_report_chart` | Add a chart "view" to an existing saved report without resending the whole body. WRITE — confirm before adding. |
| `remove_report_chart` | Remove a chart by `title`, internal `name`, or 0-based `index`. WRITE. |

**Chart types.** `area`, `bar`, `column`, `line` — each with `-stacked` and `-stacked-100` (100%-stacked) variants — plus `pie` and `donut` (single-series polar charts: use exactly one series).

**The `columnRef` rule — the thing that trips people up.** Every `categoryColumn` and every `series` references a report column via `columnRef`, and those refs MUST match columns already in the saved report's query: the `groupBy` column becomes the category (X-axis), and an aggregation becomes each series. So the build order is:

1. `get_saved_report(reportId)` → read the report's columns; the chart can only plot what the query already selects.
2. If the column you want isn't in the report, `update_saved_report` to add it (or pick a different report).
3. `add_report_chart(reportId, chart={ type, title, categoryColumn:{ displayName, columnRef:{...} }, series:[{ displayName, columnRef:{...}, color? }] })` — confirm with the user first (it's a write).

**Dashboards are still UI-composed.** There is still no `create_dashboard` MCP tool — a dashboard is a layout of saved reports arranged in the ObservePoint UI. Charting adds a chart *on a report*; arranging reports/charts into a dashboard layout remains a UI step.

## 5. Worked examples

**"Tag count by audit."** The user wants a report of how many tags each audit is firing.

1. `list_saved_reports` — check for an existing "tags by audit" report.
2. `get_report_schema(entityType="tags", search="audit")` — find the audit-name/ID column; `search="tag"` for the tag-identity column.
3. `query_report(entityType="tags", columns=["auditName", "tagName"], filters={...})` — confirm the rows group the way you expect (one row per tag observation; the count is the aggregation).
4. `create_saved_report(entityType="tags", columns=[...], filters={...})` named "Tag count by audit."
5. Add the chart: a `column` chart of *count of tags grouped by audit* is the obvious visualization — `add_report_chart(reportId, chart={type:"column", categoryColumn:{columnRef→audit}, series:[count of tags]})` (section 4). Confirm the saved report's query already selects the category + measure columns the chart references, and confirm the write with the user.

**"Broken pages this week."** The user wants every page returning a 4xx/5xx in the last seven days, across all audits.

1. `list_saved_reports` — avoid duplicating an existing broken-pages report.
2. `get_report_schema(entityType="pages", search="status")` — get the status-code column name; `search="url"` for the page URL.
3. `query_report(entityType="pages", filters={ "statusCode": { "gte": 400 }, /* last-7-days run filter */ }, columns=["url", "statusCode", "auditName"])` — eyeball the result.
4. `create_saved_report(...)` named "Broken pages — all audits, last 7 days."
5. Drop it onto the health dashboard as a tile (section 3). Defer *whether broken-page count is the right health metric* to the program health section of `account-and-program`.

## 6. Boundaries

- **Which metrics matter / what belongs on the dashboard** → program health section of `account-and-program`. This file builds whatever report you ask for; it does not decide that broken-page rate, tag duplication, or consent-leak count is the metric your account should watch. Account strategy lives there.
- **The accessibility-issues report specifics** → `accessibility`. The `accessibility-issues` entity is queryable here like any other, but which severities, WCAG criteria, and rules to surface — and how to prioritize them — is that skill's domain.
- **Charting** → `add_report_chart` / `remove_report_chart` (section 4). A chart rides an existing saved report's query, so build/confirm the report first; assembling reports/charts into a dashboard layout remains a UI step (there's no `create_dashboard` tool).
- **The MCP tool catalog and the never-invent-a-tool rule** → `references/mcp-tools.md` (shared). The grid/report/charting tools are listed there under "Grid reports"; that file is the authority on what's loaded, and the runtime tool list always overrides this doc.
- **Which template maps to a framework check** → `references/governance-frameworks.md`. That file owns the framework→report mapping (by name + search hint); this file owns shaping, saving, scheduling, and charting whatever report you land on.

*Last verified: 2026-06-12*
