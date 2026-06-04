# Industry playbook — travel & hospitality

Load this when the user is an airline, hotel or lodging brand, online travel agency (OTA) or metasearch site, cruise line, car-rental company, or experiences/tours marketplace — or asks about validating a multi-step booking funnel, honoring consent for a visitor base drawn from many countries at once, keeping loyalty-account PII off ad pixels, governing affiliate and metasearch partner tags, or measuring ancillary-revenue upsells (seats, bags, upgrades, insurance). The shape follows the retail, financial-services, and healthcare playbooks (context → use cases → business-model breakout → regulations → vendors → Rule examples → pitfalls → worked Journey → CSM cadence), but the governing fact is unique to travel: the product *is* a long, fragile booking funnel, and the same booking page serves visitors living under a dozen different privacy regimes simultaneously.

## Industry context

A travel site is a multi-step booking funnel with a marketing site wrapped around it. The canonical path is longer and more brittle than retail's: search (origin/destination, dates, occupancy) → results list → select (a flight, a room, a sailing, a vehicle) → fare or room options (the upsell fork) → passenger or guest details → payment → confirmation. Every step carries state forward — dates, party size, fare class, ancillary selections — and any step that drops a parameter or fails to fire its event silently corrupts the conversion data the whole business runs on. Revenue and the richest PII both concentrate in the back half (details → payment → confirmation), which is exactly where the funnel is most fragile and most often broken by a release.

The visitor base is heavily international by default. A single hotel-brand or airline booking page is hit, in the same hour, by a resident of Germany (GDPR), the UK (UK GDPR), California (CCPA/CPRA), Australia (Privacy Act), and Singapore (PDPA) — all on the identical URL, all expecting their own regime's consent treatment. Travel doesn't get retail's luxury of running one consent posture for a home market and bolting on exceptions; the multi-jurisdiction reality is the default state of every booking page, which makes per-geo consent validation a core obligation rather than an edge case.

The MarTech tendency in travel is *partner sprawl with a consent overlay*. On top of the retargeting pixels retail runs, travel layers metasearch and affiliate exposure: Google Hotel Ads, TripAdvisor, Kayak, Trivago, and Skyscanner feeds; affiliate networks that drive a large share of bookings; and OTA partnerships that can inject tags onto pages the brand's own tag manager never loaded. Loyalty programs add an account surface (member ID, tier, email, points balance) that must stay off the ad-tech entirely. The stack is both wide and internationally exposed, which is the combination that makes governance hard.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **Booking-funnel conversion validation (multi-step, fragile).** The defining use case. Prove the funnel fires the right event at each step — search, results, select, options, details, payment, confirmation — and that the booking-confirmation purchase event fires exactly once with a correct value and currency. The funnel only exists after interaction, so this is a Journey, not a plain Audit. The worked Journey below is the canonical recipe.
- **Multi-jurisdiction consent (one site, many visitor origins).** Travel's signature problem: the same booking page must honor GDPR, UK GDPR, several APAC regimes, and the U.S. state laws at once. Run consent-state audits per geo and use `compare_consent_states` to prove Reject-All actually suppresses the advertising and metasearch pixels for each origin — not just for the home market. The multi-jurisdiction subsection below is the detailed treatment.
- **Loyalty / account PII protection.** The loyalty program is travel's NPI analog — member ID, email, tier, and points balance are exactly the values that must never reach an ad pixel. Run `scan_audit_pii` on the loyalty-login and account pages with `customRegex` for the member-ID format so a leak of an account identifier to a third party surfaces as a masked finding.
- **Affiliate / OTA partner-pixel governance.** Metasearch feeds, affiliate networks, and OTA partnerships introduce tags the brand didn't deploy and can't see in its own container — the same provenance problem retail marketplaces have. The approved-vendor allowlist Rule turns each new partner pixel into an alert, and `find_first_observed` dates exactly when an unrecognized request domain first appeared so it traces to a specific partner.
- **Ancillary-revenue tracking (seat / bag / upgrade / insurance upsells).** Travel makes a large and growing share of revenue on ancillaries — seat selection, checked bags, room upgrades, trip insurance, lounge access. Each upsell is its own conversion event, and a missing or mis-valued ancillary event silently understates revenue and corrupts the value-based bidding the marketing team feeds. Validate that each ancillary add fires once with the correct value and a product identifier.

