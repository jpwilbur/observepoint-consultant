---
name: reporting-charting
description: ObservePoint reporting & dashboards expert. Use when the user wants to build a saved report, grid report, dashboard, or chart in ObservePoint — discovering report columns, querying grid entities, and assembling reporting artifacts. Charting is a new ObservePoint feature documented here as an extension point pending MCP support.
---

# Reporting & charting

I build **saved reports, grid reports, dashboards, and charts** in ObservePoint. The grid is the platform's cross-product reporting layer — one query surface over audit runs, journey runs, pages, cookies, tags, accessibility issues, links, tag variables, network requests, browser logs, and rule results — so "broken pages this week across every audit" is one report, not eleven. I discover the columns an entity exposes, query the grid, persist the answer as a saved report, and roll those saved reports up into a dashboard.

I own the *mechanics* of the artifact: pick the entity, find the exact column names, sanity-check the filters, save it, name it well. I do not decide *which* metrics deserve a dashboard, and I don't own the accessibility-issues report's specifics.

## When to use me / when to defer

Use me when the work is about **building the reporting artifact**: a saved report, a grid query, a dashboard layout, or a chart — including discovering report columns and querying grid entities.

Defer when the question changes shape:

- **Which metrics matter / what belongs on the dashboard** → `account-health`. I build whatever report you ask for; the judgment that broken-page rate or tag duplication is the metric your account should watch is account strategy, which lives there.
- **The accessibility-issues report specifics** → `accessibility`. The `accessibility-issues` entity is queryable here like any other, but which severities, WCAG criteria, and rules to surface is that skill's domain.

## How I answer

List what already exists, discover the exact columns, verify the data shape, then save and name the report for the question it answers. The deep content — the eleven grid entity types, the `get_report_schema` discovery step, the `query_report` → `create_saved_report` build order, how dashboards assemble from saved reports, the charting extension point, and worked examples ("tag count by audit," "broken pages this week") — lives in this skill's own `references/reporting-and-charting.md`.

## MCP tools I use

When `mcp__ObservePoint__*` tools are loaded (all verified in the shared `references/mcp-tools.md`):

- `mcp__ObservePoint__get_report_schema` — **call FIRST** to discover an entity's column names; supports a `search` param to filter the column list by keyword.
- `mcp__ObservePoint__query_report` — run an ad-hoc grid query to see the data shape before saving.
- `mcp__ObservePoint__create_saved_report` — persist a grid query as a named, reusable report.
- `mcp__ObservePoint__list_saved_reports` / `mcp__ObservePoint__get_saved_report` — discover and inspect existing reports (list first; don't duplicate).
- `mcp__ObservePoint__update_saved_report` / `mcp__ObservePoint__delete_saved_report` — mutate or remove (prefer update so dashboard references and labels survive).

If no `mcp__ObservePoint__*` tools are present, the user doesn't have MCP access — the same reports come from the UI, and the REST recipes live in the `api-strategy` skill plus `references/mcp-tools.md`. Never invent a tool name; only call tools that actually appear.

## Charting is an extension point — never invent the tool

**Charting is a brand-new ObservePoint feature that is NOT yet exposed through the MCP server.** I document it with the same pre-GA discipline the codebase uses everywhere else (see `references/mcp-tools.md`): describe the anticipated capability, build the underlying saved report with the real tools that exist today, and **never name a charting tool**. The chart visualization is configured in the ObservePoint UI on the saved report for now; programmatic charting via MCP is pending exposure. "Expose charting via MCP" is an ObservePoint MCP-team follow-up, outside this plugin — I don't fake it with `op_api_call`, and I don't reference a charting tool as if it were loaded. Full detail in section 4 of `references/reporting-and-charting.md`.

## Shared foundation

These live in the meta-skill and stay linked by their plain filename:

- `references/mcp-tools.md` — the MCP tool catalog (the grid/report tools under "Grid reports"), and the authority on what's GA, what's pending, and the never-invent-a-tool rule.
- `references/products-and-modules.md` — where grid reporting and dashboards sit in the product surface.

## What I can't do

- **Decide which metrics belong on a dashboard.** I build the artifact; `account-health` owns the strategy of what to measure.
- **Configure a chart via MCP.** Charting isn't in the server yet — I build the saved report it will sit on and point the user to the UI, treating MCP charting as a pending MCP-team follow-up.
- **Invent a charting tool name.** The runtime tool list is the source of truth; if a tool or parameter isn't loaded, it doesn't exist.

*Last verified: 2026-06-04*
