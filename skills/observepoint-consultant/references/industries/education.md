# Industry playbook — education (K-12 + Higher Ed)

Load this when the user is a school district, an edtech vendor, a college or university, or any education property, or asks about FERPA, COPPA on student portals, state student-data-privacy laws, AADC on prospective students, DOJ Title II accessibility actions against universities, or the sprawling-subdomain governance problem. This playbook is compact and covers **two distinct sub-verticals — K-12 and Higher Ed** — because their properties, regulators, and failure modes differ enough to warrant separate treatment.

## Industry context

**K-12** is school districts and the edtech vendors that serve them. The defining fact is that the users are *minors* — students under 13 trigger COPPA, students under 18 sit under FERPA and a thicket of state student-data laws. The properties are district sites, student/parent portals, and learning platforms (LMS), and the vendor relationship is the risk surface: a district hands student data to dozens of edtech tools, each of which must be governed.

**Higher Ed** is universities and colleges — large, sprawling public web estates that span marketing/admissions, a logged-in student experience, research, athletics, and alumni/donor giving. The users are mostly adults, but *prospective and incoming* students are often minors, which pulls AADC into scope. The defining problem here is not minors-everywhere but *governance at scale*: departments, athletics, and research each run their own tags on their own subdomains, and nobody has a single view.

The two share FERPA and accessibility exposure; everything else diverges. Pin down which sub-vertical you're in during the first conversation.

## K-12

The regulatory stack on a K-12 property, in layers:

