# Industry playbook — retail / e-commerce

Load this when the user is in retail or e-commerce, or asks about peak-season tracking readiness, conversion-funnel validation, ad-pixel sprawl, cross-border consent compliance, or wasted ad spend from broken conversion data. This is the first of the per-industry playbooks; the shape here (context → use cases → regulations → vendors → Rule examples → pitfalls → CSM cadence) is the template the other industries follow.

## Industry context

A retail site is a funnel with a shop bolted to the front. The canonical path is homepage → category (PLP) → product (PDP) → cart → checkout → confirmation, with account, search, and wishlist flows hanging off the side. Revenue concentrates almost entirely in the last three steps, so that's where tracking has to be perfect and where it most often isn't.

The MarTech tendency in retail is *sprawl*. Retail runs heavier ad-tech than almost any other vertical: multiple retargeting pixels (Meta, Google Ads, TikTok, Pinterest, Criteo), affiliate-network tags, several analytics platforms running in parallel during a migration, and seasonal campaign pixels that arrive in October and never leave. The stack grows by accretion, and nobody owns the cleanup.

## Business model shapes the audit surface

The three retail business models are not minor variations — they change which pages matter, which vendors you expect to find, and which regulations bite hardest. Pin down the model in the first conversation, because it determines the whole audit design.

| | **DTC (direct-to-consumer)** | **Marketplace** | **Omnichannel / BOPIS** |
|---|---|---|---|
| **Funnel** | One brand, one domain, one checkout. The cleanest funnel to script. | Many sellers feeding a shared cart and checkout; per-seller storefront pages with their own tagging. | Web + app + in-store, with buy-online-pickup-in-store and ship-from-store flows that hand off between channels. |
| **Vendor exposure** | A tight first-party stack — but one marketing hire can bolt on a pixel unnoticed. | First-party tags *plus* third-party seller-injected pixels on product and storefront pages. Tag provenance is the hard problem: a seller's Meta Pixel can fire on your domain without your container ever loading it. | First-party web stack plus the identity / loyalty vendors that stitch a shopper across channels (CDP, loyalty platform, in-store clienteling tools). |
| **Regulatory surface** | Standard consent + retargeting exposure on a single domain. | Third-party seller pixels are the consent nightmare — you are responsible for tags on your domain that you didn't deploy and can't see in your own TMS. | Online↔offline identity stitching is the privacy flashpoint: a loyalty ID that ties a web session to an in-store purchase is exactly the kind of cross-context profile state laws scrutinize. |
| **Audit emphasis** | Funnel correctness + consent gating. A single Journey covers the whole path. | Allowlist Rule per storefront template + `scan_audit_pii` on seller pages. Provenance over completeness. | Per-channel consent variants + Rules that assert the loyalty/identity tag only fires post-consent. The web audit is one slice of a larger measurement story; keep that slice honest. |

For marketplace especially, the approved-vendor allowlist Rule (below) is not a nice-to-have — it is the only practical way to catch a seller-injected pixel, because the tag never appears in your own tag manager for you to review. A useful tactic here: run the allowlist Rule per storefront template and let `find_first_observed` date when an unrecognized request domain first appeared, then trace it to the seller whose page introduced it. That turns "a stranger's pixel is firing on our domain" from an open-ended hunt into a specific seller-offboarding conversation.

## Discovery questions for a retail onboarding

Before designing anything, nail down the five facts that determine the whole audit shape:

1. **Which business model?** DTC, marketplace, or omnichannel — this picks the table row above and sets the vendor and regulatory expectations.
2. **Where's checkout hosted?** A platform-hosted checkout (Shopify, many SaaS carts) limits what tags can run on the confirmation page and changes how you script the Journey's final step.
3. **Which regions do you sell into?** Drives the consent-state variants — EU only, U.S. multi-state, or both — and whether GPC is in scope.
4. **What's the data-layer spec?** GA4 e-commerce, Adobe Data Layer, or a custom schema. The Rules assert against whatever the spec actually is, so get the field names before writing them.
5. **Is there a migration in flight?** GA4↔Adobe dual-tagging or a server-side GTM move is the single biggest source of duplicate-event and blind-spot problems — flag it now.

