# Industry playbooks — index

This directory holds the per-industry playbooks: one file per vertical, each carrying the regulatory exposure, vendor patterns, Rule examples, pitfalls, and CSM cadence that are specific to that industry. They sit on top of the cross-cutting references (the **regulation** skill, `references/solution-playbooks.md`, `references/products-and-modules.md`) and specialize the general advice for a named vertical.

**How the consultant uses these.** When a user names or implies their vertical — "we're a hospital," "we run a state benefits portal," "our checkout funnel," "we're a university" — load the matching industry file and lead with its specifics rather than the generic playbook. Each file follows the same shape: industry context → top use cases → regulations → common vendor patterns → industry-specific Rule examples → common pitfalls → CSM cadence. If a user spans two verticals (a retailer with a video catalog, a health system with a marketing site), load both and reconcile.

## The seven industries

| File | Vertical | The defining angle |
|---|---|---|
| `retail-ecommerce.md` | Retail / e-commerce | Peak-season tracking readiness, conversion-funnel validation, ad-pixel sprawl |
| `financial-services-insurance.md` | Financial services & insurance | GLBA / NPI, strict consent, regulated-tag scrutiny |
| `healthcare-life-sciences.md` | Healthcare & life sciences | HIPAA / PHI, the Meta Pixel litigation wave, patient portals |
| `travel-hospitality.md` | Travel & hospitality | Multi-step booking funnels, multi-jurisdiction visitors, OTA partners |
| `media-publishing.md` | Media & publishing | IAB TCF / GPP, VPPA on video, programmatic ad-stack governance |
| `government-public-sector.md` | Government & public sector | Section 508 / ADA Title II accessibility, no-tracking baseline |
| `education.md` | Education (K-12 + Higher Ed) | FERPA, state student-data laws, AADC, DOJ Title II accessibility |

## Routing note

The first five verticals (retail, financial services, healthcare, travel, media) reflect where the current customer base concentrates. **Government and Education are underrepresented in the current customer base but documented for completeness** — the regulatory exposure (accessibility under Section 508 / ADA Title II, student-data privacy under FERPA and the state laws) is real and well-defined, and these verticals should be ObservePoint customers. When a public-sector or education prospect appears, the playbook is ready; don't treat the thin current footprint as a reason to under-scope the engagement.

When in doubt about which file to load, the regulatory exposure is the fastest discriminator: HIPAA → healthcare, GLBA → financial services, FERPA → education, Section 508 / ADA Title II → government, VPPA / TCF → media, peak-season funnels → retail, multi-step booking → travel.

---

*Last verified: 2026-06-04*
