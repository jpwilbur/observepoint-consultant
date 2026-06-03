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
  - [EU and UK](#eu-and-uk)
    - [GDPR](#gdpr-european-union), [ePrivacy](#eprivacy-directive-european-union), [EU AI Act](#eu-ai-act), [DSA](#digital-services-act-dsa), [DMA](#digital-markets-act-dma), [Data Act](#data-act-eu), [NIS2](#nis2-directive), [UK GDPR + DPA 2018](#uk-gdpr--dpa-2018), [PECR](#pecr-privacy-and-electronic-communications-regulations-uk)
  - [Latin America](#latin-america)
    - [LGPD (Brazil)](#lgpd-brazil), [Argentina](#argentina-personal-data-protection-law), [Mexico LFPDPPP](#mexico-lfpdppp), [Chile](#chile), [Colombia](#colombia)
  - [APAC](#apac)
    - [India DPDP](#india-dpdp-act-and-rules), [China PIPL](#china-pipl), [Singapore PDPA](#singapore-pdpa), [Japan APPI](#japan-appi), [South Korea PIPA](#south-korea-pipa), [Thailand PDPA](#thailand-pdpa), [Philippines DPA](#philippines-dpa), [Indonesia PDP](#indonesia-pdp), [Vietnam PDPL](#vietnam-pdpl), [Australia](#australia-privacy-act), [New Zealand](#new-zealand-privacy-act)
  - [Canada](#canada)
    - [PIPEDA](#pipeda-federal-canada), [Quebec Law 25](#quebec-law-25), [Proposed CPPA](#proposed-cppa-federal-canada)
  - [Middle East and Africa](#middle-east-and-africa)
    - [UAE PDPL](#uae-pdpl), [Saudi PDPL](#saudi-pdpl), [Bahrain PDPL](#bahrain-pdpl), [Israel](#israel-privacy-protection-law), [South Africa POPIA](#south-africa-popia), [Kenya](#kenya-data-protection-act), [Nigeria NDPA](#nigeria-ndpa)
- [Privacy signals and frameworks](#privacy-signals-and-frameworks)
  - [GPC](#global-privacy-control-gpc), [UOOM](#universal-opt-out-mechanism-uoom), [IAB TCF](#iab-transparency-and-consent-framework-tcf), [IAB GPP](#iab-global-privacy-platform-gpp), [Google Consent Mode v2](#google-consent-mode-v2), [Apple ATT](#apple-app-tracking-transparency-att), [Privacy Sandbox](#privacy-sandbox-chrome)
- [Voluntary standards and frameworks](#voluntary-standards-and-frameworks)
  - [PCI DSS 4.0](#pci-dss-40--client-side-script-integrity-requirements-643-and-1161), [NIST Privacy Framework](#nist-privacy-framework), [ISO/IEC 27701](#isoiec-27701)
- [Accessibility](#accessibility-not-technically-privacy-but-the-same-audit-motion)
- [Coverage matrix](#coverage-matrix)
- [Out-of-scope laws](#out-of-scope-laws)
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

Organized by region. Each region opens with the most-asked-about regulations (Tier 2 — full entry) followed by shorter Tier 3 entries for completeness.

## EU and UK

### GDPR (European Union)

**Status.** In force since May 2018. Enforcement by national Data Protection Authorities (DPAs); coordinated cases via the European Data Protection Board. Recent context: the EU's Digital Omnibus Package (late 2025) proposed targeted simplifications to GDPR, particularly around AI-era data uses; final adoptions are landing through 2026.

**What it requires.** Lawful basis for processing personal data, transparent disclosure of vendors and purposes, the ability to refuse non-essential processing, and demonstrable accountability.

**ObservePoint coverage.**

- Run separate Web Audits for "Accept All," "Reject All," and the GPC signal, all on the same set of pages. `mcp__ObservePoint__setup_compliance_monitoring(regulation="ccpa", domain=...)` produces the right three-audit shape; rename them for the EU context.
- Attach Rules that assert no advertising or analytics tags fire under "Reject All" or under GPC.
- Use `compare_consent_states` to surface the actual delta between consent variants.
- Use the Cookies Privacy Compliance Report to inventory every cookie, classify it (essential, analytics, marketing), and flag anything set before consent.
- Use the Domains & Geo Privacy Report to enumerate every vendor receiving data and the country it's routed to — Article 44 cross-border-transfer questions live here.

**Doesn't cover.** Lawful-basis documentation, Data Protection Impact Assessments, Article 30 records of processing, Data Subject Access Request workflows. Those live in your privacy program, not in a scanner.

### ePrivacy Directive (European Union)

**Status.** In force since 2002, last amended 2009 ("Cookie Law"). Predates GDPR and remains independently enforceable. The long-promised ePrivacy *Regulation* (which would replace it) is still in negotiation as of mid-2026.

**What it requires.** Prior informed consent for any non-essential cookie or tracking technology — irrespective of GDPR. Member states transpose into national law (UK's PECR, Germany's TTDSG, Italy's Cookie Guidelines, etc.).

**ObservePoint coverage.** The "Reject All" baseline audit doubles as ePrivacy evidence — if no non-essential tag fires before consent, the ePrivacy bar is met. Pair with a CMP banner inspection to confirm the banner explicitly asks for cookie consent (ePrivacy) rather than just GDPR consent (broader notion).

### EU AI Act

**Status.** Adopted 2024. Prohibited practices (Article 5) in force from February 2 2025; general-purpose AI provisions from August 2 2025; **Article 50 transparency obligations from August 2 2026**; high-risk AI obligations from August 2 2027. Enforcement by national AI authorities and the European AI Office.

**What it requires.**

- **Article 5 (prohibited practices):** social scoring by public authorities, certain emotion-recognition uses, untargeted face-image scraping.
- **Article 50 (transparency, August 2026):** mandatory labels for AI-generated content used in marketing; disclosure that users are interacting with an AI chatbot; deepfake labeling.
- **High-risk AI (Annex III):** impact assessments, human oversight, technical documentation. Marketing/advertising AI generally not high-risk unless used for credit scoring, employment, or essential-services decisions.

**ObservePoint coverage.**

- Article 50: validate that marketing pages containing AI-generated copy or imagery carry the required disclosure. Build a Rule that asserts a specific data-layer flag (`page.ai_generated = true`) is paired with a visible disclosure element in the DOM. Audit at scale across the marketing site.
- Article 5 prohibited practices: out of scope for a website scanner. That's a use-case review, not a deployment check.

**Caveat.** ObservePoint validates the *disclosure*; it cannot determine whether content actually was AI-generated. That classification is upstream.

### Digital Services Act (DSA)

**Status.** In force since February 17 2024 for all online platforms in the EU. Enforcement by national Digital Services Coordinators + the European Commission directly for Very Large Online Platforms (VLOPs).

**What it requires (for most websites).** Mandatory notice-and-action mechanisms for illegal content, transparency in advertising (mandatory ad-library disclosures), restrictions on targeted advertising to minors and on sensitive-data-based targeting, mandatory recommender-system transparency.

**ObservePoint coverage — narrow.**

- Validate that the website's "report illegal content" / notice-and-action UI is present and reachable from the relevant pages.
- Audit advertising-related pages with Rules asserting no targeted-advertising tag fires on URLs likely associated with minors (often the same audit setup as COPPA / state student data laws).
- Check that the website surfaces the required ad-transparency disclosures and recommender-system explanations where applicable.

**Doesn't cover.** Internal moderation processes, transparency reports, vetted-researcher access to data. Those are program work.

### Digital Markets Act (DMA)

**Status.** In force since 2023, enforcement against designated gatekeepers from March 7 2024.

**What it requires.** Targets a small number of designated gatekeepers (Alphabet, Amazon, Apple, Meta, Microsoft, ByteDance, Booking.com as of 2026). Restricts self-preferencing, combining data across services without consent, sideloading restrictions, and ad-tech tying.

**ObservePoint coverage — very narrow.** Most ObservePoint customers are not gatekeepers. If you ARE a designated gatekeeper, web auditing helps validate the technical consent flows the DMA requires for cross-service data combination — but the bulk of DMA compliance is product/architecture work, not website tracking.

### Data Act (EU)

**Status.** Adopted 2023, fully applicable from **September 12 2025**.

**What it requires.** Primarily B2B — manufacturers of connected products and providers of related services must allow users to access and share data generated by those products. Also adds protections against switching-fees in cloud service contracts.

**ObservePoint coverage — minimal.** The Data Act is largely outside website-tracking scope. For consumer-facing pages explaining data-portability rights under the Act, validate the disclosure UI exists.

### NIS2 Directive

**Status.** Transposition deadline October 17 2024; most member states' national laws in force by 2025-2026 (Germany's NIS2UmsuCG, Italy's NIS2 decree, etc.).

**What it requires.** Cybersecurity requirements for "essential" and "important" entities across 18 sectors (energy, transport, finance, healthcare, etc.). Includes incident reporting, supply-chain security, and management accountability.

**ObservePoint coverage — narrow but real.** For NIS2-covered entities, the supply-chain-security obligation includes vendor inventories. ObservePoint's Domains & Geo Privacy Report enumerates every third-party domain on the website — that's part of the digital supply chain. Use it as the technical inventory feeding into NIS2 risk assessments.

### UK GDPR + DPA 2018

**Status.** UK GDPR is the post-Brexit retained version of GDPR (in force since January 1 2021). Paired with the Data Protection Act 2018 (DPA 2018), which adds UK-specific provisions. The Data Protection and Digital Information Act 2024 (DPDI Act) made targeted amendments to both — including narrower consent requirements for some analytics cookies and an updated regime for international transfers.

**What it requires.** Substantively very similar to EU GDPR. Where it differs in 2026: the DPDI Act's "low-risk research" carve-outs, the UK's separate adequacy regime for international transfers, and the Information Commissioner's Office (ICO) approach (often more pragmatic than continental DPAs).

**ObservePoint coverage.** Same audit pattern as EU GDPR. The reports that satisfy a continental DPA will satisfy the ICO. Watch the DPDI Act's evolving analytics-cookie guidance — if some categories shift to a legitimate-interest basis, the consent-state audits remain useful but the Rules around what may fire pre-consent change.

### PECR (Privacy and Electronic Communications Regulations, UK)

**Status.** UK's ePrivacy transposition. In force since 2003, amended multiple times.

**What it requires.** Consent before storing or accessing information on a user's device (cookies, beacons, etc.) — except for "strictly necessary" purposes. Stricter than UK GDPR's broader consent rules for the specific cookie-tracking context.

**ObservePoint coverage.** Reject-All audit is the technical proof. PECR breach is one of the easier ICO enforcement triggers — keep the audit running weekly.

## Latin America

### LGPD (Brazil)

**Status.** In effect since September 2020; enforcement by ANPD (Autoridade Nacional de Proteção de Dados). Active enforcement through 2025-2026.

**What it requires.** Consent and lawful basis for processing, similar in spirit to GDPR but with its own list of data subject rights and a Brazilian regulator with growing teeth.

**ObservePoint coverage.** Same audit pattern as GDPR. Run Reject-All and Accept-All variants; validate vendors and cookies; inventory data flows. The reports that satisfy a GDPR auditor will satisfy an ANPD auditor too.

**Gotcha.** ANPD has been focused on data-processing-agent disclosure — every vendor receiving personal data needs to be documented. Use the Domains & Geo Privacy Report as your living inventory.

### Argentina (Personal Data Protection Law)

**Status.** Law 25.326 from 2000; major reform under discussion through 2025-2026 to align with GDPR. Enforcement by the AAIP (Agencia de Acceso a la Información Pública).

**What it requires (current).** Consent-based processing with explicit rights for data subjects; sectoral rules for sensitive categories. Argentina has had EU adequacy status since 2003, kept after Brexit and post-2018 GDPR.

**ObservePoint coverage.** Standard consent-state audit pattern. Lighter regulatory cadence than Brazil or Chile.

### Mexico (LFPDPPP)

**Status.** Federal Law on Protection of Personal Data Held by Private Parties, in force since 2010. Enforcement by INAI (now restructured under the Anti-Corruption and Government Effectiveness Secretariat as of 2025).

**What it requires.** Privacy notice ("aviso de privacidad") with specific content requirements; consent for sensitive data; data-subject rights.

**ObservePoint coverage.** Validate that the privacy notice link is present on every page (a Rule that asserts the `aviso de privacidad` element exists). Standard consent-state audit for cookie / tracking validation.

### Chile

**Status.** Law 19.628 from 1999, with a comprehensive update (closer to GDPR shape) passed in 2024 — major provisions effective 2026.

**What it requires (after 2026 reform).** Consent for processing, data-subject rights aligned with GDPR, sensitive-data special protections, and a newly empowered Agency for the Protection of Personal Data.

**ObservePoint coverage.** Standard consent-state audit pattern. Treat as GDPR-aligned going forward.

### Colombia

**Status.** Statutory Law 1581 of 2012; enforcement by the SIC (Superintendency of Industry and Commerce).

**What it requires.** Authorization (consent) for data processing; registration of databases; cross-border transfer rules.

**ObservePoint coverage.** Standard consent-state audit pattern. Vendor inventory (Domains & Geo Privacy Report) feeds the cross-border-transfer documentation.

## APAC

### India DPDP Act and Rules

**Status.** Digital Personal Data Protection Act enacted August 2023. Implementing Rules approved November 2025. Phased enforcement is rolling through 2026; the soft-enforcement window ends around late 2026 and full enforcement begins thereafter.

**What it requires.** Notice and consent for personal data processing, with explicit rights for "data principals" and obligations for "data fiduciaries." Cross-border-transfer rules will be issued by the Data Protection Board of India.

**ObservePoint coverage.** Run audits geo-routed from an India location (or with an India IP via VPN allowlist), validate consent capture and vendor disclosure, and inventory data flows leaving India. Treat the GDPR template as the starting point; adjust the consent banner copy for the specific notice and grievance language the DPDP Act and Rules require.

### China PIPL

**Status.** Personal Information Protection Law in force since November 2021. Enforcement by the Cyberspace Administration of China (CAC). Companion laws: Cybersecurity Law (CSL, 2017), Data Security Law (DSL, 2021).

**What it requires.** Consent-based processing (with separate consent for sensitive data); strict cross-border transfer rules (security assessment, standard contractual clauses, or certification); designated representative for foreign processors; data-localization requirements for certain categories.

**ObservePoint coverage.**

- Standard consent-state audit pattern for the consent dimension.
- Cross-border transfer dimension: use the Domains & Geo Privacy Report to inventory every vendor receiving data from mainland-China visitors. Flag any non-China endpoint as needing a documented transfer mechanism (SCC, security assessment, or certification).
- Sensitive-data dimension: separate Rules on pages where sensitive personal information may be collected (financial info, health, biometric, location of a precise type, identification documents) asserting no third-party tracker fires before separate consent.

**Gotcha.** PIPL's extraterritorial reach is real — foreign websites processing Chinese-resident data are in scope. Don't assume you can ignore PIPL just because your servers are abroad.

### Singapore PDPA

**Status.** In force since 2014; significant amendments in 2020 (mandatory breach notification, data portability). Enforcement by the Personal Data Protection Commission (PDPC).

**What it requires.** Consent-based processing with several exceptions (legitimate interests, business improvement, research); data-subject rights; specific Do Not Call provisions for marketing.

**ObservePoint coverage.** Standard consent-state audit pattern. The DNC list applies to phone/SMS marketing; for web tracking, the consent dimension is the audit's focus.

### Japan APPI

**Status.** Act on the Protection of Personal Information, last major revision 2022. Enforcement by the Personal Information Protection Commission (PPC).

**What it requires.** Consent for cross-border transfers; sensitive-data special protections; opt-out for non-consensual sharing in some cases; pseudonymized-data category.

**ObservePoint coverage.** Standard consent-state audit pattern. Cross-border transfer dimension covered by the Domains & Geo Privacy Report.

### South Korea PIPA

**Status.** Personal Information Protection Act, last major amendment September 2023. Enforcement by the Personal Information Protection Commission (PIPC).

**What it requires.** Opt-in consent for any personal data processing (one of the strictest consent regimes globally); cross-border transfer rules; data-subject rights; mandatory data protection officer for certain entities.

**ObservePoint coverage.** Korean opt-in regime means the Reject-All audit (proving nothing non-essential fires by default) is especially important. Standard audit pattern; cross-border transfer dimension via the Domains & Geo Privacy Report.

### Thailand PDPA

**Status.** Personal Data Protection Act, fully effective since 2022. Enforcement by the PDPC.

**What it requires.** Consent-based processing aligned with GDPR shape; lawful bases including legitimate interest; data-subject rights.

**ObservePoint coverage.** Standard consent-state audit pattern.

### Philippines DPA

**Status.** Republic Act 10173, in force since 2012. Enforcement by the National Privacy Commission (NPC).

**What it requires.** Consent or lawful basis; data subject rights; mandatory breach notification; Data Protection Officer requirement for many entities.

**ObservePoint coverage.** Standard consent-state audit pattern.

### Indonesia PDP

**Status.** Personal Data Protection Law (UU PDP), passed October 2022; the two-year transition window ended October 2024 — fully enforceable since.

**What it requires.** Consent-based or contract-based processing; data-subject rights; cross-border transfer rules; mandatory DPO; significant criminal penalties (not just administrative).

**ObservePoint coverage.** Standard consent-state audit pattern. Treat the cross-border transfer dimension carefully — Indonesia's regulations are still evolving and the criminal-penalty exposure makes vendor inventory accuracy more critical than usual.

### Vietnam PDPL

**Status.** Personal Data Protection Decree (No. 13/2023) since 2023; comprehensive PDPL adopted 2025, taking effect 2026.

**What it requires (under 2026 PDPL).** Consent-based processing with strict cross-border transfer registration, mandatory data protection officer for processors, breach notification.

**ObservePoint coverage.** Standard consent-state audit pattern. Cross-border-transfer registration means the Domains & Geo Privacy Report becomes a critical input to the regulatory filing.

### Australia Privacy Act

**Status.** Privacy Act 1988, with significant reforms enacted in 2024 and additional reforms in negotiation through 2026 (the "Privacy Act Review" recommendations are being implemented in tranches). Enforcement by the OAIC (Office of the Australian Information Commissioner).

**What it requires.** Australian Privacy Principles (APPs) cover collection, use, disclosure, access. Mandatory breach notification since 2018. 2024-2026 reforms add explicit consent requirements, broader definition of personal information, and a statutory tort for serious invasions of privacy.

**ObservePoint coverage.** Standard consent-state audit pattern. The 2024+ reforms moved Australia closer to GDPR-shape, so the GDPR template fits well. Watch the statutory tort — it creates a private right of action and is a new enforcement vector.

### New Zealand Privacy Act

**Status.** Privacy Act 2020, in force since December 2020. Enforcement by the Office of the Privacy Commissioner.

**What it requires.** Privacy Principles similar to Australian APPs; mandatory breach notification; restrictions on disclosure outside NZ.

**ObservePoint coverage.** Standard consent-state audit pattern. Lighter enforcement than Australia; reuse the Australia setup.

## Canada

### PIPEDA (federal Canada)

**What it requires.** Personal Information Protection and Electronic Documents Act — meaningful consent and accountability for personal information handling in commercial activity.

**Status.** In force since 2001. The long-pending Bill C-27 (which would replace PIPEDA with the Consumer Privacy Protection Act and add an AI and Data Act) is making slow progress through Parliament; as of June 2026, PIPEDA remains the active federal framework with a CPPA replacement not yet in force.

**ObservePoint coverage.** Cookie inventory, consent-state audits, vendor disclosure. Lighter regulatory cadence than GDPR; the same audit data is sufficient evidence for the federal Privacy Commissioner.

### Quebec Law 25

**Status.** Law modernizing privacy in the private sector, fully effective since September 2024. Enforcement by the Commission d'accès à l'information du Québec (CAI). This is the most rigorous Canadian privacy regime — substantially stricter than PIPEDA on consent, transparency, and AI-driven decisions.

**What it requires.** Express, freely given, informed consent for collection beyond essentials; explicit consent for use of personal information for purposes other than the original collection purpose; mandatory privacy impact assessments; explicit notice when automated decision-making is used; cross-border transfer assessment requirements; significant administrative monetary penalties (up to CAD $10M or 2% of worldwide turnover).

**ObservePoint coverage.**

- Standard consent-state audit pattern; Quebec is GPC-friendly in spirit although GPC isn't yet mandated.
- For automated-decision-making transparency: validate that pages where automated decisions affect users carry the required disclosure (similar pattern to Colorado AI Act).
- Cross-border transfer dimension: use the Domains & Geo Privacy Report to identify where Quebec residents' data is going. Any non-Quebec endpoint requires a documented transfer assessment.

**Gotcha.** Quebec's "freely given, informed" consent standard is stricter than CCPA's opt-out model. Pre-ticked checkboxes are explicitly invalid. Validate consent banner UX: separate buttons, no dark patterns, clear consequences for each choice.

### Proposed CPPA (federal Canada)

**Status.** Part of Bill C-27. Not in force as of June 2026. If/when enacted, will replace PIPEDA with a GDPR-shape federal framework.

**ObservePoint coverage when in force.** GDPR-shape audit pattern. Watch the bill for finalization.

## Middle East and Africa

### UAE PDPL

**Status.** Federal Decree-Law No. 45 of 2021. Detailed implementing regulations have rolled out through 2024-2025.

**What it requires.** Consent for processing (with several lawful-basis exceptions); data-subject rights aligned with GDPR; cross-border transfer rules; designated Data Protection Office for some entities. UAE PDPL is distinct from the DIFC Data Protection Law (Dubai International Financial Centre, GDPR-aligned) and the ADGM Data Protection Regulations (Abu Dhabi Global Market).

**ObservePoint coverage.** Standard consent-state audit pattern. Watch the multi-jurisdiction wrinkle — companies operating in mainland UAE and DIFC/ADGM may need separate compliance flows.

### Saudi PDPL

**Status.** Personal Data Protection Law, in force March 2023 with full enforcement from September 2024. Enforcement by SDAIA (Saudi Data and Artificial Intelligence Authority).

**What it requires.** Consent-based processing with sensitive-data special handling; data-localization requirements (data of Saudi residents must be processed within the Kingdom unless specifically authorized); mandatory Data Protection Officer; cross-border transfer rules with prior authorization.

**ObservePoint coverage.**

- Standard consent-state audit pattern.
- Data-localization dimension: use the Domains & Geo Privacy Report to identify where Saudi visitors' data is going. Any non-KSA destination requires a documented authorization or transfer mechanism.

**Gotcha.** The data-localization requirement is the biggest practical hurdle — many Western MarTech stacks route data through US or EU endpoints. Surface this in the audit data so legal can plan.

### Bahrain PDPL

**Status.** In force since 2019. Enforcement by the Personal Data Protection Authority.

**What it requires.** Consent for processing; data-subject rights; cross-border transfer rules.

**ObservePoint coverage.** Standard consent-state audit pattern.

### Israel Privacy Protection Law

**Status.** Privacy Protection Law from 1981. Major amendment (Amendment 13) passed July 2024, fully effective August 2025 — substantially modernizes the regime to GDPR-style requirements. Enforcement by the Privacy Protection Authority (PPA).

**What it requires (after Aug 2025).** Explicit consent for processing; data-subject rights (access, correction, deletion); mandatory breach notification; mandatory Data Protection Officer for many entities; significantly increased enforcement powers.

**ObservePoint coverage.** GDPR-shape audit pattern. Israel had EU adequacy status since 2011; the 2024 amendment preserved that. Treat Israel similarly to a continental EU jurisdiction for audit-setup purposes.

### South Africa POPIA

**Status.** Protection of Personal Information Act, fully effective July 2021. Enforcement by the Information Regulator.

**What it requires.** Consent (or other lawful basis) for processing; data-subject rights; mandatory Information Officer registration; cross-border transfer rules; mandatory breach notification.

**ObservePoint coverage.** Standard consent-state audit pattern.

### Kenya Data Protection Act

**Status.** In force since November 2019. Enforcement by the Office of the Data Protection Commissioner (ODPC).

**What it requires.** Consent or lawful basis; data-subject rights; mandatory data-controller/processor registration; cross-border transfer rules.

**ObservePoint coverage.** Standard consent-state audit pattern. ODPC has been actively enforcing through 2025-2026, with public-facing fines that signal increasing maturity.

### Nigeria NDPA

**Status.** Nigeria Data Protection Act 2023, replaced the earlier Nigeria Data Protection Regulation. Enforcement by the Nigeria Data Protection Commission (NDPC).

**What it requires.** Consent-based processing; data-subject rights; cross-border transfer rules; mandatory Data Protection Officer for some entities.

**ObservePoint coverage.** Standard consent-state audit pattern.

## Privacy signals and frameworks

Standardized signals and industry frameworks that ride on top of (and across) the regulations above. The Rules engine work for these is essentially the same as the regulation-level work — these are the technical primitives that make compliance auditable.

### Global Privacy Control (GPC)

**What it is.** A browser-level signal that broadcasts "do not sell or share" on every request. Honored by the laws of 12+ U.S. states (see the state matrix above); broader rollout pending.

**ObservePoint coverage.** Toggle "Send GPC Signal" on an audit. The synthetic browser broadcasts the GPC header on every request. Pair with Rules that assert no covered tags fire when GPC is on. This is the cleanest way to prove your site honors GPC end-to-end. `compare_consent_states(domain=..., leftState="default", rightState="gpc")` produces the canonical side-by-side.

### Universal Opt-Out Mechanism (UOOM)

**What it is.** A regulatory concept (rather than a specific signal) for any browser-level opt-out mechanism that a state law honors. Colorado's CPA explicitly requires recognition of "universal opt-out mechanisms"; Connecticut, California, and a growing list of states have similar provisions. GPC is the dominant UOOM today; future signals (e.g., a successor to GPC, or a browser-vendor implementation) would also qualify.

**ObservePoint coverage.** Treat UOOM the same as GPC for now — they're functionally the same audit toggle. Track regulator guidance: if a state authority recognizes a new UOOM signal, the audit needs a fourth consent variant.

### IAB Transparency and Consent Framework (TCF)

**What it is.** An industry-standard format for encoding consent strings that AdTech vendors can decode.

**Current version: 2.3.** TCF 2.3 was published in 2024 with a hard cutover deadline of **February 28, 2026** — TC strings generated after that date in the 2.2 format are invalid; the disclosedVendors segment is now mandatory. Existing TC strings from before that date remain valid.

**ObservePoint coverage.** Decode TC strings from cookies, validate they meet the current version requirements, assert correct vendor disclosure. Pair with audits per consent state to validate that the string actually reflects the user's choice.

### IAB Global Privacy Platform (GPP)

**What it is.** A multi-jurisdiction consent-string standard published by the IAB Tech Lab. Designed to carry per-jurisdiction signals (US National, US-CA, US-VA, US-CO, US-CT, US-UT, and more) in one string, so a single integration can satisfy multiple state laws. Current version (mid-2026): GPP 1.x with active per-jurisdiction sections.

**ObservePoint coverage.** Validate GPP string presence in the `usnat`, `usca`, and similar cookie names; decode the per-section flags to confirm they match the user's actual consent state. The TCF audit pattern extends here: per-consent-state Rules assert the GPP section's flags match.

### Google Consent Mode v2

**What it is.** Google's mechanism for adjusting tag behavior based on consent. Four categories: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`.

**ObservePoint coverage.** Validate that Consent Mode v2 signals propagate correctly from the CMP to Google tags. Use Rules to assert that under Reject-All, `ad_storage` is "denied" and the resulting tags use the no-cookie pings instead of standard collection. The Cookies Privacy Compliance Report shows which Google tags set what cookies under each consent state — that's your evidence of correct propagation.

### Apple App Tracking Transparency (ATT)

**What it is.** Apple's iOS framework requiring apps to ask users for permission before accessing the IDFA (Identifier for Advertisers) for cross-app tracking. In effect since iOS 14.5 (April 2021).

**ObservePoint coverage — narrow.** ObservePoint is a web platform and does not test native iOS apps directly (see `references/limitations.md` → "Native mobile apps"). What it can do: when a website uses Apple SDKs, Smart App Banner pixels, or similar bridge mechanisms, audit the resulting requests to detect IDFA-related parameters. For native-app testing, capture a HAR from the device and process via HAR Analyzer; for the website-side of an iOS app ecosystem, the standard audit pattern applies.

### Privacy Sandbox (Chrome)

**What it is.** Google's Chrome initiative replacing third-party cookies and cross-site tracking with privacy-preserving alternatives. Topics API was retired (October 2025). Surviving APIs as of mid-2026: Protected Audience API (FLEDGE successor), Attribution Reporting API, CHIPS (Cookies Having Independent Partitioned State), FedCM (Federated Credential Management), Private State Tokens.

**ObservePoint coverage.**

- Inventory which Privacy Sandbox APIs your site uses (Web Audits surface the script calls).
- Validate CHIPS-partitioned cookie usage on pages with cross-site embeds.
- Audit Protected Audience auctions for participation correctness.
- For sites still relying on third-party cookies (which remain functional in Chrome but are heavily blocked by browser settings and ad-blockers), the Domains & Geo Privacy Report surfaces vendor dependency on legacy tracking.

**Caveat.** Privacy Sandbox is a moving target; verify the API set against current Chromium documentation before claiming coverage of a specific API.

## Voluntary standards and frameworks

These aren't laws — they're voluntary standards organizations and enterprises adopt as governance scaffolding. ObservePoint helps with the website-tracking-relevant slice of each.

### PCI DSS 4.0 — client-side script integrity (requirements 6.4.3 and 11.6.1)

**Status.** PCI DSS v4.0 published 2022; the future-dated requirements (originally targeted March 2025) are now mandatory across the payment industry. Enforcement by acquiring banks and the PCI Security Standards Council via QSAs.

**What it requires (tracking-relevant).**

- **Requirement 6.4.3:** Manage all scripts loaded on payment pages — maintain an inventory, document business justification, ensure authorization of each script.
- **Requirement 11.6.1:** Detect unauthorized modification of payment-page scripts and HTTP headers; alert on change.

These two requirements turned PCI compliance into a tracking-script governance problem — exactly the problem ObservePoint solves.

**ObservePoint coverage.**

- **6.4.3 — script inventory:** Web Audits on payment pages produce the full script inventory automatically. Pair with the Tag & Cookie Debugger for on-demand inspection. The Domains & Geo Privacy Report enumerates which third-party domains your payment page calls.
- **6.4.3 — script authorization:** maintain a Rule asserting only approved-vendor scripts fire on `/checkout*`, `/payment*`, `/cart*` URL patterns. New script appearing = Rule failure = investigation trigger.
- **11.6.1 — change detection:** `find_anomalies(auditId, metric="tags", thresholdPct=10)` and `find_anomalies(auditId, metric="request-domains", thresholdPct=10)` on the payment-page audit. `find_first_observed` tells you when an unauthorized script first appeared in the audit history. Alerts route to security ops.

**Doesn't cover.** Payment terminal or POS-side controls; SAQ documentation; ROC narrative writing.

### NIST Privacy Framework

**Status.** Version 1.0 published 2020 by NIST; voluntary use. Tennessee's TIPA explicitly makes a "documented NIST-aligned privacy program" an affirmative defense to state privacy claims, which has increased real-world adoption.

**What it provides.** A risk-based framework structured into five Functions (Identify-P, Govern-P, Control-P, Communicate-P, Protect-P), with implementation Tiers and Profiles. Aligns with the NIST Cybersecurity Framework.

**ObservePoint coverage — limited but real.** The Framework's data-mapping requirements (Identify-P function) benefit from ObservePoint's vendor / cookie / data-flow inventory. Use the Domains & Geo Privacy Report and Cookies Privacy Compliance Report as the technical inputs to the Framework's data-inventory work.

### ISO/IEC 27701

**Status.** ISO Privacy Information Management standard (extends ISO 27001). Certifiable by accredited bodies.

**What it provides.** Privacy Information Management System (PIMS) requirements — extends ISO 27001 with privacy-specific controls covering PII processing, consent management, data subject rights, vendor management.

**ObservePoint coverage — supports the operational evidence requirements.** A certified PIMS needs operational evidence of consent enforcement, data flow control, and vendor management. The same audit data that satisfies GDPR or CCPA evidence packs feeds ISO 27701 audits. Treat it as the certification-equivalent of the GDPR audit pattern.

## Accessibility (not technically privacy, but the same audit motion)

### WCAG 2.1 AA / European Accessibility Act

**What it requires.** Web content meeting the WCAG 2.1 AA conformance level, with the European Accessibility Act extending obligations across the EU for products and services in scope.

**ObservePoint coverage.** Web Audits include automated WCAG 2.1 AA scanning. The Accessibility Report and the new (2026) Accessibility Highlight Report show violations by severity and type. The Debugger added accessibility highlights in early 2026 for in-browser checks.

**Doesn't cover.** Manual review for things automation cannot test (color choice on photographs, semantic correctness of complex widgets, screen-reader user experience). Pair the scan with a manual review and lived-experience testing.

## Coverage matrix

Rows = every in-scope regulation / framework. Columns = the ObservePoint setup that produces evidence + the relevant MCP wrapper (where one applies). Use this matrix as the one-page reference when scoping a customer engagement.

### U.S. comprehensive

| Regulation | ObservePoint setup | Primary report | MCP wrapper hint | Schedule |
|---|---|---|---|---|
| CCPA / CPRA (California) | Three-audit setup (default + opt-out + GPC) + compare_consent_states + scan_audit_pii | Cookies Privacy Compliance, Rule Summary | `setup_compliance_monitoring(regulation="ccpa")` | Weekly |
| Colorado CPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual (CCPA template + Colorado banner) | Weekly |
| Connecticut CTDPA | Three-audit setup; GPC required since 2025 | Cookies Privacy Compliance | Manual | Weekly |
| Virginia VCDPA | Two-audit setup (default + opt-out); no GPC | Cookies Privacy Compliance | Manual | Weekly |
| Utah UCPA | Two-audit setup; no GPC | Cookies Privacy Compliance | Manual | Weekly |
| Texas TDPSA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |
| Oregon OCPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |
| Montana MCDPA | Three-audit setup; GPC required; no cure period after Oct 2026 | Cookies Privacy Compliance | Manual | Weekly |
| Delaware DPDPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |
| Iowa ICDPA | Two-audit setup; no GPC | Cookies Privacy Compliance | Manual | Weekly |
| Nebraska NDPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |
| NH NH-DPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |
| NJ NJDPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |
| Minnesota MCDPA | Three-audit setup + DPIA support via Domains report | Cookies Privacy Compliance | Manual | Weekly |
| Maryland MODPA | Three-audit setup; minor-targeting Rules | Cookies Privacy Compliance | Manual | Weekly |
| Tennessee TIPA | Three-audit setup; NIST-aligned evidence pack | Cookies Privacy Compliance | Manual | Weekly |
| Indiana ICDPA | Two-audit setup; no GPC | Cookies Privacy Compliance | Manual | Weekly |
| Kentucky KCDPA | Two-audit setup; no GPC | Cookies Privacy Compliance | Manual | Weekly |
| Rhode Island RIDTPPA | Three-audit setup; GPC required | Cookies Privacy Compliance | Manual | Weekly |

### U.S. sectoral, health, AI, kids

| Regulation | ObservePoint setup | Primary report | MCP wrapper hint | Schedule |
|---|---|---|---|---|
| HIPAA | Web Audits on PHI URLs + scan_audit_pii + Rules | Tag & Variable Rules, PII scan output | `scan_audit_pii` | Daily on PHI areas |
| GLBA | Web Audits on NPI flows + scan with customRegex | Tag & Variable Rules, PII scan output | `scan_audit_pii(customRegex=...)` | Weekly |
| COPPA / COPPA 2.0 | Age-gate Journey + Rules | Tag & Variable Rules | Manual | Daily on kids' areas |
| FERPA + state student data | Web Audits on student portal + scan_journey_pii canary | Tag & Variable Rules, PII scan output | `scan_journey_pii` | Weekly |
| Washington MHMDA | Health-context Web Audits + scan_audit_pii | Tag & Variable Rules, PII scan output | `scan_audit_pii` | Weekly |
| Nevada SB 370 | Same pattern as MHMDA | Tag & Variable Rules | `scan_audit_pii` | Weekly |
| CT health adds | Layered onto CTDPA audit | Tag & Variable Rules | Manual | Weekly |
| Colorado AI Act | AI-disclosure Rules on marketing pages | Tag & Variable Rules | Manual | Weekly |
| Texas RAIGA | AI-disclosure Rules | Tag & Variable Rules | Manual | Weekly |
| NYC LL 144 | Careers / apply page Rules | Tag & Variable Rules | Manual | Weekly |
| California AADC (where in force) | Children-likely-accessed page Rules | Tag & Variable Rules | Manual | Daily |
| State student data laws | Edtech / school-portal Rules | Tag & Variable Rules | Manual | Weekly |

### International

| Regulation | ObservePoint setup | Primary report | Schedule |
|---|---|---|---|
| GDPR (EU) | Three-audit setup + Domains & Geo for Article 44 | Cookies Privacy Compliance, Domains & Geo | Weekly + pre-deploy |
| ePrivacy Directive | Reject-All audit | Cookies Privacy Compliance | Weekly |
| EU AI Act | AI-disclosure Rules on marketing | Tag & Variable Rules | Weekly |
| DSA | Notice-UI + transparency Rules | Tag & Variable Rules | Weekly |
| DMA | Gatekeeper-specific (narrow audience) | Domains & Geo | Per release |
| Data Act | Disclosure UI Rules | Tag & Variable Rules | Per release |
| NIS2 | Vendor inventory feeding risk assessment | Domains & Geo | Weekly |
| UK GDPR + DPA 2018 | Same as GDPR | Cookies Privacy Compliance | Weekly |
| PECR (UK) | Reject-All audit | Cookies Privacy Compliance | Weekly |
| LGPD (Brazil) | Three-audit setup | Cookies Privacy Compliance | Weekly |
| Argentina PDPL | Standard consent-state audit | Cookies Privacy Compliance | Monthly |
| Mexico LFPDPPP | Privacy-notice Rule + consent audit | Tag & Variable Rules | Weekly |
| Chile (post-2026) | GDPR-aligned audit pattern | Cookies Privacy Compliance | Weekly |
| Colombia | Consent-state audit + cross-border inventory | Cookies Privacy Compliance | Weekly |
| India DPDP | Geo-routed consent audit | Cookies Privacy Compliance | Weekly |
| China PIPL | Consent + cross-border + sensitive-data Rules | Cookies Privacy Compliance, Domains & Geo | Weekly |
| Singapore PDPA | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Japan APPI | Consent-state audit + cross-border inventory | Cookies Privacy Compliance | Weekly |
| South Korea PIPA | Opt-in-strict Reject-All audit | Cookies Privacy Compliance | Weekly |
| Thailand PDPA | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Philippines DPA | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Indonesia PDP | Consent-state + cross-border inventory | Cookies Privacy Compliance | Weekly |
| Vietnam PDPL | Consent + cross-border registration | Cookies Privacy Compliance | Weekly |
| Australia Privacy Act | Consent-state audit | Cookies Privacy Compliance | Weekly |
| New Zealand Privacy Act | Consent-state audit | Cookies Privacy Compliance | Weekly |
| PIPEDA (Canada) | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Quebec Law 25 | Consent audit + ADM-disclosure Rules + cross-border inventory | Cookies Privacy Compliance, Domains & Geo | Weekly |
| UAE PDPL | Consent-state audit (split mainland/DIFC/ADGM) | Cookies Privacy Compliance | Weekly |
| Saudi PDPL | Consent + data-localization inventory | Cookies Privacy Compliance, Domains & Geo | Weekly |
| Bahrain PDPL | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Israel Privacy Law | GDPR-shape audit | Cookies Privacy Compliance | Weekly |
| South Africa POPIA | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Kenya DPA | Consent-state audit | Cookies Privacy Compliance | Weekly |
| Nigeria NDPA | Consent-state audit | Cookies Privacy Compliance | Weekly |

### Signals, frameworks, voluntary standards

| Signal / framework | ObservePoint setup | Primary report | Schedule |
|---|---|---|---|
| GPC | Web Audits with "Send GPC Signal" | Tag & Variable Rules | Weekly |
| UOOM (general) | Same as GPC for now | Tag & Variable Rules | Weekly |
| IAB TCF (current 2.3) | TC string decoding Rules | Cookies Privacy Compliance | Weekly |
| IAB GPP | GPP string decoding Rules | Cookies Privacy Compliance | Weekly |
| Google Consent Mode v2 | Per-consent-state Rules on Google tag payloads | Tag & Variable Rules | Weekly |
| Apple ATT | HAR Analyzer for native iOS bridges; web audit for Smart App Banner | HAR Analyzer | Per release |
| Privacy Sandbox | Tag inventory of Sandbox API calls | Tag Inventory | Weekly |
| PCI DSS 4.0 (6.4.3 / 11.6.1) | Payment-page audit + find_anomalies on tags/domains | Tag & Variable Rules + find_anomalies output | Daily on payment areas |
| NIST Privacy Framework | Vendor / cookie inventory as Identify-P input | Domains & Geo, Cookies Privacy Compliance | Quarterly review |
| ISO/IEC 27701 | Same audit data as GDPR feeds the PIMS certification | Cookies Privacy Compliance, Domains & Geo | Per audit cycle |
| WCAG 2.1 / 2.2 AA | Web Audits + accessibility scanning | Accessibility / Accessibility Highlight | Weekly |
| European Accessibility Act | Same as WCAG | Accessibility | Weekly |

## Out-of-scope laws

Laws that name websites or web tracking but where ObservePoint genuinely doesn't materially help. Naming them here so a user searching for the term gets a routing answer rather than silence.

| Law / topic | Why it's out of scope | Where to go instead |
|---|---|---|
| DSAR fulfillment workflows (right of access, deletion, correction) | These are program / workflow problems, not website-tracking problems. ObservePoint's scanner sees what fires; it doesn't fulfill consumer rights requests. | A privacy management platform (OneTrust DSAR, Securiti, DataGrail). |
| Employee data privacy laws (e.g., California Privacy Rights Act employee provisions) | The platform audits public-facing websites and customer journeys, not employee HR systems. | HR-system-specific compliance tools. |
| Marketing email content laws (CAN-SPAM, CASL) | These regulate the email itself — sender identification, opt-out wording, header accuracy. ObservePoint validates that links in marketing emails work and that landing pages track correctly; it doesn't validate the email content. | Email service provider compliance tools (Litmus, Email on Acid for rendering; ESP audit logs for opt-out compliance). |
| Telephone marketing (TCPA, DNC) | Phone/SMS marketing rules. Not website-tracking. | Outbound dialing compliance tools. |
| Section 230 / intermediary liability | Substantive law about hosting third-party content, not a tracking-compliance question. | Legal counsel. |
| Antitrust / competition law | Different specialty entirely. | Competition counsel. |
| Securities disclosure laws (e.g., SEC tracking-pixel disclosure) | When SEC enforcement touches website tracking, the substantive obligations live in disclosure rules, not in the scanner. ObservePoint can inventory the tracking that's happening; the disclosure obligation lives with legal. | Securities counsel; SEC EDGAR filing tools. |
| Pure data-broker laws (e.g., California Delete Act) | Regulates registered data brokers' database operations, not website tracking. | Data-broker-specific compliance tools. |

When a user asks about a law in this table, route them clearly. Saying "ObservePoint doesn't materially help with that, here's where to go" is more useful than reaching for an audit pattern that won't fit.

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
