# Solution playbooks

Pain-point and persona-led recipes. Load this file whenever the user describes a *problem* rather than asking *what ObservePoint does*. Each playbook reads:

- **The pain in one sentence.**
- **The persona it usually comes from.**
- **The ObservePoint approach** — which scanner, which Rules, which reports, which cadence.
- **A concrete Rule** in `WHEN / EXPECT` form.
- **Alert routing** — who needs to know when this fails.
- **Success metric** — how the team knows it's working a quarter later.

When you walk a user through one of these, narrate the steps in order. Don't dump the whole table at them.

## Analytics validation — events fire correctly

### "Our purchase event is broken"

**Pain.** Conversion data looks wrong; nobody can tell if the tag is broken, the data layer is wrong, or the reporting view is misconfigured.

**Persona.** Analytics Manager.

**ObservePoint approach.** Web Audit on the confirmation URL pattern (`/checkout/confirmation`, `/order-complete`, etc.). One Rule per critical attribute of the event.

**Concrete Rule.**

```
WHEN tag = "Google Analytics 4" AND event = "purchase"
EXPECT
  ecommerce.value is numeric AND > 0
  ecommerce.currency matches /^[A-Z]{3}$/
  ecommerce.items is array AND length >= 1
```

**Alert routing.** Slack `#analytics-alerts`. Also Jira issue if more than 10% of checkout pages fail.

**Success metric.** Time-to-detect for a broken purchase event drops from "discovered by the CFO" to "caught within one audit cycle" (typically 24 hours or less).

### "Events fire twice on this page"

**Pain.** Duplicate event firings inflate metrics. Hard to spot in aggregate data.

**Persona.** Analytics Manager or Analytics Engineer.

**ObservePoint approach.** Web Audit with a "fires exactly once" Rule on the URL pattern affected.

**Concrete Rule.**

```
WHEN page contains "<URL pattern>"
EXPECT tag "Google Analytics 4" event "purchase" fires exactly once
```

**Alert routing.** Slack `#analytics-alerts`.

**Success metric.** Duplicate-event incidents trend toward zero quarter-over-quarter.

### "I want to validate every release before it ships"

**Pain.** Every deploy is a chance for tagging to break; manual checks don't scale.

**Persona.** Analytics Engineer.

**ObservePoint approach.** REST API integration into CI/CD. A targeted audit on staging URLs runs as a release gate.

**Recipe.** See `references/api-reference.md` → "Recipe: CI/CD gate with GitHub Actions."

**Alert routing.** Block the release. Fail the build.

**Success metric.** Number of tagging-related incidents caught pre-production divided by incidents caught post-production trends upward.

## Consent and privacy

### "Tags fire before the user gives consent"

**Pain.** Pixels leak data before the consent banner is acknowledged. Significant regulatory exposure.

**Persona.** Privacy / Compliance Officer (often via the Analytics team).

**ObservePoint approach.** Web Audit running with the CMP in default state (no consent given). Rule asserting no advertising or analytics tags fire.

**Concrete Rule.**

```
WHEN consent state = "default" (no interaction)
EXPECT
  no tags in category "Advertising" fire
  no tags in category "Analytics" fire
  exactly 1 tag: the CMP itself
```

**Alert routing.** Slack `#privacy-compliance`. Auto-create a Jira ticket if any pages fail.

**Success metric.** Audit pass rate for the no-consent variant stays at 100%. The number is exactly that — anything less is a failure.

### "We need to prove our opt-out works on every device"

**Pain.** Multi-device opt-out enforcement is a hot enforcement area in U.S. state privacy law.

**Persona.** Privacy / Compliance Officer.

**ObservePoint approach.** Web Audit per consent state ("Accept All," "Reject All," GPC signal enabled) across the full site. Use the Cookies Privacy Compliance Report as the evidence artifact.

**Concrete Rule.**

```
WHEN consent state = "Reject All" OR GPC = true
EXPECT
  no third-party advertising domains receive data
  no cross-context behavioral advertising cookies are set
```

**Alert routing.** Privacy Officer email + Slack `#privacy-compliance`.

**Success metric.** Quarterly evidence pack demonstrates the same Rule passed on every audit run for 90 days.

### "Validate Consent Mode v2 propagation"