## Business-model breakout

The travel business models are not minor variations — they change which funnel you script, which partners you expect to find, and which regulatory surface bites hardest. Pin the model down in the first conversation; it sets the whole audit design.

| | **Airline** | **Hotel / lodging** | **OTA / metasearch** | **Cruise / experiences** |
|---|---|---|---|---|
| **Funnel shape** | Search (O&D, dates, pax) → flight results → fare-class select → seat/bag/insurance ancillaries → passenger details → payment → confirmation. Ancillary-heavy and the longest funnel. | Search (location, dates, occupancy) → room results → room-type/rate select → add-ons (breakfast, parking, upgrade) → guest details → payment → confirmation. | Aggregated search across many suppliers → results → handoff (deep-link to supplier *or* on-site book) → details → payment → confirmation. The supplier handoff is the measurement seam. | Long, high-value, consultative funnel — cabin/itinerary select, multi-passenger, deposits and balance payments, excursion add-ons. Experiences are shorter but inventory-fragmented. |
| **Partner exposure** | Metasearch feeds (Google Flights, Kayak, Skyscanner), GDS partners, affiliate networks, co-brand card pixels. | Google Hotel Ads, Trivago, TripAdvisor, OTA channel partners, brand-loyalty CRM. Heavy metasearch reliance. | The widest exposure — supplier pixels, affiliate networks, and ad-tech all at once; *and* the brand injects its own tags onto supplier deep-links. Provenance is hardest here. | Affiliate and agency-partner pixels, excursion-supplier tags; experiences marketplaces carry seller-injected pixels like a retail marketplace. |
| **Regulatory surface** | International by default (global route network); EU + UK + APAC + U.S.-state consent all in play; ancillary upsell data is rich behavioral signal. | Same multi-jurisdiction reality; loyalty/account data is the PII core; in-property and app channels are out of web scope. | Highest consent complexity — partner pixels the brand can't fully see, multiplied across every visitor origin. Allowlist governance is not optional. | Multi-passenger flows collect PII for several travelers at once; deposit/balance payment pages are high-stakes; long sales cycle means remarketing exposure. |
| **Audit emphasis** | Funnel Journey with ancillary Rules + per-geo consent variants + metasearch allowlist. | Funnel Journey + loyalty-PII scan + per-geo consent + Google Hotel Ads / metasearch governance. | Allowlist Rule per supplier/result template + `scan_audit_pii` on handoff pages + per-geo consent. Provenance over completeness. | Multi-passenger PII scan + deposit/payment-page consent + excursion-supplier allowlist. |

For OTA and metasearch especially, the approved-vendor allowlist Rule (below) is not a nice-to-have — it is the only practical way to catch a supplier- or partner-injected pixel, because the tag never appears in the brand's own tag manager for review. Run the allowlist Rule per result/supplier template and let `find_first_observed` date when an unrecognized request domain first appeared, then trace it to the partner whose template introduced it. That turns "a partner's pixel is firing on our domain" from an open-ended hunt into a specific partner-offboarding conversation.

## Regulations that hit travel hardest

Travel's defining regulatory fact is not a single sector law — it is *simultaneity*. A booking page serves visitors under many regimes at once, so several privacy frameworks apply to the same URL on the same day. Do not restate effective dates or enforcement detail here — those live in `references/privacy-and-compliance.md`. The travel-specific angle:

- **GDPR + ePrivacy (EU).** Any travel brand that markets to or sells into Europe is in scope, and travel markets to Europe by definition. The retargeting and metasearch pixels that drive travel acquisition are exactly the non-essential trackers ePrivacy requires consent for before they fire. See `references/privacy-and-compliance.md` → GDPR and ePrivacy.
- **UK GDPR + PECR.** Post-Brexit the UK runs its own regime with the same consent-before-tracking logic; a brand serving UK visitors needs the UK consent variant validated separately, not folded into "EU." See `references/privacy-and-compliance.md` → UK GDPR + DPA 2018 and PECR.
- **The APAC laws (heavy international traffic).** Travel's inbound and outbound APAC volume is large, which pulls in Australia's Privacy Act, Singapore's PDPA, Japan's APPI, South Korea's PIPA, and China's PIPL — the last with real extraterritorial reach for sites processing Chinese-resident data. Each has its own consent and disclosure expectations. See `references/privacy-and-compliance.md` → APAC (Australia, Singapore, Japan, South Korea, China PIPL).
- **CCPA/CPRA and the U.S. state laws.** A travel brand touches residents of every state with a comprehensive law. The "share for cross-context behavioral advertising" definition sweeps in the entire retargeting and metasearch stack, and GPC honoring is mandatory in most of those states. See the U.S. state matrix in `references/privacy-and-compliance.md`.
- **Consent Mode v2 / IAB TCF.** Not law itself, but the technical contract through which a travel brand proves consent to Google and the ad-tech ecosystem across all those jurisdictions at once. Getting it wrong is both a compliance gap and a measurement-quality problem that corrupts the conversion feed the bidding algorithms optimize against. See `references/privacy-and-compliance.md` → Google Consent Mode v2 and IAB TCF.

