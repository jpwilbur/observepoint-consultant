# Glossary

Terms used across ObservePoint, web governance, privacy, and the wider MarTech stack. Load this when the user uses a term you're not sure about, or when an answer needs a quick definition.

Alphabetical. Cross-references in **bold**.

## A

**AADC (Age Appropriate Design Code).** California law (2022) requiring default high-privacy settings for users likely under 18. Significant 9th Circuit injunction since 2024 has blocked enforcement of many provisions; partial revival in 2026. See the **privacy-compliance** skill.

**Accessibility Highlight Report.** An ObservePoint report (new in 2026) that surfaces WCAG 2.1 AA violations by severity and type. Companion to the broader Accessibility Report.

**ADA Title II.** The provision of the Americans with Disabilities Act covering state and local government services. The 2024 DOJ rule sets WCAG 2.1 AA as the technical standard for state/local government web content and mobile apps, phased by entity size. The accessibility hook for public-sector properties. See the **accessibility** skill.

**ADA Title III.** The provision of the Americans with Disabilities Act covering "places of public accommodation" — the basis for the dominant wave of private accessibility lawsuits and demand letters against commercial websites. See the **accessibility** skill.

**Alert.** A notification routed when a Rule fails or a threshold is crossed. Routes to Slack, Microsoft Teams, email, SMS, Jira, or a custom webhook.

**APPI (Act on the Protection of Personal Information).** Japan's national privacy law. Last major amendment 2022. Enforcement by the PPC (Personal Information Protection Commission).

**ARIA (Accessible Rich Internet Applications).** A W3C specification of HTML attributes (roles, states, properties) that convey the semantics of interactive UI to assistive technology. Misused ARIA is itself a common WCAG failure. See the **accessibility** skill.

**ATT (App Tracking Transparency).** Apple's iOS framework (in effect since iOS 14.5) requiring apps to obtain permission before accessing the IDFA for cross-app tracking. ObservePoint is web-only — see `references/limitations.md`.

**Audit.** In ObservePoint specifically, a **Web Audit** — a configured scan of a defined set of URLs by the synthetic Chromium engine. See `references/products-and-modules.md` → Web Audits.

**axe-core.** The open-source accessibility-testing rules engine (maintained by Deque) widely used to evaluate pages against **WCAG** success criteria. The de-facto standard for automated accessibility checks; like all automated tooling it covers only the machine-testable subset of WCAG. See the **accessibility** skill.

## B

**BAA (Business Associate Agreement).** A HIPAA-specific contract between a covered entity and a vendor that handles PHI. ObservePoint generally avoids being a Business Associate by not handling patient data directly.

**Beacon.** A small image or request used to transmit tracking data. Often used synonymously with "pixel."

**BIPA (Biometric Information Privacy Act).** Illinois law (2008) regulating collection, use, and storage of biometric identifiers. Notable for high statutory damages ($1K–5K per violation, no cap) and active class-action litigation. See the `litigation-defense` skill.

## C

**CCPA (California Consumer Privacy Act).** The California privacy law. **CPRA** is its amendment effective from 2023, expanding scope.

**CIPA (California Invasion of Privacy Act).** Cal. Penal Code §§ 631, 632, 638.51. California's wiretap and pen-register statutes. Drives the dominant 2024-2026 tracking-pixel class-action wave (1,000+ filings annually) via the pen-register theory applied to session-replay vendors and chat-pixel handoffs. See the `litigation-defense` skill.

**Churn.** The loss of a customer at or before renewal. In the CSM context, the outcome the account-health and renewal motions exist to prevent. The leading churn signal in a web-governance program is a healthy operation with no executive sponsor to defend it at budget time. See the `account-health` skill.

**CMP (Consent Management Platform).** The system that captures user consent and signals it to tags. Examples: OneTrust, Cookiebot, TrustArc, Didomi, Sourcepoint.

**Color contrast ratio.** The luminance ratio between text (or a UI component) and its background. WCAG 2.1/2.2 SC 1.4.3 requires at least 4.5:1 for normal text and 3:1 for large text; one of the most common — and most automatable — accessibility violations. See the **accessibility** skill.

**Colorado AI Act.** First U.S. state comprehensive AI Act, effective February 1 2026. Requires impact assessments and consumer notice for "high-risk" AI systems. ObservePoint validates marketing-side disclosure requirements; impact assessments are out of scope.

**Consent Mode v2.** Google's consent signaling mechanism. Four categories: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`. Used by Google tags to determine how to behave under various consent states.

**Cookie.** A small piece of state stored in the browser. Subject to privacy regulation when used for tracking.

