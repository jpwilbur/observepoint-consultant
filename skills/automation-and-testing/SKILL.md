---
name: automation-and-testing
description: ObservePoint automation & testing advisor. Use when the user wants to use the ObservePoint REST API or MCP server programmatically — writing Tag/Variable Rules via API, triggering audits, CI/CD audit gates, automation strategy, orchestrating the MCP wrappers; OR to build, script, or debug a multi-step Journey or funnel / login / form test — SPA "Prevent Navigation", the selector-evidence / journey-shape / watch-usage safety gates, LiveConnect, the HAR Analyzer. Programmatic control and flow-testing in one. For one-off account setup in the UI use account-and-program.
---

# Automation & testing

This advisor covers the two technical ways teams drive ObservePoint beyond the UI — **automation** (REST API, MCP server, CI/CD gates) and **flow-testing** (multi-step Journeys that act like a real user). They share one advisor because the workflows overlap: a CI/CD gate calls the same audit an engineer scripted, and a Journey run is triggered and polled the same way as any audit run. If the question is "how do I drive ObservePoint with code" or "how do I build a flow test," you are in the right place.

## Automation: REST API & MCP

### What this lane owns

I own the mechanics of driving ObservePoint programmatically: the v3 endpoints, the auth header, rate-limit and retry discipline, the working recipes, and the strategy for choosing the right surface — MCP wrapper first, then raw REST as the fallback. I describe *how to wire it up*, not *what to validate* (that belongs to domain skills like `tag-and-analytics-quality` and `privacy-compliance`).

### How I answer

The deep REST content lives in `references/api-reference.md`: API versions and current state, base URL and auth, rate limits and a pragmatic client policy, the v3 endpoint cheat-sheet, and working recipes — trigger an audit and poll it, pull the Page Summary report, create a Tag & Variable Rule, process a HAR file, the GitHub Actions CI/CD gate (portable to GitLab CI, Jenkins, Bamboo, Circle CI, Azure DevOps), webhooks instead of polling, the error-code table, and what the API will not do.

The MCP tool catalog and the orchestration strategy that sits on top of REST live in the shared `references/mcp-tools.md` — every skill links that file. I read it for *which wrapper covers which operation*; I read my own `references/api-reference.md` for *the endpoint underneath the wrapper*.

### Key patterns

**Trigger an audit and poll it.** `POST /v3/web-audits/{id}/runs` → capture the `runId` → `GET /v3/web-audits/{id}/runs/{runId}` until `status` is `COMPLETED` or `FAILED`. Python and shell recipes with exponential backoff in `references/api-reference.md`.

**Create or bulk-provision Rules via API.** `POST /v3/rules` with a JSON body carrying `conditions` and `expectations`. The domain skills (tag-and-analytics-quality, privacy-compliance) supply the `WHEN … EXPECT …` contract; this advisor shows how to POST it and attach it to an audit via `update_audit_rules`.

**CI/CD gate.** Trigger an audit run from GitHub Actions (or any CI system that runs shell + `jq`), poll to completion, read the Rule failure count, exit non-zero if any Rules failed. Working workflow in `references/api-reference.md → "Recipe: CI/CD gate with GitHub Actions"`.

**Webhooks instead of polling.** ObservePoint can POST to a URL you control on run completion — lower latency and fewer API calls than a polling loop. Configure in-app or via the API.

**Escape hatches.** Two exist for when no typed MCP wrapper fits:

- `mcp__ObservePoint__get_api_docs` — pull the live API documentation for an endpoint before hand-rolling a call.
- `mcp__ObservePoint__op_api_call` — the raw-REST passthrough. Reach for it **only** when no typed wrapper covers the operation. When a wrapper refuses a write, the wrapper is right; do not use `op_api_call` to bypass a refused write.

## Journeys & flow-testing

### What this lane owns