**The multi-jurisdiction reality, stated plainly.** A single booking page is, at any moment, serving visitors who are owed GDPR treatment, UK treatment, several APAC treatments, and a half-dozen distinct U.S.-state treatments — all from the same HTML, gated by the same CMP. The compliance question is never "does the banner work?" but "does the banner do the *right* thing for *each* origin?" That is why per-geo consent validation (the next subsection) is a core, recurring obligation in travel rather than the once-a-year check it can be in a single-market vertical.

## Common vendor patterns

The typical travel stack, by layer:

- **Booking engine / CRS.** The internet booking engine (airline PSS/Sabre/Amadeus-fed flows, hotel CRS, cruise reservation systems) dictates how the funnel is structured and where the data layer is populated. Booking engines are frequently a separate domain or a heavily-templated embed — confirm the exact funnel domain in discovery so the Journey reaches it.
- **Tag management.** Google Tag Manager or Tealium iQ. Enterprise travel often runs Tealium for its consent-and-governance features; almost everything else loads through the container, which makes it the single highest-leverage governance surface.
- **Analytics.** Adobe Analytics is common in enterprise travel (often within Adobe Experience Cloud), with GA4 alongside it or as the default for digital-native brands and OTAs. During a migration both run in parallel — the same duplicate-event risk retail has, amplified by the funnel's length.
- **CMP.** OneTrust or Cookiebot most often, configured to handle the multi-jurisdiction visitor base. The CMP is what the per-geo consent audits exercise; confirm it actually gates the advertising and metasearch categories for *each* origin, not just the home market.
- **Ad-tech and metasearch.** Meta Pixel, Google Ads, TikTok, plus the travel-specific metasearch pixels — Google Hotel Ads, TripAdvisor, Kayak, Trivago, Skyscanner. This is where the sprawl concentrates and where the consent-gating Rules earn their keep.
- **Affiliate networks.** Travel runs heavy affiliate programs (CJ, Awin, Partnerize, Impact, and travel-specific networks); the affiliate click ID must survive to the landing page for the partner to be credited, which makes it both a revenue-attribution and a governance surface.
- **Loyalty / CRM and payment / fraud.** The loyalty platform and CRM hold the account PII that must stay off ad-tech; payment gateways and fraud/risk vendors (device-fingerprinting, 3-D Secure) sit on the payment step and must be governed without leaking the cardholder or guest data they handle.

For the full module-by-module breakdown of how ObservePoint audits each of these, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the relevant URL pattern, or to a Journey step.

**1. Booking-confirmation purchase event is well-formed and fires exactly once.** The single most important Rule in travel — it guards the number the business runs on, and the funnel's length makes a double-fire or a dropped value especially common.

```
WHEN page = booking confirmation AND event = "purchase"
EXPECT
  purchase fires exactly once
  ecommerce.value is numeric AND > 0
  ecommerce.currency matches /^[A-Z]{3}$/
  ecommerce.items is array AND length >= 1 (the fare/room plus any ancillaries)
```

**2. The conversion pixel fires only at confirmation, not on every funnel step.** A Journey through the full booking funnel asserts the conversion pixel is silent on search, results, select, options, details, and payment, and fires exactly once at confirmation. Premature or per-step firing double-counts bookings and corrupts ROAS.

```
WHEN running the booking-funnel Journey
EXPECT
  the conversion pixel (Meta "Purchase" / Google Ads conversion) does NOT fire on
    search, results, select, options, details, or payment steps
  it fires exactly once on the confirmation step
```

