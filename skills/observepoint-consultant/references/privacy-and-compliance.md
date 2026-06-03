# Privacy & compliance — regulations mapped to ObservePoint coverage

Load this file whenever the user asks how ObservePoint helps with a specific privacy, accessibility, or marketing-disclosure regulation. The shape of every entry:

- **What the regulation requires** in one sentence.
- **What's enforceable today** (state of play as of `Last verified` below).
- **How ObservePoint provides evidence** — the specific scanner + Rule + report combo.
- **What it does NOT cover** — so we don't oversell.

## Contents

- [How to use this file](#how-to-use-this-file)
- [U.S. comprehensive privacy laws](#us-comprehensive-privacy-laws)
  - [Shared patterns across U.S. state laws](#shared-patterns-across-us-state-laws)
  - [California — CCPA / CPRA](#california--ccpa--cpra)
  - [Colorado — CPA](#colorado--cpa)
  - [Connecticut — CTDPA](#connecticut--ctdpa)
  - [Virginia — VCDPA](#virginia--vcdpa)
  - [Utah — UCPA](#utah--ucpa)
  - [Texas — TDPSA](#texas--tdpsa)
  - [Oregon — OCPA](#oregon--ocpa)
  - [Montana — MCDPA](#montana--mcdpa)
  - [Delaware — DPDPA](#delaware--dpdpa)
  - [Iowa — ICDPA](#iowa--icdpa)
  - [Nebraska — NDPA](#nebraska--ndpa)
  - [New Hampshire — NH-DPA](#new-hampshire--nh-dpa)
  - [New Jersey — NJDPA](#new-jersey--njdpa)
  - [Minnesota — MCDPA](#minnesota--mcdpa-1)
  - [Maryland — MODPA](#maryland--modpa)
  - [Tennessee — TIPA](#tennessee--tipa)
  - [Indiana — ICDPA](#indiana--icdpa-1)
  - [Kentucky — KCDPA](#kentucky--kcdpa)
  - [Rhode Island — RIDTPPA](#rhode-island--ridtppa)
  - [U.S. state matrix](#us-state-matrix)
- [U.S. sectoral privacy](#us-sectoral-privacy)
  - [HIPAA](#hipaa-united-states-healthcare)
  - [GLBA](#glba-united-states-financial-services)
  - [COPPA](#coppa-united-states-children-under-13)
  - [FERPA](#ferpa-united-states-education)
- [U.S. health-data-specific](#us-health-data-specific)
  - [Washington My Health My Data Act](#washington-my-health-my-data-act-mhmda)
  - [Nevada SB 370](#nevada-sb-370)
  - [Connecticut health-data add-ons](#connecticut-health-data-add-ons)
- [U.S. AI-specific](#us-ai-specific)
  - [Colorado AI Act](#colorado-ai-act)
  - [Texas Responsible AI Governance Act](#texas-responsible-ai-governance-act-raiga)
  - [NYC Local Law 144](#nyc-local-law-144-automated-employment-decision-tools)
- [U.S. kids-specific](#us-kids-specific)
  - [California AADC](#california-aadc-age-appropriate-design-code)
  - [KOSA](#kosa-federal-kids-online-safety-act)
  - [State student data privacy laws](#state-student-data-privacy-laws)
- [International privacy laws](#international-privacy-laws)
  - [GDPR (EU)](#gdpr-european-union)
  - [LGPD (Brazil)](#lgpd-brazil)
  - [PIPEDA (Canada)](#pipeda-canada)
  - [India DPDP Act](#indias-dpdp-act-and-rules)
- [Privacy signals and frameworks](#privacy-signals-and-frameworks)
- [Accessibility](#accessibility-not-technically-privacy-but-the-same-audit-motion)
- [Coverage matrix](#coverage-matrix)
- [Building a compliance evidence pack](#building-a-compliance-evidence-pack)
- [What this file deliberately does not do](#what-this-file-deliberately-does-not-do)

## How to use this file

Pick the regulation the user named. If they didn't name one, ask which jurisdiction matters most — most enterprise programs scope by region first, then layer in sector-specific (healthcare, financial, education) on top.

Then walk them through:

1. The **Rule** that proves compliance, with concrete `WHEN/EXPECT` logic.
2. The **report** that becomes their evidence artifact.
3. The **schedule** (daily for high-traffic, weekly for typical).
4. The **routing** — who gets the alert when the Rule fails.

Add the resulting Rule/Report pair to the customer's compliance evidence pack (template in `references/consulting-deliverables.md`).

For litigation-defense scenarios (responding to a class-action complaint or demand letter under CIPA, VPPA, BIPA, ECPA, or state wiretap statutes), use the companion file `references/privacy-litigation-defense.md` — different audience (in-house counsel, not privacy ops) and different evidence pattern.

## U.S. comprehensive privacy laws

### Shared patterns across U.S. state laws

By mid-2026, 19 U.S. states have comprehensive privacy laws in force. Every per-state entry below follows the same shape, so the shared technical pattern is described once here and not repeated:

**The shared audit pattern.** For any U.S. state comprehensive privacy law:

1. Run separate Web Audits for "Accept All," "Reject All," and a third audit with the GPC signal enabled (where the state recognizes GPC). The cleanest one-shot setup is `mcp__ObservePoint__setup_compliance_monitoring(regulation="ccpa", domain=...)` — it creates the three-audit pattern designed for California, and the same shape works for most other state laws with minor consent-banner-copy adjustments.
2. Attach Rules that assert no advertising or analytics tags fire under "Reject All" or GPC.
3. Use `mcp__ObservePoint__compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to surface the actual delta — the canonical "what leaks despite the opt-out" diagnostic.
4. Use the Cookies Privacy Compliance Report as the evidence artifact. Inventory every cookie; classify it (essential, analytics, marketing); flag anything set before consent.
5. Use the Domains & Geo Privacy Report to enumerate vendors receiving data. CPRA-style laws expanded "sale" to include sharing for cross-context behavioral advertising — vendors matter.

**What's shared across all states.** Opt-out for "sale" or "share" of personal information; consumer access / deletion / correction rights; an honored opt-out signal (where GPC is recognized); explicit treatment for "sensitive personal information."

**What varies.** Specific opt-out signal recognition, sensitive-data list, applicability thresholds (revenue, processing volume), private right of action (most state laws don't have one; California's CCPA has a narrow one for breach), enforcement body and timeline, cure-period availability.

### California — CCPA / CPRA

**Status.** In force since 2020 (CCPA), expanded by CPRA effective 2023. Enforcement by the California Privacy Protection Agency (CPPA) and Attorney General.

**What it requires.** Disclosure of categories of personal information collected, sold, and shared. An honored opt-out for "sale" and "share" — and GPC is treated as a valid opt-out signal. Limits on the use and disclosure of "sensitive personal information" (race, religion, biometric, geolocation, etc.). Rights of access, deletion, correction, and (for sensitive data) limit-use.

**ObservePoint coverage — Tier 1.**

- **Three-audit setup**: `mcp__ObservePoint__setup_compliance_monitoring(regulation="ccpa", domain=...)`. Creates Default (baseline), Opt-Out (CMP "Reject All" via pre-audit action), and GPC (gpcEnabled + blockThirdPartyCookies) audits. Never assign non-essential consent categories to the Opt-Out or GPC audits.
- **Cross-state-comparison Rule** — `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` and `(leftState="default", rightState="gpc")`. The canonical consent-leak diagnostic: tells you exactly which tags fire on the baseline that should NOT fire under Reject All or GPC.
- **GPC enforcement Rule**: `WHEN consent_state = "gpc" EXPECT no third-party advertising domains receive data AND no cross-context behavioral advertising cookies are set`.
- **Sensitive-data Rule**: identify pages collecting geolocation, biometric, or other sensitive categories; assert that no third-party tracker fires before explicit opt-in.
- **PII leak detection** — `scan_audit_pii` on each consent variant. Catches cases where a user identifier ends up in an analytics or advertising request despite the opt-out (a recurring class-action allegation).
- **Cookie banner check**: validate the "Do Not Sell or Share My Personal Information" link is present and functional.

**Enforcement context (2024–2026).** Recent CPPA enforcement has focused on opt-out failures across devices and on websites that ignore GPC. Multimillion-dollar settlements have specifically called out scenarios where the opt-out worked on one device but not another. The "honored across every device on every page" evidence is exactly what `compare_consent_states` produces.

**Separate California litigation theory — CIPA.** California also has the California Invasion of Privacy Act (CIPA), which underlies the dominant tracking-pixel class-action wave in 2024–2026 (pen-register / trap-and-trace theories). CIPA is a tort statute, not a comprehensive privacy law; treatment lives in `references/privacy-litigation-defense.md`.

**Doesn't cover.** Lawful-basis documentation, privacy notices, Data Subject Rights workflows (access / deletion fulfillment), employee data handling. Those live in the privacy program, not in a scanner.

### Colorado — CPA

**Status.** Colorado Privacy Act, effective July 1 2023. Enforcement by the Colorado Attorney General.

**What it requires.** Opt-out for "sale" and "targeted advertising" and "profiling." GPC must be honored as a "universal opt-out mechanism." Opt-in for sensitive data processing. Required Data Protection Assessments for high-risk processing.

**ObservePoint coverage.** Apply the shared U.S. state audit pattern. Specifically: run a GPC-enabled audit (GPC is mandatory under CPA, not optional like some states) and prove that the GPC signal blocks both "sale" and "targeted advertising" pixels. Use `compare_consent_states(domain=..., leftState="default", rightState="gpc")` to produce the side-by-side.

**Gotcha.** Colorado's "targeted advertising" definition is broader than California's "sale" — assume more pixels are in scope. Include analytics-with-cross-context-tracking in the Reject-All Rule set.

### Connecticut — CTDPA

**Status.** Connecticut Data Privacy Act, effective July 1 2023. Enforcement by the Connecticut Attorney General; cure period eliminated as of January 1 2025.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data and for under-16s. GPC recognized as a universal opt-out signal since January 1 2025.

**ObservePoint coverage.** Same as CPA, with the under-16 wrinkle: if your site has any logged-in flow where age is known, an age-gate Journey that fires advertising-tag-blocked Rules for under-16s is good defense-in-depth.

**Gotcha.** The cure period is gone. Enforcement actions can land without warning. Lean on scheduled audits and threshold alerts so you find problems before regulators do.

### Virginia — VCDPA

**Status.** Virginia Consumer Data Protection Act, effective January 1 2023. Enforcement by the Virginia Attorney General; 30-day cure period.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data. No GPC recognition (as of 2026).

**ObservePoint coverage.** Shared pattern, minus the GPC variant since Virginia doesn't require GPC honoring. Focus on the opt-out signal the CMP actually exposes; validate it blocks targeted-advertising pixels.

### Utah — UCPA

**Status.** Utah Consumer Privacy Act, effective December 31 2023. Enforcement by the Utah Attorney General via the Department of Commerce.

**What it requires.** Narrower than most states: opt-out for sale and targeted advertising. Notice for sensitive data (opt-out, not opt-in). No GPC recognition. Higher applicability thresholds — fewer businesses in scope.

**ObservePoint coverage.** Shared pattern, light. Standard opt-out validation; no GPC variant needed.

### Texas — TDPSA

**Status.** Texas Data Privacy and Security Act, effective July 1 2024. Enforcement by the Texas Attorney General.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data. GPC recognized as a universal opt-out signal.

**ObservePoint coverage.** GPC-enabled audit required. Texas is notable for an aggressive AG and notable settlements — treat enforcement seriously even though the law is younger than CCPA. Use the standard three-audit pattern plus PII scanning on sensitive-data pages.

### Oregon — OCPA

**Status.** Oregon Consumer Privacy Act, effective July 1 2024. Enforcement by the Oregon Attorney General.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data. GPC recognized.

**ObservePoint coverage.** Standard shared pattern, GPC included.

### Montana — MCDPA

**Status.** Montana Consumer Data Privacy Act, effective October 1 2024. Enforcement by the Montana Attorney General; cure period sunset on October 1 2026.

**What it requires.** Opt-out for sale and targeted advertising. Opt-in for sensitive data. GPC recognized.

**ObservePoint coverage.** Standard shared pattern, GPC included. After October 2026, no cure period — same posture as Connecticut.

### Delaware — DPDPA

**Status.** Delaware Personal Data Privacy Act, effective January 1 2025. Enforcement by the Delaware Department of Justice.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data. GPC recognized. Notable: tighter applicability than most states — businesses controlling personal data of 35,000+ Delaware residents (or 10,000+ if deriving >20% revenue from sale) are in scope.

**ObservePoint coverage.** Standard shared pattern, GPC included.

### Iowa — ICDPA

**Status.** Iowa Consumer Data Protection Act, effective January 1 2025. Enforcement by the Iowa Attorney General; 90-day cure period.

**What it requires.** Narrower than most: opt-out for sale and targeted advertising. Notice for sensitive data (opt-out, not opt-in). No GPC recognition. Closer in shape to Utah than to Colorado.

**ObservePoint coverage.** Standard shared pattern, no GPC variant required.

### Nebraska — NDPA

**Status.** Nebraska Data Privacy Act, effective January 1 2025. Enforcement by the Nebraska Attorney General.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data. GPC recognized.

**ObservePoint coverage.** Standard shared pattern, GPC included.

### New Hampshire — NH-DPA

**Status.** New Hampshire Data Privacy Act, effective January 1 2025. Enforcement by the New Hampshire Attorney General.

**What it requires.** Opt-out for sale, targeted advertising, and profiling. Opt-in for sensitive data. GPC recognized.

**ObservePoint coverage.** Standard shared pattern, GPC included.

### New Jersey — NJDPA

**Status.** New Jersey Data Privacy Act, effective January 15 2025. Enforcement by the New Jersey Division of Consumer Affairs; rulemaking in progress through 2026.

**What it requires.** Opt-out for sale, targeted advertising, profiling. Opt-in for sensitive data. GPC recognized.

**ObservePoint coverage.** Standard shared pattern, GPC included. Watch the rulemaking — the implementing regulations are being shaped through 2026 and may impose additional UI requirements on consent banners.

### Minnesota — MCDPA

**Status.** Minnesota Consumer Data Privacy Act, effective July 31 2025. Enforcement by the Minnesota Attorney General.

**What it requires.** Opt-out for sale, targeted advertising, profiling. Opt-in for sensitive data. GPC recognized. Notable: explicit "data privacy and protection assessments" requirement for high-risk processing.

**ObservePoint coverage.** Standard shared pattern, GPC included. Use the Domains & Geo Privacy Report to support DPIAs for high-risk vendors.

### Maryland — MODPA

**Status.** Maryland Online Data Privacy Act, effective October 1 2025. Enforcement by the Maryland Attorney General.

**What it requires.** Opt-out for sale, targeted advertising. Opt-in for sensitive data. GPC recognized. Distinctive feature: explicit prohibitions on selling sensitive data and on processing minors' data for targeted advertising.

**ObservePoint coverage.** Standard shared pattern, GPC included. Add Rules on pages that may collect sensitive data (geolocation, health, biometric) asserting no advertising tag fires.

### Tennessee — TIPA

**Status.** Tennessee Information Protection Act, effective July 1 2025. Enforcement by the Tennessee Attorney General.

**What it requires.** Opt-out for sale, targeted advertising. Opt-in for sensitive data. GPC recognized. Distinctive feature: a "Voluntary Privacy Program" affirmative defense — businesses with documented NIST-aligned programs get a defense against claims.

**ObservePoint coverage.** Standard shared pattern, GPC included. The "NIST-aligned program" defense means well-documented evidence packs (run history, exception logs, change logs from the activity log) are extra valuable in Tennessee.

### Indiana — ICDPA

**Status.** Indiana Consumer Data Protection Act, effective January 1 2026.

**What it requires.** Opt-out for sale and targeted advertising. Opt-in for sensitive data. No GPC recognition.

**ObservePoint coverage.** Shared pattern, no GPC variant required.

### Kentucky — KCDPA

**Status.** Kentucky Consumer Data Protection Act, effective January 1 2026.

**What it requires.** Opt-out for sale, targeted advertising, profiling. Opt-in for sensitive data. No GPC recognition (as of 2026).

**ObservePoint coverage.** Shared pattern, no GPC variant required.

### Rhode Island — RIDTPPA

**Status.** Rhode Island Data Transparency and Privacy Protection Act, effective January 1 2026.

**What it requires.** Opt-out for sale, targeted advertising, profiling. Opt-in for sensitive data. GPC recognized.

**ObservePoint coverage.** Standard shared pattern, GPC included.

### U.S. state matrix

Snapshot view across all 19 in-force U.S. comprehensive privacy laws. Use this for "do we need to do anything different in state X?" questions.

| State (abbreviation) | Effective | Enforcement body | GPC required | Sensitive data | Notable wrinkle |
|---|---|---|---|---|---|
| California (CCPA/CPRA) | 2020 / 2023 | CPPA + AG | Yes | Opt-in for limit-use | Active CPPA enforcement; CIPA is the bigger pixel-litigation risk |
| Colorado (CPA) | Jul 2023 | AG | Yes | Opt-in | Broad "targeted advertising" definition |
| Connecticut (CTDPA) | Jul 2023 | AG | Yes (2025+) | Opt-in | No cure period since 2025 |
| Virginia (VCDPA) | Jan 2023 | AG | No | Opt-in | 30-day cure period |
| Utah (UCPA) | Dec 2023 | AG via DoC | No | Opt-out | Higher applicability threshold |
| Texas (TDPSA) | Jul 2024 | AG | Yes | Opt-in | Aggressive AG, large settlements |
| Oregon (OCPA) | Jul 2024 | AG | Yes | Opt-in | |
| Montana (MCDPA) | Oct 2024 | AG | Yes | Opt-in | Cure period ends Oct 2026 |
| Delaware (DPDPA) | Jan 2025 | DOJ | Yes | Opt-in | Lower applicability threshold |
| Iowa (ICDPA) | Jan 2025 | AG | No | Opt-out | 90-day cure period |
| Nebraska (NDPA) | Jan 2025 | AG | Yes | Opt-in | |
| New Hampshire (NH-DPA) | Jan 2025 | AG | Yes | Opt-in | |
| New Jersey (NJDPA) | Jan 2025 | Div. Consumer Affairs | Yes | Opt-in | Active rulemaking through 2026 |
| Minnesota (MCDPA) | Jul 2025 | AG | Yes | Opt-in | Explicit DPIA requirement |
| Maryland (MODPA) | Oct 2025 | AG | Yes | Opt-in | Sensitive-data sale prohibition |
| Tennessee (TIPA) | Jul 2025 | AG | Yes | Opt-in | NIST-aligned program is affirmative defense |
| Indiana (ICDPA) | Jan 2026 | AG | No | Opt-in | |
| Kentucky (KCDPA) | Jan 2026 | AG | No | Opt-in | |
| Rhode Island (RIDTPPA) | Jan 2026 | AG | Yes | Opt-in | |

The 12-of-19 states that mandate GPC mean the GPC variant is essentially required for any multi-state program; one GPC audit can prove the technical signal works for the whole portfolio. Don't skip it.

## U.S. sectoral privacy

### HIPAA (United States — healthcare)

**What it requires.** Protected Health Information (PHI) must not be disclosed to unauthorized parties. The HHS Office for Civil Rights (OCR) has issued guidance specifically targeting tracking technologies on healthcare websites that transmit PHI to advertising and analytics vendors.

**Enforcement context (2024–2026).** The Meta Pixel healthcare litigation wave has produced hundreds of class actions and material settlements. OCR guidance treats a patient's appointment booking, prescription refill, condition page, or symptom-checker interaction as PHI even when paired with an IP address rather than a name. Sharing that signal with Meta or Google is the violation; the pixel firing is the technical evidence.

**ObservePoint coverage.**

- Daily Web Audits on patient-facing URL patterns: `/appointment*`, `/prescription*`, `/portal*`, `/condition/*`, `/symptom*`, `/find-a-doctor*`, etc.
- Rules that flag any third-party advertising tag firing on those URLs. `WHEN page URL matches PHI-bearing pattern EXPECT no advertising-category tags fire`.
- `scan_audit_pii` on those URLs to detect any direct PII leakage to advertising or analytics endpoints (canary mode catches typed values; OP-static-IP catches captured-visitor-IP cases).
- Inventory cookies and assert no advertising trackers are set on PHI-bearing pages.
- Validate that consent banners (when used) properly suppress all non-essential tracking on these pages — and that the audit's pre-audit-action "Reject All" actually works on the patient portal, not just the marketing site.

**Doesn't cover.** ObservePoint is not a Business Associate; it does not handle PHI itself. Customers run audits without exposing PHI to the platform — the scanner sees URLs and tag payloads, not patient data. PII scanning masks raw values in output. For the litigation-defense pattern around HIPAA-tracking-pixel claims specifically, see `references/privacy-litigation-defense.md`.

### GLBA (United States — financial services)

**What it requires.** Gramm-Leach-Bliley Act regulates how financial institutions handle nonpublic personal information (NPI). The FTC's Safeguards Rule (revised 2023) extends to safeguarding NPI from third-party tracking and ensuring vendor inventories for any third party receiving NPI.

**ObservePoint coverage.**

- Web Audits on the customer's logged-in banking / account / wealth-management pages with Rules that assert no third-party advertising or analytics tracker fires when NPI may be present (account balances, transaction histories, social security numbers in form fields).
- `scan_audit_pii(customRegex=[{name: "SSN", pattern: "..."}, {name: "account_number", pattern: "..."}])` to catch direct NPI leakage.
- Vendor inventory via the Domains & Geo Privacy Report — financial regulators care about every vendor in the chain.

**Doesn't cover.** GLBA Safeguards Rule has broader requirements (access controls, incident response, vendor management contracts) that aren't web-scanner work.

### COPPA (United States — children under 13)

**What it requires.** Verifiable parental consent before collecting personal information from children under 13. No behavioral advertising to children. The FTC's COPPA 2.0 Final Rule (published January 2025, effective phases through 2026) tightened restrictions: clearer definitions of "personal information" to include persistent identifiers, mandatory parental consent for any third-party data sharing, and explicit prohibitions on targeted advertising even with parental consent in some cases.

**ObservePoint coverage.**

- Validate that age-gate flows actually suppress advertising and analytics tags. A Journey scripted with the "child" age-gate path, paired with Rules asserting Meta Pixel, Google Ads pixel, TikTok pixel, and similar do not fire.
- `compare_consent_states` between adult and child user paths to surface any tags that fire in both contexts (a child should see a stricter subset).
- Cookie inventory on children's pages: assert all cookies are essential-only. No analytics, no advertising.

**COPPA 2.0 wrinkles.** The new persistent-identifier definition means even seemingly innocuous device IDs are in scope. Don't assume "we don't collect names from kids" is enough — the device-ID question matters too.

### FERPA (United States — education)

**What it requires.** Family Educational Rights and Privacy Act protects the privacy of student education records. Schools receiving federal funding cannot disclose personally identifiable information (PII) from education records without parental (or eligible-student) consent.

**Tracking-pixel intersection.** Tracking technologies on school websites and student portals that transmit identifiable student data to third parties are facing scrutiny — both under FERPA directly and under state student data privacy laws (see `U.S. kids-specific` below). The pattern parallels the HIPAA healthcare-pixel issue.

**ObservePoint coverage.**

- Audit student portal URL patterns with Rules asserting no advertising or analytics tracker fires.
- `scan_journey_pii` on a logged-in student journey using canary mode (the journey types a known fake student name / ID; any downstream appearance is a definitive leak).
- Vendor inventory on `/student*`, `/courses*`, `/grades*` URL patterns via the Domains & Geo Privacy Report.

**Doesn't cover.** FERPA's broader requirements (records access, amendment requests, directory information designations) live in the school's privacy program.

## U.S. health-data-specific

A growing category of state laws that target health data specifically, often broader than HIPAA (covering "consumer health data" rather than just PHI from covered entities).

### Washington My Health My Data Act (MHMDA)

**Status.** Effective March 31 2024 (large businesses) / June 30 2024 (small businesses). Enforcement by the Washington Attorney General; **private right of action** for affected consumers.

**What it requires.** Consent before collecting, sharing, or selling "consumer health data." Geofence prohibition: cannot collect health data via geofences around healthcare facilities. Broad definition of "consumer health data" — includes inferred health information (e.g., behavioral data suggesting pregnancy or mental health treatment).

**ObservePoint coverage.**

- Audit pages that touch health-adjacent topics (women's health, mental health resources, pharmacy locators, condition information) with Rules asserting no third-party advertising tracker fires before explicit opt-in.
- `scan_audit_pii` to catch any health-context value leaking to ad pixels.
- Validate consent banner UX captures consent specifically for health data — generic CMP consent is not sufficient under MHMDA.

**Notable risk.** The private right of action makes MHMDA the most plaintiff-friendly U.S. health data law. Class actions are already filed against major retailers, pharma sites, and pharmacy chains.

### Nevada SB 370

**Status.** Effective March 31 2024.

**What it requires.** Consent before selling consumer health data; opt-out for processing. Narrower than MHMDA — no private right of action, but enforcement by the Nevada Attorney General.

**ObservePoint coverage.** Same audit pattern as MHMDA, lighter on the consent-banner specificity since no private right of action drives the stakes.

### Connecticut health-data add-ons

**Status.** Connecticut amended CTDPA (effective 2024-2025) to add specific consumer health data protections.

**What it requires.** Consent for processing consumer health data; expanded sensitive-data category. Inherits CTDPA's enforcement and (lack of) cure period.

**ObservePoint coverage.** Layer health-data-specific Rules onto your existing CTDPA audit setup.

## U.S. AI-specific

A new category of laws regulating AI use, with implications for marketing and analytics teams using AI-generated content or AI-driven decision-making.

### Colorado AI Act

**Status.** Effective February 1 2026 (the first U.S. state comprehensive AI Act). Enforcement by the Colorado Attorney General.

**What it requires.** "High-risk" AI systems must undergo impact assessments and provide consumer notice. For consumer-facing marketing, AI-generated content used for material consumer decisions falls in scope. Transparency disclosures are required.

**ObservePoint coverage.**

- Audit marketing pages with Rules that assert AI-generated content carries the required disclosure. A data-layer flag like `page.ai_generated = true` paired with a DOM Rule asserting a visible disclosure element exists.
- Use the EU AI Act Article 50 audit pattern (see below) as the starting template — the technical signal is similar even though the legal trigger differs.

**Doesn't cover.** Impact assessments themselves; AI vendor risk reviews. Those are program work, not scanner work.

### Texas Responsible AI Governance Act (RAIGA)

**Status.** Signed into law 2025; effective phases through 2026-2027. Enforcement by the Texas Attorney General.

**What it requires.** Transparency disclosures for AI use in consumer-facing contexts. Prohibited discriminatory AI uses. Mandatory impact assessments for certain categories.

**ObservePoint coverage.** Same disclosure-validation Rule pattern as Colorado AI Act and EU AI Act Article 50. Validate marketing pages flag AI-generated content and that the flag pairs with a visible disclosure element.

### NYC Local Law 144 (automated employment decision tools)

**Status.** In effect since July 2023; enforcement by NYC Department of Consumer and Worker Protection.

**What it requires.** Employers using AI-driven hiring tools must (a) conduct an annual bias audit by an independent auditor, (b) publish a summary of the audit results, and (c) notify candidates that AI is being used.

**ObservePoint coverage — narrow.** ObservePoint can validate that the candidate-notification disclosure is present on careers pages and application flows where AI hiring tools are in use. Rule: `WHEN URL matches "/careers/apply*" EXPECT page contains required AEDT disclosure element`. The audit itself (the bias audit) is outside ObservePoint's scope — that's an independent auditor's work on the AI system itself.

## U.S. kids-specific

### California AADC (Age Appropriate Design Code)

**Status.** California Age-Appropriate Design Code Act passed 2022; significant 9th Circuit ruling (August 2024) blocked enforcement of many provisions; partial revival expected through 2026 as appeals proceed.

**What it requires (where unblocked).** Default high-privacy settings for users likely under 18; restrictions on profiling of minors; data protection impact assessments for products likely accessed by children.

**ObservePoint coverage.** Where AADC provisions are in force (verify the current injunction status — this is moving), audit children-likely-accessed pages with Rules asserting strict tracking limits. Cross-check with COPPA and state student-data laws — there's overlap.

### KOSA (federal Kids Online Safety Act)

**Status.** Passed the U.S. Senate (July 2024); House action pending through 2025-2026. **Not yet in force** as of June 2026.

**What it would require.** Duty of care for online platforms to mitigate harm to minors; transparency reporting; default-safest-settings for known minors; opt-out from algorithmic recommendation systems for minors.

**ObservePoint coverage if/when in force.** Default-settings validation (no targeted advertising by default for minor accounts); algorithmic-recommendation transparency Rules. Watch the bill's status before scoping work.

### State student data privacy laws

**Status.** Most states have enacted student data privacy laws targeting school vendors (SOPIPA in California 2014, equivalents in 30+ states by 2026).

**What they require.** Vendors providing services to K-12 schools cannot use student data for advertising, build student profiles, or sell student data.

**ObservePoint coverage.** Audit edtech vendor pages and school-portal landing pages with Rules asserting no advertising tracker fires. Use the FERPA pattern as the starting template; layer state-specific terms (e.g., California's SOPIPA defines "covered service" narrowly).

## International privacy laws

International coverage expands in PR #3. The current state (PR #2 baseline):

### GDPR (European Union)

**What it requires.** Lawful basis for processing personal data, transparent disclosure of vendors and purposes, the ability to refuse non-essential processing, and demonstrable accountability.

**ObservePoint coverage.**

- Run separate Web Audits for "Accept All," "Reject All," and the GPC signal, all on the same set of pages.
- Attach a Rule that asserts no advertising or analytics tags fire under "Reject All" or under GPC.
- Use the Cookies Privacy Compliance Report to inventory every cookie, classify it (essential, analytics, marketing), and flag anything set before consent.
- Use the Domains & Geo Privacy Report to enumerate every vendor receiving data and the country it's routed to.

**Doesn't cover.** Lawful-basis documentation, Data Protection Impact Assessments, Article 30 records of processing, Data Subject Access Request workflows. Those live in your privacy program, not in a scanner.

### LGPD (Brazil)

**What it requires.** Consent and lawful basis for processing, similar in spirit to GDPR but with its own list of data subject rights.

**ObservePoint coverage.** Same audit pattern as GDPR. Run Reject-All and Accept-All variants; validate vendors and cookies; inventory data flows. The reports that satisfy a GDPR auditor will satisfy an ANPD (the Brazilian regulator) auditor too.

### PIPEDA (Canada)

**What it requires.** Meaningful consent and accountability for personal information handling.

**ObservePoint coverage.** Cookie inventory, consent-state audits, vendor disclosure. Lighter regulatory cadence than GDPR; the same audit data is sufficient evidence.

### India's DPDP Act and Rules

**What it requires.** Notice and consent for personal data processing, with explicit rights for data principals and obligations for data fiduciaries. The implementing Rules were approved in late 2025 and the regime is moving into active enforcement in 2026.

**ObservePoint coverage.** Run audits in the India region (geo-routed if available, or with an India IP via VPN allowlist), validate consent capture and vendor disclosure, and inventory data flows leaving India. Treat the GDPR template as the starting point and adjust for the specific notice and grievance language the DPDP Act requires.

## Privacy signals and frameworks

### Global Privacy Control (GPC)

**What it is.** A browser-level signal that broadcasts "do not sell or share" on every request. Honored by the laws of 12+ U.S. states (see the state matrix above); broader rollout pending.

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
| CCPA / CPRA | Three-audit setup (default + opt-out + GPC) | Cookies Privacy Compliance, Rule Summary | Weekly |
| U.S. state laws (Colorado, Connecticut, Virginia, Utah, Texas, Oregon, Montana, Delaware, Iowa, Nebraska, NH, NJ, Minnesota, Maryland, Tennessee, Indiana, Kentucky, Rhode Island) | Three-audit setup, GPC variant where required | Cookies Privacy Compliance, Rule Summary | Weekly |
| LGPD, PIPEDA, DPDP | Web Audits + consent-state variants | Cookies Privacy Compliance | Weekly |
| HIPAA | Web Audits on PHI-bearing URLs + Rules + PII scan | Tag & Variable Rules Report, PII scan output | Daily on PHI areas |
| GLBA | Web Audits on logged-in financial flows + PII scan with custom regex | Tag & Variable Rules Report, PII scan output | Weekly |
| COPPA / COPPA 2.0 | Web Audits with age-gate Journey | Tag & Variable Rules Report | Daily on kids' areas |
| FERPA + state student data laws | Web Audits on student-portal URLs + PII scan | Tag & Variable Rules Report | Weekly |
| Washington MHMDA | Web Audits on health-adjacent URLs + PII scan | Tag & Variable Rules Report, PII scan output | Weekly |
| Nevada SB 370, CT health adds | Same pattern as MHMDA | Tag & Variable Rules Report | Weekly |
| Colorado AI Act | Web Audits with AI-disclosure Rules | Tag & Variable Rules Report | Weekly |
| Texas RAIGA | Web Audits with AI-disclosure Rules | Tag & Variable Rules Report | Weekly |
| NYC LL 144 | Web Audits on careers / apply pages | Tag & Variable Rules Report | Weekly |
| California AADC | Web Audits on children-likely-accessed pages | Tag & Variable Rules Report | Daily |
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

Most of items 1–4 can be exported from the API or pulled via `mcp__ObservePoint__export_report`. Item 5 lives in the activity log in the app. Bundle the lot as a quarterly PDF + CSV archive; that's the typical evidence pack format.

Full template lives in `references/consulting-deliverables.md`.

## What this file deliberately does not do

- **Legal advice.** ObservePoint produces evidence; lawyers decide whether the evidence is sufficient for a specific jurisdiction.
- **Roadmap projection.** Regulations change. Re-verify the dates in this file against current regulator guidance before using them in a customer commitment.
- **Vendor risk assessments.** Beyond identifying which vendors receive data, ObservePoint does not vet the vendors themselves.

---

*Last verified: 2026-06-03*
