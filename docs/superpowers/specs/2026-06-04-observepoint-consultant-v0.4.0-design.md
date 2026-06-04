# observepoint-consultant v0.4.0 — design spec

**Status:** Approved design. Pending user review of this spec, then implementation-plan phase.

**Date:** 2026-06-04

**Author:** Jarrod Wilbur

**Prior art:** v0.1.0 / v0.2.0 / v0.3.0 plan and execution captured at `~/.claude/plans/i-want-to-create-valiant-plum.md`.

## Context

The skill shipped v0.3.0 with comprehensive global privacy coverage and litigation-defense content. The user surfaced two remaining gaps when they prompted "what am I missing?":

1. **Plugin-standards drift.** The repo is missing scaffolding that Anthropic's first-party `skill-creator` and `example-plugin` carry — no `evals/`, no `scripts/`, no CI workflows, no `commands/`. The original v0.1.0 plan flagged the evals work as a v0.2.0 addition; it never landed. The skill's structural checks I run by hand every PR (JSON parse, frontmatter shape, `Last verified` dates, no fabricated MCP tool names) belong in CI.
2. **Content gaps in dimensions the skill should cover credibly.** Industry verticals (current playbooks are generic + healthcare); lifecycle / maturity content (no framework for "where is this customer, where do they go next"); MarTech adjacency (consultants get asked GA4 / Adobe / GTM / Tealium / CDP / attribution questions all the time, and the skill is silent); account-strategy / ROI / renewal framing (no CSM-facing tooling); accessibility (thin — just a WCAG entry in `privacy-and-compliance.md`).

v0.4.0 closes those gaps in one comprehensive release. The audience scope from v0.1.0 is preserved: **customers, prospects, partners, and ObservePoint internal teams** — explicitly NO sales / pre-sales / prospect-research content (that would be forked privately later if needed; the public plugin stays "internal use for consulting only, not research; and customer-facing/public").

## Outcome

A v0.4.0 release where the skill credibly handles:

- **Plugin standards questions** — the packaging matches Anthropic's first-party quality, CI validates every PR, slash commands provide shortcut entry points to the major workflows.
- **Industry-specific questions** — "I'm in retail / financial services / healthcare / travel / media; what's the ObservePoint playbook for my industry?" Customers in Government and Education get useful coverage too.
- **Lifecycle questions** — "where is my ObservePoint program in its maturity, what's next, what's a Day-1 / Month-1 / Quarter-1 plan?" (Starter content with explicit acknowledgement that the depth belongs in a dedicated v0.5.0 working session.)
- **MarTech adjacency questions** — "how should I implement GA4 / sGTM / Consent Mode v2 / Meta CAPI?" — with the ObservePoint validation angle for each.
- **Account / ROI / renewal questions** — "what should I focus on in my account, what's the biggest bang for buck, how do I show value to my budget owner for renewal?"
- **Accessibility questions** — "from my accessibility data, what's the highest-impact fix to target first?" plus full legal-landscape coverage (ADA Title III, EAA, DOJ Title II, state laws).

## Audience confirmation

**In scope** (preserved from v0.1.0):
- ObservePoint customers (any persona)
- Prospects evaluating ObservePoint
- ObservePoint partners
- ObservePoint internal teams in **consulting / CSM / Solution Engineering** roles

**Explicitly out of scope** (decided in this design):
- Sales / Account Executive / pre-sales prospect-research / ADM tooling. No `/op-prospect-research` command. No `references/sales-and-discovery.md` file. If an internal-only version is needed later, it gets forked privately.

## Detailed design

### Section 1 — Plugin standards

#### `evals/evals.json`

Anthropic-canonical eval format from `skill-creator`. ~20 test prompts grouped by skill area:

- Compliance routing (3 prompts: CCPA, Colorado CPA, China PIPL)
- Litigation defense (3 prompts: CIPA, VPPA, healthcare-pixel)
- Products (2 prompts: Audit-vs-Journey, HAR Analyzer use)
- API (2 prompts: write a Rule, CI/CD gate)
- MCP (2 prompts: PII scan, consent-state comparison)
- Industries (3 prompts: retail Black-Friday readiness, financial GLBA, media VPPA)
- Lifecycle (2 prompts: account-health, onboarding checklist)
- MarTech adjacency (2 prompts: Consent Mode v2 wiring, sGTM patterns)
- Out-of-scope (1 prompt: confirm honest "not us, see X" routing)

Each entry has `prompt`, `expected_output_summary`, `must_include` (phrases / tool names), `must_not_include` (fabricated tool names, regulations out of context, pricing claims).

#### `scripts/`

Three Python utilities:

- **`quick_validate.py`** — runs in CI on every PR. Validates: JSON parse for both manifests, SKILL.md frontmatter contains only `name` + `description`, SKILL.md body ≤ 500 lines, every reference file ends with `Last verified: YYYY-MM-DD`, no occurrences of removed MCP tool names (`assign_audit_consent_categories`, `export_audit_run`, `get_audit_locations`), no fabricated MCP tool names (cross-checks against a curated allowlist matching the current `mcp-tools.md` catalog), all cross-references resolve to existing files.
- **`refresh_mcp_catalog.py`** — accepts `get_api_docs` output via stdin or file. Diffs against `references/mcp-tools.md`. Outputs structured "tools added / removed / changed" report. Makes the quarterly refresh mechanical.
- **`improve_description.py`** — wires the SKILL.md `description` field into the skill-creator iteration pattern. Generates description variants, runs them against the evals, scores them. Selects best by held-out test set.

#### `.github/workflows/`

- **`validate.yml`** — runs `quick_validate.py` on every PR. Fails the PR if any check fails. Comments the failure detail.
- **`staleness-check.yml`** — weekly cron. Surfaces any reference file with `Last verified` > 90 days old. Opens or updates a tracking issue.

#### `commands/`

Seven slash commands, all `.md` files following Anthropic's example-plugin pattern:

| Command | Argument | Description |
|---|---|---|
| `op-compliance-quickcheck.md` | `<url>` | Audit URL for applicable regulations — one-shot composite read |
| `op-state-of-play.md` | `<domain>` | Current state of a domain — recent audits, issues, changes |
| `op-onboarding-checklist.md` | `<industry> <domain>` | Day-1 onboarding checklist for an industry + domain |
| `op-litigation-evidence-pack.md` | `<statute> <domain>` | Walk through evidence assembly for a class-action / demand letter |
| `op-account-strategy.md` | `[<focus>]` | MCP-driven account health diagnostic + prioritized next actions |
| `op-value-snapshot.md` | `[<period>]` | Quantified value summary for budget conversations |
| `op-accessibility-priorities.md` | none | Read accessibility data, rank by impact, surface fix-this-first |

MCP-dependent commands (account-strategy, value-snapshot, accessibility-priorities, state-of-play) handle the no-MCP case gracefully — explain the workflow, document the queries, decline to invent data.

#### `.github/CODEOWNERS`

Single line: `* @jpwilbur`. Future co-maintainers add lines as needed.

#### Cleanup

- `.gitignore` updated to ignore `**/.DS_Store` recursively.
- Existing `.DS_Store` files removed in the scaffold PR (`.claude/.DS_Store`, `skills/.DS_Store`, `skills/observepoint-consultant/.DS_Store`).

### Section 2 — Industry vertical playbooks

New directory **`references/industries/`** with one file per industry plus `index.md`.

**Per-industry structure** (consistent across all files):
- Industry context (typical site shapes, business models, MarTech stack tendencies)
- Top 3-5 use cases ObservePoint solves
- Industry-specific regulations (cross-references to `privacy-and-compliance.md` and `privacy-litigation-defense.md`)
- Common vendor patterns
- Industry-specific Rule examples (concrete WHEN/EXPECT)
- Common pitfalls
- CSM cadence recommendation

#### Core 5 (deep, ~250 lines each)