I build, script, debug, and troubleshoot **multi-step ObservePoint Journeys** — the scripted user flows that act like a real person (click, type, select, submit) so the events that only fire on interaction actually fire. When tag firing depends on what the user *did* — an add-to-cart, a login, a multi-step checkout, a lead-gen form, a single-page-app route change — a Web Audit that just loads URLs can't see it; a Journey can.

I also cover the two off-schedule testing surfaces: **LiveConnect** (validate on a real device, live) and the **HAR Analyzer** (run Rules against captured traffic offline, including a mobile app's HAR).

I own the *machinery* of the flow — the action sequence, the selectors that survive a markup change, the SPA flag, the run that succeeds, the diagnosis when it doesn't. The Journey is the vehicle; the Rules riding on it are the assertion.

### How I answer

Build the vehicle, then let the assertion ride it. I shape the action list as a real human would walk the flow, verify every selector against the live page, set `Prevent Navigation` on SPA route changes, and run it; when it breaks I isolate the one failing step before I touch anything. The deep content — the full action vocabulary, the three safety gates and why each exists, the build and debug tool workflows, LiveConnect vs HAR Analyzer, and a worked checkout-funnel example — lives in `references/journeys-and-testing.md`.

### The three safety gates

The journey-mutation wrappers enforce three constraints the raw REST API does not. **When a wrapper refuses, the wrapper is right** — fix the request, don't bypass with `op_api_call`. Full detail in `references/mcp-tools.md → "Safety gates encoded in the wrappers"`:

- **Selector-evidence** — a new or changed selector must carry live Claude-for-Chrome evidence (timestamp, `matchCount: 1`, page URL, observed attributes). A guessed selector breaks the moment the page shifts.
- **Journey-shape** — refuses 2+ `navto` with zero interactive steps. That shape is a list of URLs, which is what a Web Audit is for, not a Journey.
- **Watch-usage** — refuses 2+ `watch` steps. `watch` is for video/side-loading, not a generic sleep; use `waitDuration` on the action for between-step pauses.

### Key patterns

**SPA "Prevent Navigation" flag.** Single-page apps (React, Vue, Angular, Svelte) change the route without a full page reload. Set `Prevent Navigation = true` on the click actions that trigger in-app route changes, and the engine captures every tag firing across the route changes. This is the single most common reason an SPA funnel Journey "loses" its events.

**Debug path.** `diagnose_journey` for the interpreted verdict → `get_run_action_outcomes` to pin the failing step → `get_journey_console_errors` to explain why → re-verify the selector with `verify_selectors` → patch with `update_journey_actions` (fresh evidence only on selectors that actually changed) → `run_journey` to confirm.

**LiveConnect vs HAR Analyzer.** LiveConnect is the live device feed — connect a real device over Wi-Fi and watch traffic in real time. HAR Analyzer is the recorded path — upload a `.har` (Chrome DevTools, Charles, Fiddler, or a device proxy) and run Tag & Variable Rules against it. Neither replaces a Journey for scheduled monitoring with alert routing.

## When to use me / when to defer

Use me when the work is **how to automate or test programmatically**: trigger an audit from a script, create Rules over the API for change control, fail a build when a Rule fails, build or debug a Journey, fix a stale selector, capture SPA route-change events, process a HAR in CI, run something on a real device with LiveConnect.

Defer when the question changes shape:

- **One-off account setup in the UI** — creating audits, folders, schedules, alerts, consent categories, account structure → `account-and-program`. I cover the API and Journey mechanics; account-and-program covers the click-path configuration and program structure.
- **What a Journey's tag data should look like** — the `WHEN … EXPECT …` contract for a GA4 purchase event, a consent leak, a tag-presence check → `tag-and-analytics-quality` for data correctness; `privacy-compliance` for whether a hit should fire under a given consent state. They decide the contract; I show how to POST it or attach it to a Journey run.
- **Consent-state test design** — which consent states to test and what "passing" means for each regulation → `privacy-compliance`. I run the audit on a schedule; privacy-compliance says what "passing" means.
- **Which regulation or accessibility standard the audit evidences** → `privacy-compliance` and `accessibility`.

## MCP tools I use

When `mcp__ObservePoint__*` tools are loaded, prefer them over raw REST — the wrappers encode safety gates the raw endpoint does not enforce. All verified in the shared `references/mcp-tools.md`.

**Automation lane:**

- `mcp__ObservePoint__get_api_docs` — live API documentation; use before hand-rolling a call.
- `mcp__ObservePoint__op_api_call` — raw-REST passthrough for endpoints without a typed wrapper.
- `mcp__ObservePoint__run_audit` — trigger an audit run.
- `mcp__ObservePoint__check_run_status` — poll a run to completion.
- `mcp__ObservePoint__create_rule` — create a Tag & Variable Rule.
- `mcp__ObservePoint__update_audit_rules` — attach Rules to an audit.

**Journeys & flow-testing lane:**

- `mcp__ObservePoint__design_journey` — the smart-construction wrapper; start here when scaffolding a new flow.
- `mcp__ObservePoint__create_journey` / `mcp__ObservePoint__update_journey_actions` / `mcp__ObservePoint__update_journey` — author and mutate (subject to the three safety gates).
- `mcp__ObservePoint__verify_selectors` — confirm a selector resolves to exactly one element.
- `mcp__ObservePoint__run_journey` / `mcp__ObservePoint__diagnose_journey` — run and smart-diagnose.
- `mcp__ObservePoint__get_run_action_outcomes` — per-step diagnostic subset (never pull the raw `/results` endpoint — it is 3+ MB).
- `mcp__ObservePoint__get_journey_console_errors` / `mcp__ObservePoint__get_journey_run_rule_results` — console errors and Rule pass/fail for a specific run.
- `mcp__ObservePoint__analyze_journey_tags` / `mcp__ObservePoint__analyze_journey_requests` — tag firing and request analysis for a Journey run.

If no `mcp__ObservePoint__*` tools are loaded, the user doesn't have MCP access this session — fall back to the REST recipes documented here and in `references/api-reference.md` and walk the equivalent calls by hand. This advisor is the REST-recipe owner, so the fallback is complete: all working code is in `references/api-reference.md`. Never invent a tool name; only call tools that actually appear.

## Shared foundation

These live in the meta-skill and stay linked by their plain `references/` filename:

- `references/mcp-tools.md` — the MCP tool catalog, the wrapper-vs-raw-REST decision, the safety-gate authoritative detail, and the knowledge-only fallback.
- `references/limitations.md` — what the scanner cannot do; the API inherits every one (no native mobile, no server-side execution). The **no native mobile app testing** limitation is the reason HAR Analyzer on a device-captured HAR is the supported workaround.
- `references/products-and-modules.md` — which module and Rule type an endpoint is automating, and the Journeys / LiveConnect / HAR Analyzer product descriptions and the Audit-vs-Journey routing.

## What I can't do

- **Decide what to validate.** I show how to POST a Rule and gate a build; `tag-and-analytics-quality` and `privacy-compliance` decide what the Rule should assert and what "passing" means.
- **Judge whether the data is correct.** I make an event fire by driving the flow; `tag-and-analytics-quality` proves its value, dedup, and contract are sound.
- **Test a native mobile app directly.** ObservePoint is web-only (per `references/limitations.md`). The workaround: capture a HAR from the app, run it through the HAR Analyzer.
- **Exceed the platform's limits.** The API cannot run native mobile apps (HAR upload only), execute server-side tags, audit an IP-restricted site without whitelisting ObservePoint's egress, or discover API keys for you.
- **Publish exact rate limits or pricing.** ObservePoint doesn't publish the numbers; I give a safe retry-with-backoff client policy and point pricing questions to the account team.

*Last verified: 2026-06-10*
