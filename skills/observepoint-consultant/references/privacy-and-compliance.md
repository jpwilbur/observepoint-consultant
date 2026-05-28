# Privacy & compliance — regulations mapped to ObservePoint coverage

Load this file whenever the user asks how ObservePoint helps with a specific privacy, accessibility, or marketing-disclosure regulation. The shape of every entry:

- **What the regulation requires** in one sentence.
- **What's enforceable today** (state of play as of `Last verified` below).
- **How ObservePoint provides evidence** — the specific scanner + Rule + report combo.
- **What it does NOT cover** — so we don't oversell.

## How to use this file

Pick the regulation the user named. If they didn't name one, ask which jurisdiction matters most — most enterprise programs scope by region first, then layer in sector-specific (healthcare, financial, education) on top.

Then walk them through:

1. The **Rule** that proves compliance, with concrete `WHEN/EXPECT` logic.
2. The **report** that becomes their evidence artifact.
3. The **schedule** (daily for high-traffic, weekly for typical).
4. The **routing** — who gets the alert when the Rule fails.

Add the resulting Rule/Report pair to the customer's compliance evidence pack (template in `references/consulting-deliverables.md`).

## Major comprehensive privacy laws

### GDPR (European Union)

**What it requires.** Lawful basis for processing personal data, transparent disclosure of vendors and purposes, the ability to refuse non-essential processing, and demonstrable accountability.

**ObservePoint coverage.**

- Run separate Web Audits for "Accept All," "Reject All," and the GPC signal, all on the same set of pages.
- Attach a Rule that asserts no advertising or analytics tags fire under "Reject All" or under GPC.
- Use the Cookies Privacy Compliance Report to inventory every cookie, classify it (essential, analytics, marketing), and flag anything set before consent.
- Use the Domains & Geo Privacy Report to enumerate every vendor receiving data and the country it's routed to.

**Doesn't cover.** Lawful-basis documentation, Data Protection Impact Assessments, Article 30 records of processing, Data Subject Access Request workflows. Those live in your privacy program, not in a scanner.

### CCPA / CPRA (California)

**What it requires.** Disclosure of categories of personal information sold or shared, an honored opt-out signal (and the GPC signal is treated as a valid opt-out in California), and limits on the use of "sensitive personal information."

**ObservePoint coverage.**

- Enable "Send GPC Signal" on an audit variant and assert that no third-party data-sharing pixels fire — that's the technical proof your opt-out is honored.
- Validate the cookie banner exposes a "Do Not Sell or Share My Personal Information" link or equivalent.
- Inventory every third-party domain receiving data, since CPRA expanded "sale" to include sharing for cross-context behavioral advertising.

**Recent enforcement context.** The California Privacy Protection Agency has been active in 2025–2026, with significant settlements focused on opt-out failures across devices. The technical proof that your opt-out works on every device, on every page, is exactly what an audit produces.

### Other U.S. state privacy laws

A growing patchwork — Colorado, Connecticut, Utah, Virginia, Texas, Oregon, Montana, Delaware, Iowa, Nebraska, New Hampshire, New Jersey, Minnesota, Maryland, Tennessee, Indiana, Kentucky, Rhode Island, and more — all in force as of 2026.

**Shared technical patterns.** Most require an opt-out, several require GPC recognition, and all benefit from the same audit pattern: separate Web Audits per consent state, with Rules that assert correct tag behavior in each.

**Coverage approach.** Build a "U.S. state privacy" audit template once. Apply it across all sites; tweak the consent banner copy and opt-out path per state requirement.

### LGPD (Brazil)

**What it requires.** Consent and lawful basis for processing, similar in spirit to GDPR but with its own list of data subject rights.

**ObservePoint coverage.** Same audit pattern as GDPR. Run Reject-All and Accept-All variants; validate vendors and cookies; inventory data flows. The reports that satisfy a GDPR auditor will satisfy an ANPD (the Brazilian regulator) auditor too.

### PIPEDA (Canada)

**What it requires.** Meaningful consent and accountability for personal information handling.

**ObservePoint coverage.** Cookie inventory, consent-state audits, vendor disclosure. Lighter regulatory cadence than GDPR; the same audit data is sufficient evidence.

### India's DPDP Act and Rules

**What it requires.** Notice and consent for personal data processing, with explicit rights for data principals and obligations for data fiduciaries. The implementing Rules were approved in late 2025 and the regime is moving into active enforcement in 2026.

**ObservePoint coverage.** Run audits in the India region (geo-routed if available, or with an India IP via VPN allowlist), validate consent capture and vendor disclosure, and inventory data flows leaving India. Treat the GDPR template as the starting point and adjust for the specific notice and grievance language the DPDP Act requires.

## Sector-specific privacy laws

### HIPAA (United States, healthcare)

**What it requires.** Protected Health Information (PHI) must not be disclosed to unauthorized parties. Tracking technologies on healthcare websites that transmit PHI to advertising vendors have been the focus of significant enforcement.

**ObservePoint coverage.**

- Audit healthcare sites with Rules that flag any third-party advertising tag firing on URLs that contain PHI (appointment booking, prescription refill, health condition pages).
- Inventory cookies and assert no advertising trackers are set on PHI-bearing pages.
- Validate that consent banners (when used) properly suppress all non-essential tracking.

**Doesn't cover.** ObservePoint is not a Business Associate; it does not handle PHI itself. Customers can run audits without exposing PHI to the platform — the scanner sees URLs and tag payloads, not patient data.

### COPPA (United States, children under 13)

**What it requires.** Verifiable parental consent before collecting personal information from children, and no behavioral advertising to children.