**3. Under Reject-All, affiliate / metasearch / retargeting pixels do not fire.** The consent-leak guard for travel's wide partner stack, across the money pages and the funnel.

```
WHEN consent state = "Reject All"
EXPECT
  no tags in category "Advertising" fire
  no metasearch pixel fires (Google Hotel Ads, TripAdvisor, Kayak, Trivago, Skyscanner)
  no affiliate-network pixel fires
  no retargeting request domains receive data (Meta, Google Ads, TikTok)
```

**4. Loyalty-login and account pages do not leak member ID or email to ad pixels.** The loyalty account is travel's PII core. Run `scan_audit_pii` on the loyalty-login and account URLs with `customRegex` for the member-ID format so a leak of an account identifier to a third party surfaces as a masked finding.

```
scan_audit_pii(
  auditId=<loyalty/account audit>,
  customRegex=[
    {name: "member_id", pattern: "\\b[A-Z]{2}\\d{8,12}\\b"}
  ]
)
EXPECT no match (masked) — and no member email — is sent to any advertising or third-party destination domain
```

The numeric/ID patterns are off by default in the scanner to avoid false positives on analytics IDs — supplying the member-ID format as `customRegex` is the deliberate opt-in. Findings are masked, so the report drops straight into a ticket without re-exposing the member's data.

**5. Currency and locale variants of the same page all fire the conversion correctly.** Travel sells the same room or fare in many markets and currencies; a conversion that is correct on the `en-US`/USD variant but drops the currency or mis-formats the value on `de-DE`/EUR silently corrupts international revenue reporting.

```
WHEN page = booking confirmation across locale/currency variants (/us/, /de/, /jp/, /au/ ...)
EXPECT
  purchase fires exactly once on every variant
  ecommerce.currency is the correct ISO code for that market (USD, EUR, JPY, AUD ...)
  ecommerce.value is numeric AND > 0 in that currency (not a stale or default-locale value)
```

**6. A newly-appeared partner pixel triggers an alert.** The early-warning control for travel's signature failure — a metasearch or affiliate partner's pixel inheriting onto the funnel through a template the brand doesn't own.

```
WHEN find_first_observed reports a request domain first seen on a funnel or result-page URL pattern
EXPECT the domain is on the approved allowlist; otherwise raise an alert
```

**7. Each ancillary upsell fires its own conversion event with a value.** Ancillaries are a large share of travel revenue; a missing or zero-value seat/bag/upgrade/insurance event understates revenue and poisons value-based bidding.

```
WHEN an ancillary is added (seat | bag | upgrade | insurance | excursion)
EXPECT
  the add fires exactly once per selection
  it carries an ancillary product identifier
  ecommerce.value is numeric AND > 0
```

Pair Rule 3 with `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` per geo to produce the side-by-side evidence of exactly which partner pixels leak past the opt-out for each visitor origin, and pair Rule 6 with `find_first_observed` to date precisely when an unrecognized partner first appeared so it traces to a specific template or deploy.

**A note on "page type."** Rules 2, 5, and 7 key off funnel step or page type, but the audit doesn't know a page is the confirmation or the options step unless something tells it. Target either by URL pattern (`/booking/confirmation`, `/select`, `/passengers`) when the funnel's URLs are clean, or by a data-layer value (`page.funnelStep = "confirmation"`) when they aren't. Prefer the data-layer value where it exists — booking-engine URLs drift and re-platform often, and a Rule keyed to a stale pattern silently stops matching, which reads as a pass. Confirm the funnel-step signal during discovery before writing these.

## Multi-jurisdiction consent

The single hardest consent problem in travel is that one booking page serves visitors owed many different regimes at once. The CMP loads the same way for everyone, but the *correct* behavior differs by origin — GDPR and UK demand opt-in before any non-essential tag fires, several APAC laws have their own consent and disclosure shape, and the U.S. states run an opt-out (often GPC-honoring) model. A banner that "works" for the home market routinely does the wrong thing for a visitor from another regime, and nobody notices because the test was run from one location.