- **FERPA** protects student education records — identifiable student data cannot flow to third parties without consent. A tracking pixel on a student portal that ships an identifiable student value to an ad vendor is the FERPA fact pattern. See the **regulation** skill, FERPA.
- **State student-data-privacy laws (SOPIPA-style).** 30+ states (California's SOPIPA being the model) bar edtech vendors from using student data for advertising, building student profiles, or selling student data. See the **regulation** skill, State student data privacy laws.
- **COPPA on under-13s.** Verifiable parental consent before collecting personal information from children under 13, and no behavioral advertising to them — COPPA 2.0 (phasing through 2026) sweeps persistent identifiers into "personal information." See the **regulation** skill, COPPA.
- **Edtech vendor management** is the operational core: the district's exposure is the sum of every tool it has approved, so the vendor inventory *is* the compliance posture.

**Rule example — no advertising tracker fires on student-portal / learning URLs.**

```
WHEN page URL matches /\/student|\/portal|\/learn|\/lms|\/grades/
EXPECT
  no tags in category "Advertising" fire
  no third-party request domain receives an identifiable student value
  the approved edtech vendors are the only third parties present
```

Note **schoolyear-driven traffic**: K-12 properties spike at back-to-school and around enrollment/registration windows, then go quiet over summer. Time the audit cadence and any vendor-onboarding review to the academic calendar, and capture a clean baseline before the August surge.

## Higher Ed

The regulatory and structural picture for a university, in layers:

- **FERPA** applies the same as K-12 — the logged-in student experience (registration, grades, financial aid) is education records, and tracking on those pages is the exposure. See the **regulation** skill, FERPA.
- **AADC on under-18 prospective and incoming students.** Marketing and admissions pages are accessed by minors researching colleges, which pulls the California Age-Appropriate Design Code (where in force — verify the current injunction status) onto the prospect-facing surface. See the **regulation** skill, California AADC.
- **DOJ Title II accessibility actions (active in 2026).** The 2024 DOJ ADA Title II rule sets WCAG 2.1 AA for public university web content, and enforcement against universities is active through 2026. Course catalogs, application flows, and the logged-in student experience are the high-traffic templates that must conform. The accessibility audit motion is in the **regulation** skill, Accessibility (WCAG 2.1 AA).
- **The sprawling-subdomain problem.** A university is not one site — it is hundreds. Departments, athletics, research labs, and the alumni/donor office each run their own CMS instance and their own tags on their own subdomain, with no central container and no shared governance. This is the defining Higher Ed challenge: you cannot govern what you have not discovered.

**Rule example — PII canary on a logged-in student journey.** Script a Journey through login → a student-record page, typing a known fake student name and ID, then run `scan_journey_pii` in canary mode — any downstream appearance of that literal in a tag, cookie, or request is a definitive FERPA leak with zero false positives.

```
WHEN scan_journey_pii runs on the logged-in student journey (canary: fake student name + ID)
EXPECT
  the canary value appears in NO third-party tag, cookie, request, or POST body
```

**Rule example — accessibility scan on course-catalog + application pages.** Attach the accessibility scan to a Web Audit on the high-traffic public templates.

```
WHEN accessibility scan runs on page templates IN ("course catalog", "application / apply")
EXPECT
  zero violations at severity "critical"
  zero violations at severity "serious"
```

## Regulations

Education's exposure layers student-data privacy on top of accessibility. Do not restate effective dates or enforcement detail — those live in the **regulation** skill:

- **FERPA**, **COPPA / COPPA 2.0**, **California AADC**, and **state student data privacy laws** — see the named sections in the **regulation** skill.
- **Accessibility (WCAG 2.1 AA / EAA)** — the Section 508 / DOJ Title II target is WCAG 2.1 AA; see the **regulation** skill, Accessibility, for the regulation-to-coverage mapping and effective dates, and the **accessibility** skill for the impact-prioritization model, the violation-remediation catalog, and how the accessibility scan and reports work.

## Common vendor patterns

The education stack, by layer:

- **LMS (learning management).** Canvas, Blackboard, Moodle, D2L Brightspace — the logged-in learning core, where FERPA-protected activity lives. Confirm no advertising or behavioral tag rides inside the LMS frame.
- **Edtech tools.** A long tail of point solutions (assessment, tutoring, content, proctoring), each a separate vendor-governance question and each bound by the state student-data laws.
- **CRM / admissions.** Slate is the dominant admissions CRM; it powers the application and prospect-nurture flow where AADC and prospect-PII exposure concentrate.
- **Analytics.** GA4 most often, frequently deployed inconsistently across the subdomain estate.
- **The subdomain-sprawl governance problem (Higher Ed).** The hard part is not any single vendor but the *absence of a single view*. Departments, athletics, and research run ungoverned tags on their own subdomains. A broad crawl across the full estate is the only way to inventory what's actually firing — that discovery is the precondition for any governance.

For the module-by-module breakdown of how ObservePoint audits each layer, see `references/products-and-modules.md`.

## Common pitfalls

The failure modes that recur in education specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **Edtech vendor using student data for advertising.** *Pitfall:* an approved learning or assessment tool quietly ships an identifiable student value to an advertising endpoint, violating FERPA and the state student-data laws. *Catch:* the no-advertising-tracker Rule on student/learning URLs fails; `scan_audit_pii` (or the `scan_journey_pii` canary) surfaces the masked leak path to the third-party domain. *Fix:* reconfigure or remove the vendor's advertising integration; if the vendor can't stop, it fails the student-data-law bar and shouldn't be on the property.
- **Department subdomain with ungoverned tags.** *Pitfall:* a department or athletics site runs its own Meta Pixel or analytics tag on a university subdomain that central IT has never inventoried. *Catch:* a broad crawl across the subdomain estate plus the request-domain inventory surfaces the rogue tags; `find_first_observed` dates when each appeared. *Fix:* bring the subdomain under the shared governance baseline and the approved-vendor allowlist; remove what isn't approved.
- **Application flow leaking prospect PII.** *Pitfall:* the admissions application or inquiry form sends a prospect's name, email, or other identifying value to a third party before consent — and the prospect may be a minor (AADC). *Catch:* `scan_journey_pii` canary on the application Journey catches the typed value escaping to a third-party request. *Fix:* stop the leak at the form, gate any legitimate vendor behind consent, and re-run the canary to confirm.
- **Accessibility gaps on the course catalog.** *Pitfall:* the high-traffic course catalog or application pages carry critical WCAG violations that expose the university to a DOJ Title II action. *Catch:* the scheduled accessibility scan flags the critical/serious violations on those templates. *Fix:* remediate the flagged components and add the accessibility scan as a release gate on catalog and application changes.

## CSM cadence

The recommended rhythm for an education account:

- **Weekly audits** on the priority properties — student/parent portals and learning URLs for K-12; the logged-in student experience, course catalog, and application flow for Higher Ed.
- **Broad-crawl the Higher Ed estate** on a recurring schedule to keep the subdomain-sprawl inventory current — discovery is continuous because new department and research subdomains appear constantly.
- **Calendar-aware cadence for K-12:** capture a clean baseline before back-to-school, and tighten review around enrollment/registration windows.
- **Accessibility scan** runs weekly and trended, with a release gate on CMS, catalog, and application changes — see `references/solution-playbooks.md`.
- **Alert routing.** Student-data and PII-leak findings route to the **web and privacy** teams; accessibility failures route to web plus the accessibility lead. An ungoverned-subdomain finding goes to whoever owns central web governance.

For the boundaries of what the platform can and can't validate here (native mobile apps, manual accessibility review beyond automated WCAG checks), see `references/limitations.md`.

---

*Last verified: 2026-06-04*
