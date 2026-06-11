# Journeys & testing — build, script, debug, validate

Load this when the user wants to **build, script, debug, or troubleshoot a multi-step ObservePoint Journey**, validate a funnel / login / form flow where tag firing depends on what the user did, or use **LiveConnect** (real device) or the **HAR Analyzer** (offline / mobile-app HAR). A Web Audit loads URLs; a Journey *acts like a person* — clicks, types, submits — so the events that only fire on interaction actually fire.

The discipline of this skill is mechanical, not interpretive. It owns the *machinery* of the flow: the action sequence, the selectors that survive a page change, the SPA flag, the run that succeeds, the diagnosis when it doesn't. It does **not** judge whether the data the flow produced is correct — that is `tag-and-analytics-quality`'s job. A Journey is the vehicle; the Rules riding on it are the assertion. This file gets the vehicle running and keeps it running.

## Contents

1. [Journey construction — the action vocabulary](#1-journey-construction--the-action-vocabulary)
2. [The three safety gates](#2-the-three-safety-gates)
3. [Building a Journey](#3-building-a-journey)
4. [Debugging a Journey](#4-debugging-a-journey)
5. [LiveConnect and the HAR Analyzer](#5-liveconnect-and-the-har-analyzer)
6. [Worked example — a checkout funnel Journey](#6-worked-example--a-checkout-funnel-journey)
7. [Boundaries](#7-boundaries)

## 1. Journey construction — the action vocabulary

A Journey is an ordered list of **actions** the synthetic Chromium browser replays. The first action establishes the page; the rest are gestures and waits. Know the vocabulary before you script:

| Action | What it does |
|---|---|
| `navto` | Navigate to a URL. The first action; rarely repeated (see the journey-shape gate). |
| `click` | Click an element matched by a selector — the workhorse interaction. |
| `input` | Type a literal value into a field. Use for non-sensitive text (search terms, quantities). |
| `maskedinput` | Type a value that is **masked in the run record** — credentials, payment fields, any PII. Always prefer this for sensitive data so the literal never lands in the stored run. |
| `select` | Choose an option in a `<select>` dropdown. |
| `check` / `uncheck` | Toggle a checkbox or radio (consent boxes, terms acceptance, opt-ins). |
| `execute` | Run a snippet of JavaScript in page context — for state the UI can't express (set a variable, dispatch a custom event, clear storage). |
| `watch` | Wait on video playback or side-loading content. **Not** a generic timer (see the watch-usage gate). |
| `enteriframe` / `exitiframe` | Step the action context into and back out of an `<iframe>` — required for embedded checkout, third-party payment frames, embedded widgets whose elements aren't in the top document. |
| `actionset` | Invoke a reusable named sequence (an **action-set**) inline — e.g. a shared login block referenced from many Journeys. |

Two properties matter on nearly every action:

- **`waitDuration`** — a per-action buffer (the action waits N ms before/after it runs). This is the *correct* way to absorb between-step latency. Every action supports it. Reach for `waitDuration`, never a `watch` step, when you just need the page to settle.
- **The selector** — for the selector-bearing actions (`click`, `input`, `maskedinput`, `select`, `check`, `uncheck`, `enteriframe`), how the element is located: `css`, `id`, or `xpath`. The MCP wrappers also accept `text`, `ariaLabel`, and `name` and transparently rewrite them to css/xpath, but the backend stores only the three native types.

**Multi-step flows.** Order is everything: a `purchase` event won't fire until the steps before it (add-to-cart, fill the form, submit) have actually run. Build the flow as the human would walk it, attach Rules at the steps where the assertion belongs (section 6), and the run produces the hits in the same order a real session would. Two principles keep a multi-step flow from rotting:

- **One gesture per action.** Resist collapsing "fill the form and submit" into a single step. A separate `input` per field and a discrete `click` to submit means a failure points at the exact field, not a vague "the form step broke."
- **Verify each selector against the live page, once.** A selector captured from the real, current markup survives far longer than one inferred from a screenshot or memory — which is exactly what the selector-evidence gate enforces (section 2).

Login-gated and form flows follow the same shape: a login flow is `navto` → `input`/`maskedinput` the credentials → `click` submit (often factored into a shared **action-set**); a lead-gen or signup form is a sequence of `input`/`select`/`check` steps ending in a submit `click`, with the conversion event asserted on the post-submit page.

**The SPA "Prevent Navigation" flag.** Single-page apps (React, Vue, Angular, Svelte) change the route *without a full page reload*. By default the Journey engine treats a client-side route change as a fresh page load and **misses the tag firing** on the new route. Set `Prevent Navigation = true` on the click actions that trigger in-app route changes, and the engine keeps treating the session as one continuous page — capturing every tag firing across the route changes. This is the single most common reason an SPA funnel Journey "loses" its events. When the user mentions React/Vue/Angular, a checkout that never reloads, or "tags missing after the route changes," reach for this flag first.

## 2. The three safety gates

The MCP server's journey-mutation wrappers (`create_journey`, `update_journey_actions`, `create_actionset`, `update_actionset_actions`) enforce three constraints the raw REST API does not. **When a wrapper refuses, the wrapper is right** — fix the request, don't bypass with `op_api_call`. The authoritative detail (exact evidence shape, the shape table, which wrappers enforce which gate) lives in the shared `references/mcp-tools.md` → "Safety gates encoded in the wrappers." The summary and the *why*:

**Selector-evidence gate.** A selector-bearing action whose selector is new or changed must carry a `selector.evidence` block captured live via Claude for Chrome (a recent timestamp, `matchCount: 1`, the page URL, and the observed attributes). *Why:* a selector invented from memory or guessed from a screenshot breaks the moment the page markup shifts, and a Journey that silently clicks the wrong element produces confidently wrong results. Forcing live evidence means every selector resolved to exactly one real element on the real page at write time. The wrapper diffs per-action, so deleting steps or patching a `waitDuration` needs no evidence. `verify_selectors` is the companion sanity check that a selector resolves to one element.

**Journey-shape gate.** The wrapper refuses a journey that reduces to **2+ `navto` steps with zero interactive steps**. *Why:* that shape isn't a journey — it's a list of URLs, which is exactly what a Web Audit is for. A Journey exists to verify data flowing through *user gestures*; an "audit in disguise" wastes the more-expensive, more-fragile Journey machinery on something cheaper and more robust tooling does better. One `navto` plus gestures is fine; zero `navto` (the start URL is implicit) plus gestures is fine; 2+ `navto` with *some* interaction gets a soft warning, not a refusal.

**Watch-usage gate.** The wrapper refuses **2+ `watch` steps**. *Why:* `watch` is a special action for video playback and side-loading content, routinely misused as a generic "wait N seconds" sleep. Stacking `watch` steps to pad timing makes a Journey slow and brittle and hides the real intent. The correct tool for a between-step pause is `waitDuration` on the action itself — so the gate pushes you toward it.

## 3. Building a Journey

When `mcp__ObservePoint__*` tools are loaded (all verified in the shared `references/mcp-tools.md`):

- `mcp__ObservePoint__design_journey` — the smart-construction wrapper. Start here when scaffolding a new flow; it helps shape the action list correctly.
- `mcp__ObservePoint__create_journey` — create the Journey (subject to all three gates).
- `mcp__ObservePoint__update_journey_actions` — change the step sequence (subject to the gates; only genuinely new or changed selectors need fresh evidence).
- `mcp__ObservePoint__update_journey` — change Journey-level config (name, schedule, attached Rules, the SPA flag).
- `mcp__ObservePoint__verify_selectors` — confirm a css/id/xpath selector resolves to exactly one element on a page. Use it before and after a markup change to catch a selector that has gone stale.
- `mcp__ObservePoint__get_journey_actions` — read the current step sequence before mutating it.
- `mcp__ObservePoint__run_journey` — trigger a run (then `get_journey_runs` for history).

**Action-sets** — reusable named sequences, referenced from multiple Journeys (and from pre-audit-actions). A login block, a cookie-banner-dismiss block, an add-to-cart block: write it once, reference it everywhere.

- `mcp__ObservePoint__create_actionset` / `mcp__ObservePoint__update_actionset_actions` — author and mutate (same three gates apply).
- `mcp__ObservePoint__find_actionset_references` — **always run this before deleting** an action-set: it answers "which Journeys use this?" so you don't break a flow that depends on it. `delete_actionset` will happily tear down a set that three Journeys reference.

**Attaching Rules.** A Journey verifies *behavior*; the Tag & Variable Rules attached to it verify the *data*. Author the Rule (`create_rule`), then attach it to the Journey so the run produces a pass/fail. Authoring the assertion belongs to `tag-and-analytics-quality` / `privacy-compliance`; this skill makes sure the flow that triggers the hit actually runs.

## 4. Debugging a Journey

When a Journey fails, the question is *which step broke and why*. The diagnostic path, in order:

- `mcp__ObservePoint__diagnose_journey` — the smart-diagnosis wrapper. Start here: it interprets the failure rather than dumping raw data.
- `mcp__ObservePoint__get_journey_runs` — the run history; pick the failing run.
- `mcp__ObservePoint__get_run_action_outcomes` — the **per-step diagnostic subset**: which action passed, which failed, and where. This is the only sensible way to inspect a run — the raw `/results` endpoint is 3+ MB and will swamp the context. Always reach for the outcomes view, never the raw results.
- `mcp__ObservePoint__get_journey_console_errors` — the browser-console errors captured during the run. A step that "failed for no reason" is often a JS error on the page breaking the element the next action targets.
- `mcp__ObservePoint__get_journey_run_rule_results` — the Rule pass/fail breakdown for that specific run, when the steps all ran but an assertion failed.

The most common failure modes and where they show up:

- **Stale selector** — the markup changed and the action can no longer find its element. Shows up in `get_run_action_outcomes` as a failed step at a `click`/`input`. Fix: re-capture the selector with live evidence (the selector-evidence gate), confirm with `verify_selectors`.
- **Timing** — the action ran before the element existed. Add `waitDuration` to the action (not a `watch` step).
- **SPA route miss** — steps all pass but the expected tag never fired on a post-navigation route. Fix: set `Prevent Navigation` on the route-changing click.
- **Iframe context** — the element lives in an `<iframe>` (embedded payment, third-party widget) and the action can't reach it. Fix: wrap the interaction in `enteriframe` … `exitiframe`.
- **Page JS error** — `get_journey_console_errors` surfaces an exception that broke the page mid-flow.

A disciplined debug pass: `diagnose_journey` for the interpreted verdict → `get_run_action_outcomes` to pin the failing step → `get_journey_console_errors` to explain *why* that step failed → re-verify the suspect selector with `verify_selectors` → patch with `update_journey_actions` (fresh evidence only on the selectors that actually changed) → re-run with `run_journey` and confirm with `get_journey_run_rule_results`. Resist editing several steps at once; change one thing, re-run, confirm — a Journey that fails for two reasons looks identical to one that fails for one until you isolate them.

## 5. LiveConnect and the HAR Analyzer

Two testing surfaces that live outside the scheduled-scanner model. Source: shared `references/products-and-modules.md` → Journeys / LiveConnect / HAR Analyzer.

**LiveConnect — real device, real time.** A proxy-based harness: connect a real device (iPhone, Android phone or tablet, Mac or Windows desktop, Apple TV, other OTT devices) to LiveConnect over Wi-Fi, and every request that device makes flows through the proxy where you watch it **live**. This is the *only* way to validate behavior on a genuine device in real time — use it for ad-hoc debugging and pre-launch QA, the "test it on a real iPhone in front of me" case. The free tier ships 30 sessions per year (modern UI refresh completed 2025). It is **not** a scheduled-monitoring tool — there's no recurring run, no alert routing; it's a live console, not a cron job.

**HAR Analyzer — offline, captured traffic.** Upload a HAR file (the standard HTTP-archive export from Chrome DevTools, Charles, Fiddler, or any modern proxy) and the HAR Analyzer runs your **Tag & Variable Rules against the captured requests** — the same Rule coverage you'd get from a live scan, applied to traffic that already happened. Use it to:

- **Audit a native mobile app** — ObservePoint has no native app testing, so the supported workaround is: capture a HAR from the device, then process it through the HAR Analyzer (see shared `references/limitations.md`).
- **Audit a site you can't crawl directly** — a partner's property, a gated environment.
- **Audit one problematic session** a customer sent you, after the fact.

The HAR Analyzer is decoupled from LiveConnect — you can buy and use it standalone. The mental model: LiveConnect is the *live* device feed; the HAR Analyzer is the *recorded* one. Both terminate in your Rules.

**When to use which:**

| Situation | Use |
|---|---|
| Reproduce a tag bug on a real iPhone, right now | LiveConnect |
| Pre-launch QA on a physical device before a release | LiveConnect |
| You were handed a `.har` and asked "what's wrong?" | HAR Analyzer |
| Validate a native iOS / Android app's traffic | HAR Analyzer on a HAR captured from the app |
| The flow needs to be replayed on a schedule with alerting | Neither — script it as a **Journey** |

## 6. Worked example — a checkout funnel Journey

A retail funnel: home → product → add-to-cart → checkout → confirmation, with Rules attached at the steps where the assertion belongs. The Journey is the vehicle; the Rules are owned by `tag-and-analytics-quality`.

| # | Action | Selector / value | Rule at this step |
|---|---|---|---|
| 1 | `navto` | `https://shop.example.com/` | `page_view` fires once; CMP banner present |
| 2 | `click` | the featured-product card (live-verified css) | `view_item` fires; `item_id` non-empty |
| 3 | `select` then `click` | size dropdown, then "Add to cart" | `add_to_cart` fires; `value` numeric |
| 4 | `navto` *or* `click` | proceed to checkout | `begin_checkout` fires once |
| 5 | `maskedinput` ×N | shipping + payment fields (masked) | no PII reaches a third party (`scan_journey_pii` canary) |
| 6 | `click` | "Place order" | lands on confirmation |
| 7 | (confirmation page) | — | `purchase` fires **exactly once**; `transaction_id`, `value > 0`, `currency` well-formed |

Notes that make this run reliably:

- If the checkout is a **single-page app**, set `Prevent Navigation` on the step-4 click — otherwise the `begin_checkout` and `purchase` events on the post-navigation routes go uncaptured.
- If the payment fields live in a hosted-payment **iframe**, wrap step 5 in `enteriframe` … `exitiframe`.
- Use `maskedinput` for every payment/PII field and **test credentials / a test card only** — never a real customer's — so the literal is masked in the run record and the canary can prove (or disprove) a leak.
- Absorb load latency with `waitDuration` on the relevant actions, not a `watch` step (the watch-usage gate).
- If the add-to-cart and dismiss-cookie-banner blocks recur across many Journeys, factor them into an **action-set** and reference it.

This Journey has one `navto` (or two, with plenty of interaction) and many interactive steps, so it passes the journey-shape gate cleanly: it's a real human walking the funnel, not an audit in disguise.

## 7. Boundaries

This skill builds, runs, and debugs the *flow*. It defers in two directions:

- **`tag-and-analytics-quality`** owns *whether the resulting data is correct*. This skill makes the `purchase` event fire by driving a real checkout; tag-and-analytics-quality writes and reads the `WHEN tag = "GA4" AND event = "purchase" EXPECT value > 0` Rule that proves the data on that hit is sound. The same split applies to consent assertions on a Journey — author the Rule there, run the flow here. (`privacy-compliance` owns whether a hit should have fired at all under a given consent state.)
- **`account-and-program`** owns *audit and account setup*. Pre-audit actions, on-page actions, schedules, folders, alert routing, and the broader account structure are configuration concerns. This skill is about the Journey's *internal* mechanics; how the Journey or its sibling audits are scheduled, labeled, and alerted lives there.

For PII canary evidence on a journey run (`scan_journey_pii`), the litigation and healthcare/financial-services patterns live with `litigation-defense` and the industry references. For the persona-led end-to-end recipes — broken purchase event, validate every release — see the shared `references/solution-playbooks.md`.

*Last verified: 2026-06-04*