**How ObservePoint handles it.** Run a consent-state audit per geo — the platform can run from multiple geographic locations, so the EU variant, the UK variant, the relevant APAC variants, and the U.S.-state opt-out variant each get their own run against the same booking URLs. Then use `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` per geo to produce a side-by-side diff of exactly which pixels fire under each origin's consent treatment. The output is the evidence that Reject-All (or the regime's equivalent) actually suppresses the advertising, metasearch, and affiliate pixels *for that origin* — not just for the market the QA team happens to sit in. Cross-reference the international sections of `references/privacy-and-compliance.md` (GDPR, UK GDPR + PECR, and the APAC laws) for the per-regime expectations each variant must satisfy, and `references/solution-playbooks.md` → "Validate Consent Mode v2 propagation" for the per-geo recipe.

The reason this is a standing obligation, not a one-time check: a single CMP re-configuration, a new metasearch partner, or a re-platform of the booking engine can break the consent treatment for one origin while leaving the others intact — and only a per-geo re-audit catches it. Bundle the per-geo `compare_consent_states` diffs quarterly as the multi-jurisdiction evidence pack.

## Common pitfalls

The failure modes that recur in travel specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **Conversion pixel double-firing across funnel steps, inflating ROAS.** *Pitfall:* the long funnel makes it easy for the conversion pixel to fire on the payment step *and* the confirmation step, or to re-fire when a confirmation page reloads — every spurious fire inflates reported bookings and the ROAS the marketing team optimizes against. *Catch:* Rule 2 (conversion fires only at confirmation) and Rule 1 (fires exactly once) fail the instant a second or premature firing appears in the funnel Journey. *Fix:* scope the conversion tag to the confirmation step only, add a transaction-ID dedupe so a reload doesn't re-send, and re-run the Journey to confirm a single fire.
- **OTA / affiliate partner pixel added without governance.** *Pitfall:* a metasearch or affiliate partnership goes live and the partner's pixel inherits onto the result or funnel pages through a template the brand doesn't own — invisible in the brand's own tag manager, so it's never reviewed. *Catch:* the approved-vendor allowlist Rule (Rule 6) turns each new arrival into an alert; `find_first_observed` dates exactly when the unknown partner domain first appeared. *Fix:* trace the domain to the partner template, decide whether the partnership is sanctioned, and either allowlist it deliberately or have the partner remove it — then re-audit to confirm.
- **Loyalty PII in query strings.** *Pitfall:* the loyalty-login or account flow puts the member ID or email into a URL or query parameter, and analytics dutifully captures the full page URL — sending an account identifier to a third party. *Catch:* `scan_audit_pii` (Rule 4) flags the member ID or email reaching an analytics or advertising domain. *Fix:* move the identifier out of the URL (use a POST body or a server-side lookup), or strip it before the analytics call; re-scan the loyalty pages to confirm.
- **Consent banner tuned for the EU but not honoring U.S. state opt-out.** *Pitfall:* the CMP is configured GDPR-first because Europe was the compliance trigger, and the U.S.-state opt-out (and GPC) path does nothing — a common gap given travel's international focus. *Catch:* run the U.S.-state opt-out variant as its own per-geo audit and `compare_consent_states` it against the EU config; the pixels that leak past the U.S. opt-out show up in the diff. *Fix:* map every advertising, metasearch, and affiliate tag to the U.S. opt-out signal in the CMP, not just the GDPR category, and re-audit the opt-out variant to confirm.
- **Abandoned-booking remarketing leaking PII.** *Pitfall:* the funnel is long, so abandonment is high, and remarketing/cart-recovery vendors capture the traveler's email or trip details to power an abandonment flow — sometimes shipping them to a third party in plaintext or before consent. *Catch:* `scan_journey_pii` on the details and payment steps (where the email and itinerary enter) surfaces the masked leak path; `compare_consent_states` shows whether it persists under Reject-All. *Fix:* hash before send (or stop sending), gate the vendor behind consent, and verify both with a re-scan and a consent-state diff. This is also a CIPA/wiretap exposure — see `references/privacy-litigation-defense.md` → CIPA.

## Worked Journey — the booking funnel

The funnel Rules above are only as good as the path that exercises them. A Web Audit loads URLs directly; it never enters dates, selects a fare, adds a bag, or types passenger details, so it can't observe the events that fire *as a result of* those actions. **The search parameters, the selected fare/room, the ancillary selections, the entered passenger PII, and the purchase event only exist after interaction — which is why this is a Journey, not an Audit.** In travel the Journey isn't a nice-to-have: the funnel *is* the product, so validating it the way a traveler traverses it is the core of the engagement. (For the full Audit-vs-Journey decision, see `references/products-and-modules.md` → "Audit vs. Journey — when each wins.")

