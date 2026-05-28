# Consulting deliverables

Templates the consultant can hand back to a user. Load this when the user asks for a specific artifact — a tag audit report, a governance policy, a RACI, a release-gate checklist, a quarterly business review.

Each template below ships in two parts: a **skeleton** the user can adopt directly, and a **filled-in example** for context. Adjust both to the user's voice and organization before sharing.

## Tag Audit Report

The single most common deliverable. Hand this to executives after the inaugural Web Audit; refresh quarterly.

### Skeleton

```markdown
# <Company> — Web Tag Audit
Prepared by <consultant or team>
For <executive sponsor>
Date <YYYY-MM-DD>

## Executive summary
- Scope of the audit (which sites, which sections, how many pages)
- Top three findings in one sentence each
- Recommended next steps

## Inventory
- Total tags detected: <N>
- Total third-party vendors receiving data: <N>
- Total cookies in use: <N>
- Geographies receiving data: <list>

## Findings by category
### Analytics
### Advertising
### Functional / essential
### Unknown / unauthorized
(For each: what was found, what's working, what's broken.)

## Compliance posture
- Consent state coverage tested: <Accept All / Reject All / GPC>
- Regulations in scope: <GDPR / CCPA / CPRA / HIPAA / ...>
- Compliance gaps detected: <list with severity>

## Recommendations
- Immediate (next 30 days)
- Near-term (next 90 days)
- Strategic (next 12 months)

## Appendices
- Full tag list (CSV attached)
- Full vendor list (CSV attached)
- Audit run history
```

### Filled-in example sketch

> **Executive summary**: We audited 1,200 pages across the marketing and account areas. Three findings stand out: (1) 23 third-party vendors receive data from logged-in account pages, only 11 of which are documented in our vendor inventory; (2) the Meta Pixel fires before consent on 87% of audited pages; (3) GA4 purchase events are firing twice on the iOS Safari user-agent path due to a hydration bug.

The example doesn't need to be long. Three findings, ranked, with severity. Numbers anchor the conversation.

## Web Governance Policy

The document the governance program is built on. Living document; review annually.

### Skeleton

```markdown
# <Company> Web Governance Policy
Owner <name>
Approved by <Chief Data Officer or equivalent>
Effective date <YYYY-MM-DD>
Review cadence <annual>

## Purpose
Why this policy exists and what it covers.

## Scope
Which domains, subdomains, and properties are in scope. What is out of scope.

## Roles and responsibilities
(See RACI matrix below.)

## Tag approval process
- Who can request a new tag
- What information must be provided (vendor, purpose, data shared, lawful basis, retention)
- Who approves
- SLA for approval

## Consent and privacy obligations
- The CMP is the authoritative consent capture mechanism
- All non-essential tags must respect consent state
- GPC and equivalent opt-out signals are honored as opt-outs

## Validation requirements
- Every release that modifies tagging must pass the ObservePoint release-gate audit
- Weekly full-site audits run regardless of release activity
- Critical Rule failures escalate per the alerting policy

## Vendor management
- All third-party vendors receiving data must be in the approved-vendor list
- Adding a vendor requires privacy and security review
- Quarterly review of the vendor list for retirement candidates

## Incident response
- Severity definitions
- Escalation paths
- Post-incident review requirements

## Policy violations
- What counts as a violation
- How violations are remediated
```

### Filled-in example sketch

The example should show, in one paragraph per section, what each looks like at the user's specific company. Keep it short enough to read in five minutes; detailed enough to enforce.

## RACI matrix

Who is **R**esponsible, **A**ccountable, **C**onsulted, **I**nformed for each governance activity.

### Skeleton

| Activity | Analytics team | Privacy team | MarTech ops | Engineering | InfoSec | Executive sponsor |
|---|---|---|---|---|---|---|
| Approve a new tag | C | A | R | C | C | I |
| Configure a new tag in TMS | I | C | R | I | I | — |
| Configure a Rule in ObservePoint | A/R | C | C | — | — | I |
| Triage a Rule failure | R | C | R | C | — | I |
| Quarterly evidence pack | C | A/R | C | — | C | I |
| Vendor list review | C | A | R | — | C | I |
| Annual policy review | C | C | C | C | C | A |

R = Responsible (does the work). A = Accountable (single owner, signs off). C = Consulted. I = Informed.

Tweak the columns to the actual org chart. If the team has no dedicated MarTech ops function, fold that role into Analytics or Marketing.