1. **`retail-ecommerce.md`** — heavy ad-tech, peak-season traffic patterns (Black Friday / Cyber Monday), conversion-funnel focus, EU + state privacy. Vendor patterns: Meta / Google / TikTok pixels, Salesforce Commerce Cloud, Shopify, BigCommerce.
2. **`financial-services-insurance.md`** — GLBA + Safeguards Rule + state law + fiduciary disclosure + heavy regulated-tag scrutiny. Vendor patterns: Tealium iQ heavy use, OneTrust strict CMP, low ad-tech relative to retail.
3. **`healthcare-life-sciences.md`** — deepening of existing healthcare playbook. HIPAA + Meta Pixel litigation + MHMDA + patient-portal patterns. Vendor patterns: Epic / Cerner integrations, dedicated healthcare MarTech.
4. **`travel-hospitality.md`** — multi-step booking funnels, loyalty programs, multi-jurisdiction visitors (so multi-region privacy hits hard), OTA partner integrations.
5. **`media-publishing.md`** — TCF 2.3 + GPP critical, VPPA on video content, paywall / subscription tracking, recirculation analytics, heavy programmatic ad-tech.

#### Compact 2 (~100-150 lines each)

6. **`government-public-sector.md`** — Section 508 + ADA accessibility + state-residency considerations + the no-third-party-tracking baseline.
7. **`education.md`** — combined K-12 + Higher Ed in one playbook with sections for each. FERPA + state student data laws + COPPA on K-12 + AADC on under-18 incoming students + DOJ Title II accessibility actions.

#### `index.md`

Lists all 7 industries with a one-line description each. Routes the consultant to the right file. Acknowledges the 2 compact entries are "underrepresented in current customer base but documented for completeness; the regulatory exposure is real."

**Total Section 2:** ~1,500 lines.

### Section 3 — Lifecycle and maturity (starter)

New file **`references/lifecycle-and-maturity.md`** (~400 lines).

**Explicit header on the file:**

> **Starter content.** This file establishes the framework; customer-size-aware timelines and ObservePoint's actual internal program processes need a dedicated working session to integrate. See the v0.5.0 follow-up work-item.

#### Sections

1. **Web Governance Maturity Model** — crawl / walk / run / fly. For each stage: diagnostic indicators, what "good" looks like, common stuck-at-this-stage patterns, next-stage transition checklist.
2. **Onboarding workflow** — Day 1 → Year 1 with milestones (Week 1 / Month 1 / Quarter 1).
3. **CSM operational cadences** — weekly / monthly / quarterly / annual rhythms.
4. **Common stuck patterns** — diagnose + break-through plays for the most common "we bought it but…" situations.
5. **Maturity-driven roadmap** — 30 / 90 / 180-day transition plans.

Cross-references `references/account-health-and-strategy.md` (MCP workflows) and `references/roi-and-renewal-framing.md` (value snapshots per maturity stage).

### Section 4 — MarTech adjacency

New file **`references/martech-adjacency.md`** (~700 lines, 12 sub-sections).

Each sub-section: implementation patterns, common antipatterns, ObservePoint validation approach (specific Rule examples), what ObservePoint can / can't see.

1. **GA4 implementation patterns** — event taxonomy, enhanced measurement, Measurement Protocol, conversion modeling, audience export, consent integration.
2. **Adobe Analytics implementation patterns** — eVars / props / events, AAM audiences, mobile + web combined view.
3. **Google Tag Manager (client-side)** — container design, variable architecture, lookup tables, common antipatterns ObservePoint catches.
4. **Server-side GTM** — Cloud Run / Stape / Addingwell hosts, server-container architecture, Consent Mode v2 in server-side context, what ObservePoint can / can't validate.
5. **Adobe Launch / Adobe Tags** — rules architecture, extensions, publish workflow.
6. **Tealium iQ** — universal data layer, extensions, templated tags, publish-event audit triggering (native ObservePoint integration).
7. **Consent Mode v2 — deep-dive** — beyond the brief mention in `privacy-and-compliance.md`. CMP + Consent Mode wiring, fallback ping patterns, `ads_data_redaction`, server-side patterns.
8. **Meta CAPI (Conversions API)** — server-side conversion sending, deduplication with pixel, Privacy Sandbox future.
9. **Conversions API ecosystem** — Google Enhanced Conversions, TikTok Events API, Pinterest CAPI, LinkedIn CAPI.
10. **Customer Data Platforms** — Segment / mParticle / RudderStack / Adobe RT-CDP / Tealium AudienceStream / Treasure Data. What each does, where ObservePoint validates.
11. **Attribution and measurement** — first-touch / last-touch / position-based / time-decay / data-driven / MMM / incrementality. ObservePoint's role as the conversion-event truth source.
12. **Privacy Sandbox APIs** — Protected Audience, Attribution Reporting, CHIPS, FedCM, Private State Tokens.

