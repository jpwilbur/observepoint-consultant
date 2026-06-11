# Industry playbook — government / public sector

Load this when the user is a federal agency, a state or local government body, or any public-sector property (.gov, .mil, .us, state/county/city sites), or asks about Section 508 accessibility, ADA Title II web obligations, a no-third-party-tracking baseline on a public site, or serving residents across many states. This playbook is compact: government's MarTech surface is deliberately thin, so the work concentrates on accessibility conformance and on keeping the property clean of unauthorized trackers.

## Industry context

Public-sector web spans three tiers: **federal** (agency sites, .gov/.mil, federal services), **state** (state agencies, DMV, benefits portals, tax), and **local** (county and city sites, utilities, courts, libraries). The unifying trait across all three is that these are public services, not commercial properties — there is no funnel to optimize and no ad spend to attribute. That changes the entire audit emphasis.

Three traits define the vertical:

- **Accessibility is the primary driver.** A government website that a person with a disability cannot use is an excluded citizen, and that exclusion is legally actionable. Section 508 (federal) and ADA Title II (state and local) make WCAG conformance a binding obligation, not a best practice. This is the single biggest reason a public-sector body buys web governance.
- **A no-third-party-tracking baseline is the expectation.** A .gov property is not supposed to surveil its visitors. The working assumption for a public site is that *no* third-party advertising or behavioral tracker fires at all — the baseline is zero, and any third-party domain is an exception that needs justification.
- **Multi-state residency considerations** apply to state and local bodies whose sites are used by residents (and non-residents) from many states. A state benefits portal touches people who fall under a patchwork of state privacy laws, so the cross-jurisdiction question is real even when the property runs almost no tracking.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **Accessibility conformance (Section 508 / ADA Title II / WCAG 2.1 AA).** Run Web Audits with accessibility scanning across the public site and pull the Accessibility Report (and the 2026 Accessibility Highlight Report) to track violations by severity. This is the recurring deliverable — the conformance evidence the agency's accessibility lead and legal counsel rely on.
- **Zero-unauthorized-tracking baseline enforcement.** Assert that no third-party advertising or analytics tracker fires anywhere on the property, then alert the instant one appears. The baseline is strict because the expectation is strict.
- **Cross-jurisdiction privacy for state/local.** A property serving residents of many states inherits a patchwork of obligations. Where any tracking exists at all, audit it against the strictest applicable state posture and confirm opt-out / GPC signals are honored.
- **Vendor inventory for public-records and transparency.** Public bodies are frequently subject to records and transparency obligations. A standing inventory of every request domain and cookie on the property — via the Domains & Geo Privacy Report and the cookie inventory — answers "what runs on our site?" without a fire drill.

## Regulations

Government's regulatory exposure is dominated by **accessibility**, with a thin privacy layer on top for state/local bodies. Do not restate effective dates or enforcement detail — the accessibility audit motion lives in the **privacy-compliance** skill, Accessibility (WCAG 2.1 AA / European Accessibility Act).

- **Section 508 (federal accessibility).** Section 508 of the Rehabilitation Act requires federal agencies' electronic and information technology to be accessible, and it incorporates WCAG 2.1 AA as the technical standard. This is the dominant exposure for any federal property. ObservePoint's automated WCAG scanning produces the conformance evidence; pair it with manual review for what automation cannot test.
- **ADA Title II (state and local government).** The 2024 DOJ rule under ADA Title II sets WCAG 2.1 AA as the standard for state and local government web content and mobile apps, with compliance deadlines phasing in by entity size. This is the dominant exposure for state and local bodies — the same WCAG scan motion, a different legal hook.
- **U.S. state privacy laws (state/local, where any tracking exists).** A state or local site serving residents of many states sits under the patchwork of comprehensive state laws. See the U.S. state matrix in the **privacy-compliance** skill. In practice the cleanest defense is the zero-tracking baseline below — if nothing non-essential fires, most of the state-law surface never engages.

Both Section 508 and ADA Title II resolve to the same technical target — WCAG 2.1 AA — so the audit is one motion that satisfies two legal regimes. For the impact-prioritization scoring, the violation-remediation catalog, and the MCP-tool workflow that turns a raw scan into a ranked queue, see the **accessibility** skill; the WCAG/EAA section of the **privacy-compliance** skill carries the regulation-to-coverage mapping and effective dates.

## Common vendor patterns

The public-sector stack is restrained by design — this is the thinnest vendor footprint of any vertical.

