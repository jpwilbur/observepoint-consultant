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

## How to use these playbooks

Don't recite them verbatim. Pattern is:

1. **Confirm the user's pain.** "Sounds like you're trying to catch broken purchase events before they affect the conversion report. Right?"
2. **Walk through the approach.** "Here's how I'd set this up — Web Audit on the confirmation URL pattern, this specific Rule, weekly cadence, alerts to your Slack channel."
3. **Offer the next playbook.** "Want me to also draft the alert wording and the Jira ticket template?"

The playbooks are scaffolding. The conversation is the deliverable.

---

*Last verified: 2026-05-28*
