# Industry playbook — financial services & insurance

Load this when the user is a bank, credit union, brokerage, wealth manager, insurer, or fintech, or asks about protecting nonpublic personal information (NPI) on logged-in account pages, proving a conservative tag posture to an examiner, justifying every vendor in a third-party inventory, or keeping advertising and session-replay code off pages where account balances and application data live. The shape follows the retail playbook (context → use cases → regulations → vendors → Rule examples → pitfalls → CSM cadence), but the governing instinct is the opposite of retail's: where retail fights *sprawl*, financial services fights *leakage* — fewer vendors, each one accounted for, none of them touching NPI.

## Industry context

A financial-services site is two sites wearing one domain. The public side — rate pages, product marketing, branch locators, quote and application forms — behaves like any lead-generation marketing site and carries a normal-to-light MarTech stack. The logged-in side — the account dashboard, balances, transaction history, statements, funds transfer, beneficiary and profile management — is where NPI lives, and it is governed under a different and stricter standard. The hard line in this vertical runs at the login boundary: a tag that is merely a governance smell on the marketing site becomes a regulatory and reputational event the moment it fires on an authenticated account page.

The MarTech tendency here is *restraint*, not accretion. A regulated institution runs far less ad-tech than a retailer: often a single analytics platform, a tightly governed tag manager, a strict CMP, and a deliberately short pixel list — every one of which a marketing or compliance lead can name and justify. The risk is not that the stack grows by accretion; it is that a vendor approved for the marketing site quietly extends across the login boundary, or that a chat / session-replay / call-tracking script captures form-field input on a quote page. The whole audit posture is built to catch that one class of failure early and prove, on demand, that it isn't happening.

This is also the vertical most likely to be examined. Banking regulators, insurance commissioners, and the FTC's Safeguards Rule all expect a financial institution to know every third party that receives customer data and to have controls that demonstrably work. "Prove it" is a recurring, scheduled ask here — not a once-a-year scramble — so the audit history is the artifact that answers it.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **NPI leak prevention on logged-in pages.** The defining use case. Assert that no third-party advertising or analytics tracker fires on authenticated account, balance, transaction, or statement pages, and that no NPI (account number, SSN, balance) leaves those pages to any third party. This requires a Journey with credentials — a Web Audit can't log in and traverse the account area the way a customer does. The worked Journey below is the canonical recipe.
- **Strict consent + low-ad-tech validation.** The institution's posture is "the minimum set of tags, each consent-gated." Run consent-state audits and use `compare_consent_states` to prove that under Reject-All nothing non-essential fires anywhere — and that the short approved list is the *whole* list, with no surprises hiding in it.
- **Regulated-tag scrutiny — every vendor justified.** Unlike retail, where a new pixel is a cleanup chore, here a new vendor is a control question: who approved it, did it pass security review, does it touch NPI? Inventory every tag and request domain, and turn the approved-vendor allowlist into the standing control that flags the next unapproved arrival.
- **Third-party vendor inventory for audits and exams.** Regulators and internal audit want a current, evidence-grade list of every domain that receives data, refreshed on a schedule and diffable over time. The Domains & Geo Privacy Report via `get_request_privacy_report` is that inventory; standing it up early means the answer to an exam request is a saved report, not a fire drill.
- **Fiduciary / disclosure-page integrity.** Rate disclosures, APR/APY tables, fee schedules, fund prospectus links, and regulatory disclaimers are content the institution is legally obligated to present correctly and keep available. Audit these pages for broken links, missing disclosure modules, and unexpected changes so a silently-dropped disclosure surfaces as an alert, not as a finding in an exam.

## Business-model breakout

The four financial-services business models are not minor variations — they change which pages carry NPI, which funnels you script, which vendors you expect, and which regulator is looking. Pin the model down in the first conversation; it sets the whole audit design.

