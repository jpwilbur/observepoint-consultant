# Industry playbook — retail / e-commerce

Load this when the user is in retail or e-commerce, or asks about peak-season tracking readiness, conversion-funnel validation, ad-pixel sprawl, cross-border consent compliance, or wasted ad spend from broken conversion data. This is the first of the per-industry playbooks; the shape here (context → use cases → regulations → vendors → Rule examples → pitfalls → CSM cadence) is the template the other industries follow.

## Industry context

A retail site is a funnel with a shop bolted to the front. The canonical path is homepage → category (PLP) → product (PDP) → cart → checkout → confirmation, with account, search, and wishlist flows hanging off the side. Revenue concentrates almost entirely in the last three steps, so that's where tracking has to be perfect and where it most often isn't.

Business models shape the audit surface:

- **DTC (direct-to-consumer).** One brand, one domain, full control of the stack. The cleanest case — but also the one where a single marketing hire can bolt on a pixel without anyone noticing.
- **Marketplace.** Many sellers, shared checkout, frequently a mix of first-party and seller-injected tags. Tag provenance is the hard problem.
- **Omnichannel.** Web plus app plus in-store, with loyalty and identity stitched across them. The web audit is one slice of a larger measurement story; the consultant's job is to keep that slice honest.

The MarTech tendency in retail is *sprawl*. Retail runs heavier ad-tech than almost any other vertical: multiple retargeting pixels (Meta, Google Ads, TikTok, Pinterest, Criteo), affiliate-network tags, several analytics platforms running in parallel during a migration, and seasonal campaign pixels that arrive in October and never leave. The stack grows by accretion, and nobody owns the cleanup.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **Peak-season readiness (Black Friday / Cyber Monday).** The highest-revenue days of the year are also when the most campaign code ships and the least time exists to test it. Escalate audit cadence to daily on the checkout funnel through November and December, and use `find_anomalies` (metric `tags`) to catch a tag count that jumps or drops between runs — the early signal that a deploy broke or duplicated tracking before the revenue lands.
- **Conversion-funnel validation (cart → checkout → confirmation).** Prove the purchase event fires exactly once on the confirmation page, with a correct numeric value, a valid currency, and a populated items array. A Journey scripted through add-to-cart → checkout → confirmation, with Rules at each step, validates the funnel the way a real shopper traverses it.
- **Ad-pixel sprawl control.** Inventory every retargeting pixel (Meta, Google Ads, TikTok, Pinterest, Criteo, affiliate networks), de-duplicate the ones firing twice, and confirm each is consent-gated. A Web Audit's tag inventory is the baseline; a Rule that asserts the approved-vendor allowlist catches the next unauthorized add.
- **Consent compliance across many jurisdictions.** Retail is cross-border by default — a U.S. brand ships to the EU, a European brand sells into California. Run consent-state audits per region and use `compare_consent_states` to prove Reject-All actually blocks the advertising pixels.
- **Wasted ad-spend reduction.** Broken or absent Consent Mode v2 signals corrupt the conversion data Google Ads optimizes against, so the bidding algorithm spends against bad signal. Validating Consent Mode v2 correctness keeps the conversion feed clean — a measurement-quality win that the marketing team feels directly in cost-per-acquisition.

## Regulations that hit retail hardest

Retail's cross-border footprint and ad-tech density put it squarely in the path of the consent-and-tracking regulations. Do not restate effective dates or enforcement detail here — those live in `references/privacy-and-compliance.md`. The retail-specific angle:

- **GDPR + ePrivacy (EU/UK).** Any retailer that ships to or markets in Europe is in scope. The retargeting pixels that drive retail acquisition are exactly the non-essential trackers ePrivacy requires consent for before they fire. See `references/privacy-and-compliance.md` → GDPR and ePrivacy.
- **CCPA/CPRA and the U.S. state laws.** A national retailer touches residents of every state with a comprehensive law. The "share for cross-context behavioral advertising" definition sweeps in the entire retargeting stack, and GPC honoring is mandatory in most of those states. See the U.S. state matrix in `references/privacy-and-compliance.md`.
- **Consent Mode v2 / IAB TCF.** Not law itself, but the technical contract through which a retailer proves consent to Google and the ad-tech ecosystem. Getting it wrong is both a compliance gap and a measurement-quality problem. See `references/privacy-and-compliance.md` → Google Consent Mode v2 and IAB TCF.
- **VPPA (where the catalog has video).** Product videos and shoppable video on PDPs can pull a retailer into the Video Privacy Protection Act litigation wave when viewing data flows to Meta or TikTok. If the user has video content, route to `references/privacy-litigation-defense.md` → VPPA.

