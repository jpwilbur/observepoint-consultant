# Analytics validation — is my data firing correctly?

Load this when the user asks whether their analytics **data** is right: are the GA4 or Adobe events and variables firing, is the data layer populated correctly, does the purchase carry a real value, are events duplicated or missing, do attribution parameters survive the landing. This is the **is-my-data-right** layer, and it is the flagship ObservePoint use case.

The shape of the discipline: you do not trust a number in a report until a Rule has asserted the request that produced it. Every section below ends in a `WHEN … EXPECT …` Rule, because a claim about data is only as good as the assertion that catches it failing. ObservePoint runs the page (or the checkout journey) in a real Chromium browser and inspects the actual hit on the wire, then a Tag & Variable Rule evaluates the payload and routes a failure before the conversion report goes sideways.

This reference sits between two siblings. `martech` explains *how the platform is built* — GA4's event model, Adobe's Web SDK, the dataLayer→tag handoff. `tags` answers *what a tag is and whether it belongs on the page*. This skill takes the platform as built and the tag as present, and proves the **data coming out of it is sound**.

## Contents

1. [The analytics implementations — what "correct" means](#1-the-analytics-implementations--what-correct-means)
2. [The data-layer contract](#2-the-data-layer-contract)
3. [Value-integrity Rules](#3-value-integrity-rules)
4. [Dedup — fires exactly once](#4-dedup--fires-exactly-once)
5. [Missing-event detection](#5-missing-event-detection)
6. [Attribution-parameter survival](#6-attribution-parameter-survival)
7. [MCP workflow](#7-mcp-workflow)
8. [Boundaries](#8-boundaries)

## 1. The analytics implementations — what "correct" means

You cannot validate data without a contract for what correct looks like. The two implementations ObservePoint validates most are GA4 and Adobe Analytics, and "correct" is defined differently for each.

**GA4.** Everything is an event with parameters. The events that carry a defined contract — and therefore the ones worth Rules — are the *recommended* events with reserved names: `purchase`, `add_to_cart`, `view_item`, `begin_checkout`, `login`, `sign_up`. Google publishes the expected parameters for each; `purchase` is expected to carry `transaction_id`, `value`, `currency`, and an `items` array. Custom events the implementer names have whatever contract your team wrote down — so the contract has to exist before you can assert it.

On the wire, a GA4 hit goes to `google-analytics.com/g/collect` (or a region endpoint, or a first-party `/collect` path if the customer proxies it). The event name rides in the `en` parameter; ecommerce items are encoded in the `pr1`, `pr2`… product parameters; consent flags ride in `gcs` / `gcd`. "Correct" means: the right event name fired, on the right page, exactly once, carrying the registered parameters with values of the right type and range.

The **dataLayer→tag pickup** is where GA4 data most often breaks. The dataLayer push is upstream of the tag; the tag (gtag or a GTM tag) reads from it and constructs the hit. If the push lands *after* the tag reads, the hit fires with empty or stale values — a timing failure, not a tagging failure (section 2). A parameter that fires correctly on the wire but was never registered as a custom dimension is invisible in the GA4 UI — that is a console problem, not a data problem, and ObservePoint validates the wire, so it will confirm the data is there even when the report can't show it.

**Adobe Analytics.** The variable model is eVars (conversion variables, persistent), props (traffic variables, pageview-scoped), and events (success metrics / counters). "Correct" means the right eVar/prop/event slots are populated with the expected values on the expected pages — `eVar12` carries the order ID on the confirmation page, `event1` increments on a purchase, `prop4` carries the page category.

The transport matters for *where you read the value*. **AppMeasurement** (the legacy `s.t()` / `s.tl()` library) sends a hit to a `/b/ss/` collection path with the variables as named query parameters (`v12` for eVar12, `c4` for prop4, `events`). The **Web SDK** (`alloy`, the Edge Network path) sends an XDM payload to an Edge endpoint as a structured POST body, mapped to eVars/props server-side. ObservePoint validates both, but the assertion targets the parameter for AppMeasurement and the XDM field for the Web SDK. Confirm which one the customer runs before writing the Rule.

## 2. The data-layer contract

Most "broken event" tickets are not broken tags — they are a data layer that wasn't populated when the tag read it. Validating the data layer is validating a **contract and its timing**: the data layer must contain the agreed keys, with values of the agreed type, *before* the tag fires.

**The contract.** Treat the data layer (GA4 `dataLayer`, Adobe Client Data Layer / Tealium `utag_data`) like a schema. On a product page you expect `ecommerce.items[0].item_id`, `item_name`, `price`, `currency`; on a confirmation page you expect `ecommerce.transaction_id`, `value`, `currency`, `items[]`. The contract is what your Rules assert against — without it, "is the data layer correct" has no answer.

**Common hydration / timing failures ObservePoint catches:**

- **Late push.** The dataLayer push runs after the page-view tag reads, so the hit fires with empty values. The dataLayer object eventually looks right in the console, which is why this hides — the value is present *now* but was absent *when the tag fired*. A Journey that drives the real interaction and a Rule on the resulting hit catch it; inspecting the static dataLayer does not.
- **Wrong type.** `value` pushed as the string `"129.00"` instead of the number `129.00`, or `price` with a currency symbol baked in. GA4 and Adobe both tolerate strings on ingest but degrade in reporting/attribution.
- **Stale carry-over.** On a single-page app, a route change reuses the prior route's dataLayer because nothing cleared it — the new page-view event carries the old page's values.
- **Missing key.** A key the contract requires never gets pushed on a given template (the new PDP variant forgot `item_category`).

You validate the *effect* of the data layer on the hit, not the data-layer object in isolation — the hit is what the downstream platform actually receives.

```
WHEN page matches "/product/" AND event ("en") = "view_item"
EXPECT
  the items array is present (at least one product parameter)
  parameter "item_id" (pr1 "id") is present and non-empty
  parameter "value" is numeric AND >= 0
  parameter "currency" matches /^[A-Z]{3}$/
```

## 3. Value-integrity Rules

The single highest-stakes assertion in analytics validation: when money is involved, a wrong value corrupts the conversion report, the ROAS calculation, and the bid signal sent to every ad platform downstream. Value-integrity Rules assert that the purchase/conversion payload is not just present but *sane*.

The three checks that catch the overwhelming majority of value bugs:

- **Numeric and positive.** `value` is a number, greater than zero. Catches the string-typed value, the `0` from an empty cart, the `undefined` rendered as `NaN`.
- **Currency well-formed.** A three-letter uppercase ISO code. Catches the missing currency (GA4 silently drops revenue when `currency` is absent on `purchase`), the lowercase `usd`, the `"$"`.
- **Items array populated.** At least one item, each with an id and a price. Catches the purchase that reports revenue with no line items — which breaks product-level attribution even when the top-line number looks right.

```
WHEN tag = "Google Analytics 4" AND event ("en") = "purchase"
EXPECT
  parameter "transaction_id" is present and non-empty
  parameter "value" is numeric AND > 0
  parameter "currency" matches /^[A-Z]{3}$/
  the items array is present (at least one product parameter)
```

The Adobe equivalent asserts the same intent against the variable model — `event1` (purchase) present, `products` string non-empty, the revenue eVar/event numeric and positive:

```
WHEN tag = "Adobe Analytics" AND request matches "/b/ss/" AND "events" contains "purchase"
EXPECT
  variable "products" is present and non-empty
  the revenue event is numeric AND > 0
  variable "eVar<order-id>" is present and non-empty
```

Drive these through a real checkout with a Journey so the `purchase` event actually fires, then attach the Rule to the Journey run — a Web Audit will not complete a purchase on its own.

## 4. Dedup — fires exactly once

A duplicated event inflates conversions, doubles revenue, and over-counts the signal sent to ad platforms. It is hard to spot in aggregate — the report just looks "a bit high." A fires-exactly-once Rule catches it deterministically.

The classic causes: a confirmation page that double-fires on reload because there is no idempotency on `transaction_id`; a `page_view` firing once from GA4 enhanced measurement and once from a manual GTM tag; an SPA that re-fires the route's event on a back-then-forward navigation; a tag deployed both directly and through the tag manager.

```
WHEN page matches "/order-complete"
EXPECT tag "Google Analytics 4" event "purchase" fires exactly once
```

For the same-`transaction_id`-twice case, pair the count Rule with `profile_variable` on the `transaction_id` parameter across the run — a transaction id that appears on more than one hit is a duplicate even if each individual page fired "once."

## 5. Missing-event detection

The inverse failure: the event should fire on a class of pages and silently doesn't on some of them. This is the "should be everywhere but isn't" problem, and the aggregate report can't show you a hit that never happened — you only notice the revenue is light.

`get_pages_without_tag` is the workhorse here: it returns the pages in an audit run where a specific tag (or event) did **not** fire. Run it scoped to the page class where the event is contractually required — every confirmation page should fire `purchase`, every PDP should fire `view_item` — and the result is your gap list: the page templates, the one locale, the new checkout variant that shipped without the tag.

The pattern:

1. Define the population — the URL pattern where the event must fire (`/order-complete`, `/product/`).
2. Run `get_pages_without_tag` for the tag/event against that population on the latest run.
3. Every page returned is a miss. Triage by template — a single broken page is a content issue; a whole template missing is a deploy regression.
4. Pair with `find_coverage_gaps` for the cross-audit "what's missing across the whole property" view.

The release-gate use case lives here too: a targeted audit on staging confirmation URLs, with a missing-event check, run as a CI/CD gate so a deploy that drops the `purchase` tag fails the build instead of shipping. The `api-strategy` skill owns the working CI/CD gate recipe.

## 6. Attribution-parameter survival

Attribution breaks before any analytics event fires if the campaign parameters don't survive the landing. The marketing parameters — `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, plus the click IDs `gclid`, `gbraid`, `wbraid`, `fbclid`, `msclkid`, `ttclid` — must reach the landing page intact for the analytics platform and ad network to attribute the session correctly.

The killers ObservePoint catches:

- **A redirect that drops the query string.** The landing URL 301s to a canonical that strips `?utm_*` — the campaign arrives as "direct / none."
- **A consent or geo gate that reloads to a clean URL** before gtag reads the parameters.
- **A marketing tag firing before the click ID lands**, so the conversion can't be tied back to the click.

Validate by landing ObservePoint on the campaign URL *with the parameters attached* (a Journey whose first step navigates to the full tagged URL) and asserting both that the parameters survive on the final URL and that the analytics hit carries them.

```
WHEN page = "<the tagged landing URL>"
EXPECT
  final URL query contains "utm_source" AND "utm_medium" AND "utm_campaign"
  if "gclid" was on the entry URL, "gclid" is present on the final URL
  the GA4 page_view hit carries the campaign parameters
```

## 7. MCP workflow

When `mcp__ObservePoint__*` tools are loaded, this is the order of operations for an analytics-validation engagement. All are verified in the shared `references/mcp-tools.md`.

**Confirm what fired.**

- `mcp__ObservePoint__get_tag_inventory` — which tags and events fired, on which pages. The starting population for every validation.

**Inspect the values.**

- `mcp__ObservePoint__query_report` on the **`tag-variables`** entity — the ad-hoc query for the actual parameter/variable values across the run. Call `mcp__ObservePoint__get_report_schema` (with `search`) first to discover the column names for the entity before you build the query.
- `mcp__ObservePoint__profile_variable` — profile the values a single tag-variable takes across pages, to surface outliers and unexpected values: the `value` that came through as a string on one template, the `currency` blank on a locale, the `transaction_id` that repeats.

**Find the gaps.**

- `mcp__ObservePoint__get_pages_without_tag` — the pages where an event should fire but doesn't (section 5).

**Assert and read results.**

- `mcp__ObservePoint__create_rule` / `mcp__ObservePoint__update_rule` — author the Tag & Variable Rules. Pair with `mcp__ObservePoint__update_audit_rules` to actually attach the Rule to the audit (or the journey equivalent) — a Rule that exists but isn't attached evaluates nothing.
- `mcp__ObservePoint__analyze_rule_results` — interpret Rule pass/fail across runs, so you can tell a one-run blip from a sustained regression.

If no `mcp__ObservePoint__*` tools are loaded, the user doesn't have MCP access — the same reads come from the UI, and the REST recipes for Rules CRUD and the CI/CD gate live in the `api-strategy` skill plus the shared `references/mcp-tools.md`. Never invent a tool name; only call tools that actually appear.

## 8. Boundaries

This skill proves the data is correct. It defers in three directions:

- **`martech`** — *how the platform is set up*. GA4's event model, Adobe's Web SDK vs AppMeasurement transport, the dataLayer→tag handoff architecture, server-side GTM, the Conversions API ecosystem. martech describes the build; this skill validates the data the build produces. The can't-see line is martech's too: anything server-side (Measurement Protocol, sGTM's server→vendor send, CAPI's server leg) is invisible to ObservePoint — validate the client-side hit and pair with server logs.
- **`tags`** — *what tags exist and whether they belong*. Tag identity, the analytics-vs-advertising-vs-social classification, risk tier, the should-it-be-here judgment. tags says the `purchase` tag belongs on the confirmation page; this skill proves the `purchase` data it sends is sound.
- **`privacy-compliance`** — *consent wiring and regulation*. Whether Reject-All actually suppresses the analytics hit, whether Consent Mode v2 is propagating, whether the banner behaves, and what the law requires. This skill validates the hit's payload; privacy-compliance validates whether the hit should have fired at all under the current consent state.

For the end-to-end recipes — the broken purchase event, events firing twice, validating every release — see the shared `references/solution-playbooks.md` → "Analytics validation — events fire correctly."

*Last verified: 2026-06-04*
