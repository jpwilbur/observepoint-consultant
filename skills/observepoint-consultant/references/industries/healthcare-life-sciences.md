# Industry playbook — healthcare & life sciences

Load this when the user is a hospital or health system, a payer or health insurer, a pharma or life-sciences company, a telehealth or digital-health platform, or any health-tech vendor — or asks about keeping advertising pixels off patient-facing pages, building litigation-defense evidence against a Meta Pixel or Google Analytics claim, proving consent suppression works on a patient portal (not just the marketing site), complying with Washington's My Health My Data Act, or producing a third-party vendor inventory for OCR or outside counsel. This is the highest-litigation vertical the skill covers, so it gets the deepest treatment. The shape follows the financial-services and retail playbooks (context → use cases → business-model breakout → regulations → vendors → Rule examples → pitfalls → worked Journey → CSM cadence), but the governing fact is unique to healthcare: on a patient-facing page, a URL paired with an IP address can itself constitute Protected Health Information (PHI), so a tag that merely tracks a page view is the violation.

## Industry context

A healthcare site is two surfaces with very different exposure. The public side — service-line marketing, condition and symptom information, a find-a-doctor directory, location pages, bill-pay landing pages — reads like a content-heavy lead-generation site and carries the MarTech you'd expect there. The patient-facing side — appointment booking, the prescription / refill flow, the logged-in patient portal, condition and symptom-checker pages — is where the litigation lives, because the OCR position is that a visit to one of these pages, paired with the visitor's IP address, is PHI even when no name is ever entered.

That reframes the whole audit posture. In retail a stray pixel is a governance smell; in financial services it's a regulatory event on the login boundary. In healthcare the line is drawn earlier and lower: an advertising or analytics pixel firing on a patient-facing URL — *before* any login, on a page that merely describes a condition or lets a visitor search for an oncologist — is the precise fact pattern in hundreds of class actions. The patient portal raises the stakes further (it has authenticated PHI behind it), but the public condition and appointment pages are where most of the filed cases actually start.

The vendors that cause the trouble are ordinary marketing tools used in an extraordinary context. Meta Pixel, Google Ads, and analytics platforms configured to capture page URLs are deployed across healthcare marketing sites the same way they are everywhere else — and then the same global container or template silently extends them onto the appointment, prescription, and portal pages where the page URL is PHI. The defining failure mode is not sprawl (retail) or login-boundary leakage (financial services); it is an everyday marketing pixel inheriting onto a page where its normal behavior becomes a reportable disclosure.

This is also the vertical where the consequence is most concrete. OCR has issued substantial settlements over tracking technologies, and the private-litigation wave has produced hundreds of class actions and multi-million-dollar settlements against hospital systems, telehealth platforms, and pharmacy chains since 2023. "Prove what fired on which patient-facing page, and when" is therefore not a hypothetical — it is the question a demand letter or an OCR inquiry actually asks, and the audit history is the artifact that answers it. The whole posture below is built to make that answer a saved report rather than a forensic reconstruction.