## Common vendor patterns

The typical retail stack, by layer:

- **Commerce platform.** Salesforce Commerce Cloud, Shopify (and Shopify Plus), BigCommerce, or Adobe Commerce (Magento). The platform dictates how the data layer is populated and where checkout lives — Shopify's hosted checkout, for example, constrains what tags can run on the confirmation page.
- **Tag management.** Google Tag Manager or Tealium iQ. Almost everything else loads through here, which makes the container the single highest-leverage governance surface.
- **Analytics.** GA4 as the default, sometimes Adobe Analytics alongside it, and frequently both running during a migration — a prime source of duplicate-event and double-counting problems.
- **CMP.** OneTrust or Cookiebot most often. The CMP is what the consent-state audits exercise; confirm it actually gates the advertising category, not just sets a cookie.
- **Retargeting and acquisition.** Meta Pixel, Google Ads, TikTok Pixel, Pinterest Tag, Criteo, plus affiliate-network tags (Rakuten, Impact, CJ). This is where the sprawl concentrates and where the consent-gating Rules earn their keep.

For the full module-by-module breakdown of how ObservePoint audits each of these, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the relevant URL pattern, or to a Journey step.

The purchase event carries correct, well-formed ecommerce data on the confirmation page:

```
WHEN tag = "Google Analytics 4" AND event = "purchase"
EXPECT
  ecommerce.value is numeric AND > 0
  ecommerce.currency matches /^[A-Z]{3}$/
  ecommerce.items is array AND length >= 1
```

Under Reject-All consent, no advertising-category pixel fires on the checkout or confirmation pages — the highest-stakes pages for a consent leak, since they carry order value and customer identity:

```
WHEN consent state = "Reject All" AND page URL matches /\/checkout|\/order-complete|\/confirmation/
EXPECT
  no tags in category "Advertising" fire
  no advertising request domains receive data (Meta, Google Ads, TikTok, Pinterest, Criteo)
```

A given retargeting pixel fires exactly once on a product page — duplicate firings double-count audience signal and corrupt retargeting pools:

```
WHEN page type = "product detail" (PDP)
EXPECT tag "Meta Pixel" event "ViewContent" fires exactly once
```

Pair the Reject-All Rule with `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to produce the side-by-side evidence of exactly which pixels leak past the opt-out.

## Common pitfalls

The failure modes that recur in retail specifically:

- **Tag bloat under peak load.** The stack that loads fine in July adds 200ms per pixel on a Black Friday page already straining under traffic. Every seasonal pixel is a performance tax on the busiest day. Diff page-load metrics before and after the seasonal additions.
- **Seasonal campaign pixels added without governance.** Marketing bolts on a new partner pixel for a holiday push and never removes it. By spring the container has a dozen orphaned tags nobody can attribute. The approved-vendor allowlist Rule turns each new arrival into an alert instead of a silent add.
- **Cart-abandonment vendors leaking PII.** Email-retargeting and cart-recovery vendors capture the email address at checkout — and sometimes ship it to a third party in plain text or as an inadequately hashed value. Run `scan_audit_pii` on the cart and checkout URLs to catch the leak path; the finding is masked, so it's safe to drop in a ticket.
- **Duplicate-purchase double-counting.** Two analytics platforms during a migration, or a confirmation page that re-fires on refresh, inflate revenue in the reporting. The "fires exactly once" Rule on the confirmation page is the guard.
- **Asymmetric consent enforcement.** The banner correctly blocks tags for an EU visitor but the U.S. state opt-out path does nothing — a common gap when the CMP is configured for GDPR first and the U.S. opt-out is bolted on later. Audit each consent variant separately; do not assume the EU configuration covers the U.S. opt-out.

## CSM cadence

The recommended rhythm for a retail account:

- **Peak season (November–December).** Daily audits on the checkout funnel. This is the window where a broken purchase event costs the most and where the most untested code ships. Run `find_anomalies` after each run to catch tag drift early.
- **Off-peak.** Weekly audits on the full funnel; weekly consent-state audits per region.
- **Pre-deploy gate.** Any change touching checkout runs a targeted audit as a release gate before it ships — see the CI/CD gate recipe in `references/solution-playbooks.md`.
- **Alert routing.** Funnel and purchase-event failures route to the analytics + marketing-ops teams; consent-leak failures route to privacy. During peak season, escalate routing so a checkout failure pages someone the same day rather than waiting for the weekly review.

---

*Last verified: 2026-06-04*