### Section 5 — Account, ROI, accessibility

#### `references/account-health-and-strategy.md` (~350 lines)

Powers `/op-account-strategy`.

1. **Account health diagnostic framework** — how to read an account and score it.
2. **Common underuse patterns** — for each: detection via MCP, what fixing it unlocks.
   - Single-folder organization at scale
   - Audits without Rules
   - Rules without alerts
   - Alerts to one person's email
   - No PII scanning
   - No consent-state coverage
   - No anomaly detection wired
   - No labels / saved reports
3. **Biggest-bang-for-buck rubric** — impact × effort prioritization.
4. **MCP-tool workflows** — concrete sequences:
   - Account audit: `list_audits` → `get_audit_health` → score
   - Usage trend: `get_usage_overview` → `get_usage_trends`
   - Gap analysis: `find_coverage_gaps` → `find_rare_observations`
   - Anomaly review: `find_anomalies` → `get_metric_trend`
   - Vendor inventory: `get_inventory` → `query_report(entity=request-domains)`
5. **Recommended next-action templates** keyed to maturity stage (cross-references `lifecycle-and-maturity.md`).

#### `references/roi-and-renewal-framing.md` (~300 lines)

Powers `/op-value-snapshot`. **No pricing disclosure** — value framing only.

1. **ROI framework** — categories the customer can quantify.
2. **Quantifiable value categories:**
   - Incident avoidance (broken tracking caught early → revenue protected)
   - Compliance evidence readiness (audit hours saved)
   - Ad-spend efficiency (clean conversion data → wasted-spend reduction)
   - Legal / fine exposure reduction (privacy / CIPA defense readiness)
   - Operational efficiency (audit automation vs manual)
   - Team-time savings (analytics + privacy + dev hours)
3. **Before / after framing templates**.
4. **Renewal narrative templates** — 3-4 templates by maturity stage.
5. **Common budget-owner objections + rebuttals** — "nice-to-have," "we'll do this manually," "OneTrust does this," etc.
6. **The "price of NOT renewing" angle**.
7. **Cross-reference to `consulting-deliverables.md`** for the artifact templates.

#### `references/accessibility-playbooks.md` (~400 lines)

Powers `/op-accessibility-priorities`. Beyond the WCAG section in `privacy-and-compliance.md`.

1. **Accessibility legal landscape (2026)** — ADA Title III (private litigation wave), DOJ Title II (state / local gov, active in 2026), EAA (effective June 28 2025), state laws (Unruh Act, NY 110).
2. **ObservePoint accessibility tooling deep-dive** — Accessibility Report, Accessibility Highlight Report (new 2026), Debugger accessibility additions.
3. **Impact-prioritization framework** — severity × traffic-weighted page exposure × user-population impact.
4. **Top-10 common violations + remediation patterns** — alt text, form labels, color contrast, focus management, ARIA misuse, heading hierarchy, language attribute, link text, table semantics, video captions.
5. **MCP-tool workflows for accessibility** — `query_report(entityType="accessibility-issues")`, `get_report_schema(entityType="accessibility-issues", search="severity")`, `find_anomalies(metric="pages-with-browser-errors")`, trend over time.
6. **Industry-specific accessibility patterns** — Healthcare, Higher Ed, Government, Retail.
7. **Accessibility lawsuit defense** — parallel to `privacy-litigation-defense.md`. Evidence patterns for ADA Title III demand letters.

