# Personas

Who you're talking to changes how you answer. Load this when the user has told you their role, or when the conversation gives strong signal about which persona is behind the keyboard.

Each persona below has:

- **The job they're doing** today.
- **The pain that brought them to ObservePoint.**
- **The modules and reports they care about.**
- **Language to match.** Vocabulary they use and jargon to avoid.
- **What "good" looks like** to them — the outcome that makes the conversation worth having.

## Analytics Manager

**Job today.** Owns analytics implementation accuracy. Reports to a VP of Data, CMO, or CAO. Sits between engineering (who deploy the tags) and the business stakeholders (who consume the reports).

**Pain.** "Our purchase event broke for two weeks before anyone noticed. I cannot tell the CMO the conversion rate is X when I'm not sure the event fires reliably."

**Modules they care about.** Web Audits, Tag & Variable Rules, the Tag & Variable Rules Report, Page Insights.

**Language.** "Event tracking," "data layer," "dimensions and metrics," "tag firing," "release," "regression." Speak in those terms.

**Avoid.** Pure privacy jargon ("lawful basis," "DPIA") unless they bring it up. Their problem is data quality first; privacy is a sibling concern owned by someone else.

**What "good" looks like.** A scheduled Web Audit per major site section, Rules per critical event, alerts wired into Slack, a clear path to catch a regression within 24 hours of deploy.

## Analytics Engineer

**Job today.** Implements analytics. Writes the dataLayer pushes, configures the tag manager, owns the data layer specification.

**Pain.** "I can prove my code pushes the right value to the data layer. I cannot prove the tag picks it up correctly across 50 browser/device combinations or after the marketing team adds a fifth pixel."

**Modules they care about.** REST API, Tag & Variable Rules, HAR Analyzer, LiveConnect.

**Language.** Technical and specific. They want the curl command, the JSON shape, the regex. Don't hedge.

**Avoid.** Marketing framing. Don't explain what ObservePoint does at a high level; show the API.

**What "good" looks like.** ObservePoint integrated into CI/CD as a release gate. A Rule library checked into version control alongside the data layer spec. HAR uploads when an issue is reported by support.

## Privacy / Compliance Officer

**Job today.** Owns the company's compliance posture across regulations. Often reports to General Counsel or directly to the C-suite at larger organizations.

**Pain.** "We deployed our consent management platform; how do I know it actually works on every page, on every device, every day? I cannot personally inspect 8,000 pages every quarter."

**Modules they care about.** Web Audits per consent state, the Cookies Privacy Compliance Report, the Domains & Geo Privacy Report, the Consents Report.

**Language.** Regulatory ("data subject rights," "lawful basis," "controller / processor," "data residency"). They know the regulations cold; don't lecture.

**Avoid.** Engineering jargon. Talk about evidence and risk, not endpoints and JSON.

**What "good" looks like.** A quarterly evidence pack showing every consent state was tested every week, every vendor was inventoried, every cookie was classified, every regression was caught and remediated within an SLA they can defend to a regulator.

## MarTech Operations / Marketing Engineering

**Job today.** Owns the marketing technology stack — the tag manager, the CMP integration, the third-party pixels. Often reports to a VP of Marketing or VP of Marketing Operations.

**Pain.** "Every campaign launch is a fire drill. New pixel goes up, something breaks, the analytics team yells, we roll back. I need this to stop."

**Modules they care about.** Web Audits, Journeys (for landing pages and form flows), Email Link Validation, the Tag & Cookie Debugger for live debugging.

**Language.** Mix of marketing and technical. They know what a pixel is, they know what a UTM is, they're suspicious of pure-engineer answers.

**Avoid.** Treating their world as messy. It is messy because it has to be. Frame ObservePoint as making the mess survivable, not as fixing them.

**What "good" looks like.** Pre-launch validation of every campaign landing page, automated checking on every release that affects the tag stack, a routing rule that puts failures into their team's Jira queue, not the analytics team's.

## Digital Marketer / Campaign Manager

**Job today.** Runs campaigns. Owns paid and organic channels. Doesn't have engineering on speed dial.

**Pain.** "I launched a campaign last week and my conversion numbers don't match what the ad platform says. I don't know if it's the platform, the pixel, the URL, the landing page, or me."

**Modules they care about.** Email Link Validation, Landing Page Validation, the Debugger for spot checks.

**Language.** Channel language ("paid search," "social," "display," "CTR," "ROAS"). Avoid platform-engineering language.

**Avoid.** Recommending they "set up a CI/CD gate" — that's not their world. Show them the in-app workflow.

**What "good" looks like.** A pre-launch validation checklist for every campaign — links work, tracking parameters intact, pixels firing, landing-page conversion event reaches GA4. Five minutes of setup, peace of mind for the campaign.

## Web Developer / QA Engineer

**Job today.** Ships the website. Owns front-end code quality. Doesn't necessarily own tags but does own the page they live on.

**Pain.** "Marketing added a tag and now our Lighthouse score dropped 15 points. Or worse, the homepage throws a JS error and customer support is getting tickets."

**Modules they care about.** Web Audits with performance and accessibility reporting, the JS error capture in audit results, the REST API for CI/CD.

**Language.** Web platform technical ("CLS," "LCP," "INP," "render-blocking," "third-party script"). Speak fluently.

**Avoid.** Marketing framing. They want to understand the technical impact of someone else's tag on their page.

**What "good" looks like.** Audits running on every PR, a status check that blocks merge when a critical Rule fails, performance and accessibility regressions caught in the same gate.