## Release-gate checklist

For every release that touches tagging or the data layer.

### Skeleton

```markdown
# Release gate — <release name or ticket>

## Pre-deploy
- [ ] Data layer changes documented in spec
- [ ] New tags or vendors approved per governance policy
- [ ] Targeted Web Audit run on staging URL
- [ ] All critical Rules pass on staging
- [ ] No new third-party domains appear in the Domains report
- [ ] No new cookies appear in the Cookies report (or any new cookies are categorized and approved)
- [ ] Consent-state variants tested (Accept All, Reject All, GPC if applicable)
- [ ] Accessibility scan passes severity 1 thresholds

## Deploy
- [ ] Deploy proceeds only if all above are checked
- [ ] Post-deploy Web Audit triggered automatically against production

## Post-deploy (within 24 hours)
- [ ] Full-site audit completes on production
- [ ] All critical Rules pass on production
- [ ] No regression in Page Insights real-user metrics

## Rollback criteria
- Any critical Rule fails post-deploy
- Performance metrics regress beyond the agreed SLA
- An unauthorized vendor appears in the Domains report
```

### How to use the checklist

Embed it in the release ticket. Engineering or release management owns running through it. ObservePoint produces the audit data; the human checks the boxes. Don't over-automate the checklist itself — the act of pausing to check creates the discipline.

## Compliance evidence pack

The quarterly artifact for legal, privacy, or external auditors.

### Skeleton

```markdown
# <Company> Compliance Evidence Pack — Q<N> <year>
Prepared by <Privacy Officer or designee>
For <internal audit committee / external auditor>

## Scope of evidence
- Period covered <YYYY-MM-DD to YYYY-MM-DD>
- Domains audited
- Regulations addressed

## Audit configurations
- Per-audit summary: URL scope, schedule, consent states tested
- Rule library snapshot (version-controlled)

## Run history
- Audit run completion rate <should be 100%>
- Rule pass/fail trend, per Rule, per audit
- Exceptions log: failures, time to remediate, owner

## Vendor inventory
- Full list of third-party vendors receiving data
- Geographic distribution
- Change log since last evidence pack

## Cookie inventory
- Full list with consent classification
- Change log since last evidence pack

## Incidents
- Any critical Rule failures during the period
- Remediation details
- Root cause analysis

## Attestation
- Signed statement from the Privacy Officer confirming the audit ran as scheduled and findings were remediated per policy
```

### Cadence

Quarterly is the standard. Some industries (healthcare, financial) push to monthly. Match the regulator's expectation.

## Quarterly Business Review (QBR)

The document that ties everything together for the executive sponsor.

### Skeleton

```markdown
# Web Governance QBR — Q<N> <year>

## Where we were
Recap of Q-1 priorities and what we said we'd do.

## What we did
- Audits operating: <N>
- Rules in production: <N>
- Coverage: <% of high-traffic pages>, <% of revenue-driving pages>
- Incidents detected: <N>
- Incidents resolved within SLA: <%>
- Time to detect (P50, P90)
- Time to resolve (P50, P90)

## What we learned
- Patterns in incidents
- Failure modes that surfaced
- Wins (broken tracking caught early, regulator inquiry avoided, etc.)

## Where we're going
- Next quarter's priorities
- Resourcing needs
- Risks we want the executive sponsor to weigh in on
```

### Length

Two pages max. Executives skim. The numbers matter more than the prose.

## Tag inventory CSV

For when the user asks "just give me a list."

### Columns

```
domain, tag_name, tag_category, vendor, first_seen_date, last_seen_date,
url_pattern, fires_on_consent_state, data_layer_attributes_used, owner,
business_justification, retention_period, lawful_basis
```

The last four columns aren't from ObservePoint directly — they require human input from the privacy or analytics owner. The skeleton invites that input.

## Style notes for every deliverable

- **Concise over comprehensive.** Two-page documents get read; ten-page documents get filed.
- **Numbers before prose.** "We detected 23 vendors" lands harder than "We detected a significant number of vendors."
- **Severity before everything.** Don't make the reader figure out what matters; rank it.
- **Date the artifact.** Anything undated decays in trust.
- **Sign the artifact.** Even internally — accountability matters.
- **Link the source.** Every claim in the deliverable should be traceable to an ObservePoint report or a documented decision.

---

*Last verified: 2026-05-28*
