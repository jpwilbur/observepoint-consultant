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

> Sections 10-12 are populated in a companion update.

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

## 5. Adobe Launch / Adobe Tags

Adobe Launch (now branded **Adobe Tags**, part of Adobe Experience Platform Data Collection) is Adobe's tag manager — the equivalent layer to GTM for an Adobe-centric stack. It is where Adobe Analytics, Target, Audience Manager, and the Web SDK get deployed.

**Implementation patterns.**

- **Rule architecture: event → condition → action.** A Launch *rule* is the unit of execution. Each rule has an **event** (what triggers it — page bottom, DOM ready, a click, a custom event, a direct-call), optional **conditions** (logic that must pass — a path regex, a data-element value), and **actions** (what it does — set variables, send the Adobe Analytics beacon, fire a custom code block). This is the mental model to validate against: a beacon firing is the *action* of a rule whose *event* matched.
- **Data elements.** Launch's variable abstraction — named references that read from the dataLayer, a DOM attribute, a cookie, a JS variable, or query string. The Adobe analog of a GTM variable. Variable-drift problems usually trace back to a data element reading the wrong source.
- **Extensions.** Pre-packaged integrations installed into the property (the Adobe Analytics extension, the Adobe Experience Platform Web SDK extension, the Google Analytics extension, the Marketing Cloud ID Service / Experience Cloud ID extension). An extension carries its own configuration (report suite IDs, tracking server, the org ID for ECID). An extension misconfigured at the property level breaks every rule that depends on it.
- **Build / publish workflow.** Changes flow through **libraries** promoted across environments: a **Development** library (built to the dev environment embed code), then **Staging**, then **Production**. A library is *built* (compiled to the hosted container files) and then *published*. The critical behavior: a tag added to a **Development** library only — and never promoted — fires on dev/staging embed codes but is **absent in production**. The reverse trap is the **"combine" / library-merge behavior**: when changes from multiple libraries are combined into the production build, a resource present because *another* library carried it can mask the fact that *your* library never included it. The published production container is the only ground truth.
- **Embed codes.** Each environment has its own embed code (script URL). Validating "is the right thing live" means validating against the **production embed code** on the production site — not the dev embed that a staging mirror might still carry.

**Common antipatterns ObservePoint catches.**

- A rule firing on the **wrong event** — e.g. an Analytics beacon wired to "DOM Ready" / library-loaded on every page when it should fire on a specific direct-call or click, inflating page views (the Launch analog of the `s.t()`-on-a-click bug from section 2).
- An **extension misconfiguration** shipped to production — the Adobe Analytics extension pointing at the dev report suite, or the wrong tracking server, so beacons land in the wrong place. Visible on the wire as the wrong report-suite ID.
- A **tag left in the Development library only**, never promoted — works in the QA mirror, silently missing in production. ObservePoint catches it because the production crawl simply never sees the beacon.
- **Combine behavior masking a gap** — the resource appears in QA because a sibling library supplied it; the production build that omits your library quietly drops it.
- A **rule's condition too loose**, so the action fires on page types it shouldn't (leakage), or too tight, so it never fires where it should (coverage gap — use `find_coverage_gaps`).

**ObservePoint validation approach.**

ObservePoint loads the production page against the production embed code and observes the *result* of the rule engine — the beacon that the event→condition→action chain produced. It does not read the Launch property; it reads the network output. Confirm the beacon with `get_page_requests` / `get_tag_inventory`, then assert the payload with a Rule.

```
WHEN tag = "Adobe Analytics" AND page URL matches /products\//
EXPECT
  the Adobe Analytics beacon fires exactly once (the product-view rule's action)
  the "events" string contains "prodView"
  the report-suite ID equals the production suite (NOT the dev suite)
  the product eVar (e.g. eVar2 = product ID) is present and non-empty
```

The "fires exactly once on the right page" framing is what catches a wrong-event rule (over-firing) and a dev-only tag (under-firing) in the same Rule. Pair with `find_first_observed` to answer "when did this beacon first appear?" after a publish, and `find_anomalies` (metric = tags) to catch a publish that suddenly changed the tag count.

**What ObservePoint can / can't see.**