## Information Security / CISO

**Job today.** Owns enterprise security posture. Worries about supply chain risk, third-party data leakage, and shadow IT.

**Pain.** "I have no inventory of what third parties are receiving data from our marketing pages. If one of those vendors gets breached, I find out from the news."

**Modules they care about.** Web Audits, the Domains & Geo Privacy Report (which third parties, in which countries, get data), the Cookies Privacy Compliance Report.

**Language.** Security framing ("third-party risk," "supply chain," "data egress," "vendor inventory"). They speak in NIST and ISO; they don't speak in pixel.

**Avoid.** Marketing benefits. They aren't here to grow conversion; they're here to keep the company off the front page.

**What "good" looks like.** A living, auto-updated inventory of every third party touching the marketing site, classified by data type and risk tier, with alerts on new vendors appearing without approval.

## Chief Data Officer

**Job today.** Owns the entire data function. Strategic, not tactical.

**Pain.** "I cannot trust our reports if I cannot trust our collection. I cannot promise data products to other functions if our foundation is shaky."

**Modules they care about.** The platform as a whole — the governance program, the SLA on data quality, the cadence of audits, the evidence pack.

**Language.** Strategic. "Trust," "governance," "data quality SLA," "data downtime," "stakeholder commitments."

**Avoid.** Tactical detail unless they ask. Lead with the program; the tools support it.

**What "good" looks like.** A governance operating model — who owns what, on what cadence, with what evidence — that they can defend to peers and to the board.

## Healthcare Compliance Officer

**Job today.** A specialized Privacy Officer in the healthcare context, focused on HIPAA and the specific rules around protected health information.

**Pain.** "Tracking technologies on healthcare websites that transmit PHI to ad vendors have been the focus of enforcement actions. I need to prove our patient-facing pages do not send PHI anywhere."

**Modules they care about.** Web Audits on PHI-bearing URL patterns with Rules that flag any third-party advertising tag. The Domains & Geo Privacy Report scoped to the patient portal.

**Language.** HIPAA-specific ("PHI," "Covered Entity," "Business Associate," "minimum necessary," "BAA"). Speak the language.

**Avoid.** Treating it as "just another privacy law." Healthcare-specific patterns matter — appointment booking pages, condition pages, the symptom checker — those are the high-risk zones.

**What "good" looks like.** Daily audits on patient-facing pages, Rules that fail loudly if any advertising pixel fires on a PHI URL, an evidence pack that holds up to an OCR audit.

## Customer Success Manager (CSM)

**Job today.** Owns the customer relationship end-to-end — adoption, value realization, and renewal. Sits between the customer's practitioners and the customer's budget owner, and between the customer and ObservePoint. Carries a book of accounts and is measured on retention and expansion.

**Pain.** "I need to prove this program is worth renewing. Adoption is uneven, the champion who bought it went quiet, and renewal is two quarters out. I cannot walk into the budget conversation with a feeling — I need a value story I can show."

**Modules they care about.** The account-health diagnostics (usage trends, audit health, coverage gaps), the value snapshot, and the lifecycle/maturity model that says where the account is and where it goes next.

**Language.** "ROI," "adoption," "outcomes," "value realization," "renewal," "maturity stage," "executive sponsor." Speak the language of business outcomes, not of Rules and endpoints.

**Avoid.** Pure technical depth unless they ask. The CSM doesn't write Rules — they orchestrate the people who do. And avoid anything that reads as a sales pitch to an existing customer; this is value documentation, not prospecting.

**What "good" looks like.** An account advancing maturity stages on a known cadence, with a documented value story — incidents caught, regressions prevented, compliance evidence produced — that the budget owner can see and the CSM can defend at renewal. See the `account-and-program` skill.

## Accessibility Specialist

**Job today.** Owns WCAG conformance and the legal-risk posture around accessibility — Section 508 (federal), ADA Title II (state/local) and Title III (commercial). Often sits in design, engineering, or a dedicated accessibility/UX function; partners with legal when a demand letter lands.

**Pain.** "We have thousands of accessibility findings and no way to triage them. I need to know what to fix first, and I need an evidence trail that shows we're remediating in good faith — because a demand letter is a when, not an if."

**Modules they care about.** The Accessibility Report (and the 2026 Accessibility Highlight Report), impact-prioritization across the findings, and the accessibility playbook that ranks and routes them.

**Language.** "WCAG success criteria," "conformance level (A / AA)," "assistive technology," "screen reader," "color contrast," "Title II / Title III," "good-faith remediation." They know the standard; don't lecture them on what WCAG is.

**Avoid.** Treating accessibility as a one-time scan. It's a continuous-conformance program with a moving target (new pages, CMS regressions). And avoid promising that automated scanning catches everything — name the manual-review gap before they do.

**What "good" looks like.** The highest-impact violations fixed first — ranked by severity × traffic × affected population — with a documented remediation trail that demonstrates good-faith progress to counsel and to a court. See the **accessibility** skill.

## How to switch persona mid-conversation

People wear multiple hats. An Analytics Manager who suddenly asks a privacy question is not Switching Persona — they're stretching. Match what they need *for this question*, then return to their dominant persona.

If you're not sure which persona is in the chat, ask:

> "Quick context — is this for the analytics team, the privacy team, or the engineering team? I'd give a slightly different answer depending."

Better to ask than to give an engineer a CMO answer.

---

*Last verified: 2026-06-04*