The patient-facing URL patterns where PHI tends to live are worth naming up front, because the Rules key off them: `/appointment*`, `/prescription*`, `/portal*`, `/condition/*`, `/symptom*`, `/find-a-doctor*`, and `/bill-pay*`. These are the patterns to enumerate in discovery and the patterns the daily audit must reach.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **PHI-leak prevention on patient-facing pages.** The defining use case. Assert that no advertising-category tag and no third-party analytics tag fires on appointment, prescription, portal, condition, symptom, find-a-doctor, or bill-pay pages, and that no PHI-bearing value (an MRN, a member ID, a condition parameter, an appointment confirmation number) leaves those pages to any third party. Daily Web Audits on the patient-facing URL patterns are the baseline; the Rules below are the assertions.
- **Meta Pixel / GA litigation-defense readiness.** Healthcare is the most-litigated vertical for tracking-pixel claims, and the strongest defensive position is a continuous, dated audit history showing what fired on which patient-facing URL on which date. When a complaint alleges a specific date range, the run history is the rebuttal. Stand it up before a demand letter, not after — the data can't be back-filled. See `references/privacy-litigation-defense.md` → healthcare-tracking pixel claims.
- **Consent + CMP suppression on the portal, not just marketing.** The recurring gap is a CMP that is correctly wired on `www` and absent (or non-functional) on the patient portal and appointment flow. Run consent-state audits across the patient-facing surface and use `compare_consent_states` to prove that Reject-All suppresses all non-essential tracking on the portal itself — not only on the marketing pages where the banner is easy to test.
- **MHMDA / consumer-health-data compliance.** Washington's My Health My Data Act (and Nevada SB 370, and Connecticut's health add-ons) regulate "consumer health data" far more broadly than HIPAA regulates PHI — they reach health-adjacent pages on sites that aren't even covered entities. Audit condition, symptom, women's-health, mental-health, and pharmacy-locator pages with Rules that assert no third-party advertising tracker fires before explicit opt-in. See `references/privacy-and-compliance.md` → Washington My Health My Data Act.
- **Vendor inventory for OCR and legal.** OCR and outside counsel want a current, evidence-grade list of every third party that receives data from patient-facing pages, refreshed on a schedule and diffable over time. The Domains & Geo Privacy Report via `get_request_privacy_report`, paired with `find_first_observed` for a "first seen" date per vendor, is that inventory — and it turns "when did this pixel start firing?" into a lookup instead of an investigation.

## Business-model breakout

The four healthcare business models are not minor variations — they change which pages carry PHI, which regulator is looking, which vendors you expect, and which funnel you script. Pin the model down in the first conversation; it sets the whole audit design.

| | **Hospital / provider** | **Payer / insurer** | **Pharma / life sciences** | **Telehealth / health-tech** |
|---|---|---|---|---|
| **PHI / health-data exposure** | High and broad — appointment booking, find-a-doctor, the patient portal (MyChart-style), bill-pay, and condition pages. URL-plus-IP PHI across a large patient-facing surface. | Member portal (claims, benefits, EOBs), find-a-provider, plan-selection and enrollment flows. PHI plus member-ID and plan data. | Often *not* a HIPAA covered entity — but disease-state and treatment-information sites collect consumer-health signal that MHMDA-class laws reach directly; co-pay / patient-support program sign-ups collect real PII. | Heavy SPA app over a clinical back-end; the intake, symptom, and visit flows surface PHI directly, and the marketing stack is usually the most aggressive of the four. |
| **Key funnel** | Find-a-doctor → provider page → book appointment → portal login → bill-pay. The appointment-booking flow is the litigation-sensitive path. | Find-a-provider → plan compare → enroll → member-portal login → claims / EOB. Enrollment is the public conversion; the portal is the PHI core. | Condition / disease-state education → HCP vs. patient gating → co-pay enrollment / "find a specialist." The disease-state page is the consumer-health-data pressure point. | Sign-up → symptom intake → provider match → visit → prescription. SPA-heavy, fast release cadence, intake step surfaces PHI immediately. |
| **Primary regulators / regimes** | HIPAA + OCR; state privacy laws; MHMDA-class consumer-health laws; CIPA / state wiretap on booking and chat. | HIPAA + OCR; state insurance regulators; ACA marketplace rules; state privacy laws. | Often outside HIPAA — but MHMDA / Nevada SB 370 / CT health add-ons apply directly; FDA promotional rules on claims; state privacy laws. | HIPAA where it operates as a covered entity / business associate; MHMDA-class laws; state privacy laws; CIPA on chat/intake. |
| **Audit emphasis** | Daily PHI-leak Rules across the patient-facing surface + portal consent suppression + a Journey through the booking flow. | Member-portal NPI/PHI Rules + enrollment-flow PII scan + consent suppression on the portal. | Consumer-health-data Rules on disease-state pages (MHMDA framing, not HIPAA) + co-pay-form PII scan. | SPA-aware Journeys with `Prevent Navigation`; fast cadence; `scan_journey_pii` canary on the intake step. |

For pharma and life sciences especially, do not assume HIPAA is the operative law. A disease-state or treatment-information site run by a manufacturer is frequently *not* a covered entity, so HIPAA may not bite — but Washington's MHMDA reaches "consumer health data" on exactly those pages, with a private right of action behind it. Frame that engagement around MHMDA-class consumer-health-data Rules, not HIPAA.