- **Analytics.** Often a government-approved analytics deployment. Federal agencies frequently standardize on the U.S. Digital Analytics Program (DAP), and GA4 appears on state and local sites. The expectation is first-party, privacy-respecting measurement, not behavioral profiling.
- **Ad-tech.** Minimal to none. A public service has nothing to retarget, so there should be no Meta Pixel, Google Ads tag, or programmatic vendor on the property. Finding one is the headline event.
- **The characteristic risk: an inherited marketing tag on a .gov page.** The way a tracker lands on a government site is almost never deliberate — it rides in through a CMS theme, an embedded widget (a social-share button, a YouTube embed, a third-party form vendor), or a contractor who copied a snippet from a commercial template. The governance job is catching the inherited tag, not policing an ad team that doesn't exist.

For the module-by-module breakdown of how ObservePoint audits each layer, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the property.

**1. No third-party tracker fires anywhere on the property (strict baseline).** The defining government Rule — the baseline is zero, not "consent-gated."

```
WHEN page URL matches /.*/ (entire property)
EXPECT
  no tags in category "Advertising" fire
  no tags in category "Analytics" fire EXCEPT the approved analytics (DAP / GA4 property ID)
  no third-party request domains receive data EXCEPT the approved-vendor allowlist
```

**2. Accessibility scan passes Section 508 / WCAG 2.1 AA thresholds.** The conformance guard. Attach the accessibility scan to the Web Audit and assert no critical/serious violations on the priority templates (home, primary navigation, the top public-service pages and forms). The **accessibility** skill carries the full prioritization and Rule pattern; the scan itself is the WCAG motion from the **privacy-compliance** skill.

```
WHEN accessibility scan runs on page templates IN ("home", "service landing", "online form")
EXPECT
  zero violations at severity "critical"
  zero violations at severity "serious"
  (track "moderate" / "minor" as a backlog, not a gate)
```

**3. A newly-appeared third-party domain triggers an alert.** Because the baseline is zero, any new request domain is by definition an exception worth a human's attention.

```
WHEN a request domain appears that is NOT on the approved-vendor allowlist
EXPECT an alert fires to the web team + accessibility/privacy lead
  (use find_first_observed to date exactly when the domain first appeared,
   then trace it to the CMS change or embed that introduced it)
```

Pair Rule 1 with the cookie inventory and `get_request_privacy_report` to produce the standing "what runs on our site" record, and use `find_first_observed` whenever Rule 3 fires to turn "a stranger's tag is on our site" into a specific change to roll back.

## Common pitfalls

The failure modes that recur in public-sector specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **Inherited marketing tag on a public-service page.** *Pitfall:* a third-party tracker rides in through a CMS theme, an embedded widget, or a contractor's copied snippet and starts firing on a benefits or tax page — a public site quietly surveilling citizens. *Catch:* the zero-tracking baseline Rule (Rule 1) fails the instant the tag fires; `find_first_observed` dates when the domain first appeared. *Fix:* remove the embed or theme component that carries it; if the third-party feature is genuinely needed, self-host or proxy it so no tracker loads.
- **Accessibility regressions from a CMS update.** *Pitfall:* a CMS or theme update changes markup — drops an `alt` attribute pattern, breaks heading order, lowers contrast — and silently regresses Section 508 / WCAG conformance that was previously passing. *Catch:* the scheduled accessibility scan (Rule 2) shows the new critical/serious violations against the prior clean run. *Fix:* treat the accessibility scan as a release gate on CMS and theme changes; revert or patch the regressing component before it ships to the public site.
- **A vendor added without authorization.** *Pitfall:* a department or contractor adds a form vendor, chat widget, or analytics tag without going through governance, and it lands on a .gov page outside the approved-vendor list. *Catch:* the new-domain alert (Rule 3) flags the unrecognized request domain on the next run. *Fix:* enforce the allowlist as policy — every new vendor is an exception that gets reviewed before it ships, not discovered after.

## CSM cadence

The recommended rhythm for a public-sector account:

- **Weekly audits** on the public property, with an **accessibility focus** — the WCAG scan is the recurring deliverable, run every week and trended so a CMS-driven regression surfaces within days, not at the next legal review.
- **Baseline enforcement** runs alongside every accessibility audit: the zero-tracking Rule (Rule 1) and the new-domain alert (Rule 3) on every run.
- **Release gate.** Any CMS or theme change runs a targeted accessibility scan before it goes live — see the CI/CD gate recipe in `references/solution-playbooks.md`.
- **Alert routing.** Accessibility failures route to the **web team and the accessibility lead**; an unauthorized-tracker or new-domain finding routes to the same group plus whoever owns privacy. Because the baseline is strict, a single new third-party domain is worth a same-week conversation.

For the boundaries of what the platform can and can't validate here (native mobile apps, manual accessibility review beyond automated WCAG checks), see `references/limitations.md`.

---

*Last verified: 2026-06-04*