Script a single Journey through the canonical booking path and attach Rules step by step:

| Step | Action | Rules that attach | Why here |
|---|---|---|---|
| **1. Search** | Enter origin/destination (or location), dates, occupancy in default (no-consent) state | CMP banner present; no advertising/metasearch tag fires pre-consent; search event carries the search parameters | Establishes the consent baseline before any booking starts. |
| **2. Results** | View the results list | `view_item_list` (or equivalent) fires with populated results; conversion pixel silent (Rule 2) | The merchandising surface; metasearch pixels concentrate here. |
| **3. Select** | Choose a flight / room / sailing / vehicle | `select_item` / `view_item` carries the fare/room id and price; conversion pixel still silent | The choice that sets the booking value. |
| **4. Fare / room options** | Add ancillaries (seat, bag, upgrade, insurance) | Rule 7 — each ancillary add fires once with a value and product id | The upsell fork; a large share of travel revenue. |
| **5. Passenger / guest details** | Enter traveler PII, accept consent | `scan_journey_pii` on the entered email/details; no PII reaches a third party; cart-recovery vendor receives only post-consent data | The page where PII enters the flow — the leak watch point. |
| **6. Payment** | Enter payment (test card), submit | Payment/fraud vendors governed; no cardholder or guest data leaks; conversion pixel still silent (Rule 2) | The highest-stakes page; fraud vendors live here. |
| **7. Confirmation** | Complete the booking (test transaction) | Rule 1 — `purchase` well-formed and fires exactly once; conversion pixel fires exactly here | The number the business runs on. |

Run the same Journey a second time with the CMP in Reject-All state and attach Rule 3 to every step — that is the consent-leak evidence for the funnel. Run it once more from each major visitor-origin geo (EU, UK, an APAC market, a U.S.-state) for the multi-jurisdiction evidence (see the subsection above). Use *test* credentials and a *test* payment method, never a real traveler's, and supply PII via `maskedinput` so the values are masked in the run record. For the persona-led version of this recipe, see `references/solution-playbooks.md` → "Validate Consent Mode v2 propagation" and the campaign/landing-page playbooks.

**SPA caveat.** Many modern booking engines are single-page apps. Set the `Prevent Navigation` flag on the Journey or the engine treats client-side route changes as reloads and misses the tag firing — see `references/products-and-modules.md` → Journeys.

## Peak / event cadence

Travel has no single Black Friday, but it has a calendar of high-booking, high-change windows where campaign code ships onto the funnel under deadline pressure — exactly when a broken funnel event or an un-gated partner pixel is most likely and least likely to be caught. The discipline is the same as retail's — escalate cadence and freeze change around the spike — applied to travel's events:

- **Booking-season surges (wave season for cruise, roughly January–March; summer-travel and holiday-booking windows for airlines and hotels).** Search and booking volume spikes and acquisition pixels arrive on the funnel. Escalate the booking-funnel Journey to daily, freeze the booking-engine container so any new tag is a deliberate exception, and run `find_anomalies` each morning to separate real tag drift from volume noise.
- **Fare sales and flash promotions.** A flash sale ships a campaign landing page and new pixels fast, and the traffic spike lands on a funnel that may have changed hours earlier. Treat the sale launch as a release gate: run the funnel Journey against staging first, then re-run immediately after the page goes live.
- **New-market or new-currency launches.** Opening a new country or currency is the moment the locale/currency conversion Rule (Rule 5) matters most — run it across the new variant before and after launch so a dropped or mis-formatted currency surfaces immediately rather than as a quarter-end reporting gap.

In every case the pattern is: capture a clean baseline before the window, escalate to daily on the funnel during it, freeze the booking-engine container, and keep the consent Rules (Rule 3) live — the pressure to ship a last-minute partner pixel is highest now, and an un-gated metasearch or affiliate pixel on the funnel is both a leak and a litigation exposure.

## Reporting and the evidence artifacts

Two saved-report artifacts carry most of the value for a travel account, and both are worth standing up early so the data accumulates before anyone needs it.