| | **Retail / consumer banking** | **Wealth / brokerage** | **Insurance** | **Fintech** |
|---|---|---|---|---|
| **NPI exposure** | High and broad — account numbers, balances, transactions, SSN at onboarding, across a large logged-in surface. | Highest sensitivity — portfolio holdings, net worth, trade history, beneficiary data. Smaller audience, richer profiles. | Concentrated in the application and claims flows — health, financial, and sometimes driving or property data entered into quote/app forms. | Variable — often a thin, modern logged-in app over a banking or brokerage back-end; NPI exposure depends on what the app actually surfaces. |
| **Key funnel** | Login → account summary → transaction detail → transfer / bill-pay. Account opening is the public-side conversion. | Login → portfolio dashboard → holdings / performance → trade ticket. Onboarding is a long, document-heavy application. | Public **quote flow** (enter PII to get a price) → **application** → bind → logged-in policy/claims servicing. The quote form is the litigation-sensitive page. | Sign-up → KYC / identity verification → funded account → in-app activity. Heavy SPA, fast release cadence. |
| **Primary regulators / regimes** | GLBA + FTC Safeguards Rule; banking regulators (OCC/FDIC/NCUA); U.S. state privacy laws. | GLBA; SEC/FINRA for the brokerage entity; state privacy laws. | GLBA for financial NPI; state insurance commissioners and NAIC model rules; state privacy laws; CIPA/wiretap on quote forms. | GLBA (the institution behind the app); state money-transmitter rules; state privacy laws; partner-bank obligations. |
| **Audit emphasis** | Logged-in NPI Rules + broad consent coverage across a large account surface. | Tightest NPI Rules on the smallest, highest-value surface; portfolio pages get daily scrutiny. | `scan_journey_pii` on the quote/application form (pre- and post-consent) + session-replay/chat scrutiny; disclosure-page integrity on the offer. | SPA-aware Journeys with `Prevent Navigation`; fast cadence to keep up with releases; KYC-step PII scanning. |

For insurance especially, the quote form is the pressure point: it is public (no login to gate it), it collects real PII to return a price, and it frequently carries chat and session-replay vendors — exactly the combination that draws CIPA/wiretap filings. Treat it with the same rigor the others reserve for logged-in pages.

## Regulations that hit financial services hardest

Financial services sits under a sector-specific federal regime *plus* the general state privacy laws *plus* the wiretap litigation wave. Do not restate effective dates or enforcement detail here — those live in the **regulation** skill. The FS-specific angle:

- **GLBA + the FTC Safeguards Rule.** The governing federal regime. GLBA regulates how institutions handle NPI; the revised Safeguards Rule extends to safeguarding NPI from third-party tracking and maintaining a vendor inventory for any third party that receives it. The logged-in-NPI Rules and the vendor-inventory report below are the direct web-surface controls. See the **regulation** skill, GLBA (United States — financial services).
- **The U.S. comprehensive state privacy laws.** A national bank or insurer touches residents of every state with a comprehensive law, and the "sensitive data" and "financial information" categories in those laws raise the bar on the logged-in surface and on quote/application forms. GLBA-regulated data is exempt under several state laws, but the exemption is entity- and data-scoped — not a blanket pass — and the marketing side rarely qualifies. See the U.S. state matrix in the **regulation** skill.
- **CIPA / wiretap on quote and application forms.** Session-replay, chat, and call-tracking vendors on a public quote or application form are prime targets for the pen-register and wiretap class actions — the plaintiff frames a third party capturing keystrokes and entered PII as interception. The quote-form Rule and the pitfalls below are the FS-specific entry point; the statutory theory and the evidence-pack workflow are in the `litigation-defense` skill → CIPA and the session-replay section.

The other privacy regulations (GDPR/ePrivacy for institutions with EU customers, Consent Mode v2 as the technical consent contract) apply where the footprint reaches them, but GLBA, the state laws, and wiretap litigation are the three that define the FS posture. Route to the **regulation** skill for any regulation the institution's geography pulls in.

Beyond privacy, financial services carries affirmative **disclosure obligations** — Truth in Lending (APR), Truth in Savings (APY), fee schedules, fund prospectuses, and the regulatory disclaimers that must accompany an advertised rate or product. These aren't privacy rules, but they're a web-surface compliance obligation a scanner is well-suited to police: a disclosure that silently disappears in a template change, or a stale APR left up after a rate move, is an examinable finding. The disclosure-integrity use case above is where ObservePoint covers this — link audits and content-presence Rules on the disclosure pages, run around every rate-change event.

## Common vendor patterns

The typical FS stack is short and governed, by layer:

- **Tag management.** Tealium iQ is common in enterprise financial services — its consent-and-governance features and per-tag load controls fit the regulated posture, and it's frequently the single highest-leverage control surface. Google Tag Manager appears in fintech and smaller institutions.
- **Analytics.** Adobe Analytics is common in enterprise FS (often alongside Adobe Experience Cloud); GA4 is the default in fintech and on the marketing side. During a migration both run in parallel — the same duplicate-event risk retail has, but with higher stakes if the duplicate lands on a logged-in page.
- **CMP.** OneTrust, configured strictly. The CMP is what the consent-state audits exercise; confirm it actually gates the (short) advertising category and that its reach extends across the login boundary, not just the marketing site.
- **A conservative pixel set.** Where retail runs five-plus retargeting pixels, FS typically runs a deliberately short list — perhaps a single paid-search/conversion pixel and one social pixel, scoped to the marketing site and the top of the application funnel. The governance question is less "how many" and more "is each one staying on the public side."
- **Call-tracking and chat vendors.** Call-tracking (dynamic number insertion — Invoca, CallRail-style) and chat / virtual-assistant widgets are heavily used in FS for advised products and claims. Both are session-replay-adjacent: chat captures typed input and call-tracking scripts rewrite page content and observe behavior. These are the FS-specific session-replay exposure and the reason the quote-form PII scan matters.
- **Server-side tagging and data layer.** Enterprise FS increasingly routes tags through a server-side container to keep the browser surface clean and to interpose a governance layer before data reaches a vendor. That's a genuine privacy improvement, but it also moves the data flow out of sight of a naive client-side scan — the tag still receives the data, it just fires from a first-party collection subdomain. Audit the collection endpoint and the outbound server-to-vendor requests, not just the browser tags, or a server-side leak reads as "clean."

For the full module-by-module breakdown of how ObservePoint audits each of these, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the relevant URL pattern, or to a Journey step.

**1. No third-party advertising or analytics tracker fires on logged-in account pages.** The defining FS Rule — it guards the login boundary.

```
WHEN page URL matches /\/account|\/dashboard|\/balances|\/transactions|\/statements|\/transfer/
EXPECT
  no tags in category "Advertising" fire
  no third-party analytics tag fires (only the approved first-party / server-side analytics endpoint)
  no advertising request domains receive data (Meta, Google Ads, TikTok, LinkedIn, etc.)
```

**2. No NPI leaks to any third party.** Run `scan_audit_pii` (or `scan_journey_pii` on the logged-in steps) with `customRegex` for the institution's account-number and SSN formats so the scan catches NPI leaving a page to a third-party request, cookie, or tag variable.

```
scan_audit_pii(
  auditId=<logged-in audit>,
  customRegex=[
    {name: "SSN", pattern: "\\b\\d{3}-\\d{2}-\\d{4}\\b"},
    {name: "account_number", pattern: "\\b\\d{10,17}\\b"}
  ]
)
EXPECT no match (masked) is sent to any third-party destination domain
```

The numeric patterns above are off by default in the scanner to avoid false positives on analytics IDs — supplying them as `customRegex` is the deliberate opt-in for NPI formats. Findings are masked, so the report drops straight into a ticket or an exam-evidence pack without re-exposing the customer's data.

**3. Only approved vendors receive data.** The standing vendor-inventory control. Pull the Domains & Geo Privacy Report with `get_request_privacy_report` and assert the live request-domain set is a subset of the approved allowlist.

```
WHEN any audit run completes
EXPECT every request domain receiving data is on the approved-vendor allowlist
  (any domain not on the list is an alert, not a silent pass)
```

**4. The quote / application form does not send entered PII to a session-replay or chat vendor before consent.** The insurance/lending litigation-sensitive Rule. Use `scan_journey_pii` on the quote-form step — its canary mode flags any value typed via the journey's `input` / `maskedinput` steps that appears downstream in a third-party request, with zero false positives.

```
WHEN consent state = "default (pre-consent)" AND page = quote/application form
EXPECT
  no value entered into the form appears in a session-replay or chat vendor request
  no session-replay / chat / call-tracking vendor fires before consent
```

**5. Under Reject-All, no non-essential tag fires anywhere.** The institution's posture is that opt-out means opt-out across the whole property — marketing site and logged-in app alike.

```
WHEN consent state = "Reject All"
EXPECT
  no tags in category "Advertising" fire on any page
  no non-essential analytics or session-replay tag fires on any page
```

**6. A newly-appeared vendor on a logged-in page triggers an alert.** The early-warning control for the failure mode that matters most — a vendor silently crossing the login boundary.

```
WHEN find_first_observed reports a request domain first seen on a logged-in URL pattern
EXPECT the domain is on the approved allowlist; otherwise raise an alert
```

**7. The application / account-opening conversion event is well-formed.** Account-opening and policy-bind are the public-side conversions the business measures itself by; a broken or duplicate funnel event corrupts marketing-spend attribution and the product-team's funnel reporting. This is a data-quality Rule, not a consent Rule — and it stays on the public side, where measurement is allowed.