### Companion updates

- **`SKILL.md`**:
  - Decision tree adds routing rows: industry questions → `references/industries/index.md`; lifecycle / maturity → `references/lifecycle-and-maturity.md`; MarTech / GA4 / sGTM / Tealium / CDPs / attribution → `references/martech-adjacency.md`; account strategy → `references/account-health-and-strategy.md`; ROI / renewal → `references/roi-and-renewal-framing.md`; accessibility → `references/accessibility-playbooks.md`.
  - Frontmatter description extended with v0.4.0 trigger keywords (industries, lifecycle, maturity, GA4, sGTM, Tealium, CDP, attribution, account health, ROI, renewal, accessibility, ADA, Section 508). Keep under Anthropic's 1,536-char cap.
- **`references/personas.md`** — add CSM (Customer Success Manager) and Accessibility Specialist personas.
- **`references/consulting-deliverables.md`** — add Value Snapshot template, Renewal Narrative template, Accessibility Priority Report template.
- **`references/glossary.md`** — add accessibility terms (axe-core, ARIA, contrast ratios, WCAG 2.2, Section 508, DOJ Title II, Unruh Act, EAA), ROI framing terms.
- **`references/solution-playbooks.md`** — add: Account Health Check, Renewal Prep, Accessibility Impact-Prioritization. (Consistent with the audience scope — no Prospect Research playbook, since sales / pre-sales tooling is explicitly out of scope.)
- **`.claude-plugin/plugin.json` + `marketplace.json`** — description expansion for marketplace search hits.

## PR sequencing (16 PRs)

| # | Branch | Scope | Est. diff |
|---|---|---|---|
| 1 | `chore/plugin-standards-scaffold` | `evals/`, `scripts/`, CI workflows, `commands/`, CODEOWNERS, `.DS_Store` cleanup, `.gitignore` enhancement | ~700 lines |
| 2 | `feat/industry-retail` | Retail / E-commerce playbook | ~250 lines |
| 3 | `feat/industry-financial-services` | Financial Services & Insurance playbook | ~250 lines |
| 4 | `feat/industry-healthcare` | Healthcare & Life Sciences (deepen existing) | ~250 lines |
| 5 | `feat/industry-travel` | Travel & Hospitality playbook | ~250 lines |
| 6 | `feat/industry-media` | Media & Publishing playbook | ~250 lines |
| 7 | `feat/industry-gov-education` | Government + Education (K-12 + HE combined) + `industries/index.md` | ~330 lines |
| 8 | `feat/lifecycle-maturity-starter` | Starter `lifecycle-and-maturity.md` with explicit starter header + spec follow-up note | ~400 lines |
| 9 | `feat/martech-adjacency-1` | GA4 + Adobe Analytics + GTM (client + server) | ~250 lines |
| 10 | `feat/martech-adjacency-2` | Adobe Launch + Tealium + Consent Mode v2 + Meta CAPI + Conversions API ecosystem | ~250 lines |
| 11 | `feat/martech-adjacency-3` | CDPs + Attribution + Privacy Sandbox | ~200 lines |
| 12 | `feat/account-health-strategy` | `account-health-and-strategy.md` | ~350 lines |
| 13 | `feat/roi-renewal-framing` | `roi-and-renewal-framing.md` | ~300 lines |
| 14 | `feat/accessibility-playbooks` | `accessibility-playbooks.md` | ~400 lines |
| 15 | `docs/v040-companion-updates` | SKILL.md routing + personas + consulting-deliverables + glossary + solution-playbooks + manifests | ~400 lines |
| 16 | `chore/v0.4.0` | README + CHANGELOG + tag v0.4.0 | ~150 lines |

**Total estimated content:** ~4,200 lines across 16 PRs.

## Follow-up work-item (NOT v0.4.0)