- **Can see:** the resulting network beacons — the Adobe Analytics `b/ss` hit (or the Web SDK `/ee` call) the Launch rule fired, its report suite, eVars, props, the `events` string; which page it fired on; whether it fired once or duplicated; whether the production embed code is live. The *effect* of the rule engine.
- **Can't see:** the **Launch build/publish pipeline itself** — the rule definitions, the event/condition/action logic, the data-element configuration, which library a resource lives in, the combine/merge behavior, the publishing-flow status, version history. Those live in the Data Collection UI / Reactor API, not the browser. ObservePoint sees what got published and fired, not how it was authored or promoted. If a tag is missing, ObservePoint tells you it's absent in production; *why* (stuck in a dev library, a condition that never matched) is a question for the Launch property. Wiring Launch's publish pipeline to trigger an audit follows the same webhook pattern as the Tealium integration — see `references/integrations.md`.

## 6. Tealium iQ

Tealium iQ is an enterprise tag-management system built around a strong, explicit data-layer contract. It is common in large organizations that standardized on Tealium's broader CDP/EventStream suite.

**Implementation patterns.**

- **The Universal Data Layer (UDL / `utag_data`).** Tealium's data-layer object, conventionally `utag_data`, declared before the `utag.js` loader so values are available at load. The UDL is the agreed interface between the site and Tealium — every templated tag reads its inputs from UDL variables (mapped to Tealium "data sources"). As with GTM's dataLayer, most data-quality problems are UDL problems, not tag problems.
- **`utag.js` and the loader.** The Tealium loader (`utag.js`) is the container; `utag.view()` signals a page view and `utag.link()` signals an interaction (the Tealium analog of Adobe's `s.t()` / `s.tl()`). Each fires the load rules and dispatches the qualifying tags.
- **Load rules.** The conditions that decide which tags fire, evaluated against UDL / page values — the Tealium analog of GTM triggers. Scope is the classic failure point: a load rule scoped too broadly fires a tag site-wide; scoped to the wrong variable or value, it fires on the wrong pages or never fires.
- **Extensions.** Tealium's data-transformation layer — JavaScript / pre-built logic that runs at defined scopes (pre-loader, before/after load rules, before/after tags) to set, transform, or enrich UDL values before tags read them. Sequencing matters: an extension that populates a value *after* the tag that needs it has already fired produces an empty parameter.
- **Templated tags.** Vendor tags configured from Tealium's template library, each mapping UDL data sources to the vendor's expected parameters. Validation asserts the templated tag fired with the UDL value it was supposed to read.
- **Publish workflow.** Changes are saved to a Tealium **profile** and **published** to an environment (**dev**, **qa**, **prod**), each with its own `utag.js` URL/environment path. A change saved but not published to prod is not live; a tag enabled only in the dev/qa environment is missing in prod — the same environment-promotion trap as Launch libraries.
- **Tealium → ObservePoint publish trigger (integration).** ObservePoint has a Tealium integration: a **Tealium publish event can trigger an ObservePoint audit**, so the newly published profile is validated *before* real traffic hits it — a release gate on the publish itself. This is a bi-directional webhook integration; see `references/integrations.md` (Tealium iQ) for the wiring and the "block a problematic publish before it propagates" use case. The publish pipeline lives outside ObservePoint, but the publish *event* drives the audit.

**Common antipatterns ObservePoint catches.**

- **UDL populated after `utag` loads** — `utag_data` (or a `utag.view()` data object) set late, so the loader and its tags read `undefined`. The hits fire with empty parameters; it looks like it works until you inspect the payload (the Tealium analog of the GTM race condition in section 3).
- **Load-rule scoping errors** — a tag firing site-wide that should be page-scoped (leakage), or scoped to a UDL value that's misspelled / wrong so it never qualifies (coverage gap).
- **An extension sequencing bug** — a transform that runs after the tag it feeds, leaving the parameter empty.
- A tag **published to dev/qa only**, missing in prod — caught because the prod crawl never sees it.
- The **wrong profile/environment `utag.js`** loaded on a page (a qa loader left on a production template).

**ObservePoint validation approach.**

ObservePoint loads the production page with the production `utag.js` and observes the tags `utag` dispatched and the requests they made. Confirm with `get_page_requests` / `get_tag_inventory`, then assert that a templated tag carried the UDL value it should have read. Use `profile_variable` to check a UDL-sourced parameter's values across pages for drift.

```
WHEN tag = "Tealium-managed Google Analytics 4" AND event ("en") = "purchase"
EXPECT
  the templated tag fires (utag dispatched it)
  parameter "transaction_id" is present and non-empty (read from the UDL order_id data source)
  parameter "value" is numeric AND > 0
  parameter "currency" matches /^[A-Z]{3}$/
```

Drive it with a Journey through real checkout so `utag.view()`/`utag.link()` fire with a populated UDL, attach the Rule to the Journey run. For the publish-gate pattern, let the Tealium publish event trigger the audit (per the integration above) and attach the Rules to that audit so a bad publish is caught before propagation.

**What ObservePoint can / can't see.**

- **Can see:** the `utag.js`-driven network calls — every templated tag `utag` dispatched, its destination, its parameters, and the UDL-sourced values *as they ended up in the fired request*; which environment loader is live; duplicate loaders; tags firing on the wrong pages.
- **Can't see:** the **inside of the Tealium profile** — the UDL-to-data-source mappings, load-rule logic, extension code and scope/sequencing, templated-tag configuration, profile version history. Those live in the Tealium iQ UI / management API, not the browser. ObservePoint sees the *effect*: it can tell you a parameter arrived empty, but whether the cause was a late UDL push, an extension sequencing bug, or a bad data-source mapping is a question for the profile. The **publish pipeline is external** — but, uniquely among the tag managers here, the publish *event can trigger* the ObservePoint audit, so validation runs at exactly the right moment.

## 7. Consent Mode v2 (deep-dive)

This is the deepest section, because Consent Mode v2 is where a privacy program most often *thinks* it's compliant while the wire says otherwise — and the wire is exactly what ObservePoint reads. Cross-reference the **Google Consent Mode v2** entry in `references/privacy-and-compliance.md`; this section is the implementation-and-validation companion to that regulatory summary.

**Implementation patterns.**

- **The CMP → Google tag wiring.** A consent management platform (OneTrust, Cookiebot, Usercentrics, a custom banner) is the source of consent state. It calls `gtag('consent', 'default', {...})` *before* any Google tag loads, then `gtag('consent', 'update', {...})` when the user interacts with the banner. Google tags (gtag.js, GA4, Google Ads, Floodlight) read this consent state and adjust their behavior. The wiring is the thing that breaks: a CMP that fires `update` too late, or never sets a `default`, leaves Google tags running in an unintended state.
- **The four signals.** Consent Mode v2 carries four consent types:
  - **`ad_storage`** — cookies/identifiers for advertising.
  - **`analytics_storage`** — cookies/identifiers for analytics.
  - **`ad_user_data`** — whether user data may be *sent* to Google for advertising (added in v2).
  - **`ad_personalization`** — whether data may be used for ad personalization / remarketing (added in v2).
  The two `ad_user_data` / `ad_personalization` signals are what make it "v2" and are mandatory for Google advertising features in the EEA.
- **Default vs updated consent.** **Default** consent is the state *before* the user chooses (set by the CMP's `default` call — for EEA users this should be `denied` for the ad/analytics signals). **Updated** consent reflects the user's actual choice (`gtag('consent','update',...)`). A correct implementation always sets a default *before* tags load, then updates on interaction. The most common bug is a missing or late default, so tags fire under the wrong assumption.
- **The no-cookie "ping" / cookieless pings under denied.** When a relevant signal is `denied`, Google tags don't go silent — they send **cookieless pings**: lightweight requests that set no identifiers and carry no cookies, used for conversion modeling and basic measurement. So "consent is respected" does **not** mean "no request fires" — it means the request that fires is the *cookieless ping* shape, with the consent flags signaling denial, rather than a full identified hit. Counting requests is the wrong test; inspecting the consent parameters and the request shape is the right one.
- **Advanced vs basic implementation.** In **advanced** mode, the Google tags load *unconditionally* and self-adjust based on consent — under denied they fire cookieless pings (giving Google modeling data). In **basic** mode, the tags are *blocked entirely* until consent is granted (often via the CMP gating the tag load), so under denied **nothing fires at all**. This materially changes what ObservePoint should expect on the wire: advanced → expect a cookieless ping under Reject-All; basic → expect no Google request at all under Reject-All. Know which mode the customer implemented before writing the Rule.
- **`ads_data_redaction`.** A related setting: when `true` and `ad_storage` is denied, Google Ads / Floodlight tags redact ad-click identifiers (e.g. `gclid`) and route through cookieless pings, further stripping identifying data from the denied-state request.
- **On the wire.** Consent state rides on the Google request in the **`gcs`** parameter (a string like `G100` / `G111` encoding the granted/denied bits) and the **`gcd`** parameter (the v2 "consent default" descriptor that also encodes the `ad_user_data` / `ad_personalization` state). These are the parameters to assert against.

**Common antipatterns ObservePoint catches.**

- **No default set before tags load** — the CMP only ever calls `update`, so for the pre-interaction window tags ran under Google's implicit assumption rather than a `denied` default.
- **`update` fires too late** — tags fire a full identified hit *before* the consent update lands, leaking an identified request under what should have been denied.
- **Wrong signals on Reject-All** — the user rejected, but the `gcs`/`gcd` parameters still encode `granted` (the CMP-to-gtag wiring is broken).
- **A full hit instead of a cookieless ping under denied** (advanced mode) — the tag ignored consent and sent identifiers.
- **A request firing at all under denied** when the customer believes they run **basic** mode (the tag wasn't actually gated).
- **Missing the v2 signals entirely** — `ad_user_data` / `ad_personalization` never set, so the implementation is still Consent Mode v1 and non-compliant for EEA Google advertising.

**ObservePoint validation approach.**

ObservePoint runs the site in a real browser under a chosen consent state — drive the CMP via a pre-audit `privacyoptout` action (or a Journey that clicks Reject-All) — and reads the consent parameters on the resulting client-side Google requests. The strongest pattern is **two audits, Accept-All and Reject-All**, compared with `compare_consent_states`. Two illustrative Rules:

```
# Rule 1 — under Reject-All, ad_storage is denied in the Google tag request
WHEN page is crawled under the Reject-All (opt-out) consent state
  AND a request fires to "google-analytics.com" OR "googleadservices.com" OR "google.com/pagead"
EXPECT
  the "gcs" parameter encodes ad_storage = denied (e.g. value "G100" — leading-bits denied)
  the "gcd" parameter is present (the v2 consent descriptor, carrying ad_user_data / ad_personalization)
```

```
# Rule 2 — under Reject-All (advanced mode), the tag sends the cookieless ping, not a full hit
WHEN page is crawled under the Reject-All (opt-out) consent state
  AND tag = "Google Analytics 4" fires
EXPECT
  the request is the cookieless ping shape — no analytics cookie (e.g. _ga / _ga_* ) is set or sent on it
  the consent parameters signal denial (gcs ad_storage/analytics_storage = denied)
  (NOT a full identified hit carrying the client_id from a persistent cookie)
```

Run both consent states, then `compare_consent_states(domain, leftState="default", rightState="opt-out")` to surface any tag that fires identified on Accept-All but should be cookieless/absent on Reject-All. Use `get_cookie_privacy_report` to confirm which Google tags set cookies under each state, and `scan_audit_pii` if you suspect an identified value leaks under denial. For basic mode, invert Rule 2 to expect *no* Google request at all under Reject-All. See `references/privacy-and-compliance.md` (Google Consent Mode v2) and `references/solution-playbooks.md` for the end-to-end consent-validation workflow.

**What ObservePoint can / can't see.**

- **Can see:** the **consent parameters on the client-side Google request** via the request log — the `gcs` / `gcd` values, whether the request is a full identified hit or a cookieless ping, which cookies were set under each consent state, and (via two audits) the *difference* between Accept-All and Reject-All behavior. It sees that the browser sent the right (or wrong) consent signal. Pair it with `compare_consent_states` across consent variants for the authoritative diff.
- **Can't see:** what **Google does server-side** with the consent signal — conversion modeling, how denied-state pings are used, whether modeled conversions appear in Google Ads. It also can't read the CMP's internal configuration or its consent-record database; it observes the *output* (the `gtag consent` calls' effect on requests), not the CMP's stored decisions. And per section 4, if Google tags route through **server-side GTM**, ObservePoint validates that the consent parameters left the browser correctly on the client→server hop but cannot confirm the server honored them. Validate the server side with Google's Tag Assistant / DebugView and your sGTM logs.

## 8. Meta CAPI (Conversions API)

Meta's Conversions API (CAPI) sends conversion events to Meta **server-to-server**, alongside (or instead of) the browser-side Meta Pixel. It exists because the browser pixel is increasingly lossy.

**Implementation patterns.**

- **Why CAPI exists — browser-pixel loss.** Ad blockers, ITP/ETP cookie restrictions, browser tracking-prevention, and consent gating drop a growing share of client-side Meta Pixel events. CAPI recovers them by sending from the server, where the browser's restrictions don't apply.
- **The browser-pixel + CAPI dedup model.** The recommended Meta architecture is **both**: the browser Pixel *and* the server CAPI send the same conversion. Meta then **deduplicates** so the event isn't double-counted. Deduplication keys on:
  - **`event_id`** — the primary dedup key. The *same* `event_id` must be generated for the conversion and sent on **both** the browser Pixel event and the CAPI event, so Meta recognizes them as one. (The Pixel field is `eventID`; the CAPI field is `event_id`.)
  - **`fbp`** (the `_fbp` first-party cookie) and **`fbc`** (the click ID from `fbclid`, stored in `_fbc`) — supporting matching/identity signals that also help Meta tie the browser and server events together.
- **Event Match Quality.** CAPI sends hashed customer information (email, phone, etc., SHA-256 hashed) to improve matching. The hashing happens server-side; what's relevant client-side is whether the identifiers and the `event_id` exist to dedup against.

**Common antipatterns ObservePoint catches.**

- **A missing dedup key causing double-count** — the browser Pixel fires *without* an `eventID` (or with one that doesn't match the CAPI `event_id`), so Meta counts the browser event and the server event as two conversions. ObservePoint catches the **client-side** half: the Pixel fired without an `event_id`.
- **CAPI-only events with no client signal to validate** — a conversion sent purely server-side with no corresponding browser Pixel event. There is nothing on the wire for ObservePoint to see; the gap itself (an expected Pixel event that never fires client-side) is the finding, but the server send can't be confirmed from the browser.
- The Pixel firing with the wrong **pixel ID**, or `_fbp` / `_fbc` absent so identity matching degrades.
- Duplicate browser Pixel `PageView` / conversion events (a double-implemented pixel), inflating the client side before dedup even enters the picture.

**ObservePoint validation approach.**

ObservePoint validates the **client-side Meta Pixel** and, critically, the **presence of the `event_id` dedup key** on it — the one thing that makes server-side dedup possible. Meta Pixel hits go to `facebook.com/tr`. Confirm with `get_page_requests` / `get_tag_inventory`, then assert the dedup key.

```
WHEN tag = "Meta Pixel" AND parameter "ev" = "Purchase"
EXPECT
  the request fires to "facebook.com/tr"
  parameter "eventID" (the event_id dedup key) is present and non-empty
  the pixel ID ("id") equals the production pixel ID
  parameter "cd[value]" is numeric AND > 0 AND "cd[currency]" matches /^[A-Z]{3}$/
```

Drive a real purchase with a Journey so the `Purchase` event fires, attach the Rule. The point of the Rule is the **`eventID` assertion** — if it's present and matches the value the server sends, dedup works; if it's missing, you've found the double-count root cause on the client side. For the server leg, pair with Meta's **Events Manager** (its event-deduplication and Event Match Quality views).

**What ObservePoint can / can't see.**

- **Can see:** the **client-side Meta Pixel** request to `facebook.com/tr` — the event name (`ev`), the pixel ID, the conversion parameters, the `_fbp` / `_fbc` cookies, and the **`eventID` dedup key**. Whether the browser half of the dedup pair is correctly formed. Duplicate client-side pixel firings.
- **Can't see:** the **server-side CAPI send** — it goes server-to-server from the customer's backend to Meta and never touches the browser, so it is invisible to ObservePoint (consistent with the server-side-execution limitation in `references/limitations.md`). ObservePoint cannot confirm the CAPI event fired, what it contained, the hashed customer data, or whether Meta actually deduplicated the pair. The honest framing: **ObservePoint validates the client signal and the dedup parameter; confirm the server send and the realized deduplication in Meta's Events Manager.**

## 9. Conversions API ecosystem

Meta popularized the pattern, but every major ad platform now offers a server-side conversions API with the same browser-pixel + server-send dedup model. The validation posture is identical across all of them: **ObservePoint validates the client-side trigger and the identifier/dedup parameter it sets; the server send is invisible.** This section maps the pattern per vendor so a consultant can recognize each one on the wire.

**The shared pattern.** A client-side tag fires and sets an identifier — a generated event ID, a click ID, and/or a hashed customer identifier — that the parallel server send will dedup or match against. The server call (backend → vendor) is out of view. ObservePoint's job everywhere is the same: confirm the client tag fired and carried the right dedup/identifier parameter.

**Per-vendor map.**

- **Google Enhanced Conversions (web / for leads).** Augments a standard Google Ads conversion with **hashed first-party data** (email/phone, SHA-256) captured client-side and sent with the conversion, so Google can match to logged-in Google users when the cookie/`gclid` path fails. *Client-visible:* the Google Ads conversion tag / gtag conversion event, the `gclid`/`wbraid`/`gbraid` click IDs, and (in the client-collected variant) the presence of the hashed-identifier fields before send. *Server-only:* Enhanced Conversions **for leads** uploaded from a CRM, and any backend-sent variant. *Dedup/identifier:* the click ID (`gclid`) plus hashed email/phone as the match key.
- **TikTok Events API.** The server-side twin of the TikTok Pixel. *Client-visible:* the TikTok Pixel event and its **`event_id`** dedup key, plus the **`ttclid`** click ID and the `_ttp` cookie. *Server-only:* the Events API send from the backend. *Dedup/identifier:* matching `event_id` on the Pixel event and the Events API event (same model as Meta).
- **Pinterest Conversions API.** Server-side twin of the Pinterest Tag. *Client-visible:* the Pinterest Tag event and its **`event_id`**, plus the **`epik`** click ID. *Server-only:* the Conversions API send. *Dedup/identifier:* shared `event_id` across the tag event and the API event.
- **LinkedIn CAPI (Conversions API).** Server-side conversions for LinkedIn campaigns. *Client-visible:* the LinkedIn Insight Tag and its conversion events, plus the **`li_fat_id`** click identifier. *Server-only:* the Conversions API send (often CRM/offline-driven). *Dedup/identifier:* an event identifier plus hashed contact data as the match key.

**Common antipatterns ObservePoint catches.**

- A client tag firing **without the `event_id` / dedup key** the server send needs (the cross-vendor version of the Meta double-count bug) — caught on the client side.
- The **wrong account/tag/pixel ID** for the vendor shipped to production.
- The click-ID parameter (`ttclid`, `epik`, `gclid`, `li_fat_id`) **absent** when first-party-context matching was the whole point.
- A **server-only conversion** with no client tag at all — visible only as the *absence* of an expected client event; the server send itself can't be confirmed from the browser.

**ObservePoint validation approach.**

Pick the vendor, confirm the client tag fires with `get_page_requests` / `get_tag_inventory`, then assert the dedup/identifier parameter the server will match against. Generic shape (TikTok shown):

```
WHEN tag = "TikTok Pixel" AND parameter (event) = "CompletePayment"
EXPECT
  parameter "event_id" is present and non-empty (the dedup key the Events API will match)
  the click identifier ("ttclid" / "_ttp") is present when available
  the pixel ID equals the production pixel ID
```

Swap the tag and identifier names for Pinterest (`event_id` + `epik`), Google Enhanced Conversions (`gclid` + hashed-identifier fields), or LinkedIn (event ID + `li_fat_id`). Drive a real conversion with a Journey so the client event fires, attach the Rule. As with Meta, confirm the server send and the realized deduplication in each vendor's own events/diagnostics console.

**What ObservePoint can / can't see.**

- **Can see:** the **client-side trigger and its parameters** for each vendor — the pixel/tag event, the `event_id`/event-identifier dedup key, the click IDs (`ttclid`, `epik`, `gclid`/`wbraid`/`gbraid`, `li_fat_id`), the account/pixel ID, and (where collected client-side) the presence of hashed-identifier fields before send. Whether the browser half of the dedup pair is correctly formed.
- **Can't see:** the **server-to-server sends** — every vendor's Conversions/Events API call originates from the customer's backend and never reaches the browser, so it is invisible to ObservePoint (per the server-side-execution limitation in `references/limitations.md`). It cannot confirm the server event fired, its contents, the hashed customer data, or whether the vendor deduplicated the pair. Validate the client trigger + dedup parameter with ObservePoint; confirm the server leg in each vendor's events manager / diagnostics.

---

*Last verified: 2026-06-04*