The honest scope boundary to set in the same conversation: ObservePoint validates the *web* surface. A native iOS or Android shopping app, the in-store POS, and the loyalty back-end are out of scope for direct scanning (a HAR captured from the app is the supported workaround for app traffic — see `references/limitations.md`). For an omnichannel retailer, say this plainly so the customer doesn't expect the web audit to cover the whole identity-stitching story.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **Peak-season readiness (Black Friday / Cyber Monday).** The highest-revenue days of the year are also when the most campaign code ships and the least time exists to test it. Escalate audit cadence to daily on the checkout funnel through November and December, and use `find_anomalies` (metric `tags`) to catch a tag count that jumps or drops between runs — the early signal that a deploy broke or duplicated tracking before the revenue lands. The full cadence is in the peak-season runbook below.
- **Conversion-funnel validation (cart → checkout → confirmation).** Prove the purchase event fires exactly once on the confirmation page, with a correct numeric value, a valid currency, and a populated items array. A Journey scripted through add-to-cart → checkout → confirmation, with Rules at each step, validates the funnel the way a real shopper traverses it. See the worked Journey below.
- **Ad-pixel sprawl control.** Inventory every retargeting pixel (Meta, Google Ads, TikTok, Pinterest, Criteo, affiliate networks), de-duplicate the ones firing twice, and confirm each is consent-gated. A Web Audit's tag inventory is the baseline; a Rule that asserts the approved-vendor allowlist catches the next unauthorized add.
- **Consent compliance across many jurisdictions.** Retail is cross-border by default — a U.S. brand ships to the EU, a European brand sells into California. Run consent-state audits per region and use `compare_consent_states` to prove Reject-All actually blocks the advertising pixels.
- **Wasted ad-spend reduction.** Broken or absent Consent Mode v2 signals corrupt the conversion data Google Ads optimizes against, so the bidding algorithm spends against bad signal. Validating Consent Mode v2 correctness keeps the conversion feed clean — a measurement-quality win that the marketing team feels directly in cost-per-acquisition.

## Regulations that hit retail hardest

Retail's cross-border footprint and ad-tech density put it squarely in the path of the consent-and-tracking regulations. Do not restate effective dates or enforcement detail here — those live in the **regulation** skill. The retail-specific angle:

- **GDPR + ePrivacy (EU/UK).** Any retailer that ships to or markets in Europe is in scope. The retargeting pixels that drive retail acquisition are exactly the non-essential trackers ePrivacy requires consent for before they fire. See the **regulation** skill, GDPR and ePrivacy.
- **CCPA/CPRA and the U.S. state laws.** A national retailer touches residents of every state with a comprehensive law. The "share for cross-context behavioral advertising" definition sweeps in the entire retargeting stack, and GPC honoring is mandatory in most of those states. See the U.S. state matrix in the **regulation** skill.
- **Consent Mode v2 / IAB TCF.** Not law itself, but the technical contract through which a retailer proves consent to Google and the ad-tech ecosystem. Getting it wrong is both a compliance gap and a measurement-quality problem. See the **regulation** skill, Google Consent Mode v2 and IAB TCF.
- **VPPA (where the catalog has video).** Product videos and shoppable video on PDPs can pull a retailer into the Video Privacy Protection Act litigation wave when viewing data flows to Meta or TikTok. If the user has video content, route to the `litigation-defense` skill → VPPA.
- **CIPA and the wiretap theories.** Cart-abandonment, session-replay, and chat vendors on a retail checkout are prime targets for the pen-register and wiretap class actions hitting consumer-facing sites. The cart-abandonment PII subsection below is the retail-specific entry point; the statutory treatment is in the `litigation-defense` skill.

## Common vendor patterns

The typical retail stack, by layer:

