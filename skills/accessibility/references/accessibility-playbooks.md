# Accessibility playbooks — prioritizing and defending WCAG conformance work

Load this file when the user needs to prioritize accessibility findings, asks about ADA / Section 508 / European Accessibility Act obligations, wants the "highest-impact fix first" on a site full of violations, or runs the `/op-accessibility-priorities` command. It also covers what to do when a customer receives an ADA Title III demand letter and needs technical evidence.

This is the operational companion to the WCAG / European Accessibility Act entry in the **regulation** skill. That file carries the regulation-to-coverage mapping and the effective dates; this file carries the litigation framing, the impact-prioritization scoring, the violation-remediation catalog, and the MCP-tool workflows that turn a raw scan into a ranked work queue. Read both together; this file does not restate the dates.

The job is almost never "fix everything." A real site produces hundreds to thousands of automated findings, and they are not equal — a missing form label on the checkout button matters far more than a low-contrast caption on an archived blog post. The value this playbook adds is the ranking: severity times traffic-weighted exposure times affected-population impact, so the team works the queue in the order that reduces the most user harm and the most legal exposure per hour spent.

## Contents

- [Accessibility legal landscape (2026)](#accessibility-legal-landscape-2026)
- [ObservePoint accessibility tooling](#observepoint-accessibility-tooling)
- [Impact-prioritization framework](#impact-prioritization-framework)
- [Top accessibility violations + remediation](#top-accessibility-violations--remediation)
- [MCP-tool workflows for accessibility](#mcp-tool-workflows-for-accessibility)
- [Industry-specific accessibility patterns](#industry-specific-accessibility-patterns)
- [Accessibility lawsuit defense](#accessibility-lawsuit-defense)

## Accessibility legal landscape (2026)

There is no single federal web-accessibility statute in the United States, yet web accessibility is one of the most-litigated areas of digital compliance. The pressure comes from several directions at once, and the through-line is WCAG: even where no law names it, courts and regulators treat WCAG 2.1 AA as the de-facto technical standard. For the conformance-level definitions and the European Accessibility Act effective date, see the WCAG / EAA entry in the **regulation** skill; the framing below is the litigation and enforcement layer that file does not cover.

**ADA Title III (private businesses).** Title III of the Americans with Disabilities Act bars discrimination in places of "public accommodation." There is no federal regulation specifying a web standard, so courts have filled the gap by applying WCAG 2.1 AA as the measuring stick. The result is a sustained serial-litigation wave: thousands of demand letters and federal complaints filed every year, concentrated in a handful of plaintiff-friendly jurisdictions, often targeting retail, hospitality, and consumer-services sites. Many resolve as quick settlements because litigating is more expensive than remediating — which is exactly why a defensible remediation record matters.

**ADA Title II (state and local government).** The DOJ's April 2024 final rule under Title II adopted WCAG 2.1 AA as the binding technical standard for state and local government web content and mobile apps. Compliance deadlines phase in by entity size: larger entities (population 50,000 and above) hit their deadline first, smaller entities and special-district governments later. Those deadlines are landing across 2026 and into 2027, so this is an active, near-term obligation for any public-sector property — not a future concern. See `references/industries/government-public-sector.md`.

**Section 508.** Section 508 of the Rehabilitation Act requires federal agencies' electronic and information technology to be accessible, incorporating WCAG 2.1 AA as the technical standard. It reaches federal agencies directly and flows down to contractors and vendors selling into the federal government through procurement requirements (the Accessibility Conformance Report / VPAT is the standard artifact). A vendor that wants federal business needs conformance evidence for its own product, not just the agency's site.

**European Accessibility Act (EAA).** Effective June 28 2025, the EAA extends accessibility obligations across the EU to a defined set of products and services (e-commerce, banking, e-books, transport ticketing, and more), with WCAG-aligned technical requirements via the EN 301 549 standard. For the date and scope detail, cross-reference the **regulation** skill; the operational motion is the same WCAG scan, applied to in-scope EU services.

**State laws amplifying the ADA.** Several states add statutory teeth on top of the federal ADA. California's Unruh Civil Rights Act is the most consequential: it ties to ADA violations and provides statutory minimum damages (per the statute, a floor per violation) plus attorney's fees, which is what makes California a hotspot for accessibility filings. New York's accessibility case law is similarly active under state and city human-rights provisions. The pattern: the ADA supplies the standard, the state law supplies the damages, and that combination drives the volume.

**The unifying technical target.** Section 508, ADA Title II, ADA Title III (as courts apply it), the EAA, and the state amplifiers all resolve to the same place: WCAG 2.1 AA conformance. One scan motion produces evidence relevant to all of them. That is why accessibility work is best run as a single recurring program rather than per-statute.

**WCAG 2.2 as the forward target.** WCAG 2.2 AA (finalized 2023) is the direction of travel — it adds success criteria around focus appearance, dragging alternatives, target size, and consistent help. Most binding U.S. obligations still name 2.1 AA in 2026, but 2.2 is what new procurement language and forward-looking programs increasingly reference. Treat 2.1 AA as the floor you must clear and 2.2 AA as the bar you build toward; the prioritization framework below is version-agnostic.

**Procurement and the VPAT.** Section 508's reach into the private sector runs through procurement: a vendor selling software or a website experience to a federal agency is expected to supply an Accessibility Conformance Report (ACR), commonly delivered as a VPAT (Voluntary Product Accessibility Template). The VPAT documents conformance claim-by-claim against the WCAG criteria. ObservePoint's scan history feeds the machine-testable portion of that document with current, dated evidence — but the VPAT is an attestation that also requires the manual-testing record, so automation supports it rather than producing it.

## ObservePoint accessibility tooling

ObservePoint adds automated WCAG checks to the same browser-based scanning engine it uses for tag and privacy work, so accessibility findings come out of the same audit run that produces the tag inventory and cookie report. See `references/products-and-modules.md` for the module map.

- **Automated WCAG 2.1 AA scanning in Web Audits.** Attach accessibility scanning to a Web Audit and every crawled page is checked against the machine-testable WCAG success criteria. Because it rides the existing crawl, you get site-wide coverage on the same schedule as the rest of the audit, and findings are trended run over run.
- **The Accessibility Report.** The standing report that lists violations by page, by WCAG success criterion, and by severity. This is the analyst's working surface for triage.
- **The Accessibility Highlight Report (new in 2026).** A severity-graded view designed to surface the findings that matter most, faster — the report a lead opens to answer "where do we start?" rather than reading the full violation list.
- **The Debugger accessibility additions (early 2026).** The Tag & Cookie Debugger (Chrome extension) added in-browser accessibility highlights, so an analyst can see violations live on a single page during hands-on debugging. Use it for spot-checking a fix; use the cloud Web Audit for reporting and trending. The Debugger is not a compliance-reporting surface.

**Be honest about what automation covers.** Automated scanning reliably detects roughly 30-40% of WCAG success criteria — the machine-testable ones (missing alt text, missing labels, programmatic contrast ratios, missing `lang`, broken heading structure, ARIA validity). It cannot judge whether alt text is *meaningful*, whether a complex custom widget actually works with a screen reader, whether focus order makes *sense* to a human, or whether captions are *accurate*. Those require manual review and assistive-technology testing by people, ideally including people with disabilities. ObservePoint's automated scan is the high-volume, repeatable, regression-catching layer; it is not a conformance certificate. State this plainly to customers — overselling automated coverage is itself a liability. See `references/limitations.md` for the boundary detail.

**Where automation earns its keep.** The 30-40% it catches is exactly the high-volume, repetitive, regression-prone layer that manual testing is worst at: a single CMS theme change can drop the `alt` pattern across thousands of images, and only a scheduled site-wide scan catches that the same day. The right division of labor is automation for breadth and regression-catching (run every release, trend over time), manual and assistive-tech testing for depth on the tier-1 flows. The accessibility evidence belongs in the same recurring deliverable as the rest of the governance program — fold the Accessibility Highlight Report into the cadence and exception log described in `references/consulting-deliverables.md`.

## Impact-prioritization framework

The core of this file. A scan returns a flat list of violations; the team needs a ranked queue. Rank by three factors, then sort descending. The output is "fix this first," with a defensible reason attached to every item.

**The three factors.**

1. **Severity (how badly it breaks the experience).** Map the scanner's severity to a weight. A *critical* violation blocks a user from completing a task (an unlabeled checkout button a screen-reader user cannot identify). A *serious* violation makes a task painful but not impossible. *Moderate* and *minor* degrade quality. Suggested weights: critical = 10, serious = 6, moderate = 3, minor = 1.
2. **Traffic-weighted page exposure (how many people hit it).** A violation on the homepage, the primary navigation, or the checkout flow is seen by orders of magnitude more users than the same violation on a low-traffic archived page. Weight by relative traffic or page tier: tier-1 templates (home, nav, checkout, primary forms, sign-in) = 5, tier-2 (category and key content pages) = 3, tier-3 (long-tail, archive) = 1. Pull traffic from the customer's analytics; absent that, use page-template tiers.
3. **User-population impact (who it harms, and how central the task is).** A violation that blocks a transactional or essential task (apply for benefits, book an appointment, complete a purchase, pay a bill) outranks one on an informational page. A violation affecting a broad population (no keyboard access affects every keyboard and switch user) outranks a narrow edge case. Weight: blocks an essential/transactional task = 3, important task = 2, informational = 1.

**The priority score.**

```
priority_score = severity_weight x page_exposure_weight x population_impact_weight
```

A worked example. A missing form label (critical, weight 10) on the checkout button (tier-1, weight 5) blocking a purchase (transactional, weight 3) scores `10 x 5 x 3 = 150`. A low-contrast caption (minor, weight 1) on an archived blog post (tier-3, weight 1) on an informational page (weight 1) scores `1 x 1 x 1 = 1`. The checkout label is 150x the priority. That ratio is the whole point — it tells a team with limited hours exactly where the next hour goes.

**The "fix this first" output.** Sort the violations by `priority_score` descending and present the top items as a ranked work queue. Each row carries: the violation, the WCAG success criterion, the affected scope (which templates / how many pages / estimated traffic), the priority score, and the remediation step. A practical refinement: when two items score close, break the tie by remediation effort — a one-line `alt` attribute fix that clears a tier-1 critical beats a deep custom-widget rebuild of equal score, because it removes user harm sooner. Track the running total of cleared critical/serious findings on tier-1 templates as the headline metric; that trajectory is also what the lawsuit-defense section below relies on.

A ranked queue for a retail site looks like this — the exact shape the `/op-accessibility-priorities` command should emit:

| Rank | Violation | WCAG SC | Scope | Sev x Exp x Pop | Score | Fix |
|---|---|---|---|---|---|---|
| 1 | Unlabeled "Place order" button | 4.1.2 (A) | Checkout (tier-1, transactional) | 10 x 5 x 3 | 150 | Add `aria-label` / associated label to the submit control |
| 2 | No visible focus on cart controls | 2.4.7 (AA) | Cart (tier-1, transactional) | 6 x 5 x 3 | 90 | Restore a visible focus style on the quantity / remove controls |
| 3 | Product images missing alt text | 1.1.1 (A) | Product pages (tier-2, important) | 6 x 3 x 2 | 36 | Generate meaningful `alt` from product name + key attribute |
| 4 | Low contrast on promo banner text | 1.4.3 (AA) | Home (tier-1, informational) | 3 x 5 x 1 | 15 | Darken text or lighten background to meet 4.5:1 |
| 5 | "Read more" links in blog feed | 2.4.4 (A) | Blog index (tier-3, informational) | 3 x 1 x 1 | 3 | Rewrite link text to name the destination article |

The two critical/serious findings on the conversion path (ranks 1-2) are where the team spends its first hours; the blog-feed link text (rank 5) is real but waits. The score column is the defensible reason attached to every line — when a stakeholder asks "why isn't *my* page first?", the math answers.

**A note on gates vs. backlog.** Treat critical and serious findings on tier-1 templates as a release gate (block the deploy, see the CI/CD recipe in `references/solution-playbooks.md`). Treat moderate and minor findings as a managed backlog worked down over time. Trying to gate on every finding stalls releases and trains teams to ignore the gate; gating on the findings that cause real harm keeps the gate credible.

## Top accessibility violations + remediation

The most common machine-detectable violations, the ones an automated scan surfaces in volume. For each: what it is, who it harms, the WCAG success criterion, and the fix. These are the building blocks of the ranked queue above.

| Violation | What it is / who it harms | WCAG SC | Remediation |
|---|---|---|---|
| **Missing alt text** | Images with no text alternative. Screen-reader users hear "image" or a filename instead of meaning; decorative images that should be silent get announced. | 1.1.1 Non-text Content (A) | Add concise, meaningful `alt` describing the image's purpose. Use empty `alt=""` for purely decorative images so they're skipped. Don't stuff keywords. |
| **Missing form labels** | Inputs with no programmatically associated label. Screen-reader users can't tell what a field is for; the canonical "what is this checkout button?" failure. | 1.3.1 Info and Relationships (A); 4.1.2 Name, Role, Value (A) | Associate a visible `<label for>` with each input, or use `aria-label` / `aria-labelledby` where a visible label isn't feasible. Placeholder text is not a label. |
| **Insufficient color contrast** | Text whose contrast against its background is below the threshold. Low-vision users and anyone in bright light can't read it. | 1.4.3 Contrast (Minimum) (AA) | Meet 4.5:1 for normal text and 3:1 for large text. Adjust foreground/background colors; don't rely on color alone to convey meaning (1.4.1). |
| **Missing focus indicators / focus order** | No visible focus ring, or a tab order that jumps around illogically. Keyboard and switch users can't see where they are or navigate predictably. | 2.4.7 Focus Visible (AA); 2.4.3 Focus Order (A) | Keep a visible focus style (don't `outline: none` without a replacement). Ensure DOM order matches visual order so focus moves logically. |
| **ARIA misuse** | Wrong roles, invalid attributes, or ARIA layered on native elements that didn't need it. Often *worse* than no ARIA — it lies to assistive tech about what an element is. | 4.1.2 Name, Role, Value (A) | Prefer native HTML elements over ARIA. Where ARIA is needed, use valid role/property combinations and keep state attributes (`aria-expanded`, `aria-checked`) in sync with the UI. |
| **Broken heading hierarchy** | Skipped levels (h1 → h4) or headings used for visual size, not structure. Screen-reader users navigate by headings; a broken outline makes the page a maze. | 1.3.1 Info and Relationships (A); 2.4.6 Headings and Labels (AA) | One `h1` per page, then descend without skipping levels. Use CSS for size; use heading tags for structure. |
| **Missing `lang` attribute** | The page's `<html>` element has no language declared. Screen readers may pronounce content in the wrong language, producing gibberish. | 3.1.1 Language of Page (A) | Set `<html lang="en">` (or the correct code). Mark in-page language changes with `lang` on the relevant element (3.1.2). |
| **Non-descriptive link text** | Links reading "click here" / "read more" / a raw URL. Screen-reader users tabbing through a link list hear no destination, only "read more, read more, read more." | 2.4.4 Link Purpose (In Context) (A) | Write link text that describes the destination ("Read the 2026 accessibility report"). Avoid bare "click here"; avoid exposing raw URLs as link text. |
| **Tables without headers** | Data tables with no `<th>` or header associations. Screen-reader users lose the row/column context that makes a table readable. | 1.3.1 Info and Relationships (A) | Use `<th>` for header cells with `scope="col"` / `scope="row"`. Reserve tables for tabular data, not layout. |
| **Missing video captions** | Pre-recorded video/audio with no captions or transcript. Deaf and hard-of-hearing users get no access to the content. (Automation flags the *absence* of a caption track; it can't judge caption accuracy — that's manual.) | 1.2.2 Captions (Prerecorded) (A) | Provide synchronized captions for prerecorded audio content and a transcript where appropriate. Auto-captions need human review for accuracy. |

These ten cover the bulk of what an automated scan returns. The first five (alt text, labels, contrast, focus, ARIA) are where most tier-1 critical/serious findings concentrate, so they tend to dominate the top of the ranked queue.

## MCP-tool workflows for accessibility

Concrete tool sequences that turn the accessibility scan into a ranked queue and a monitoring posture. The `accessibility-issues` entity type is a real grid-report entity (see the grid-report entity list in `references/mcp-tools.md`). Only the tool names below are real — verify any tool against `references/mcp-tools.md` before using it. These sequences power the `/op-accessibility-priorities` command.

**1. Discover the columns before you query.** Always start here — grid-report column names vary by entity type, and guessing wastes a round trip.

```
mcp__ObservePoint__get_report_schema(entityType="accessibility-issues", search="severity")
```

*What you learn:* the actual column names for severity, the WCAG criterion, the affected page/URL, and the rule identifier. *Action:* use those exact column names in the query below. Re-run with `search="page"` or `search="wcag"` to find the exposure and criterion columns.

**2. Pull and rank the findings.** Query the `accessibility-issues` entity for the audit run, then apply the prioritization framework.

```
mcp__ObservePoint__query_report(entityType="accessibility-issues", auditId=..., runId=...,
  columns=[severity, wcagCriterion, pageUrl, ...], filters={ severity in ["critical","serious"] })
```

*What you learn:* every violation with its severity, criterion, and affected page. *Action:* compute `priority_score = severity x page_exposure x population_impact` per the framework, sort descending, and emit the "fix this first" queue. Filtering to critical/serious first keeps the initial queue focused on the findings that cause real user harm and carry the most legal exposure.

**3. Catch accessibility-adjacent regressions.** Browser errors and broken pages frequently break the accessibility tree (a JavaScript error that fails to render a labeled component shows up as a console error before it shows up as a missing-label finding).

```
mcp__ObservePoint__find_anomalies(auditId=..., metric="pages-with-browser-errors")
```

*What you learn:* runs where pages-with-browser-errors jumped versus the prior run (scope-aware — a page-count change of 20%+ is labeled "scope-change," not a false anomaly). *Action:* investigate the spiking run; a rendering regression that breaks components is often an accessibility regression too. Pair with `mcp__ObservePoint__get_browser_logs` to read the specific errors and `mcp__ObservePoint__get_metric_trend(metric="pages-with-browser-errors")` to see the trajectory.

**4. Date when a regression first appeared.** When a critical finding shows up, prove when it landed.

```
mcp__ObservePoint__find_first_observed(auditId=..., ...)
```

*What you learn:* the run/date a finding (or a page condition) first appeared in the audit history. *Action:* trace the regression to the deploy or CMS change that introduced it, and feed the date into the conformance-trajectory evidence for lawsuit defense below.

**5. Build a standing accessibility dashboard.** Make the ranked view a saved report the team and the customer's accessibility lead can open any time.

```
mcp__ObservePoint__create_saved_report(entityType="accessibility-issues",
  filters={ severity in ["critical","serious"] }, columns=[severity, wcagCriterion, pageUrl, ...])
```

*What you learn / produces:* a persistent dashboard of critical/serious findings by page and criterion, trended run over run. *Action:* schedule the underlying Web Audit (weekly for most sites; align with the CSM cadence in the relevant industry playbook), route failures to the web team and accessibility lead, and use the saved report as the recurring conformance-status artifact. Visual evidence for a specific finding comes from `mcp__ObservePoint__get_page_screenshot`.

## Industry-specific accessibility patterns

Short notes on where accessibility pressure concentrates per vertical. Each cross-references the full industry playbook.

- **Healthcare.** Patient portals, appointment booking, and symptom/condition pages are both ADA Title III targets *and* the highest-stakes accessibility surface — a patient who can't book an appointment or read medication instructions is denied care, not just convenience. Prioritize the transactional patient-facing flows. See `references/industries/healthcare-life-sciences.md`.
- **Higher Ed.** Public universities fall under ADA Title II, so the DOJ 2024 rule's WCAG 2.1 AA deadlines are active across 2026. The surface is large and federated (course catalogs, LMS, departmental microsites, PDFs), which makes site-wide automated scanning and a prioritized queue essential — you cannot manually review everything before the deadline. See `references/industries/education.md`.
- **Government.** Section 508 (federal) and ADA Title II (state/local) both resolve to WCAG 2.1 AA, so one scan satisfies two regimes. Public-service flows (apply for benefits, pay a bill, renew a license) are essential tasks, so they top the priority queue by population impact. See `references/industries/government-public-sector.md`.
- **Retail / e-commerce.** The serial-litigation epicenter under ADA Title III, concentrated on the conversion path: product pages, cart, and checkout. A screen-reader-inaccessible checkout is both the most-litigated failure and the highest-revenue-impact one, so it sits at the top of the queue on a retail site. See `references/industries/retail-ecommerce.md`.

## Accessibility lawsuit defense

This section parallels the tort-defense pattern in the `litigation-defense` skill. When a customer receives an ADA Title III demand letter or class complaint, ObservePoint produces the technical record of what their accessibility posture was and how it has moved over time. As with the privacy file: this is technical evidence, not legal advice, and automated scanning alone does not prove conformance. Coordinate with the customer's accessibility and legal experts.

**What's typically alleged.** The plaintiff (often a serial filer, frequently a screen-reader user) states they could not use the site to complete a task and that the site fails WCAG 2.1 AA. Demand letters tend to be templated and short on specifics; the leverage is the cost asymmetry — settling is cheaper than litigating. A demonstrable, ongoing remediation program changes that calculus.

**What ObservePoint produces.**

- **Conformance trajectory.** The audit run history showing accessibility findings over time — ideally a declining count of critical/serious violations on tier-1 templates. This is the central artifact: it shows the site was being actively monitored and was improving, not neglected. Pull it from the run history plus the `accessibility-issues` saved report.
- **Remediation timeline.** When specific findings were detected and when they were resolved, with dates. `find_first_observed` dates when an issue appeared; the subsequent runs where it no longer appears date the fix. This is the "we found it and fixed it within a defined window" evidence.
- **Current state.** The most recent scan results for the pages named in the complaint — what passes now, and the manual-testing record that backs up the automated scan.
- **Process evidence.** The audit definitions, the schedule cadence, and the alert routing — proof that accessibility checking is a regular, defined process rather than an after-the-fact scramble. This mirrors the "reasonable practices" narrative in the privacy-litigation file.

**Assemble the pack as** (parallel to the `litigation-defense` skill → producing the evidence pack):

1. An executive summary: what was scanned, the conformance trajectory, what was remediated, current state.
2. A trajectory appendix: run-over-run critical/serious counts on the named pages, with dates (export via `mcp__ObservePoint__export_report`).
3. A remediation log: findings, detection dates, resolution dates.
4. The process record: audit definitions, schedule, alert routing.
5. The manual-testing record (from the customer's accessibility team) that pairs with the automated scan — because automation alone does not prove conformance.

**Frame it honestly.** The evidence shows a good-faith, documented, improving remediation program and the current technical state. It does not — and ObservePoint should never claim it does — prove WCAG or ADA *conformance*, guarantee a litigation outcome, or substitute for manual and assistive-technology testing. ObservePoint detects the machine-testable subset and produces the technical record; counsel and accessibility experts build the defense around it. The strongest position is the customer who can show they were already scanning, already prioritizing by impact, and already remediating before the letter arrived.

---

*Last verified: 2026-06-04*

*This describes technical detection and evidence, not legal advice or a conformance guarantee. Automated scanning catches a subset of WCAG criteria; pair with manual and assistive-technology testing. Coordinate with accessibility and legal experts.*
