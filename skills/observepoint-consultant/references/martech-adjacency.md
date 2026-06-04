# MarTech adjacency — validating the platforms ObservePoint touches but doesn't own

Load this when the user asks about implementing or validating an adjacent MarTech platform — GA4, Adobe Analytics, a tag manager, a CMP's consent signals, a conversions API, a CDP. ObservePoint touches these but doesn't own them. It is not a GA4 console, an Adobe report suite, or a GTM workspace. The value is the **validation angle**: what ObservePoint can confirm from the browser, and — just as important — what it can't see because the action happens server-side or inside a vendor's backend.

The recurring shape of every section below: how the platform is implemented, the antipatterns ObservePoint reliably catches, an ObservePoint validation approach with at least one `WHEN ... EXPECT ...` Rule, and an explicit **can see / can't see** boundary. The boundary is the part to get right — overselling what ObservePoint observes is how a validation program loses trust.

This is a large reference. A full table of contents follows so it stays navigable as it grows.

## Contents

1. [GA4 implementation patterns](#1-ga4-implementation-patterns)
2. [Adobe Analytics implementation patterns](#2-adobe-analytics-implementation-patterns)
3. [Google Tag Manager (client-side)](#3-google-tag-manager-client-side)
4. [Server-side GTM (sGTM)](#4-server-side-gtm-sgtm)
5. [Adobe Launch / Adobe Tags](#5-adobe-launch--adobe-tags)
6. [Tealium iQ](#6-tealium-iq)
7. [Consent Mode v2 (deep-dive)](#7-consent-mode-v2-deep-dive)
8. [Meta CAPI (Conversions API)](#8-meta-capi-conversions-api)
9. [Conversions API ecosystem](#9-conversions-api-ecosystem)
10. [Customer Data Platforms (CDPs)](#10-customer-data-platforms-cdps)
11. [Attribution and measurement](#11-attribution-and-measurement)
12. [Privacy Sandbox APIs](#12-privacy-sandbox-apis)

> Sections 5-12 are populated in companion updates.

## 1. GA4 implementation patterns

GA4 is event-based: there is no pageview-vs-event distinction the way Universal Analytics drew one. Everything is an event with parameters.

**Implementation patterns.**

- **Event taxonomy.** Three tiers: *automatically collected* events (`page_view`, `session_start`, `first_visit`), *recommended* events with reserved names and expected parameters (`purchase`, `add_to_cart`, `view_item`, `login`, `sign_up`), and *custom* events the implementer names. The recommended events matter most for validation because Google defines the parameter contract — `purchase` is expected to carry `transaction_id`, `value`, `currency`, and an `items` array, and reporting/attribution degrade quietly when those are missing.
- **Parameters and custom dimensions.** Event parameters are only queryable in reports once registered as custom dimensions/metrics (event-scoped or user-scoped). A param that fires correctly on the wire but was never registered is invisible in the GA4 UI — a common "the data is there but I can't see it" confusion.
- **Enhanced measurement.** A set of automatic interaction events (scrolls, outbound clicks, site search, video engagement, file downloads) toggled on at the data-stream level. Convenient, but it fires from GA4's own listeners, so what you see on the wire may not match a hand-built dataLayer event of the same intent.
- **Conversions / key events.** "Conversions" were renamed **key events** in 2024. Marking an event as a key event is a property-side configuration; on the wire it is still just the same event hit. ObservePoint validates that the underlying *event* fires correctly — whether GA4 has it flagged as a key event is a console setting, not something visible in the request.
- **Consent integration.** GA4 respects Consent Mode (see section 7). With consent denied, gtag sends cookieless *pings* rather than full hits — a different request shape, not the absence of a request. Validating "GA4 respects consent" means inspecting the consent parameters on the hit, not just counting hits.
- **Measurement Protocol.** A server-to-server path: your backend POSTs events directly to GA4 with an API secret. This is **not client-visible** — it never touches the browser, so ObservePoint cannot observe it.

**Common antipatterns ObservePoint catches.**

- `purchase` events missing `value`, `currency`, or `transaction_id` — or sending `value` as a string, or firing on cart-view instead of order-confirmation.
- Duplicate `purchase` events from a confirmation page that double-fires on reload (no idempotency on `transaction_id`).
- The wrong `measurement_id` (a staging stream ID shipped to production, or one property's ID leaking onto another brand's pages).
- `page_view` firing twice — once from enhanced measurement and once from a manual GTM tag.
- PII in event parameters (email in a `search_term`, a customer ID in a custom param) — surfaced by `scan_audit_pii` / `scan_journey_pii`.

**ObservePoint validation approach.**

GA4 hits go to `google-analytics.com/g/collect` (or a region endpoint / first-party `/collect` path). The event name rides in the `en` parameter; ecommerce items are encoded in the `pr1`, `pr2`… product parameters; consent flags ride in `gcs` / `gcd`. Use `get_page_requests` or `get_tag_inventory` to confirm the hit fires, then a Tag & Variable Rule to assert the payload. See `references/products-and-modules.md` for how Rules attach to audits and journeys.

```
WHEN tag = "Google Analytics 4" AND event ("en") = "purchase"
EXPECT
  parameter "transaction_id" is present and non-empty
  parameter "currency" matches /^[A-Z]{3}$/
  parameter "value" is numeric AND > 0
  the items array is present (at least one product parameter)
```

Drive it through a real checkout with a Journey so the `purchase` event actually fires, then attach the Rule to the Journey run.

**What ObservePoint can / can't see.**

- **Can see:** the client-side gtag/GTM request to `google-analytics.com/collect` — event name, every parameter, the measurement ID, the consent (`gcs`) flags, ecommerce items. Whether the event fired, on which page/step, and with what payload.
- **Can't see:** **Measurement Protocol** hits sent server-to-server (they never reach the browser); whether an event is flagged as a key event in the GA4 console; how GA4 attributes or models the data after ingestion; BigQuery export contents. Validate the server path with your backend logs and the GA4 DebugView, not ObservePoint.

## 2. Adobe Analytics implementation patterns

Adobe Analytics predates GA4's event model and carries a different vocabulary. Two implementation libraries coexist in the wild: the legacy **AppMeasurement** (`s.t()` / `s.tl()`) and the newer **Web SDK (Alloy)** that sends to the Adobe Experience Platform Edge Network.

**Implementation patterns.**

- **Variables.** *eVars* (conversion variables, persistent — they hold a value across hits until expired), *props* (traffic variables, hit-scoped), and *events* (counters / success metrics like `purchase`, `prodView`). A correct implementation maps each business concept to a stable variable number; the classic failure is drift, where `eVar5` means campaign on one template and search term on another.
- **`s.t()` vs `s.tl()`.** `s.t()` is the page-view call (the `s.pageName` beacon); `s.tl()` is the link/track call for an interaction that should not increment page views (a click, a form submit). Misusing them inflates or deflates page-view counts — firing `s.t()` on a button click is a common inflation bug.
- **AppMeasurement vs Web SDK (Alloy).** AppMeasurement sends the classic image beacon to a data-collection domain (the `b/ss` path). The Web SDK sends an XHR/fetch to the Edge Network at the `/ee` interaction endpoint with an XDM payload — a completely different request shape. An implementation mid-migration often runs **both at once**, double-counting; ObservePoint reliably surfaces that.
- **Adobe Audience Manager (AAM).** Audience segmentation and the `demdex` ID-sync calls. Visible on the wire as requests to `*.demdex.net`; the segment *membership* and downstream activation are not.
- **Processing rules / VISTA / marketing-channel rules** run server-side inside Adobe after the hit lands. They rewrite and enrich the data you sent. ObservePoint sees what the browser sent — not what Adobe's processing turned it into.

**Common antipatterns ObservePoint catches.**

- Both AppMeasurement and Alloy firing on the same page (a half-finished Web SDK migration) — double counting.
- A key event (e.g. order confirmation) that fails to set the expected `events` string or its purchase eVar.
- `s.t()` firing on an interaction that should be an `s.tl()` link call (page-view inflation).
- The wrong report-suite ID (`s.account`) — dev suite IDs shipped to production, or prod and dev suites both receiving the hit.
- eVar drift across templates — the same variable carrying different meanings on different page types (surfaced via `profile_variable`).

**ObservePoint validation approach.**

For AppMeasurement, parse the `b/ss` beacon: the report suite is in the path, `events` / `v`-numbered eVars / `c`-numbered props are query parameters. For the Web SDK, inspect the `/ee` interaction call and the XDM object inside it. Use `get_page_requests` / `get_tag_inventory` to confirm the call, then a Rule on the variable contract.

```
WHEN tag = "Adobe Analytics" AND page URL matches /order\/confirmation/
EXPECT
  the "events" string contains "purchase"
  the purchase eVar (e.g. eVar10 = order ID) is present and non-empty
  the report-suite ID equals the production suite (NOT the dev suite)
```

**What ObservePoint can / can't see.**

- **Can see:** the `b/ss` AppMeasurement beacons and the `/ee` Web SDK (Alloy) network calls — report suite, eVars, props, the `events` string, the XDM payload; the `demdex` ID-sync requests; whether both libraries fire on one page.
- **Can't see:** Adobe's **server-side processing** — processing rules, VISTA, marketing-channel processing, classification imports, segment membership in AAM/RT-CDP. Server-side forwarding (Adobe → downstream destinations) is invisible. Anything that transforms the hit *after* it lands in Adobe is out of view; validate that with Adobe's own debugging tools and the data after processing.

## 3. Google Tag Manager (client-side)

Client-side GTM is the most common tag-deployment layer ObservePoint encounters. Understanding its architecture is what makes ObservePoint findings actionable rather than just "a tag is missing."

**Implementation patterns.**

- **Container architecture.** One container (`GTM-XXXXXXX`) loads the GTM library, which then loads and fires the *tags* configured inside it. The container snippet usually sits high in `<head>`; tags fire based on triggers.
- **The dataLayer contract.** The `dataLayer` is the agreed interface between the website and GTM: the site `push`es structured objects (`dataLayer.push({event: 'purchase', ecommerce: {...}})`), and GTM reads variables out of them. This contract is the single most important thing to get right — most analytics quality problems are dataLayer problems, not tag problems. The relationship between the dataLayer and the ObservePoint Rules that validate it is described in `references/products-and-modules.md`.
- **Variables, triggers, tags.** *Variables* extract values (from the dataLayer, the DOM, cookies, URL). *Triggers* decide when a tag fires (a specific event, a page-path match, a click). *Tags* are the vendor pixels themselves. **Lookup tables** and **regex tables** are variable types that map an input (hostname, page path, environment) to an output (the right measurement ID, the right report suite) — the standard way one container serves multiple environments or brands.
- **Consent.** GTM integrates with Consent Mode and CMP triggers so tags hold until consent (see section 7).

**Common antipatterns ObservePoint catches.**

- **Tags firing on All Pages that shouldn't.** A pixel set to the All Pages trigger when it belongs only on conversion pages — leaking a remarketing or conversion tag site-wide. `get_pages_without_tag` (inverted: which pages have a tag they shouldn't) and `get_tag_inventory` surface this.
- **Race conditions.** The tag fires before the dataLayer push that carries its data, so the tag reads `undefined`. The hit goes out, but with empty parameters — it looks like it's working until you inspect the payload.
- **dataLayer pushed after the tag fires.** The mirror image: the confirmation page pushes ecommerce data late (after `gtm.load`), so the purchase tag fires with no items.
- A **lookup table missing a row** — a new environment or brand hostname falls through to a default (often the wrong) measurement ID.
- **Duplicate containers** — two GTM snippets on one page, each firing the same tags, doubling every hit.

**ObservePoint validation approach.**

ObservePoint loads the page in a real Chromium browser, so it sees exactly what GTM fired and with what values — the same vantage point as the browser's own network tab, but scriptable and scheduled. The most useful pattern is asserting a tag fires **only where intended**.

```
WHEN tag = "Floodlight - Purchase Conversion" fires
EXPECT
  the page URL matches /checkout\/confirmation/
  (i.e. this conversion tag fires on NO other page type — assert it is absent elsewhere)
```

Pair that with the inverse coverage check: `WHEN page URL matches /checkout\/confirmation/ EXPECT the purchase tag fires exactly once`. The two Rules together catch both over-firing (leakage) and under-firing (missing conversions). Use `find_coverage_gaps` for the "should be everywhere but isn't" case and `get_pages_without_tag` for the specific tag-coverage question.

**What ObservePoint can / can't see.**

- **Can see:** every tag GTM fires client-side, on which pages, with what payload; the resulting network requests to each vendor; the dataLayer values *as they ended up in the fired request*; duplicate containers; tags firing on the wrong pages.
- **Can't see:** the **inside of the GTM container** — it does not read your workspace, your trigger logic, your variable definitions, or your version history (those live in the GTM admin API, not the browser). It sees the *effect* of the configuration, not the configuration. It also can't see a tag that never fired at all if no trigger matched — absence of evidence reads as the tag simply not being there, which is why coverage Rules (asserting a tag *should* fire) matter as much as leakage Rules.

## 4. Server-side GTM (sGTM)

Server-side GTM moves tag execution off the browser and onto a server container you host. This is the single most important section to get right on the boundary question, because it is exactly the case where what ObservePoint sees and what actually happens diverge. It must align with the **"Server-side tag execution"** limitation in `references/limitations.md` — ObservePoint cannot run or observe server-side tags.

**Implementation patterns.**

- **Hosting.** The server container runs somewhere you control — **Google Cloud Run** is the canonical host; managed providers like **Stape** and **Addingwell** are common alternatives that simplify first-party domain mapping and cookie handling.
- **The web-container → server-container handoff.** A client-side GTM web container (or gtag) is configured to send its hits not to the vendor directly, but to **your server container's URL** — typically a first-party endpoint like `https://sgtm.example.com/g/collect` or a custom `/collect`-style path. The browser POSTs (or GETs) to that endpoint; the server container then parses the event and fans it out to vendors (GA4, Meta, Floodlight, etc.) **server-to-server**.
- **Why teams do it.** First-party request context, longer-lived first-party cookies, payload control / PII scrubbing before vendor send, and resilience against client-side ad blockers.
- **Consent Mode v2 in the server context.** Consent state still originates in the browser and is carried *into* the request to the server container (the `gcs`/`gcd` parameters travel on the client→server hop). The server container is supposed to honor it when deciding what to forward. ObservePoint can confirm the consent signal *left the browser* correctly; it cannot confirm the server honored it. See section 7 for Consent Mode v2 detail.

**Common antipatterns ObservePoint catches.**

- The client-side hit going **directly to the vendor** when it was supposed to route through the server container (the migration didn't actually move the traffic).
- The client→server POST firing with a **malformed or empty payload** (missing event name, missing consent parameters, missing the ecommerce object).
- The server endpoint **not on a first-party domain** when first-party context was the whole point (the `/collect` call still hits a `*.googleapis`-style or third-party host).
- Consent parameters **stripped before the client→server hop**, so the server has nothing to honor.
- The client-side hit firing **before consent** even though sGTM was supposed to gate it.

**ObservePoint validation approach.**

ObservePoint validates the **client → server hop** — the request the browser makes to your sGTM endpoint. That request is in the browser, so it is fully observable. What happens after (server → vendor) is not.

```
WHEN page URL matches /checkout\/confirmation/
EXPECT
  a request fires to the sGTM endpoint host "sgtm.example.com"
  the request path matches /\/g\/collect|\/collect/
  the payload contains event name "purchase" AND a non-empty transaction_id
  the consent parameters (gcs/gcd) are present on the request
```

Drive it with a Journey through real checkout so the client→server call actually fires, attach the Rule, and confirm the hop. For the server→vendor leg, **pair ObservePoint with your sGTM server logs**: the server container should log every request it processes and every downstream send. ObservePoint validates the browser side; the logs validate the server side; together they cover the full round-trip.

**What ObservePoint can / can't see.**

- **Can see — the client→server hop only:** that the browser sent the request to your sGTM endpoint, the destination host (so you can confirm it's first-party), the path, the full payload, and the consent parameters riding along. Whether that hop fired before or after consent.
- **Can't see — the server execution or any server→vendor send:** ObservePoint does not run server-side tags and does not observe them (per `references/limitations.md`). It cannot tell you whether the server container forwarded to GA4, what it sent to Meta CAPI, whether it scrubbed PII, or whether it honored the consent signal it received. Those are server-side facts. Validate them with your sGTM server logs, the vendors' own debug/event-quality tools, and a backend observability platform (Datadog, New Relic). The honest framing for a customer: **ObservePoint proves the browser did its job and handed off correctly; your server logs prove the server did the rest.**

---

*Last verified: 2026-06-04*