- **Commerce platform.** Salesforce Commerce Cloud, Shopify (and Shopify Plus), BigCommerce, or Adobe Commerce (Magento). The platform dictates how the data layer is populated and where checkout lives — Shopify's hosted checkout, for example, constrains what tags can run on the confirmation page.
- **Tag management.** Google Tag Manager or Tealium iQ. Almost everything else loads through here, which makes the container the single highest-leverage governance surface.
- **Analytics.** GA4 as the default, sometimes Adobe Analytics alongside it, and frequently both running during a migration — a prime source of duplicate-event and double-counting problems.
- **CMP.** OneTrust or Cookiebot most often. The CMP is what the consent-state audits exercise; confirm it actually gates the advertising category, not just sets a cookie.
- **Retargeting and acquisition.** Meta Pixel, Google Ads, TikTok Pixel, Pinterest Tag, Criteo, plus affiliate-network tags (Rakuten, Impact, CJ). This is where the sprawl concentrates and where the consent-gating Rules earn their keep.
- **Lifecycle and cart-recovery.** Klaviyo, Bloomreach, Listrak, and similar email/SMS platforms that fire on cart and checkout to power abandonment flows. These see the email address, which makes them the PII-leak watch list (see the cart-abandonment subsection).

For the full module-by-module breakdown of how ObservePoint audits each of these, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the relevant URL pattern, or to a Journey step.

**1. Purchase event is well-formed on the confirmation page.** The single most important Rule in retail — it guards the number the business runs on.

```
WHEN tag = "Google Analytics 4" AND event = "purchase"
EXPECT
  ecommerce.value is numeric AND > 0
  ecommerce.currency matches /^[A-Z]{3}$/
  ecommerce.items is array AND length >= 1
```

**2. No advertising pixel fires under Reject-All on the money pages.** Checkout and confirmation are the highest-stakes pages for a consent leak, since they carry order value and customer identity.

```
WHEN consent state = "Reject All" AND page URL matches /\/checkout|\/order-complete|\/confirmation/
EXPECT
  no tags in category "Advertising" fire
  no advertising request domains receive data (Meta, Google Ads, TikTok, Pinterest, Criteo)
```

**3. Retargeting pixel fires exactly once on a PDP.** Duplicate firings double-count audience signal and corrupt retargeting pools.

```
WHEN page type = "product detail" (PDP)
EXPECT tag "Meta Pixel" event "ViewContent" fires exactly once
```

**4. Search / category event carries the item-list parameters.** A `view_item_list` with an empty or missing `items` array silently breaks merchandising analytics and product-feed-based ad campaigns — the data looks present but conveys nothing.

```
WHEN page type IN ("search results", "category / PLP") AND event = "view_item_list"
EXPECT
  ecommerce.item_list_id is non-empty string
  ecommerce.item_list_name is non-empty string
  ecommerce.items is array AND length >= 1
  each item has item_id AND item_name
```

**5. Add-to-cart fires once with product id and price.** This is the funnel's mid-point conversion signal; a missing or zero price here poisons every downstream value-based bidding strategy.

```
WHEN event = "add_to_cart"
EXPECT
  add_to_cart fires exactly once per click
  ecommerce.items[0].item_id is non-empty
  ecommerce.items[0].price is numeric AND > 0
  ecommerce.value equals items[].price × quantity (summed)
```

**6. Affiliate / attribution click id survives to the landing page.** Affiliate networks pay on the click id (Impact's `irclickid`, Rakuten's `ranMID`/`ranSiteID`, a generic `gclid`/`fbclid`). If a redirect, a consent script, or a canonicalization strips it before the analytics and affiliate tags read it, the partner doesn't get credited and the retailer overpays or underpays. This is a revenue-attribution Rule, not a consent Rule.

```
WHEN landing URL contains affiliate parameter (irclickid | ranSiteID | gclid | fbclid | utm_source)
EXPECT
  the parameter is present in the page URL at load (not stripped by redirect)
  the affiliate / analytics tag request includes the click id value
  the value is non-empty and unchanged from the inbound URL
```