**Pain.** The CMP claims to send the right Consent Mode signals to Google; nobody has proven it end-to-end.

**Persona.** Privacy / Compliance Officer + Analytics Engineer.

**ObservePoint approach.** Web Audit per consent state. Rules that read the Consent Mode parameters off the Google tag's request payload.

**Concrete Rule.**

```
WHEN consent state = "Reject All"
EXPECT Google tag request includes:
  ad_storage = "denied"
  analytics_storage = "denied"
  ad_user_data = "denied"
  ad_personalization = "denied"
```

**Alert routing.** Privacy Officer + Analytics team.

**Success metric.** Consent Mode signal correctness validated on every audit run.

### "Find tags I didn't authorize"

**Pain.** Marketing teams add pixels without IT/privacy approval — shadow MarTech.

**Persona.** Privacy / Compliance Officer or InfoSec.

**ObservePoint approach.** Web Audit. Rule asserting the *only* third-party domains receiving data are on an approved allowlist.

**Concrete Rule.**

```
WHEN any third-party request is made
EXPECT request domain is in approved-vendor list
```

**Alert routing.** Privacy + InfoSec. Anything new = an investigation, not a quiet add.

**Success metric.** Mean time from unauthorized tag deployment to detection drops to under 24 hours.

## Accessibility

### "Our site fails WCAG and we don't know where"

**Pain.** Accessibility complaint, demand letter, or proactive risk review.

**Persona.** Engineering manager or Privacy/Compliance Officer.

**ObservePoint approach.** Web Audit with accessibility scanning enabled across the site. The Accessibility Report and the new Accessibility Highlight Report enumerate violations by severity.

**Concrete next step.** Triage by severity. Critical WCAG 2.1 AA failures (missing alt text on critical images, no form labels, color contrast on primary CTAs) get fixed first.

**Alert routing.** Engineering ticketing system (Jira), assigned to the team that owns the affected pages.

**Success metric.** Severity 1 (critical) violations trend toward zero. Severity 2 and 3 trend downward over quarters.

## Performance

### "Our site got slow and we suspect a new tag"

**Pain.** Site speed regressed; suspicion points at a recent tag addition but no proof.

**Persona.** Web Developer or Analytics Manager.

**ObservePoint approach.** Web Audit with performance metrics captured per page. Compare runs before and after the suspected change.

**Concrete next step.** Pull the Page Summary Report for the run *before* the change and the run *after*. Diff page load times by page; correlate the regressions to the new tag's presence in the request waterfall.

**Alert routing.** Slack `#site-performance` or a dedicated performance channel.

**Success metric.** Performance regressions are detected within one audit cycle, with clear attribution to the offending tag.

## CMP-specific

### "Validate that OneTrust does what privacy configured it to do"

**Pain.** OneTrust setup is complex; nobody is certain every category and every region works as intended.

**Persona.** Privacy / Compliance Officer.

**ObservePoint approach.** Per-region Web Audits with OneTrust banner present; Rules asserting category-by-category behavior.

**Concrete Rule.**

```
WHEN OneTrust category "C0002 — Performance Cookies" = denied
EXPECT no analytics tags fire
WHEN OneTrust category "C0004 — Targeting Cookies" = denied
EXPECT no advertising tags fire
```

**Alert routing.** Privacy + the OneTrust admin.

**Success metric.** Quarterly evidence pack shows every category mapped, validated, and passing.

### "We have many OneTrust instances and need a consistent config"

**Pain.** Multi-brand or multi-regional organizations run OneTrust separately per property and configurations drift.

**Persona.** Privacy / Compliance Officer.

**ObservePoint approach.** The Bulk OneTrust Updates feature (shipped March 2026) lets you push consistent updates across multiple OneTrust instances. Pair with audits per instance for verification.

**Success metric.** Configuration drift across instances becomes detectable and remediable in a single workflow.

## Campaign and landing-page

### "I'm about to launch a campaign; validate the landing page first"

**Pain.** Conversion tracking on a brand-new landing page is invisible until traffic starts.

**Persona.** MarTech Ops or Digital Marketer.

**ObservePoint approach.** Journey scripted to mimic the campaign user flow — land on the page from the ad URL (with UTM intact), interact with the form, submit, land on the confirmation. Rules at each step.