**COPPA (Children's Online Privacy Protection Act).** U.S. federal law requiring parental consent before collecting personal information from children under 13. **COPPA 2.0** Final Rule was published January 2025, tightening definitions (persistent identifiers now in scope) and restrictions.

**CrUX (Chrome User Experience report).** Google's field-data source for Core Web Vitals. Not an ObservePoint product but referenced when discussing performance.

## D

**Data Act (EU).** EU regulation, fully applicable September 12 2025. Primarily B2B — covers user access to data from connected products and cloud-switching protections. Limited website-tracking applicability.

**Data downtime.** Borrowed from the data-observability field: the periods when data is missing, wrong, or untrustworthy — the analytics equivalent of system downtime. The cost web governance reduces by catching broken or misfiring tracking before it corrupts the reports. A useful framing for Chief Data Officers and in ROI narratives. See the `roi` skill.

**Data layer.** A standardized JavaScript object on a page that holds structured information about the user, the page, and events. Tag managers read from it. ObservePoint validates it.

**DMA (Digital Markets Act).** EU regulation targeting designated gatekeepers (large platform operators). In force March 7 2024 for designated entities. Most ObservePoint customers are not gatekeepers; relevant when one is.

**DPDP (Digital Personal Data Protection) Act.** India's comprehensive privacy law. Rules finalized late 2025, phased enforcement entering 2026.

**DSA (Digital Services Act).** EU regulation for online platforms in force since February 17 2024. Requires notice-and-action mechanisms, advertising transparency, restrictions on minor-targeting and sensitive-data-based targeting.

**DSAR (Data Subject Access Request).** A request from an individual to see, correct, or delete their personal data. Workflow-level, owned by privacy programs — not an ObservePoint feature directly.

## E

**EAA (European Accessibility Act).** EU directive extending accessibility obligations across member states. In force June 28 2025.

**ECPA (Electronic Communications Privacy Act).** Federal U.S. law including the Wiretap Act (18 U.S.C. § 2511). Used in tracking-pixel litigation alongside state wiretap statutes and CIPA. See the `litigation-defense` skill.

**EU AI Act.** European regulation governing artificial intelligence systems. Prohibited practices (Article 5) in force February 2 2025; Article 50 transparency obligations August 2 2026; high-risk AI obligations August 2 2027.

**ePrivacy Directive.** EU directive (2002, amended 2009) covering electronic communications privacy, including cookie consent requirements that predate and are independent of GDPR.

## F

**FERPA (Family Educational Rights and Privacy Act).** U.S. law protecting student education records. Tracking-pixel litigation around student portals is a growing enforcement area.

## G

**GA4 (Google Analytics 4).** Current generation of Google Analytics. Event-based model. Replaced Universal Analytics.

**GDPR (General Data Protection Regulation).** The European Union's comprehensive privacy regulation. In force May 2018.

**GLBA (Gramm-Leach-Bliley Act).** U.S. law governing financial institutions and customer data. The FTC's revised Safeguards Rule (2023) is the operational-controls bite.

**GPC (Global Privacy Control).** A browser-level "do not sell or share" signal honored as a valid opt-out under 12+ U.S. state privacy laws as of 2026. Toggle in ObservePoint as "Send GPC Signal" on an audit.

**GPP (Global Privacy Platform).** IAB Tech Lab's multi-jurisdiction consent-string standard. Carries per-jurisdiction signals (US National, US-CA, US-CO, US-VA, etc.) in one string.

**GTM (Google Tag Manager).** Google's tag management system, both client-side and server-side variants.

## H

**HAR (HTTP Archive).** A standard JSON file format capturing the network requests a browser made on a page. Exportable from Chrome DevTools, Charles, Fiddler, mitmproxy. Processable by ObservePoint's **HAR Analyzer**.

**HIPAA (Health Insurance Portability and Accountability Act).** U.S. law governing health information privacy and security. The 2022 OCR bulletin on tracking technologies on healthcare websites underlies the active healthcare-pixel litigation wave.

**Hydration.** A pattern in modern JS frameworks (React, Vue) where the page is server-rendered then "hydrated" with client-side interactivity. A common cause of tag firing inconsistencies; the **Journey** with **Prevent Navigation** is the workaround.

## I

**IAB (Interactive Advertising Bureau).** Industry body publishing the **TCF** consent framework and the **GPP** Global Privacy Platform.

**INP (Interaction to Next Paint).** A Core Web Vitals metric. Captures interaction responsiveness.

**ISO/IEC 27701.** ISO Privacy Information Management standard (extends ISO 27001). Certifiable; used by enterprises as a governance framework.

## J

**Journey.** In ObservePoint specifically, a scripted multi-step user flow run by the synthetic browser. See `references/products-and-modules.md` → Journeys.

**JourneyStream.** One of the Strala-acquired products. Automates campaign tracking and touchpoint management.

## K

**KOSA (Kids Online Safety Act).** U.S. federal bill (passed Senate July 2024; House action pending). **Not in force as of June 2026.** Would impose duty of care on online platforms for harm to minors.

## L

**LCP (Largest Contentful Paint).** A Core Web Vitals metric. Captures perceived load time.

**LGPD (Lei Geral de Proteção de Dados).** Brazil's comprehensive privacy law. GDPR-style framework. Enforcement by ANPD.

**LiveConnect.** ObservePoint product for connecting real devices via proxy for live network inspection.

## M

**MCP (Model Context Protocol).** Anthropic's open protocol for connecting AI systems to external tools. The ObservePoint MCP server is in development. See `references/mcp-tools.md`.

**MHMDA (Washington My Health My Data Act).** Washington state law (effective 2024) covering consumer health data more broadly than HIPAA. Has a private right of action — making it the most plaintiff-friendly U.S. health-data law.

## N

**NIS2.** EU Network and Information Security Directive (2). Cybersecurity directive for "essential" and "important" entities across 18 sectors. Transposition deadline October 2024; national laws in force 2025-2026.

**NIST Privacy Framework.** Voluntary framework (v1.0 2020) for managing privacy risk. Tennessee's TIPA makes a documented NIST-aligned program an affirmative defense.

## P

**Page Insights.** ObservePoint's real-user telemetry dashboard, fed by a lightweight tag deployed on the customer's site.

**PCI DSS.** Payment Card Industry Data Security Standard. Version 4.0 mandatory across the payment industry as of 2025. Requirements 6.4.3 and 11.6.1 — script inventory and change detection on payment pages — are the tracking-relevant bite.

**Pen-register.** A statutory concept (originally telecommunications) referring to a device that captures dialing or routing information. Pen-register theory under CIPA § 638.51 is the dominant tracking-pixel litigation theory.

**Pixel.** A tag used for ad attribution or analytics, originally implemented as a 1x1 image request. Used loosely to mean any analytics or advertising request.

**PHI (Protected Health Information).** Health information that identifies an individual. Under HIPAA, very strictly regulated.

**PIPA (Personal Information Protection Act).** South Korea's comprehensive privacy law. One of the strictest opt-in regimes globally.

**PIPEDA (Personal Information Protection and Electronic Documents Act).** Canada's federal private-sector privacy law.

**PIPL (Personal Information Protection Law).** China's comprehensive privacy law. In force November 2021. Extraterritorial reach; strict cross-border-transfer requirements.

**POPIA (Protection of Personal Information Act).** South Africa's comprehensive privacy law. Fully effective July 2021.

**Prism.** One of the Strala-acquired products. Attribution and ROI analysis layer.

**Privacy Sandbox.** Google Chrome's initiative replacing third-party cookies with privacy-preserving alternatives. Topics API retired October 2025; surviving APIs include Protected Audience, Attribution Reporting, CHIPS, FedCM, Private State Tokens.

## Q

**QBR (Quarterly Business Review).** The recurring strategic review between a CSM (or program owner) and the customer's executive sponsor — what the program caught and prevented, how fast it detected and resolved, where coverage expands next. The cadence that keeps a mature program executive-owned and renewal-ready. Template in `references/consulting-deliverables.md`; cadence in the `account-health` skill.

**Quebec Law 25.** Quebec's modernized private-sector privacy law (fully effective September 2024). Stricter than federal PIPEDA on consent, transparency, and automated decision-making. Up to CAD $10M or 2% global turnover penalties.

## R

**RACI.** A framework for assigning roles to activities — Responsible, Accountable, Consulted, Informed. Template in `references/consulting-deliverables.md`.

**RAIGA (Texas Responsible AI Governance Act).** Texas AI law (signed 2025, phased through 2026-2027). Transparency disclosures for AI use in consumer-facing contexts.

**Rule.** In ObservePoint specifically, a Tag & Variable Rule — `WHEN` condition + `EXPECT` condition. The mechanism by which audit findings turn into pass/fail signals.

## S

**Section 508.** Section 508 of the U.S. Rehabilitation Act, requiring federal agencies' electronic and information technology to be accessible. It incorporates **WCAG** 2.1 AA as the technical standard, so the same automated scan that proves WCAG conformance satisfies 508. The dominant accessibility hook for federal properties. See the **accessibility** skill.

**Session replay.** A category of vendor that records user interactions (mouse movements, scrolls, keystrokes, form inputs) for product / UX analytics. Central to CIPA pen-register theory and to ECPA wiretap claims. ObservePoint detects via vendor inventory and consent-state diff.

**sGTM (Server-side Google Tag Manager).** A GTM container that runs on the customer's own servers rather than in the browser. ObservePoint observes the client-side request that triggers it, not the server execution. See `references/limitations.md`.

**SOC 2.** A security and operational controls audit framework. Common enterprise procurement requirement.

**SPA (Single-Page Application).** A web app where navigation happens without full page reloads. Examples: React, Vue, Angular, Svelte apps. Requires **Journey** + **Prevent Navigation** for full coverage.

**Strala.** The company ObservePoint acquired in February 2020. Brought **Touchpoints**, **JourneyStream**, and **Prism**.

## T

**Tag.** A small piece of code that runs on a page to collect data or render content. Analytics tags, advertising tags, functional tags, and so on.

**TCF (Transparency and Consent Framework).** The IAB's standard for encoding consent strings. **TCF 2.3** is the current version; non-compliant strings became invalid February 28, 2026.

**TCO (total cost of ownership).** The full cost of a capability across people, tooling, and incident fallout — not just the line-item price. In a web-governance ROI narrative, the relevant comparison is the TCO of an undetected incident (lost conversion data, a reportable consent leak, an accessibility lawsuit) against the cost of catching it early. Used for value framing only; this skill does not discuss ObservePoint pricing. See the `roi` skill.

**TMS (Tag Management System).** GTM, Tealium iQ, Adobe Launch, Ensighten, etc. ObservePoint is vendor-neutral across TMS choices.

**Touchpoints.** One of the Strala-acquired products. Standardizes and unifies online and offline customer touchpoint data.

**Trap-and-trace.** Statutory concept paired with **pen-register** under CIPA § 638.51. Refers to a device capturing the source of incoming communications. Used analogously to capture-on-arrival website tracking in current pixel litigation.

## U

**UK GDPR.** UK's post-Brexit retained version of GDPR. In force since January 1 2021. Paired with the Data Protection Act 2018 and the 2024 Data Protection and Digital Information Act amendments. Substantively very similar to EU GDPR with UK-specific divergences.

**Unruh Civil Rights Act.** California's civil-rights statute (Cal. Civ. Code § 51), used as the state-law vehicle for website accessibility suits — often paired with **ADA Title III**. Notable for statutory damages (minimum $4,000 per violation), which makes California a hotspot for accessibility demand letters. See the **accessibility** skill.

**UOOM (Universal Opt-Out Mechanism).** Regulatory concept for a browser-level signal that conveys a user's opt-out across all sites visited. **GPC** is the dominant UOOM today; multiple state laws require its recognition.

**UTM (Urchin Tracking Module) parameters.** Query-string parameters (`utm_source`, `utm_medium`, etc.) used to attribute traffic to campaigns. Predates Google's acquisition of Urchin; the name stuck.

## V

**VPAT (Voluntary Product Accessibility Template).** A standardized document a vendor publishes to report how its product conforms to accessibility standards (**Section 508**, **WCAG**, EN 301 549). Frequently requested in procurement, especially by public-sector buyers. See the **accessibility** skill.

**VPPA (Video Privacy Protection Act).** 18 U.S.C. § 2710. Federal U.S. law originally enacted 1988 (post-Bork-nomination). Currently underlies a substantial pixel-litigation wave against sites with video content. Statutory damages up to $2,500/violation. See the `litigation-defense` skill.

## W

**WCAG (Web Content Accessibility Guidelines).** The W3C standard for web accessibility. WCAG 2.1 Level AA is the conformance level most commonly enforced. **WCAG 2.2** (W3C Recommendation, October 2023) adds nine success criteria — focus appearance, dragging-movement alternatives, target size, accessible authentication, and more — and is the level newer obligations increasingly point to; 2.1 AA remains the dominant legal target as of 2026. See the **accessibility** skill.

**Web Audit.** See **Audit**.

**Web governance.** The category ObservePoint operates in. Continuous, automated validation that a website behaves correctly for analytics, privacy, accessibility, and operational quality. See `references/verbiage-and-messaging.md`.

**Wiretap Act.** The federal Wiretap Act (18 U.S.C. § 2511), part of the **ECPA**. Prohibits unauthorized "interception" of electronic communications. State equivalents exist (CIPA, Massachusetts § 99, Pennsylvania § 5703, Florida § 934, Washington § 9.73). All used in tracking-pixel litigation. See the `litigation-defense` skill.

---

*Last verified: 2026-06-04*