For telehealth especially, the intake step is the pressure point and the architecture works against you: the app is usually a single-page app, so tag firing on the symptom-intake and visit screens only registers if the Journey carries the `Prevent Navigation` flag, and the marketing stack on a digital-health product is typically the most aggressive of the four models — a growth team's instinct to instrument every step collides head-on with an intake screen that surfaces PHI on the first interaction. Script the intake as a `scan_journey_pii` canary step early, and treat every SPA release as a moment a tag can inherit onto the visit flow unseen.

## Regulations that hit healthcare hardest

Healthcare sits under a sector-specific federal regime (HIPAA), *plus* a fast-growing set of state consumer-health-data laws that reach further than HIPAA, *plus* the tracking-pixel litigation wave that has made it the most-sued vertical. Do not restate effective dates or enforcement detail here — those live in the privacy references. The healthcare-specific angle:

- **HIPAA + OCR tracking-technology guidance.** The governing federal regime for covered entities and their business associates. The OCR position is that a patient's interaction with an appointment, prescription, condition, or symptom-checker page constitutes PHI when paired with the visitor's IP address — so disclosing that page-visit signal to Meta, Google, or an analytics vendor without authorization is the violation, and the pixel firing is the technical evidence. The patient-facing-page Rules below are the direct web-surface control. See `references/privacy-and-compliance.md` → HIPAA (United States — healthcare).
- **Washington MHMDA and the consumer-health-data wave.** MHMDA regulates "consumer health data" — including *inferred* health information — far more broadly than HIPAA regulates PHI, and it reaches sites that aren't covered entities at all (pharma marketing, health-adjacent retail, wellness apps). It carries a private right of action, which makes it the most plaintiff-friendly health-data law in the country. Nevada SB 370 and Connecticut's health add-ons follow the same shape with narrower reach. The condition / symptom / pharmacy-locator Rules below are where ObservePoint covers this. See `references/privacy-and-compliance.md` → Washington My Health My Data Act and Nevada SB 370.
- **The healthcare-pixel litigation wave (HIPAA + state torts + CIPA/VPPA layered).** Hundreds of class actions since 2023 against hospital systems, telehealth platforms, pharmacy chains, and healthcare-adjacent retailers, typically pleading HIPAA-adjacent state torts plus CIPA / state wiretap and sometimes VPPA as layered claims. The pattern is always the same: Meta Pixel or Google Analytics on a patient-facing page transmits the URL — PHI when paired with an IP — to a third party. The litigation-readiness section below is the healthcare-specific entry point; the statutory theory and the evidence-pack workflow are in `references/privacy-litigation-defense.md` → healthcare-tracking pixel claims.

**Why "URL + IP = PHI" changes the audit.** The fact that makes healthcare different from every other vertical is worth stating in technical terms, because it sets what the scan has to prove. In retail or financial services the question is usually "did an *identified* value (an email, an account number) leak?" In healthcare the disclosure can be complete without any name at all: a request to Meta carrying the page URL `/condition/oncology` plus the visitor's IP address is, on the OCR reading, a disclosure of a health condition tied to an identifiable individual — the IP is the identifier and the URL is the health fact. That is exactly why the `scan_audit_pii` **OP-static-IP** mode matters here in a way it doesn't elsewhere: it flags the captured-visitor-IP case directly, catching the disclosure even when no traditional PII field is present. A scan that only hunts for emails and ID numbers would read this page as clean while the litigated harm is sitting in the request.

The other privacy regimes (the U.S. comprehensive state laws, GDPR for any EU footprint, Consent Mode v2 as the technical consent contract) apply where the geography pulls them in, but HIPAA, the consumer-health-data laws, and the pixel litigation wave are the three that define the healthcare posture. Route to `references/privacy-and-compliance.md` for any regulation the organization's footprint adds.

## Common vendor patterns

The healthcare stack pairs ordinary MarTech with portal and clinical platforms that the marketing tools must never touch:

- **Patient-portal platforms.** Epic (MyChart) and Oracle Health / Cerner (HealtheLife and similar) dominate provider portals; payers run their own member portals. These often live on a portal subdomain (`mychart.example.org`) with a distinct authentication boundary — and the recurring failure is a marketing tag from the main site's container reaching the portal. Confirm the portal's exact domain in discovery so the audit reaches it.
- **Healthcare-specific MarTech and CMS.** Dedicated provider-marketing and patient-acquisition platforms, plus content-management systems that template condition and service-line pages — the templating is exactly how a single pixel ends up on every condition page at once.
- **Telehealth and scheduling platforms.** Telehealth visit platforms, online-scheduling widgets, and appointment-booking tools — frequently third-party embeds that bring their own scripts onto the booking page, which is the litigation-sensitive step.
- **Tag management, analytics, CMP.** Google Tag Manager or Tealium iQ as the container; GA4 and/or Adobe Analytics; OneTrust as the CMP. The governance question is whether the CMP and the firing rules actually extend to the patient-facing and portal surfaces, not just `www`.
- **The advertising pixels that cause the trouble.** Meta Pixel, Google Ads, and analytics configured to capture page URLs and query parameters — and chat / virtual-assistant and scheduling widgets that capture typed input. None of these is unusual; the harm is entirely about *where* they fire. The Rules below exist to prove they stay off the patient-facing surface.

For the full module-by-module breakdown of how ObservePoint audits each of these, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the relevant URL pattern, or to a Journey step.

**1. No advertising-category tag fires on any PHI-bearing URL pattern.** The defining healthcare Rule — it guards every patient-facing page at once.

```
WHEN page URL matches /\/appointment|\/prescription|\/portal|\/condition\/|\/symptom|\/find-a-doctor|\/bill-pay/
EXPECT
  no tags in category "Advertising" fire
  no third-party analytics tag fires that captures the page URL or query string
  no advertising request domains receive data (Meta, Google Ads, TikTok, etc.)
```

**2. A daily PII scan on patient-facing URLs detects no PII reaching a third party.** Run `scan_audit_pii` on the patient-facing audit with `customRegex` for the organization's MRN, member-ID, and appointment-confirmation formats so the scan catches a health-context identifier leaving a page to a third-party request, cookie, or tag variable.

```
scan_audit_pii(
  auditId=<patient-facing audit>,
  customRegex=[
    {name: "MRN", pattern: "MRN-\\d{8}"},
    {name: "member_id", pattern: "\\b[A-Z]{3}\\d{9}\\b"},
    {name: "appt_confirmation", pattern: "APPT-\\d{6,10}"}
  ]
)
EXPECT no match (masked) is sent to any third-party destination domain
```

Numeric patterns are off by default in the scanner to avoid false positives on analytics IDs — supplying these as `customRegex` is the deliberate opt-in for health-context identifier formats. Findings are masked, so the report drops straight into a ticket or an evidence pack without re-exposing patient data.

**3. The appointment-booking flow sends no condition or provider parameter to an ad pixel.** The booking page often carries the specialty, provider name, or reason-for-visit in the URL or a form field — exactly the signal that becomes PHI when it reaches Meta or Google. Use `scan_journey_pii` canary mode on the booking step.

```
WHEN page = appointment-booking flow
EXPECT
  no condition / specialty / provider parameter appears in any advertising or third-party request
  no value entered into the booking form (reason for visit, provider) reaches a third party
```

**4. Under Reject-All, no non-essential tracking fires on the patient portal.** The posture is that opt-out means opt-out on the portal itself — not only on the marketing pages where the banner is easy to test.

```
WHEN consent state = "Reject All" AND page URL matches /\/portal|mychart|\/member/
EXPECT
  no tags in category "Advertising" fire
  no non-essential analytics, session-replay, or chat tag fires
  no non-essential advertising or analytics cookie is set
```

**5. Symptom-checker and condition pages set no advertising cookies.** These are the consumer-health-data pages MHMDA-class laws reach, and a retargeting cookie set here is both a consent gap and a litigation signal.

```
WHEN page URL matches /\/condition\/|\/symptom|\/health-library/
EXPECT
  no cookie classified "Advertising" / "Targeting" is set
  no advertising or social pixel fires before explicit opt-in
```

**6. A newly-appeared third-party domain on a patient-facing page triggers an alert.** The early-warning control for the failure that matters most — a marketing vendor silently inheriting onto a PHI-bearing page.