**Concrete Rule.**

```
WHEN URL contains "utm_campaign=spring2026"
EXPECT
  GA4 page_view fires with the correct campaign attributes
  Meta Pixel PageView fires
  After form submit: GA4 lead event fires with form_id attribute populated
```

**Alert routing.** Email the campaign owner; Slack `#campaign-ops` for the team.

**Success metric.** Zero campaign launches that go live with broken tracking.

### "Validate the marketing emails — links, redirects, landing pages"

**Pain.** Broken links in marketing emails are embarrassing and expensive.

**Persona.** MarTech Ops or Digital Marketer.

**ObservePoint approach.** Email Link Validation. Drop the email HTML or campaign URL list in; ObservePoint follows every link, validates the destination, captures redirect chains.

**Alert routing.** Email the campaign owner before send.

**Success metric.** Broken or misconfigured links caught pre-send approach 100%.

## Healthcare-specific

### "Prove no PHI leaks to ad networks"

**Pain.** Tracking technologies on healthcare sites that transmit identifiable patient data to advertising vendors are a high-enforcement risk.

**Persona.** Healthcare Compliance Officer.

**ObservePoint approach.** Daily Web Audits on patient-facing URL patterns. Rules that flag any third-party advertising tag on PHI-bearing pages.

**Concrete Rule.**

```
WHEN page URL matches /\/appointment|\/prescription|\/portal|\/condition\//
EXPECT
  no third-party advertising tags fire
  no third-party advertising cookies are set
```

**Alert routing.** Healthcare Compliance Officer + Privacy Officer. Critical severity.

**Success metric.** Evidence pack defensible to a regulator audit. Zero ad-tag firings on PHI-bearing URLs for the past 90 days.

## Litigation defense

When a customer has received a demand letter, class-action filing, or discovery request, these playbooks apply. See the `litigation-defense` skill for the per-statute deep treatment.

### "Defend a CIPA / VPPA / BIPA / wiretap claim"

**Pain.** A demand letter or class-action complaint alleging unauthorized tracking under CIPA pen-register theory, VPPA video-tracking, BIPA biometric capture, or federal/state wiretap claims. Counsel needs technical evidence quickly.

**Persona.** In-house counsel or litigation-support engineer, often via Privacy / Compliance Officer escalation.

**ObservePoint approach.**

1. Confirm the audit scope covers the URLs / vendors named in the complaint (if not, expand audit coverage and back-date the historical evidence from existing run data).
2. Pull the audit run history for the alleged period via `mcp__ObservePoint__get_audit_runs` and `query_report` against rule-summary.
3. Use `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to surface what fired on default versus opt-out — central evidence for "did the tracker fire before consent?"
4. Use `find_first_observed` to establish when the named vendor first appeared in the audit history.
5. Use `scan_audit_pii` or `scan_journey_pii` to demonstrate (a) the masked finding of any PII leak, or (b) absence of leakage to the named third party.
6. Export the evidence pack via `export_report`. Bundle with audit configurations, Rules library, exception log, and change log.

**Alert routing.** Privacy Officer + General Counsel. Critical severity.

**Success metric.** Counsel has the technical record needed within 48 hours of the demand letter. The "reasonable practices" narrative the customer's counsel constructs is supported by the audit data.

**Limitations.** ObservePoint produces evidence; it does not defeat liability. Coordinate with the customer's counsel; do not promise outcomes.

### "Set up state-specific privacy monitoring (Colorado / Texas / Washington / …)"

**Pain.** "We're already running CCPA audits. Do we need separate audits per state we operate in?"

**Persona.** Privacy / Compliance Officer.

**ObservePoint approach.**

1. Identify which states the customer operates in (where it processes residents' data) — this is a legal question, not a technical one. Ask counsel for the list.
2. For each state, check the U.S. state matrix in the **regulation** skill — note whether GPC is required, opt-in vs. opt-out for sensitive data, and any distinctive features (e.g., NIST-aligned-program defense in Tennessee, MHMDA-style strict consent for health data in Washington).
3. Use `setup_compliance_monitoring(regulation="ccpa", domain=...)` as the starting template — it produces the three-audit (default + opt-out + GPC) shape that fits most state laws. Adjust the consent banner copy and the opt-out path per state.
4. For states without GPC recognition (Virginia, Utah, Iowa, Indiana, Kentucky), skip the GPC variant — just default + opt-out.
5. Schedule weekly; route alerts per region to the responsible team.

**Alert routing.** Privacy / Compliance Officer, with per-region routing if the org has regional privacy leads.

**Success metric.** A single dashboard view (custom saved report) showing pass/fail per state per week. Failures route to the right human within the SLA.

### "Validate AI-Act and Colorado AI Act marketing transparency disclosures"

**Pain.** Marketing pages contain AI-generated copy, imagery, or chatbot interactions. Need to prove the required disclosure is present on every page where AI content is used.

**Persona.** Privacy / Compliance Officer + MarTech Ops.

**ObservePoint approach.**

1. Marketing or content tooling marks AI-generated pages with a data-layer flag — `page.ai_generated = true` (or whatever the customer's spec).
2. Web Audit attaches a Rule that asserts: `WHEN page.ai_generated = true EXPECT visible disclosure element exists in DOM`.
3. Schedule weekly across the full marketing site.
4. Routes failures to the content team — they own remediation.

**Alert routing.** Slack `#marketing-compliance` channel + content ops Jira queue.

