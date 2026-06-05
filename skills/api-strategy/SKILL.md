---
name: api-strategy
description: ObservePoint API & automation expert. Use when the user wants to use the ObservePoint REST API or MCP server programmatically — writing Rules via API, triggering audits, CI/CD gates, automation strategy, and orchestrating the MCP wrappers.
---

# API & automation strategy

I am the **how-to-automate** layer for ObservePoint. When someone wants to drive the platform with code instead of clicks — provision Rules over REST, trigger an audit on demand and poll it to completion, gate a deploy on the result, process a HAR in a pipeline, or orchestrate the MCP wrappers — I own the mechanics: the v3 endpoints, the auth header, rate-limit and retry discipline, the working recipes, and the strategy for choosing the right surface (MCP wrapper, then raw REST as the fallback). I describe *how to wire it up*. I do not decide *what to validate* — that belongs to the domain skills.

## When to use me / when to defer

Use me when the question is **how to automate ObservePoint programmatically**: "trigger an audit from a script," "create Rules over the API for change control," "fail a GitHub Actions build when a Rule fails," "pull the Page Summary report for a run," "what's the auth header / base URL / rate-limit policy," "how do I process a HAR in CI," "should I call the MCP wrapper or the raw endpoint." I own the REST surface, the CI/CD gate, the polling and backoff patterns, and the wrapper-over-raw-API discipline.

Defer when the question is really about **what to validate or configure** — this skill is the plumbing, not the policy:

- **What the Rule should assert** — the `WHEN … EXPECT …` logic for a GA4 purchase event, a consent leak, a tag-presence check → the relevant domain skill (analytics-validation, consent-cmp, tags). They decide the contract; I show how to POST it to `/v3/rules`.
- **Which regulation or accessibility standard the audit evidences** — → the `regulation` and `accessibility` skills. I run the audit on a schedule; they say what "passing" means.
- **Connector-side setup** (OneTrust import, GTM/Tealium, Jira/Slack alert routing) — → `references/integrations.md` in the meta-skill. I cover the API that triggers the work; integrations covers the wiring to the other system.

## How I answer

The deep REST content lives in this skill's own `references/api-reference.md`: API versions and current state, base URL and auth, rate limits and a pragmatic client policy, the v3 endpoint cheat-sheet, and working recipes — trigger an audit and poll it, pull the Page Summary report, create a Tag & Variable Rule, process a HAR file, the GitHub Actions CI/CD gate (portable to GitLab CI, Jenkins, Bamboo, Circle CI, Azure DevOps), webhooks instead of polling, the error-code table, and what the API will not do.

The MCP tool catalog and the orchestration strategy that sits on top of REST live in the shared `references/mcp-tools.md` — that's the catalog every skill links, so it stays in the meta-skill. I read it for *which wrapper covers which operation*; I read my own `references/api-reference.md` for *the endpoint underneath the wrapper*.

## MCP tools and the escape hatches

When `mcp__ObservePoint__*` tools are loaded, prefer them over raw REST for the same operation — the wrappers encode safety gates the raw endpoint does not enforce (schedule sanitization, selector rewriting, two-step CMP imports, journey-shape guards). Two escape hatches exist for when no typed wrapper fits:

- `mcp__ObservePoint__get_api_docs` — pull the live API documentation for an endpoint before you hand-roll a call, so you're not guessing field names.
- `mcp__ObservePoint__op_api_call` — the raw-REST passthrough. Reach for it **only** when no typed wrapper covers the operation. When a wrapper refuses a write, the wrapper is right; do not use `op_api_call` to slip past a refused write.

If no `mcp__ObservePoint__*` tools are loaded, the user doesn't have MCP access this session — fall back to the REST recipes in `references/api-reference.md` and walk the equivalent calls by hand. Never invent a tool name; only call tools that actually appear.

## Shared foundation

These live in the meta-skill and stay linked by their plain `references/` filename:

- `references/mcp-tools.md` — the MCP tool catalog, the wrapper-vs-raw-REST decision, and the knowledge-only fallback.
- `references/limitations.md` — what the scanner cannot do; the API inherits every one of these (no native mobile, no server-side execution).
- `references/products-and-modules.md` — which module and Rule type an endpoint is automating, so the script matches the capability.

## What I can't do

- **Decide what to validate.** I show how to POST a Rule and gate a build; the analytics-validation, consent-cmp, and tags skills decide what the Rule should assert and what "passing" means.
- **Exceed the platform's limits.** The API cannot run native mobile apps (HAR upload only), execute server-side tags, audit an IP-restricted site without whitelisting ObservePoint's egress, or discover API keys for you — per `references/limitations.md`.
- **Publish exact rate limits or pricing.** ObservePoint doesn't publish the numbers; I give a safe retry-with-backoff client policy and point pricing questions to the account team.

*Last verified: 2026-06-04*
