# MCP tools — the extension point

The ObservePoint MCP server is in active development and **not yet generally available** as of the `Last verified` date below. This file documents the extension pattern the skill uses so the moment the server ships, the skill picks it up without code changes — and stays safe until then.

## Rules of engagement

Three hard rules:

1. **Never invent an MCP tool name.** If a tool is not present in the available-tools list at runtime *and* not documented in this file with verified status, do not pretend it exists.
2. **Prefer real MCP tools when present.** If you see a tool prefixed `mcp__observepoint__` at runtime, use it over a REST equivalent. Name the tool you used in your reply so the user can audit.
3. **Fall back to REST when MCP is absent.** Use `references/api-reference.md` recipes. Tell the user MCP is coming and what the call *would* look like — in plain language, not pseudo-tool-names.

## How the skill discovers MCP at runtime

Claude sees its own available tools each turn. The skill's behavior:

1. On any operational request ("trigger an audit," "fetch a report," "create a Rule"), check whether any tool prefixed `mcp__observepoint__` is in the available tools.
2. If yes — use that tool. Surface its name in the reply.
3. If no — proceed with the REST recipe and note the MCP fallback path.

No configuration is needed by the user. The detection is implicit in every response.

## Anticipated tool catalog (TBD pending GA)

The table below sketches the tool families the MCP server is expected to expose, based on the REST API surface they'd most naturally wrap. **Every entry below is `TBD pending GA`**: do not cite it as fact, and do not call any of these tools — they don't exist yet.

When the server ships, each row gets updated with the real tool name, parameter shape, and return type, sourced from the published server documentation. Until then, this is a placeholder structure to keep the skill organized.

### Audits

| Anticipated tool | What it would do | REST equivalent | Status |
|---|---|---|---|
| `mcp__observepoint__list_audits` | List Web Audits the caller can see | `GET /v3/web-audits` | TBD pending GA |
| `mcp__observepoint__start_audit_run` | Trigger a new run of an audit | `POST /v3/web-audits/{id}/runs` | TBD pending GA |
| `mcp__observepoint__get_audit_run` | Get the status and metadata of a run | `GET /v3/web-audits/{id}/runs/{runId}` | TBD pending GA |
| `mcp__observepoint__get_audit_report` | Fetch a specific report from a run | `GET /v3/web-audits/{id}/runs/{runId}/reports/...` | TBD pending GA |

### Journeys

| Anticipated tool | What it would do | REST equivalent | Status |
|---|---|---|---|
| `mcp__observepoint__list_journeys` | List Journeys | `GET /v3/web-journeys` | TBD pending GA |
| `mcp__observepoint__start_journey_run` | Trigger a Journey run | `POST /v3/web-journeys/{id}/runs` | TBD pending GA |
| `mcp__observepoint__get_journey_run` | Get the status of a Journey run | `GET /v3/web-journeys/{id}/runs/{runId}` | TBD pending GA |

### Rules

| Anticipated tool | What it would do | REST equivalent | Status |
|---|---|---|---|
| `mcp__observepoint__list_rules` | List Tag & Variable Rules | `GET /v3/rules` | TBD pending GA |
| `mcp__observepoint__create_rule` | Create a new Rule | `POST /v3/rules` | TBD pending GA |
| `mcp__observepoint__update_rule` | Edit an existing Rule | `PATCH /v3/rules/{id}` | TBD pending GA |
| `mcp__observepoint__delete_rule` | Remove a Rule | `DELETE /v3/rules/{id}` | TBD pending GA |

### HAR processing

| Anticipated tool | What it would do | REST equivalent | Status |
|---|---|---|---|
| `mcp__observepoint__process_har` | Upload and process a HAR file | `POST /v3/har-analyzer/process` | TBD pending GA |

### Alerts and notifications

| Anticipated tool | What it would do | REST equivalent | Status |
|---|---|---|---|
| `mcp__observepoint__list_alerts` | List configured Alerts | `GET /v3/alerts` | TBD pending GA |

The actual server may use different names, group operations differently, or expose tools none of these placeholders anticipate. **Do not call these placeholders.** They are typed examples of the shape this catalog will take, not specifications.

## What this file becomes once the MCP server reaches GA

A PR will:

1. Replace each placeholder row with the real tool name and parameter description, sourced from the official MCP server documentation.
2. Add a "Setup" section explaining how the user installs or connects the MCP server.
3. Add per-tool examples (the exact tool-call shape, expected returns, error patterns).
4. Update the `Last verified` date.
5. Bump the plugin/skill version.

If you (a future contributor) have a verified tool list from the actual server, that's the PR to open.

## How to respond TODAY when a user says "use the ObservePoint MCP"

Template reply, paraphrased to the user's tone:

> The ObservePoint MCP server isn't generally available yet, so the tools to call it aren't loaded in my session. I'll do this through the REST API instead — same end result, different transport. Once the MCP server ships, this skill will automatically pick it up and prefer it.
>
> Here's the REST approach: `<call out the recipe from references/api-reference.md>`.
>
> The MCP call, when it lands, will look roughly like a `start_audit_run` operation taking an audit ID and returning a run ID — but I won't speculate on the exact name until the server documents it.

That's it. Honest, useful, and doesn't lie about tools that don't exist.

---

*Last verified: 2026-05-28*