```
WHEN page = application-complete / account-opened / policy-bound confirmation
EXPECT
  the conversion event fires exactly once
  it carries the expected product / line-of-business identifier
  no advertising tag re-fires the conversion on a page refresh
```

Pair Rule 5 with `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to produce the side-by-side evidence of exactly which tags (if any) leak past the opt-out, and pair Rule 6 with `find_first_observed` to date precisely when an unrecognized vendor first appeared so it traces to a specific deploy.

**A note on "logged-in page."** Rules 1, 2, and 6 key off the authenticated account area, but the audit only reaches those pages if it can log in — a Web Audit with a configured login flow, or a Journey with credentials. Target the pages either by URL pattern (`/account/`, `/dashboard/`) when the site's URLs are clean, or by a data-layer value (`page.authState = "loggedin"`) when they aren't. Prefer the data-layer value where it exists; URL patterns drift on re-platform and a Rule keyed to a stale pattern silently stops matching, which reads as a pass. Confirm the page-state signal during discovery before writing these.

## Quote-form and lead-form PII — the FS litigation surface

Where retail's PII-leak flashpoint is the cart-and-checkout email handoff, the financial-services analog is the public **quote and lead form** — the page where a prospect types real PII (name, date of birth, SSN-fragment, income, health or property facts) to get a rate or start an application. It's the most exposed page in the vertical for two reasons at once: it sits *outside* the login wall, so there's no authentication gate limiting who reaches it, and it's exactly where chat widgets, session-replay tools, and call-tracking scripts are most heavily deployed to lift conversion on a high-intent visitor.

This is **both a privacy gap and a litigation exposure.** The same data flow that violates the consent posture is the one plaintiffs frame as a CIPA pen-register / wiretap interception when a third party captures keystrokes and entered identifiers off the form without consent. Financial services and insurance are named among the most-targeted verticals in the 2024–2026 filing wave. See the `litigation-defense` skill → CIPA and the session-replay section for the statutory theory and the evidence-pack workflow.

**How ObservePoint catches it.** Script the quote/application form as a Journey and run `scan_journey_pii` on that step — its canary mode flags any literal typed via the journey's `input` / `maskedinput` steps that turns up downstream in a third-party request, cookie, or POST body, with zero false positives. That's the difference between "a session-replay vendor is present" (which the request inventory shows) and "a session-replay vendor received the SSN the prospect typed" (which the canary proves). Findings are masked, so the result is safe to drop straight into a ticket or an evidence pack. Pair it with `compare_consent_states` to show whether the capture persists under Reject-All, which separates a configuration bug from a consent-enforcement failure.

## Common pitfalls

The failure modes that recur in financial services specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **A marketing pixel accidentally extended to the logged-in app.** *Pitfall:* a tag approved for the public marketing site loads through a shared container or a global template and starts firing on authenticated account pages — the single highest-stakes FS failure. *Catch:* Rule 1 fails the instant an advertising or third-party analytics tag appears on a logged-in URL; `find_first_observed` (Rule 6) dates when it crossed the boundary. *Fix:* scope the tag to the public-side firing rules in the TMS (not a site-wide trigger), and re-audit the logged-in area to confirm it's gone.
- **A chat or session-replay vendor capturing form fields.** *Pitfall:* a chat widget or session-recording script on a quote, application, or login form captures keystrokes — including PII and credentials — and ships them to the vendor, which is both an NPI leak and a CIPA/wiretap exposure. *Catch:* `scan_journey_pii` canary mode (Rule 4) proves a typed value reached a third party; `compare_consent_states` shows whether it persists under Reject-All. *Fix:* mask sensitive fields in the vendor's config (most session-replay tools support field exclusion), gate the vendor behind consent, and re-scan to confirm the value no longer escapes.
- **Call-tracking number-insertion scripts leaking.** *Pitfall:* a dynamic-number-insertion script rewrites the page and observes visitor behavior to attribute calls; on an advised-product or quote page it can sweep up entered data or fire pre-consent. *Catch:* the call-tracking domain shows in `get_request_privacy_report`; `scan_audit_pii` / `scan_journey_pii` catches any entered value reaching it; the consent-state diff shows pre-consent firing. *Fix:* scope the script off PII-bearing forms, gate it behind consent, and confirm with a re-scan.
- **A vendor added without security review.** *Pitfall:* a new tag is deployed for a campaign or a feature and goes live before it passes the institution's third-party-risk review — exactly the gap GLBA's Safeguards Rule vendor-inventory requirement exists to close. *Catch:* the approved-vendor allowlist Rule (Rule 3) turns each new arrival into an alert instead of a silent add; `find_first_observed` dates its first appearance. *Fix:* hold new tags behind the allowlist as the standing control, and route any flagged arrival into the vendor-review process before it stays.
- **Server-side tagging hiding the data flow.** *Pitfall:* tags moved to a server-side container fire from a first-party collection subdomain, so a client-side-only scan sees a clean browser surface while NPI still flows out the back to the vendor — a particular risk when the server-side move is sold internally as the privacy fix. *Catch:* audit the first-party collection endpoint and inspect the outbound server-to-vendor requests, not just the browser tags; a request-domain Rule on the collection subdomain catches what the tag inventory misses. *Fix:* extend the allowlist and consent Rules to cover the server-side endpoint and confirm the consent signal propagates server-side, not just in the browser.

## Peak / event cadence

Financial services has no Black Friday, but it has its own calendar of high-change, high-scrutiny windows. The discipline is the same as retail's — escalate cadence and freeze change around the spike — applied to different events:

- **Tax season (January–April).** Statement, tax-document (1099 / 1098), and document-center pages get a traffic and content surge, and seasonal landing pages ship. Escalate the logged-in document-area audit and watch for new vendors on statement pages.
- **Open enrollment (insurance, roughly October–January for health; varies by line).** Quote and application volume spikes and campaign pixels arrive on the public funnel. Run the quote-form PII scan (Rule 4) daily through the window and freeze the quote-flow container so any new tag is a deliberate exception.
- **Rate-change events.** When the Fed moves or a product reprices, rate, APR/APY, and disclosure pages change fast and under deadline pressure. Run the disclosure-integrity audit around the change so a dropped or stale disclosure surfaces immediately.
- **Earnings / quiet periods (public institutions).** Around earnings and during the quiet period, treat investor-relations and disclosure pages as frozen; an unexpected content or tag change there is worth an alert. Coordinate cadence with the IR and legal teams.

In every case the pattern is: capture a clean baseline before the window, escalate to daily on the affected surface during it, freeze the relevant container, and run `find_anomalies` (metric `tags`) each morning to separate real tag drift from volume noise — anomaly detection is scope-aware, so a traffic spike alone doesn't trip it.

## Worked Journey — the logged-in account flow

The logged-in Rules above are only as good as the path that exercises them, and a Web Audit can only reach authenticated pages by loading their URLs after a one-time login — it never *acts* like a customer moving money or pulling a statement. **Account state, a funds-transfer confirmation, and the events that fire as a result of those gestures only exist after interaction behind authentication — which is why this is a Journey with credentials, not a plain Audit.** (For the full Audit-vs-Journey decision and how login is configured, see `references/products-and-modules.md` → "Audit vs. Journey — when each wins.")

Script a single Journey through the canonical authenticated path and attach Rules step by step:

| Step | Action | Rules that attach | Why here |
|---|---|---|---|
| **1. Login** | Enter credentials via `maskedinput`, submit | CMP banner state captured; no advertising tag fires on the auth page; credentials don't reach any third party (`scan_journey_pii` canary) | The boundary itself — credentials must never leak. |
| **2. Account summary** | Land on the post-login dashboard | Rule 1 — no advertising / third-party analytics tag fires; Rule 2 — no NPI in any outbound request | The most-visited authenticated page; the core NPI surface. |
| **3. Transaction detail** | Open a transaction or statement | Rule 1 + Rule 2 on the detail view; account number and amount stay first-party | Statement/transaction data is high-sensitivity NPI. |
| **4. Funds transfer (or quote)** | Initiate a transfer (test account) — or, for insurance, complete a quote form | Rule 2 — no NPI leaks; Rule 4 — no entered value reaches a session-replay / chat vendor | The action that generates the richest NPI; the litigation-sensitive step for insurance. |

Run the same Journey a second time with the CMP in Reject-All state and attach Rule 5 to every step — that is the consent-leak evidence for the authenticated surface. Use credentials provisioned for a *test* account, never a real customer's, and supply them via `maskedinput` so the value is masked in the run record. For the persona-led version of this recipe (pain → approach → alert routing → success metric), see `references/solution-playbooks.md`.

**SPA caveat.** Many modern banking and fintech apps are single-page apps. Set the `Prevent Navigation` flag on the Journey or the engine treats client-side route changes as reloads and misses the tag firing — see `references/products-and-modules.md` → Journeys.

## Reporting and the exam-evidence artifacts

In financial services the audit history *is* the compliance record — the answer to "prove the controls work" that examiners, internal audit, and litigation counsel all ask on a schedule. Two saved-report artifacts carry most of that value, and both are worth standing up early so the data accumulates before anyone needs it.

**The vendor-inventory exam pack.** Build a saved report with `create_saved_report` over the `network-requests` (or request-domain) data so a current, diffable list of every third party that receives data is always one click away — that is the direct web-surface answer to the Safeguards Rule's vendor-inventory expectation. Use `get_report_schema` (with the `search` parameter) to find the exact column names before building it — don't guess column names. Pair it with `find_first_observed` so each domain carries a "first seen" date, which turns the exam question "when did this vendor start receiving data?" into a lookup instead of an investigation.

**The logged-in NPI evidence pack.** For the authenticated surface, the recurring privacy/security ask is "prove no tracker and no NPI is escaping the account area, every week." Keep the masked `scan_audit_pii` / `scan_journey_pii` findings, the Cookies and Domains & Geo Privacy Reports for the logged-in audit, and the `compare_consent_states` diffs (default vs. opt-out) on file. `query_report` against the rule-summary lets you pull the pass/fail history for Rules 1, 2, and 6 across the period — the record that the login-boundary controls held run-over-run — without re-running anything. Bundled quarterly, that's the "reasonable practices" record counsel wants if a demand letter or an exam arrives.

The point of standing both up early: evidence you didn't collect before the incident can't be back-filled with the same fidelity. In a vertical where the ask is scheduled and adversarial, the accumulated audit history is the deliverable.

## CSM cadence

The recommended rhythm for a financial-services account:

- **Logged-in NPI areas.** Daily audits on the authenticated account / portfolio surface — the cost of an advertising tag or NPI leak landing there is high enough that a weekly cadence is too slow. Run `find_anomalies` after each run to catch a vendor crossing the login boundary early, and keep Rules 1, 2, and 6 live.
- **Public marketing + quote/application funnel.** Weekly audits, escalated to daily through the relevant event window (tax season, open enrollment, a rate change). Run the quote-form PII scan (Rule 4) on every cadence for insurance and lending.
- **Consent-state audits.** Weekly per region, with the `compare_consent_states` diff (default vs. opt-out) kept on file as standing evidence.
- **Vendor inventory.** Refresh the Domains & Geo Privacy Report on a schedule so the exam-ready vendor list is always current and diffable.
- **Alert routing.** NPI-leak and logged-in-vendor failures route to **privacy and security** (the latter because a vendor crossing the login boundary is a third-party-risk question, not just a marketing one); consent and quote-form failures route to **privacy**; analytics-quality failures route to **analytics**. Escalate routing during event windows so a logged-in failure pages a human same-day.

## Discovery checklist

Before designing anything, nail down the five facts that determine the whole audit shape:

1. **Which business model?** Retail banking, wealth/brokerage, insurance, or fintech — this picks the table row above and sets the NPI exposure, the funnel, and the regulator.
2. **What's behind login, and can we get test credentials?** The logged-in NPI surface is the core of the engagement, and reaching it requires a login flow or a Journey with provisioned *test*-account credentials. Confirm both exist before scoping the authenticated work.
3. **Is there a public quote or application form, and what's on it?** For insurance and lending, the quote form's chat / session-replay / call-tracking vendors are the litigation-sensitive surface — identify them early.
4. **What's the approved-vendor list?** The allowlist Rule and the vendor-inventory exam evidence both depend on knowing the sanctioned set; if there isn't a current one, building it from the first audit is the first deliverable.
5. **Which regulators and regions apply?** GLBA always; then the relevant banking/insurance/SEC-FINRA body and the U.S. states (and EU, if applicable) — this drives the consent variants and which regulations in the **regulation** skill are in scope.

The honest scope boundary to set in the same conversation: ObservePoint validates the *web* surface. A native iOS or Android banking app, the core banking or policy-administration back-end, an IVR phone channel, and a human advisor's CRM are out of scope for direct scanning (a HAR captured from the app is the supported workaround for app traffic — see `references/limitations.md`). For a fintech whose product is primarily a mobile app, or an insurer whose claims flow runs through a call center, say this plainly so the customer doesn't expect the web audit to cover the whole NPI story.

---

*Last verified: 2026-06-04*
