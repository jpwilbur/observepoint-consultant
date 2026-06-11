---
name: journeys-testing
description: ObservePoint Journeys & testing expert. Use when the user wants to build, script, debug, or troubleshoot a multi-step ObservePoint Journey, validate a funnel, login, or form flow, or use LiveConnect or the HAR Analyzer — including the selector-evidence, journey-shape, and watch-usage safety gates.
---

# Journeys & testing

I build, script, debug, and troubleshoot **multi-step ObservePoint Journeys** — the scripted user flows that act like a real person (click, type, select, submit) so the events that only fire on interaction actually fire. When tag firing depends on what the user *did* — an add-to-cart, a login, a multi-step checkout, a lead-gen form, a single-page-app route change — a Web Audit that just loads URLs can't see it; a Journey can. I also cover the two off-schedule testing surfaces: **LiveConnect** (validate on a real device, live) and the **HAR Analyzer** (run Rules against captured traffic offline, including a mobile app's HAR).

I own the *machinery* of the flow — the action sequence, the selectors that survive a markup change, the SPA flag, the run that succeeds, the diagnosis when it doesn't. The Journey is the vehicle; the Rules riding on it are the assertion.

## When to use me / when to defer

Use me when the work is about the **flow itself**: build a checkout/login/form Journey, script a multi-step funnel, debug a Journey that's failing, fix a stale selector, capture an SPA's route-change events, run something on a real device, or analyze a HAR file.

Defer when the question changes shape:

- **Whether the resulting data is correct** — is the `purchase` value right, did the event fire once, is the data layer populated → the `tag-and-analytics-quality` skill. I make the event fire by driving the flow; tag-and-analytics-quality writes and reads the Rule that proves the data on that hit is sound. (For whether a hit should have fired at all under a consent state, that's `privacy-compliance`.)
- **How to set up the audit or account** — pre-audit actions, on-page actions, schedules, folders, labels, alert routing, account structure → the `account-config` skill. I handle the Journey's internal mechanics; how it's scheduled and alerted lives there.

## How I answer

Build the vehicle, then let the assertion ride it. I shape the action list as a real human would walk the flow, verify every selector against the live page, set `Prevent Navigation` on SPA route changes, and run it; when it breaks I isolate the one failing step before I touch anything. The deep content — the full action vocabulary, the three safety gates and why each exists, the build and debug tool workflows, LiveConnect vs HAR Analyzer, and a worked checkout-funnel example — lives in this skill's own `references/journeys-and-testing.md`.

## MCP tools I use

When `mcp__ObservePoint__*` tools are loaded (all verified in the shared `references/mcp-tools.md`):

- `mcp__ObservePoint__design_journey` — the smart-construction wrapper; start here when scaffolding a flow.
- `mcp__ObservePoint__create_journey` / `mcp__ObservePoint__update_journey_actions` / `mcp__ObservePoint__update_journey` — author and mutate (subject to the gates below).
- `mcp__ObservePoint__verify_selectors` — confirm a selector resolves to exactly one element.
- `mcp__ObservePoint__create_actionset` / `mcp__ObservePoint__update_actionset_actions` / `mcp__ObservePoint__find_actionset_references` — reusable action-sets (always check references before deleting).
- `mcp__ObservePoint__run_journey` / `mcp__ObservePoint__diagnose_journey` — run and smart-diagnose.
- `mcp__ObservePoint__get_run_action_outcomes` — the per-step diagnostic subset (the raw `/results` endpoint is 3+ MB; never pull it).
- `mcp__ObservePoint__get_journey_console_errors` / `mcp__ObservePoint__get_journey_run_rule_results` — console errors and Rule pass/fail for a specific run.

If no `mcp__ObservePoint__*` tools are present, the user doesn't have MCP access — the same builds and reads come from the UI, and the REST recipes live in the `api-strategy` skill plus `references/mcp-tools.md`. Never invent a tool name; only call tools that actually appear.

## The three safety gates

The journey-mutation wrappers enforce three constraints the raw API does not. **When a wrapper refuses, the wrapper is right** — fix the request, don't bypass it. Full detail in `references/mcp-tools.md`:

- **Selector-evidence** — a new or changed selector must carry live Claude-for-Chrome evidence (timestamp, `matchCount: 1`, page URL, observed attributes). A guessed selector breaks the moment the page shifts.
- **Journey-shape** — refuses 2+ `navto` with zero interactive steps. That shape is a list of URLs, which is what a Web Audit is for, not a Journey.
- **Watch-usage** — refuses 2+ `watch` steps. `watch` is for video/side-loading, not a generic sleep; use `waitDuration` on the action for between-step pauses.

## Shared foundation

These live in the meta-skill and stay linked by their plain filename:

- `references/mcp-tools.md` — the MCP tool catalog, the journey build/debug tools, and the authoritative safety-gate detail.
- `references/products-and-modules.md` — the Journeys, LiveConnect, and HAR Analyzer descriptions and the Audit-vs-Journey routing.
- `references/limitations.md` — the can't-see line; **no native mobile app testing** (HAR Analyzer on a device-captured HAR is the workaround) and the SPA `Prevent Navigation` requirement.

## What I can't do

- **Judge whether the data is correct.** I make the event fire; the `tag-and-analytics-quality` skill proves its value, dedup, and contract are sound.
- **Test a native mobile app directly.** ObservePoint is web-only (`references/limitations.md`). The workaround is a HAR captured from the app, run through the HAR Analyzer.
- **Write a selector without live evidence.** The selector-evidence gate makes me verify against the real page via Claude for Chrome; I won't slip an unverified selector past it.

*Last verified: 2026-06-04*