**Success metric.** Time-to-detect for missing-disclosure pages drops to within one audit cycle. Zero AI-generated pages in production without disclosure for the past 30 days.

**Limitations.** ObservePoint validates the disclosure UI; it cannot determine whether content actually was AI-generated. That classification is upstream — content management or AI-generation tooling owns the flag.

### "Maintain a multi-jurisdiction compliance program"

**Pain.** Organization operates globally. Different audit setups for EU GDPR vs. CCPA vs. Quebec Law 25 vs. China PIPL vs. Australia Privacy Act. Risk of drift between regions, missed updates, inconsistent evidence.

**Persona.** Chief Data Officer or global Privacy / Compliance Officer.

**ObservePoint approach.**

1. Use ObservePoint folders to organize audits by region: `EU`, `US`, `APAC`, `LATAM`, `CA`, `MEA`. Sub-folders per country within each region for the high-volume jurisdictions.
2. Per-region audit template using the appropriate `setup_compliance_monitoring` regulation (or manual configuration where the wrapper doesn't cover the regulation yet — see `references/mcp-tools.md`).
3. Apply consistent labels across regions so saved reports can roll up cross-region (e.g., label = "compliance-monitoring").
4. Schedule per-region audits on cadences that match enforcement risk (daily for high-risk like Washington MHMDA pages, weekly for standard, monthly for low-volume regions).
5. Build a saved report per region + a global rollup using `create_saved_report` with entity type `web-audit-runs`, filtered by label.
6. Quarterly evidence-pack generation per region via `export_report`.

**Alert routing.** Per-region Privacy lead via per-region Slack channels; global summary monthly to CDO.

**Success metric.** Quarterly business review for the CDO shows: regions in scope, audits operating, pass rate per region, incidents and time-to-remediate per region, change history. Single source of truth across the program.

## Cross-functional

### "Build a Web Governance program from scratch"

**Pain.** No formal program exists. Analytics, Privacy, and Marketing all complain about tags; nobody owns the problem.

**Persona.** Chief Data Officer.

**ObservePoint approach.** Start with the governance policy and RACI (see `references/consulting-deliverables.md`), then layer in the audits.

**Phase 1 (Month 1):** Inventory. One large Web Audit across the entire site. Output: a list of every tag, every vendor, every cookie. Use this as the baseline.

**Phase 2 (Month 2):** Critical Rules. Top 10 Rules covering the most painful failure modes — purchase tracking, consent compliance, PHI (if applicable), homepage performance. Schedule weekly.

**Phase 3 (Month 3):** Operationalize. Wire alerts into the team's tooling. Define ownership per Rule. Establish a weekly review meeting.

**Phase 4 (Quarter 2):** Expand coverage. Add Journeys for funnels. Add CI/CD gates. Add the evidence pack cadence.

**Success metric.** A quarterly report to the executive sponsor showing: tag inventory, Rule coverage, incidents detected, incidents resolved, time-to-detect, and time-to-resolve.

## Account health and renewal

For existing customers — reading whether the account is on track and building the value story for renewal. This is value documentation, never prospecting.

### "Account Health Check — what should we focus on?"

**Pain.** A CSM or consultant needs to know where an account actually stands and what to prioritize next — not a feeling, a diagnosis read off the account itself.

**Persona.** Customer Success Manager or consultant.

**ObservePoint approach.** Run the account-health diagnostic from `references/account-health-and-strategy.md`: read breadth and usage (`get_usage_overview`, `get_usage_trends`, `list_audits`), whether what exists is working (`get_audit_health`), what's missing (`find_coverage_gaps`), and whether alerts and saved reports exist (`list_alerts`, `list_saved_reports`). Map the readings to a maturity stage (see `references/lifecycle-and-maturity.md`) and the stuck-pattern it implies.

**Workflow.** Diagnose → identify the single biggest gap (most often "Rules but no alerts" or "program but no exec sponsor") → produce a prioritized action list, highest-leverage first.

**Alert routing.** N/A — this is a diagnostic the CSM runs, not a monitored Rule.

**Success metric.** A prioritized, ranked action list delivered to the customer — the top three moves that advance the account, not an undifferentiated audit of everything.

### "Renewal Prep — build the value story"

**Pain.** Renewal is approaching and the CSM needs to show the budget owner what the program delivered — in their terms, with evidence, not a sales pitch to an existing customer.

**Persona.** Customer Success Manager, for the customer's budget owner / executive sponsor.

**ObservePoint approach.** Assemble the value story from `references/roi-and-renewal-framing.md`: pull the period's incidents-caught, regressions-detected, vendors-inventoried, compliance-evidence, and accessibility-progress numbers (via `query_report`, `get_usage_trends`, run history), then frame them against a metric the budget owner already owns. Package as the Value Snapshot and Renewal Narrative from `references/consulting-deliverables.md`. No pricing.

**Workflow.** Pull the numbers → frame in the budget owner's terms → produce the Value Snapshot (the numbers) and the Renewal Narrative (the before/after arc by maturity stage).

**Alert routing.** N/A — deliverable production, not monitoring.

**Success metric.** A Value Snapshot and Renewal Narrative ready to hand to the budget owner before the renewal conversation — a documented value story, not a feeling.

## Accessibility prioritization

### "Rank our accessibility findings — what do we fix first?"

**Pain.** Thousands of accessibility findings and no way to triage. The team needs a fix-this-first queue and an evidence trail that shows good-faith remediation.

**Persona.** Accessibility Specialist (often with legal in the loop on a demand letter).

**ObservePoint approach.** Run a Web Audit with accessibility scanning across the property, then apply the impact-prioritization model from `references/accessibility-playbooks.md` — rank by impact = severity × traffic × affected population. Pull the ranked findings with `query_report` against the accessibility-issues entity (use `get_report_schema` to confirm the column names first), joined to page-traffic tier.

**Workflow.**

1. Confirm accessibility scanning is enabled on the Web Audit covering the in-scope templates.
2. `query_report` against the accessibility-issues entity to enumerate violations by WCAG success criterion and severity.
3. Rank by severity × traffic × affected population — a critical violation on the high-traffic signup flow outranks a minor one on archived pages.
4. Produce the Accessibility Priority Report (see `references/consulting-deliverables.md`) with the fix-this-first queue and per-item remediation guidance; flag the criteria automation can't fully verify for manual review.

**Alert routing.** Engineering / design ticketing (Jira), assigned to the team that owns the affected templates; legal copied when a demand letter is in play.

**Success metric.** A ranked fix-this-first queue the team works top-down, with a dated remediation trail demonstrating good-faith progress.

## How to use these playbooks

Don't recite them verbatim. Pattern is:

1. **Confirm the user's pain.** "Sounds like you're trying to catch broken purchase events before they affect the conversion report. Right?"
2. **Walk through the approach.** "Here's how I'd set this up — Web Audit on the confirmation URL pattern, this specific Rule, weekly cadence, alerts to your Slack channel."
3. **Offer the next playbook.** "Want me to also draft the alert wording and the Jira ticket template?"

The playbooks are scaffolding. The conversation is the deliverable.

---

*Last verified: 2026-06-04*