**The booking-funnel health dashboard.** Build a saved report with `create_saved_report` over the booking-funnel Journey, scoped to the funnel Rules (Rules 1, 2, 5, 7) so a CSM can see at a glance, per scheduled run, whether each funnel event passed — the conversion fired exactly once, the value and currency were well-formed, the ancillaries carried their values, and no PII leaked at the details step. Use `get_report_schema` (with the `search` parameter) to find the exact column names before building it — don't guess column names. During a high-booking window this is the morning artifact: open the dashboard, confirm the purchase-event and conversion-fires-once rows are green, scan `find_anomalies` for tag drift, done. The trend view turns "is the funnel healthy?" from a half-day investigation into a ten-second glance.

**The multi-jurisdiction consent evidence pack.** For a brand selling into the EU, the UK, APAC markets, and multiple U.S. states, the recurring ask from privacy is "prove the opt-out works for every origin, every week." Run a consent-state audit per geo, pull the Cookies Privacy Compliance Report (`get_cookie_privacy_report`) and the Domains & Geo Privacy Report (`get_request_privacy_report`) as the evidence artifacts, and keep the `compare_consent_states` diffs (default vs. opt-out) per geo on file. `query_report` against the rule-summary lets you pull the pass/fail history for the consent Rules (Rule 3) across the period and per origin without re-running anything. Bundled quarterly, that's the multi-jurisdiction "reasonable practices" record counsel wants if a demand letter ever arrives — see the litigation-defense evidence-pack workflow in `references/privacy-litigation-defense.md`.

The point of standing both up early: evidence you didn't collect before the incident can't be back-filled with the same fidelity. The audit history is the record.

## CSM cadence

The recommended rhythm for a travel account:

- **Booking funnel.** A scheduled Journey on the full booking funnel, run on a regular cadence (at minimum weekly, daily during high-booking windows) so a broken funnel event surfaces before it costs bookings. Run `find_anomalies` (metric `tags`) after each run to catch tag drift on the funnel pages early — anomaly detection is scope-aware, so a traffic spike alone doesn't trip it.
- **Per-geo consent.** Weekly consent-state audits per major visitor-origin geo (EU, UK, the relevant APAC markets, a U.S.-state opt-out), with the `compare_consent_states` diff (default vs. opt-out) kept on file per geo as standing multi-jurisdiction evidence.
- **Loyalty / account.** Weekly `scan_audit_pii` on the loyalty-login and account surface so an account-PII leak surfaces quickly.
- **Pre-deploy gate.** Any change touching the booking flow runs a targeted Journey or audit as a release gate before it ships — the funnel is fragile enough that a release is the most likely thing to break it. See the CI/CD gate recipe in `references/solution-playbooks.md`.
- **Alert routing.** Funnel, conversion, and ancillary-event failures route to the **analytics and marketing-ops** teams; consent-leak, partner-pixel, and loyalty-PII failures route to **privacy**. Escalate routing during peak-booking windows so a funnel failure pages a human same-day rather than waiting for the weekly review.

## Discovery checklist

Before designing anything, nail down the five facts that determine the whole audit shape:

1. **Which business model?** Airline, hotel/lodging, OTA/metasearch, or cruise/experiences — this picks the table row above and sets the funnel shape, the partner exposure, and the regulatory surface.
2. **Where does the booking engine live, and what's the funnel?** The internet booking engine is often a separate domain or a heavily-templated embed; confirm the exact funnel domain and the step-by-step path so the Journey reaches every step.
3. **Which visitor origins matter most?** Travel is international by default, so identify the top markets (EU, UK, APAC countries, U.S. states) — this drives how many per-geo consent variants the engagement runs.
4. **What's the data-layer spec, and how is funnel step signaled?** Adobe Data Layer, GA4 e-commerce, or a custom schema — the Rules assert against whatever the spec actually is, and the funnel-step signal (URL pattern vs. data-layer value) determines how the step-keyed Rules target.
5. **What are the loyalty and partner surfaces?** Identify the loyalty member-ID format (for the PII scan's `customRegex`) and the metasearch/affiliate/OTA partners that may inject pixels (for the allowlist Rule).

The honest scope boundary to set in the same conversation: ObservePoint validates the *web* surface. A native iOS or Android booking app, the in-property hotel systems, the airport kiosk and IVR channels, and the GDS/CRS reservation back-end are out of scope for direct scanning (a HAR captured from the app is the supported workaround for app traffic — see `references/limitations.md`). For a brand whose bookings increasingly run through a mobile app, say this plainly so the customer doesn't expect the web audit to cover the whole booking story.

---

*Last verified: 2026-06-04*