Pair Rule 2 with `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to produce the side-by-side evidence of exactly which pixels leak past the opt-out.

**A note on "page type."** Rules 3 and 4 key off page type (PDP, PLP), but the audit doesn't know a page is a PDP unless something tells it. In practice you target one of two ways: a URL pattern (`/product/`, `/p/`, `/category/`) when the site's URLs are clean, or a data-layer value (`page.type = "pdp"`) when they aren't. Prefer the data-layer value where it exists — URL patterns drift as the site is re-platformed, and a Rule keyed to a stale pattern silently stops matching, which reads as a pass. Confirm the page-type signal during discovery (question 4 above) before writing these.

## Worked example — the conversion-funnel Journey

The funnel Rules above are only as good as the path that exercises them. A Web Audit loads URLs directly; it never adds an item to a cart, so it can't observe the events that fire *as a result of* shopper actions. **Add-to-cart, the cart state, and the purchase event only exist after interaction — which is why this is a Journey, not an Audit.** (For the full Audit-vs-Journey decision, see `references/products-and-modules.md` → "Audit vs. Journey — when each wins.")

Script a single Journey through the canonical path and attach Rules step by step:

| Step | Action | Rules that attach | Why here |
|---|---|---|---|
| **1. Home** | Land on homepage in default (no-consent) state | CMP banner present; no advertising/analytics tag fires pre-consent | Establishes the consent baseline before any shopping starts. |
| **2. Category / PLP** | Click into a category | Rule 4 — `view_item_list` with populated `items` and list id/name | Merchandising and product-feed campaigns depend on this event. |
| **3. PDP** | Open a product | Rule 3 — `Meta Pixel ViewContent` fires exactly once; `view_item` carries `item_id` + `price` | The single most-trafficked event type; duplicate firings here corrupt retargeting pools. |
| **4. Add to cart** | Click add-to-cart | Rule 5 — `add_to_cart` fires once with `item_id` + `price` | The mid-funnel conversion signal value-based bidding feeds on. |
| **5. Checkout** | Proceed to checkout, accept consent | `begin_checkout` fires; cart-recovery vendor receives only post-consent data; no PII in plaintext (see cart-abandonment subsection) | The page where the email address enters the flow — the PII watch point. |
| **6. Confirmation** | Complete the order (test transaction) | Rule 1 — `purchase` well-formed and fires exactly once | The number the business runs on. |

Run the same Journey a second time with the CMP in Reject-All state and attach Rule 2 to steps 5 and 6 — that is the consent-leak evidence for the money pages. For the persona-led version of this recipe (pain → approach → alert routing → success metric), see `references/solution-playbooks.md` → "Validate Consent Mode v2 propagation" and the campaign/landing-page playbooks.

**SPA caveat.** Many modern checkouts are single-page apps. Set the `Prevent Navigation` flag on the Journey or the engine treats client-side route changes as reloads and misses the tag firing — see `references/products-and-modules.md` → Journeys.

## Peak-season runbook — Black Friday / Cyber Monday

Peak is where retail measurement either holds or fails publicly. The discipline is a calendar, not a scramble. Cross-reference the CI/CD release-gate recipe in `references/solution-playbooks.md` for the pre-deploy half of this.

**Weeks before (early-to-mid November):**

- Capture a clean baseline run of the full funnel while traffic is still normal. This is the reference `find_anomalies` will diff against once volume spikes.
- Land every seasonal campaign pixel that's going to ship, then **freeze the tag container.** After the freeze, any new tag is an exception that goes through the allowlist Rule, not a silent add.
- Escalate the checkout-funnel audit to daily; confirm alert routing pages a human same-day, not at the next weekly review.
- Dry-run the rollback: confirm the team can revert the checkout container to the frozen baseline in minutes, and that ObservePoint has the pre-change run saved as the "known good" comparison.

**During (Black Friday through Cyber Monday):**

- Run the daily checkout-funnel audit and review `find_anomalies` (metric `tags`) every morning. Anomaly detection is **scope-aware** — it compares each run against the prior runs *for that same audit scope*, so a traffic spike alone doesn't trip it; a tag count that jumps or drops against the frozen baseline does. That's the signal a deploy broke or duplicated tracking, separated from the noise of higher volume.
- Watch the purchase-event Rule (Rule 1) and the fires-exactly-once guard most closely — a double-firing confirmation page during peak inflates revenue reporting in real time.
- Keep the consent Rules (Rule 2) live. The pressure to ship a last-minute partner pixel is highest now, and an un-gated pixel on the checkout page is both a leak and a litigation exposure.

**Rollback posture for a checkout change during peak.** Treat any checkout deploy during peak as guilty until proven innocent. If the post-deploy audit shows the purchase event degraded — value missing, currency malformed, firing twice, or a new un-gated pixel — revert to the frozen container first and diagnose second. The cost of a few hours on the prior known-good config is trivial against the cost of corrupted revenue data across the highest-traffic days of the year.

**After (December):**

- Diff the peak runs against the pre-freeze baseline to inventory every tag that got added under pressure. Most seasonal pixels are meant to be temporary — this is the moment to remove them before they become next year's orphans.
- Lift the freeze deliberately, not by default.
- Capture a post-peak baseline as the new off-season reference.

## Cart-abandonment and email-retargeting PII

Cart-recovery and email-retargeting vendors (Klaviyo-style flows, plus the retargeting pixels) are the retail-specific PII-leak surface. To power an abandonment email, the vendor has to know *who* abandoned — so the email address is captured at checkout and frequently sent to the vendor's endpoint. The failure mode is sending it in plaintext, or as a weakly/un-hashed value, or before consent.

This is **both a privacy gap and a litigation exposure.** The same data flow that violates the consent posture is the one plaintiffs frame as a CIPA pen-register / wiretap interception when a third party receives identifying signal off the checkout without consent. See the `litigation-defense` skill → CIPA for the statutory theory and the evidence-pack workflow.

**How ObservePoint catches it.** Run `scan_audit_pii` on the cart and checkout URLs (or `scan_journey_pii` on steps 5–6 of the funnel Journey, since the email only enters after interaction). The scan flags an email address — or other PII — leaving the page to a third-party request, and the finding is **masked**, so it's safe to drop straight into a ticket or an evidence pack without re-exposing the customer's data. Pair it with `compare_consent_states` to show whether the leak persists under Reject-All, which is the difference between a configuration bug and a consent-enforcement failure.

## Common pitfalls

The failure modes that recur in retail specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **Tag bloat under peak load.** *Pitfall:* the stack that loads fine in July adds 200ms per pixel on a Black Friday page already straining under traffic — every seasonal pixel is a performance tax on the busiest day. *Catch:* diff the Page Summary load metrics for a run before the seasonal additions against one after, and correlate regressions to the new tags in the request waterfall. *Fix:* defer or remove the non-essential seasonal tags; gate the rest behind the container freeze so additions are deliberate.
- **Seasonal campaign pixels added without governance.** *Pitfall:* marketing bolts on a partner pixel for a holiday push and never removes it; by spring the container has a dozen orphaned tags nobody can attribute. *Catch:* the approved-vendor allowlist Rule turns each new arrival into an alert instead of a silent add; `find_first_observed` dates exactly when an unknown vendor first appeared. *Fix:* the container freeze plus a post-peak teardown pass (see the runbook) removes them on a schedule instead of never.
- **Cart-abandonment vendors leaking PII.** *Pitfall:* email-retargeting and cart-recovery vendors capture the email at checkout and sometimes ship it to a third party in plaintext or as an inadequately hashed value. *Catch:* `scan_audit_pii` on the cart and checkout URLs surfaces the masked leak path. *Fix:* hash before send (or stop sending), and gate the vendor behind consent — verify both with a re-scan and a `compare_consent_states` diff.
- **Duplicate-purchase double-counting.** *Pitfall:* two analytics platforms running during a migration, or a confirmation page that re-fires on refresh, inflate revenue in the reporting. *Catch:* the "fires exactly once" Rule on the confirmation page fails the instant a second firing appears. *Fix:* suppress the duplicate platform's purchase tag, or add an idempotency guard (transaction-id dedupe) so a refresh doesn't re-send.
- **Asymmetric consent enforcement.** *Pitfall:* the banner correctly blocks tags for an EU visitor but the U.S. state opt-out path does nothing — a common gap when the CMP is configured for GDPR first and the U.S. opt-out is bolted on later. *Catch:* audit each consent variant separately and `compare_consent_states` the EU config against the U.S. opt-out; the leaking pixels show up in the diff. *Fix:* map every advertising tag to the U.S. opt-out signal in the CMP, not just the GDPR category; re-audit the opt-out variant to confirm.
- **Server-side GTM migration blind spots.** *Pitfall:* moving tags to a server-side GTM container hides them from a naive client-side scan — the tag still receives the data, but it fires from your own first-party collection subdomain, so it looks "clean" while the data flow is unchanged. *Catch:* audit the first-party collection endpoint and inspect the outbound server-to-vendor requests, not just the browser tags; a request-domain Rule on the collection subdomain catches what the tag inventory misses. *Fix:* extend the allowlist and consent Rules to cover the server-side endpoint, and confirm the consent signal propagates server-side — see `references/martech-adjacency.md` for the full server-side governance treatment.

## Reporting and the evidence artifacts

Two saved-report artifacts carry most of the value for a retail account, and both are worth standing up early so the data accumulates before anyone needs it.

**The peak-season funnel dashboard.** Build a saved report with `create_saved_report` over the checkout-funnel audit, scoped to the funnel Rules (Rules 1–6) so a CSM can see at a glance, per daily run, whether each funnel event passed. Use `get_report_schema` (with the `search` parameter) to find the exact column names before building it — don't guess column names. During peak this is the morning artifact: open the dashboard, confirm the purchase-event and fires-exactly-once rows are green, scan `find_anomalies` for tag drift, done. The trend view turns "is the funnel healthy?" from a half-day investigation into a ten-second glance.

**The cross-border consent evidence pack.** For a retailer selling into the EU and multiple U.S. states, the recurring ask from privacy is "prove the opt-out works everywhere, every week." Run a consent-state audit per region, pull the Cookies Privacy Compliance Report and the Domains & Geo Privacy Report as the evidence artifacts, and keep `compare_consent_states` diffs (default vs. opt-out) per region on file. Bundled quarterly, that's the "reasonable practices" record counsel wants if a demand letter ever arrives — see the evidence-pack workflow in the `litigation-defense` skill. `query_report` against the rule-summary lets you pull the pass/fail history for a named vendor across the period without re-running anything.

The point of standing both up early: evidence you didn't collect before the incident can't be back-filled with the same fidelity. The audit history is the record.

## CSM cadence

The recommended rhythm for a retail account:

- **Peak season (November–December).** Daily audits on the checkout funnel. This is the window where a broken purchase event costs the most and where the most untested code ships. Run `find_anomalies` after each run to catch tag drift early. The full week-by-week sequence is in the peak-season runbook above.
- **Off-peak.** Weekly audits on the full funnel; weekly consent-state audits per region.
- **Pre-deploy gate.** Any change touching checkout runs a targeted audit as a release gate before it ships — see the CI/CD gate recipe in `references/solution-playbooks.md`.
- **Alert routing.** Funnel and purchase-event failures route to the analytics + marketing-ops teams; consent-leak and PII failures route to privacy. During peak season, escalate routing so a checkout failure pages someone the same day rather than waiting for the weekly review.

For the boundaries of what the platform can and can't validate here (native mobile apps, in-store systems), see `references/limitations.md`.

---

*Last verified: 2026-06-04*