**ObservePoint coverage.** Validate that age-gate flows actually suppress advertising tags. Run audits with the "child" path enabled in your age gate and assert that the Meta Pixel, Google Ads pixel, and similar do not fire.

### FERPA, GLBA

**Education and financial services equivalents.** Same audit-and-validate pattern: identify pages handling protected data, assert that no unauthorized third-party tracker fires on those pages.

## Privacy signals and frameworks

### Global Privacy Control (GPC)

**What it is.** A browser-level signal that broadcasts "do not sell or share" on every request. Honored by the laws of multiple U.S. states; broader rollout pending.

**ObservePoint coverage.** Toggle "Send GPC Signal" on an audit. The synthetic browser broadcasts the GPC header on every request. Pair with Rules that assert no covered tags fire when GPC is on. This is the cleanest way to prove your site honors GPC end-to-end.

### IAB Transparency and Consent Framework (TCF)

**What it is.** An industry-standard format for encoding consent strings that AdTech vendors can decode.

**Current version: 2.3.** TCF 2.3 was published in 2024 with a hard cutover deadline of **February 28, 2026** — TC strings generated after that date in the 2.2 format are invalid; the disclosedVendors segment is now mandatory. Existing TC strings from before that date remain valid.

**ObservePoint coverage.** Decode TC strings from cookies, validate they meet the current version requirements, assert correct vendor disclosure. Pair with audits per consent state to validate that the string actually reflects the user's choice.

### Google Consent Mode v2

**What it is.** Google's mechanism for adjusting tag behavior based on consent. Four categories: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`.

**ObservePoint coverage.** Validate that Consent Mode v2 signals propagate correctly from the CMP to Google tags. Use Rules to assert that under Reject-All, `ad_storage` is "denied" and the resulting tags use the no-cookie pings instead of standard collection. The Cookies Privacy Compliance Report shows which Google tags set what cookies under each consent state — that's your evidence of correct propagation.

### EU AI Act (Article 50 transparency)

**What it requires for marketing.** AI-generated content used in marketing campaigns must be labeled. The transparency obligations under Article 50 take effect **August 2, 2026**. Penalties scale to a percentage of global annual turnover.

**ObservePoint coverage.** Validate that marketing pages containing AI-generated copy or imagery carry the required disclosure. Build a Rule that asserts a specific data-layer flag (`page.ai_generated = true`) is paired with a visible disclosure element in the DOM. Audit at scale across the marketing site.

**Caveat.** ObservePoint can validate the *disclosure*; it cannot determine whether content actually was AI-generated. That classification is upstream.

## Accessibility (not technically privacy, but the same audit motion)

### WCAG 2.1 AA / European Accessibility Act

**What it requires.** Web content meeting the WCAG 2.1 AA conformance level, with the European Accessibility Act extending obligations across the EU for products and services in scope.

**ObservePoint coverage.** Web Audits include automated WCAG 2.1 AA scanning. The Accessibility Report and the new (2026) Accessibility Highlight Report show violations by severity and type. The Debugger added accessibility highlights in early 2026 for in-browser checks.

**Doesn't cover.** Manual review for things automation cannot test (color choice on photographs, semantic correctness of complex widgets, screen-reader user experience). Pair the scan with a manual review and lived-experience testing.

## Coverage matrix

| Regulation | ObservePoint module | Primary report | Schedule |
|---|---|---|---|
| GDPR | Web Audits + Rules + CMP validation | Cookies Privacy Compliance, Domains & Geo Privacy | Weekly, plus pre-deploy |
| CCPA / CPRA | Web Audits + GPC signal | Cookies Privacy Compliance | Weekly |
| Other U.S. state privacy | Web Audits + GPC + opt-out validation | Cookies Privacy Compliance, Consents | Weekly |
| LGPD, PIPEDA, DPDP | Web Audits + consent-state variants | Cookies Privacy Compliance | Weekly |
| HIPAA | Web Audits on PHI-bearing URLs + Rules | Tag & Variable Rules Report | Daily on PHI areas |
| COPPA | Web Audits with age-gate Journey | Tag & Variable Rules Report | Daily on kids' areas |
| GPC | Web Audits with "Send GPC Signal" | Tag & Variable Rules Report | Weekly |
| TCF (current 2.3) | Web Audits + TC string decoding rules | Cookies Privacy Compliance | Weekly |
| Consent Mode v2 | Web Audits per consent state | Tag & Variable Rules Report | Weekly |
| EU AI Act Article 50 | Web Audits with disclosure rules | Tag & Variable Rules Report | Weekly |
| WCAG 2.1 AA | Web Audits + accessibility scanning | Accessibility / Accessibility Highlight | Weekly |

## Building a compliance evidence pack

When the customer asks for an "audit evidence pack" — a deliverable to hand to a regulator or to internal legal — assemble:

1. The audit definitions (URL scope, consent states, schedule cadence).
2. The Rules attached, with their `WHEN/EXPECT` logic.
3. The last 90 days of run histories showing pass/fail trends.
4. The exception log: every failure, when it was fixed, and by whom.
5. The change log for the audit/Rules themselves (who edited, when).

Most of items 1–4 can be exported from the API. Item 5 lives in the activity log in the app. Bundle the lot as a quarterly PDF + CSV archive; that's the typical evidence pack format.

Full template lives in `references/consulting-deliverables.md`.

## What this file deliberately does not do

- **Legal advice.** ObservePoint produces evidence; lawyers decide whether the evidence is sufficient for a specific jurisdiction.
- **Roadmap projection.** Regulations change. Re-verify the dates in this file against current regulator guidance before using them in a customer commitment.
- **Vendor risk assessments.** Beyond identifying which vendors receive data, ObservePoint does not vet the vendors themselves.

---

*Last verified: 2026-05-28*