**v0.5.0 — Lifecycle & maturity deep session.** Separate brainstorm, separate spec, separate plan, separate implementation cycle. Inputs the v0.4.0 starter content does NOT capture:
- Customer-size-aware timelines (SMB vs. mid-market vs. enterprise)
- ObservePoint's actual internal program processes and playbooks
- Real-world maturity-transition data (from CSM experience)
- Stage-specific KPIs and exit criteria

The v0.4.0 starter file references this explicitly so customers reading it understand the depth comes later.

## Verification

After each PR merges, run `scripts/quick_validate.py` (which lands in PR #1). After PR #16 merges and v0.4.0 is tagged:

1. Install the v0.4.0 plugin in a fresh Claude Code session.
2. Run the eval grid via `scripts/improve_description.py` — confirm baseline scores.
3. Run a smoke-test grid of new-content prompts:
   - "What's the ObservePoint playbook for a retail site preparing for Black Friday?"
   - "Map GLBA Safeguards Rule to ObservePoint coverage in financial services."
   - "Set up the Consent Mode v2 wiring between OneTrust and GTM, what should ObservePoint check?"
   - "Server-side GTM — what does ObservePoint validate?"
   - "What's my account underutilizing? Use the MCP tools."
   - "Build a value snapshot for our budget owner showing the past 6 months."
   - "What's the highest-impact accessibility fix to target first across our portfolio?"
   - "We got an ADA Title III demand letter. What evidence does ObservePoint produce?"
4. Confirm each loads the right reference file and returns the canonical answer shape.
5. Confirm `scripts/quick_validate.py` passes on `main`.

## Risks

- **Lifecycle starter undersells intentionally.** Mitigate via the explicit header at the top of the file and the v0.5.0 work-item callout in the release notes.
- **MarTech adjacency is the broadest single file** (~700 lines). Mitigate with an internal TOC at the file head; Anthropic supports refs > 500 lines as long as they have TOCs.
- **Account / ROI / accessibility commands assume MCP access.** Mitigate by documenting the graceful-degradation path in each command file (no MCP → describe the workflow, decline to fabricate data).
- **Accessibility lawsuit-defense content is sensitive** (parallel to CIPA / VPPA litigation). Mitigate with the same disclaimer framing — technical evidence, not legal advice.
- **Date assumptions in industry playbooks** can drift fast for privacy law. Mitigate by cross-referencing `privacy-and-compliance.md` rather than restating dates in the industry files.
- **CI workflows depend on Anthropic's marketplace.json schema URL being stable.** Already verified working in v0.2.0; spot-check during PR #1.

## Audience confirmation (final, repeated for emphasis)

The plugin remains **customer-facing AND internal-consulting/CSM**. No sales / pre-sales / prospect-research / ADM tooling. If an internal-only sales-flavored version is needed later, it gets forked privately from this repo. The public plugin stays neutral on competitive sales positioning beyond what's already in `references/competitive-positioning.md` (and that file's "public sources only" rule stands).

## Critical files

- `evals/evals.json` (new)
- `scripts/quick_validate.py`, `scripts/refresh_mcp_catalog.py`, `scripts/improve_description.py` (new)
- `.github/workflows/validate.yml`, `.github/workflows/staleness-check.yml` (new)
- `commands/op-compliance-quickcheck.md` and 6 sibling command files (new)
- `references/industries/` directory with 7 playbooks + `index.md` (new)
- `references/lifecycle-and-maturity.md` (new — starter)
- `references/martech-adjacency.md` (new)
- `references/account-health-and-strategy.md`, `references/roi-and-renewal-framing.md`, `references/accessibility-playbooks.md` (new)
- `skills/observepoint-consultant/SKILL.md` (decision tree + description)
- `skills/observepoint-consultant/references/personas.md`, `consulting-deliverables.md`, `glossary.md`, `solution-playbooks.md` (updates)
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (description updates)
- `.gitignore`, `.github/CODEOWNERS` (new / updated)
- `README.md`, `CHANGELOG.md` (release plumbing)

---

*Spec date: 2026-06-04*