```
WHEN find_first_observed reports a request domain first seen on a patient-facing URL pattern
EXPECT the domain is on the approved allowlist; otherwise raise an alert
```

**7. A logged-in patient-journey canary proves no typed PHI leaks downstream.** The strongest defensive signal — `scan_journey_pii` canary mode flags any value typed via the journey's `input` / `maskedinput` steps that turns up downstream in a tag, cookie, request, or POST body, with zero false positives.

```
WHEN scan_journey_pii runs on the logged-in patient journey with a canary identifier
EXPECT no canary value (member ID, DOB, condition) appears in any third-party request, cookie, or POST body
```

Pair Rule 4 with `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to produce the side-by-side evidence of exactly which tags (if any) leak past the opt-out on the portal, and pair Rule 6 with `find_first_observed` to date precisely when an unrecognized vendor first appeared so it traces to a specific deploy.

**A note on "patient-facing page."** Rules 1, 2, 4, 5, and 6 key off URL pattern, and Rules 3 and 7 require interaction behind the booking form or the login. Target the pages either by URL pattern when the site's URLs are clean, or by a data-layer value (`page.section = "portal"`) when they aren't. Prefer the data-layer value where it exists; URL patterns drift on re-platform and a Rule keyed to a stale pattern silently stops matching, which reads as a pass. The portal frequently sits on a separate subdomain — confirm both the patterns and the portal domain during discovery before writing these.

## PHI-leak detection deep-dive

PII scanning is the technical heart of the healthcare engagement, and it works without ObservePoint ever holding PHI. Two mechanisms matter, and both produce masked output.

**`scan_audit_pii` across the patient-facing surface.** Run it over the daily patient-facing audit run. It inspects tag-variable values, cookie values, and request query strings using three detection modes: a REGEX mode (email by default, plus the `customRegex` health-context formats — MRN, member ID, appointment confirmation — since numeric patterns are off by default to avoid false-positiving on analytics IDs); an **OP-static-IP** mode that flags the captured-visitor-IP case, which is the precise OCR concern (a page URL paired with an IP is PHI); and a destination-severity weighting that distinguishes a value landing in the first-party data layer (a governance smell) from the same value reaching a third-party domain (an active leak). The scanner sees URLs and tag payloads — not patient records — so a customer audits their PHI-bearing pages without exposing patient data to the platform.

**`scan_journey_pii` canary mode on the logged-in patient journey.** Script a Journey through the authenticated path and type a *canary* identifier — a fake patient's member ID, date of birth, or condition — via the journey's `input` / `maskedinput` steps. Canary mode then flags any appearance of that literal downstream in a tag, cookie, request, or POST body, with **zero false positives**: if the canary turns up in a Meta request, a real value would too. This is the difference between "a pixel is present on the portal" (which the tag inventory shows) and "the pixel received the member ID the patient typed" (which the canary proves). Use a provisioned *test* patient identity, never a real patient's, and supply it via `maskedinput` so the value is masked in the run record.

Why this is the strongest defensive evidence: it produces a dated, reproducible, *masked* record that a specific PHI-class value did or did not reach a specific third party on a specific date — exactly the rebuttal a tracking-pixel complaint requires — while keeping ObservePoint outside the PHI boundary entirely. PII masking is enforced in the wrapper (see `references/mcp-tools.md` → PII masking), so the finding lands in an evidence pack without re-exposing the very data the scan was looking for.

## Common pitfalls

The failure modes that recur in healthcare specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **A marketing pixel inherited onto the patient portal.** *Pitfall:* a Meta or Google tag approved for the marketing site loads through a shared container or global template and starts firing on the appointment, prescription, or portal pages — the single highest-stakes healthcare failure, and the exact fact pattern in the filed cases. *Catch:* Rule 1 fails the instant an advertising or third-party analytics tag appears on a PHI-bearing URL; `find_first_observed` (Rule 6) dates when it crossed onto the patient surface. *Fix:* scope the tag to the marketing-side firing rules in the TMS (not a site-wide trigger), and re-audit the patient-facing area to confirm it's gone.
- **A chatbot or scheduling widget leaking.** *Pitfall:* a third-party chat / virtual-assistant or appointment-scheduling widget on a booking or symptom page captures typed input — reason for visit, condition, provider — and ships it to the vendor, which is both a PHI leak and a CIPA/wiretap exposure. *Catch:* `scan_journey_pii` canary mode (Rule 3 / Rule 7) proves a typed value reached a third party; `compare_consent_states` shows whether it persists under Reject-All. *Fix:* mask sensitive fields in the widget's config, gate the widget behind consent, and re-scan to confirm the value no longer escapes.
- **"Find a doctor" search terms in query strings to analytics.** *Pitfall:* the directory search puts the specialty or condition a visitor searched (`?q=oncology`, `?specialty=cardiology`) into the URL, and analytics dutifully captures the full page URL — sending a health-interest signal to a third party. *Catch:* `scan_audit_pii` and Rule 1 flag the condition/specialty parameter reaching an analytics or advertising domain. *Fix:* strip health-context parameters before the analytics call, or move the search term out of the URL; re-scan the find-a-doctor pages to confirm.
- **BAA assumptions that don't cover tracking.** *Pitfall:* the team assumes a signed Business Associate Agreement with a vendor makes the data flow compliant — but the major advertising platforms do not sign BAAs for pixel data, and OCR's position is that the disclosure is the violation regardless of a contract elsewhere. The "we have a BAA" belief masks an open leak. *Catch:* the vendor inventory (`get_request_privacy_report`) plus Rule 1 show an advertising domain receiving data on a PHI page no matter what contracts exist. *Fix:* remove the advertising/analytics pixel from the patient-facing surface entirely — a BAA is not a substitute for the pixel not firing there — and confirm with a re-audit.
- **A consent banner on www but not the portal.** *Pitfall:* the CMP is correctly wired on the marketing site and is missing, mis-scoped, or non-functional on the patient portal and appointment subdomain, so the consent posture that passes a quick marketing-page check is absent exactly where PHI lives. *Catch:* run the consent-state audit against the portal domain specifically; Rule 4 fails and `compare_consent_states` (default vs. opt-out) shows the portal tracking that ignores the opt-out. *Fix:* extend the CMP and its firing rules to the portal and appointment subdomains, then re-audit the opt-out variant on the portal to confirm suppression.

## Worked Journey — the patient booking flow

The patient-facing Rules above are only as good as the path that exercises them, and a Web Audit can load the booking and portal URLs directly but never *acts* like a patient searching for a doctor, entering a reason for visit, or logging in. **The reason-for-visit value, the provider selection, the post-login portal state, and the events that fire as a result of those gestures only exist after interaction — which is why this is a Journey with a canary identity, not a plain Audit.** (For the full Audit-vs-Journey decision and how login is configured, see `references/products-and-modules.md` → "Audit vs. Journey — when each wins.")

Script a single Journey through the canonical patient path and attach Rules step by step:

| Step | Action | Rules that attach | Why here |
|---|---|---|---|
| **1. Find-a-doctor** | Search the directory for a specialty (canary term) | Rule 1 — no advertising / third-party analytics tag fires; the specialty search term does not reach an analytics domain | The entry point; the search term is a health-interest signal. |
| **2. Provider page** | Open a provider / condition page | Rule 1 + Rule 5 — no advertising tag fires, no advertising cookie is set | A condition-bearing URL — PHI when paired with the visitor IP. |
| **3. Book appointment** | Enter reason-for-visit via `input` / `maskedinput`, submit | Rule 3 — no condition/provider value reaches a pixel; `scan_journey_pii` canary on the typed reason-for-visit | The litigation-sensitive step; the richest PHI the public flow surfaces. |
| **4. Portal login + bill-pay** | Log in with test credentials via `maskedinput`, open bill-pay | Rule 1 + Rule 7 — no advertising/analytics tag fires post-login; canary member ID never leaks; Rule 2 PII scan on the authenticated pages | The authenticated PHI core; bill-pay adds payment context. |

Run the same Journey a second time with the CMP in Reject-All state and attach Rule 4 to every step — that is the consent-suppression evidence for the patient surface. Use a *test* patient identity and *test* credentials, never a real patient's, and supply them via `maskedinput` so the values are masked in the run record. For the persona-led version of this recipe (pain → approach → alert routing → success metric), see `references/solution-playbooks.md`.

**SPA caveat.** Many telehealth and modern portal apps are single-page apps. Set the `Prevent Navigation` flag on the Journey or the engine treats client-side route changes as reloads and misses the tag firing — see `references/products-and-modules.md` → Journeys.

## Peak / event cadence

Healthcare has no Black Friday, but it has its own calendar of high-change, high-scrutiny windows where new campaign pixels ship onto patient-facing pages under deadline pressure — exactly when a leak is most likely and least likely to be tested. The discipline is the same as retail's and FS's — escalate cadence and freeze change around the spike — applied to healthcare's events:

- **Open enrollment (payers and ACA marketplace, roughly October–January).** Plan-compare, enrollment, and find-a-provider pages get a traffic-and-content surge and acquisition pixels arrive on the public funnel. Escalate the patient-facing audit to daily, run the enrollment-flow PII scan, and freeze the enrollment container so any new tag is a deliberate exception.
- **Flu / vaccine and seasonal-campaign pushes.** Scheduling and "find a clinic" pages get new campaign tags and landing pages fast. Watch for advertising pixels appearing on the booking and clinic-locator pages with `find_first_observed` (Rule 6).
- **Awareness-month service-line campaigns (e.g., heart, cancer, mental-health months).** Condition and service-line pages — the consumer-health-data surface MHMDA-class laws reach — get campaign code and retargeting pushes. Run the no-advertising-cookie Rule (Rule 5) daily through the campaign and freeze the condition-page templates.
- **Portal or telehealth releases.** A portal or SPA release is the moment a marketing tag most often inherits onto an authenticated surface. Treat any release touching the portal or booking flow as a release gate: run the booking-and-portal Journey (Rule 3 / Rule 7) against staging before it ships, and re-run the patient-facing audit immediately after.

In every case the pattern is: capture a clean baseline before the window, escalate to daily on the affected surface during it, freeze the relevant container, and run `find_anomalies` (metric `tags`) each morning to separate real tag drift from volume noise — anomaly detection is scope-aware, so a traffic spike alone doesn't trip it.

## Litigation-readiness

Healthcare is the vertical where the audit history most directly becomes legal evidence, so the artifacts are worth standing up before any demand letter arrives — the fidelity of "what fired on which patient-facing URL on which date" cannot be back-filled after the fact. Keep an evidence pack ready with three components:

- **Audit run history** on the patient-facing URL patterns — the dated record of what fired where, run-over-run. When a complaint alleges a specific date range, `query_report` against the rule-summary pulls the pass/fail history for Rules 1, 4, 5, and 6 across that period without re-running anything.
- **`scan_audit_pii` / `scan_journey_pii` results** — the masked, dated proof that a PHI-class value did or did not reach a named third party, including the canary-mode journey results.
- **Vendor-removal timeline** — `find_first_observed` for when a vendor first appeared on a patient page, paired with the later run that shows it gone, documents remediation timing — the "here's how fast we caught and fixed it" half of the narrative.

Frame the evidence as technical detection, not legal conclusions: *we audit these pages daily, here is what we found and when, here is how quickly we remediated, here is the ongoing process that catches it.* That "reasonable practices" narrative is what counsel builds around the technical record. See `references/privacy-litigation-defense.md` → healthcare-tracking pixel claims for the full evidence-pack workflow. **ObservePoint is not a Business Associate and does not handle PHI itself** — the scanner sees URLs and tag payloads, not patient records, and PII findings are masked — which is exactly why it can produce this evidence without itself becoming part of the PHI exposure.

## Reporting and the evidence artifacts

Two saved-report artifacts carry most of the value for a healthcare account, and both are worth standing up early so the data accumulates before anyone needs it.

**The patient-facing pixel-posture dashboard.** Build a saved report with `create_saved_report` over the daily patient-facing audit, scoped to the PHI-leak Rules (Rules 1, 2, 4, 5, 6) so a CSM can see at a glance, per daily run, whether each patient-facing page stayed clean of advertising and third-party analytics tags. Use `get_report_schema` (with the `search` parameter) to find the exact column names before building it — don't guess column names. This is the morning artifact: open the dashboard, confirm the no-advertising-on-PHI rows are green, scan `find_anomalies` for tag drift, done. The trend view turns "is the patient surface clean?" from a half-day investigation into a ten-second glance.

**The OCR / legal vendor-inventory pack.** For the litigation-readiness narrative, the recurring ask is a current, diffable list of every third party that receives data from patient-facing pages, with a first-seen date per vendor. Build a saved report over the `network-requests` (or request-domain) data, pair it with `find_first_observed` so each domain carries a "first seen" date, and keep the Cookies and Domains & Geo Privacy Reports for the patient-facing audit on file alongside the masked `scan_audit_pii` / `scan_journey_pii` findings. `query_report` against the rule-summary pulls the pass/fail history for Rules 1, 4, 5, and 6 across the period — the record that the patient-facing controls held run-over-run — without re-running anything. Bundled, that's the technical-evidence pack counsel assembles the "reasonable practices" story around.

The point of standing both up early: evidence you didn't collect before the incident can't be back-filled with the same fidelity. In the most-litigated vertical the skill covers, the accumulated audit history is the deliverable.

## CSM cadence

The recommended rhythm for a healthcare account:

- **Patient-facing PHI areas.** Daily audits on the appointment, prescription, portal, condition, symptom, find-a-doctor, and bill-pay surface — the cost of an advertising or analytics pixel landing there is a reportable disclosure, so weekly is too slow. Run `scan_audit_pii` on every run and `find_anomalies` after each to catch a vendor crossing onto the patient surface early; keep Rules 1, 2, 5, and 6 live.
- **Patient journey + portal.** Run the booking-and-portal Journey (Rule 3 / Rule 7 canary) on a regular cadence and after any release touching the booking flow or portal; run the Reject-All variant (Rule 4) weekly against the portal domain specifically.
- **Consumer-health-data pages (MHMDA-class).** Weekly audits on condition, symptom, women's-health, mental-health, and pharmacy-locator pages with the no-advertising-cookie Rule (Rule 5).
- **Vendor inventory.** Refresh the Domains & Geo Privacy Report on a schedule so the OCR/legal-ready vendor list is always current and diffable, with `find_first_observed` dating each arrival.
- **Alert routing.** PHI-leak and patient-facing-pixel failures route to **privacy, compliance, and legal** together — in this vertical a pixel on a PHI page is a legal-exposure event, not just a marketing one — and escalate routing so a patient-facing failure pages a human same-day rather than waiting for the weekly review.

## Discovery checklist

Before designing anything, nail down the five facts that determine the whole audit shape:

1. **Which business model?** Hospital/provider, payer/insurer, pharma/life-sciences, or telehealth/health-tech — this picks the table row above and, critically, decides whether HIPAA even applies or whether MHMDA-class consumer-health-data law is the operative regime.
2. **What are the patient-facing URL patterns, and where is the portal?** Enumerate the appointment, prescription, condition, symptom, find-a-doctor, and bill-pay patterns, and confirm the portal's exact subdomain — the portal frequently lives apart from `www` and is the page most often missed.
3. **Can we get a test patient identity and test portal credentials?** The canary journey and the authenticated PHI Rules need a provisioned *test* patient — never a real one. Confirm both exist before scoping the journey work.
4. **Is the CMP wired on the portal and appointment flow, or only on www?** The single most common gap; confirm the consent surface reaches the patient-facing pages before assuming the opt-out works there.
5. **Which regulators and regions apply?** HIPAA where the entity is covered; then MHMDA / Nevada / Connecticut and the U.S. states (and EU, if applicable) — this drives the consent variants and which regulations in `references/privacy-and-compliance.md` are in scope.

The honest scope boundary to set in the same conversation: ObservePoint validates the *web* surface. A native iOS or Android patient app, the EHR / clinical back-end (Epic, Cerner), an IVR phone-scheduling channel, and the claims-processing systems are out of scope for direct scanning (a HAR captured from the app is the supported workaround for app traffic — see `references/limitations.md`). For a telehealth provider whose product is primarily a mobile app, say this plainly so the customer doesn't expect the web audit to cover the whole PHI story.

---

*Last verified: 2026-06-04*

This playbook describes technical evidence and detection, not legal advice. ObservePoint is not a Business Associate and does not handle PHI; verify against current OCR guidance and coordinate with counsel.
