# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.1] — 2026-06-10

MCP tool-catalog refresh. No roster or skill-structure changes.

### Changed

- **Refreshed `references/mcp-tools.md`** (the shared MCP catalog) with newer live tools, each sourced from its real tool schema: **charting** (`add_report_chart`, `remove_report_chart`), **report templates** (`list_report_templates`, `create_report_from_template`), **bulk operations** (`bulk_create`/`update`/`delete`/`assign`/`describe`), **Site Census** scoping (admin: `start`/`size`/`sample_site_census_pages`/`list`/`create`/`update`/`delete_site_censuses`), the **HAR Analyzer** (`summarize_har_file`, `upload_har_file`, `create_har_config`, `update_har_config_rules`, `get_har_run_status`/`results`, `list_har_configs`), **account governance & event log** (`get_account_health`, `get_audits_status`, `query_user_events`, `review_account_access`, `get_user`), plus `reprocess_audit_rules`, `analyze_journey_failures`, `update_journey_rules`, `stop_journey`, `find_item`, and the admin-impersonation write-arming gate (`confirm_account_plan`) with an operating doctrine. Tool count note raised to 160+; new common-pattern recipes (reprocess-after-rule-change, mobile HAR validation, bulk-create, add-a-chart, Site Census sizing).
- **Charting is now in the MCP** — corrected the previously-pending "charting is an extension point / not yet exposed" framing in `account-and-program`'s SKILL.md and `references/reporting-and-charting.md` to document `add_report_chart`/`remove_report_chart` (a chart rides an existing saved report's query; `get_saved_report` first; dashboards remain UI-composed).



The "advisor consolidation" release. The 14 customer-facing specialists are consolidated into a hub plus **6 broad advisors**, and the plugin is now cleanly customer-facing and pricing-free.

### Changed — BREAKING

- **14 specialists → 6 advisors.** `regulation` + `consent-cmp` → **`privacy-compliance`**; `tags` + `analytics-validation` + `martech` → **`tag-and-analytics-quality`**; `account-config` + `account-health` + `reporting-charting` → **`account-and-program`**; `api-strategy` + `journeys-testing` → **`automation-and-testing`**; `litigation-defense` and `accessibility` keep their names. Each advisor absorbs its predecessors' deep references as sub-sections. **The old specialist invocation names (`/observepoint-consultant:regulation`, `:martech`, `:tags`, `:account-config`, etc.) no longer exist.** Auto-trigger-by-description is unchanged, so users who never typed a specialist name are unaffected; the picker drops from 22 entries to 7.
- **Removed `roi` and `content-creation`** from this plugin; they move to a separate internal revenue plugin. This plugin is now pricing-free and purely customer-facing.
- **Removed the 7 `op-*` slash commands**; their MCP workflow recipes are folded into the matching advisors' references (e.g. the compliance quick-check into `privacy-compliance`, the evidence-pack workflow into `litigation-defense`, the account diagnostics into `account-and-program`).

### Changed — standards

- Validator (`scripts/quick_validate.py`) description ceiling tightened 1536 → 1024 chars (the skill-spec limit); the `commands/` directory and its validator plumbing are removed.
- `evals/evals.json` remapped to the 6 advisors with new merge-boundary disambiguation cases.

## [0.5.2] — 2026-06-05

Documentation correction. No skill content changes.

### Fixed

- **README "Updating → Cowork" section corrected.** v0.5.1 incorrectly claimed Cowork shares the terminal's `~/.claude/plugins/` install state. It does not — Cowork is a separate distribution channel that tracks plugins via an Anthropic cloud-hosted snapshot of the repo, so a terminal `/plugin marketplace update` has no effect on Cowork (which can stay frozen on an old version with a greyed-out Update button). The section now documents the real behavior and the three ways to get updates into Cowork: an org marketplace with "Sync automatically" (recommended, org-wide), a per-user remove/re-add refresh, or using the Desktop Code tab / terminal. Notes the known greyed-button limitation for personal / third-party GitHub marketplaces in Cowork.

## [0.5.1] — 2026-06-05

A distribution-hygiene release. No skill content changes — this fixes how teammates *receive* updates.

### Added

- **Explicit `version` field** (`0.5.1`) in both `.claude-plugin/plugin.json` and the plugin's `.claude-plugin/marketplace.json` entry. Until now the plugin had no version, so Claude Code identified installed copies by opaque git commit SHA and the `/plugin` Update button compared SHAs. Both sides now resolve to a legible semver, so the Update button shows a real `0.5.0 → 0.5.1`-style diff and future update detection is deterministic.
- **README "Updating" section** documenting the two-command refresh (`/plugin marketplace update` → `/plugin update`), the stale-cache fix (`rm -rf ~/.claude/plugins/cache/observepoint-consultant`), a **Cowork** note (shares install state with the terminal — no separate step), and an optional **admin auto-update** path via managed-settings `autoUpdate`.

### Notes

- The version field does **not** retroactively unstick anyone already on a stale marketplace cache — Claude Code only learns about new commits/versions when the local marketplace clone is re-pulled (`/plugin marketplace update`), which is never automatic for self-hosted marketplaces. Every already-installed teammate must run that refresh once; the version field makes everything *after* that cleaner.

## [0.5.0] — 2026-06-05

The "skill-breakout" release. v0.4.0 made the skill act like a consultant; v0.5.0 changes the *shape* of that consultant. The single mega-skill is split into a hybrid multi-skill plugin — a thin `observepoint-consultant` hub that routes (and answers cross-cutting questions itself) plus 14 flat, independently-triggered specialist skills, each owning its lane and its deep reference. Triggering gets sharper because each specialist advertises a narrow `description`, and answers get deeper because each specialist can carry more domain detail without bloating one dispatcher. The audience scope is unchanged — customer + internal-consulting / CSM, with **no** sales / pre-sales / prospect-research content.

### Changed — architecture

- **Hybrid hub + specialists.** The plugin is now a thin `observepoint-consultant` hub (router + persona contract + shared foundation) plus **14 flat, independently-triggered specialist skills**. The hub routes a question to the specialist whose lane it sits in, and answers cross-cutting or above-the-lane questions itself. **Non-breaking:** the hub keeps the `observepoint-consultant` name and entry point, so existing `/observepoint-consultant …` invocations and auto-triggering continue to work unchanged.
- **Shared foundation lives under the hub.** The ~11 shared reference files (products, MCP tools, verbiage, limitations, glossary, competitive positioning, personas, consulting deliverables, solution playbooks, integrations, industries) stay under the meta-skill; every specialist cross-links them. Each specialist owns its own deep reference under `skills/<specialist>/references/`.

### Added — specialists

Fourteen specialist skills under `skills/`, each with its own `SKILL.md`, narrow trigger `description`, and references:

- **Net-new** (no prior content): `consent-cmp`, `account-config`, `analytics-validation`, `tags`, `journeys-testing`, `reporting-charting`, `content-creation`.
- **Migrated** from existing v0.4.0 references: `regulation` (privacy-and-compliance), `litigation-defense` (privacy-litigation-defense), `accessibility` (accessibility-playbooks), `account-health` (account-health-and-strategy + lifecycle-and-maturity), `roi` (roi-and-renewal-framing), `martech` (martech-adjacency), `api-strategy` (api-reference).

### Added — bundled scripts

Three TDD'd helper scripts, each owned by its specialist:

- **`skills/tags/scripts/classify_tag_inventory.py`** — classifies a tag inventory by vendor / purpose / risk for the tags specialist.
- **`skills/account-config/scripts/config_blueprint.py`** — emits a regulation→config blueprint (audits, Rules, consent categories) for account-config.
- **`skills/roi/scripts/roi_model.py`** — a value-model helper for the roi specialist (no pricing).

### Added — new capability surface

- **Tag intelligence** (`tags`) as a live judgment layer over `list_tags` / `get_tag_inventory` — identity, classification, and the "should this tag be here?" call, distinct from data-correctness and consent mechanics.
- **Account-config blueprints** (`account-config`) — turning a regulation or program goal into a concrete account structure (audits, Rules, consent categories, folders/labels, alerts, schedules).
- **Content creation** (`content-creation`) as an output skill — produces external content (blog post, how-to, one-pager, thought-leadership) in ObservePoint's voice, pairing with the `humanizer` skill on the final pass.
- **Reporting & charting** (`reporting-charting`) — saved-report CRUD and report-schema column discovery, with charting documented as an extension point pending MCP support.

### Changed — standards

- **`scripts/quick_validate.py` reworked to be multi-skill-aware** — discovers every `skills/*/SKILL.md`, validates frontmatter and body-size ceilings across all skills, checks `Last verified` footers on every reference in every skill, and resolves cross-references against a dual base (the owning skill's `references/` **or** the shared meta-skill `references/`).
- **Evals grew to 39** (`evals/evals.json`) — the original 21 plus a per-specialist triggering eval for each of the 14 specialists and an adjacent-quartet disambiguation set (tags / analytics-validation / consent-cmp / martech). The original evals' `must_include` expectations were refreshed to name the **skill** that now owns each answer instead of the moved reference filename.
- **`references/mcp-tools.md` gained the admin / CSM tools** — `find_account`, `login_as_account`, `whoami`, `stop_impersonation`.
- **New test** — `scripts/test_quick_validate_multiskill.py` covers the multi-skill discovery and dual-base cross-reference resolution; `scripts/test_quick_validate.py` continues to cover the single-skill checks.

### Notes

- **v0.6.0 follow-ups:** deepen `account-health`'s lifecycle / maturity content (customer-size onboarding timelines, internal program material); an `mcp-tools.md` catalog refresh — newer live tools surfaced during this build (`stop_journey`, `confirm_account_plan`, `find_item`, and others) are not yet catalogued; and general tooling polish.
- The shared foundation lives under the meta skill; specialists cross-link it rather than duplicating it.
- Audience scope is unchanged: customer + internal-consulting / CSM. There is intentionally **no** sales, pre-sales, or prospect-research content.
- File totals: 15 `SKILL.md` files (hub + 14 specialists), ~11 shared-foundation references under the hub plus each specialist's own deep reference, 3 bundled scripts, 39 evals. Every `SKILL.md` body remains well under Anthropic's 500-line ceiling.

## [0.4.0] — 2026-06-04

The "consultant, not just encyclopedia" release. v0.3.0 made the skill know everything about website privacy; v0.4.0 makes it act like a seasoned ObservePoint consultant — talking the language of a specific industry, meeting an account where it is in its lifecycle, validating the adjacent MarTech a customer actually runs, and framing value for the person who signs the renewal. It also brings the repo up to Anthropic's full plugin-standards bar: evals, a CI validation gate, and slash commands. The audience scope is unchanged — customer + internal-consulting/CSM, with **no** sales / pre-sales / prospect-research content.

### Added — Plugin standards

- **`evals/evals.json`** — 21 evals across 10 areas (accessibility, api, compliance, industries, lifecycle, litigation, martech, mcp, out-of-scope, products), runnable via `python3 scripts/run_evals.py`.
- **`scripts/`** — `quick_validate.py` (the CI validation gate: frontmatter, line-count ceilings, `Last verified` footers, and now broken-reference scanning across `commands/`), `refresh_mcp_catalog.py` (MCP catalog refresh helper), `run_evals.py` (eval lister/runner, hardened against malformed JSON), and `test_quick_validate.py`.
- **7 slash commands in `commands/`** — `/op-compliance-quickcheck <url>`, `/op-state-of-play <domain>`, `/op-onboarding-checklist <industry> <domain>`, `/op-litigation-evidence-pack <statute> <domain>`, `/op-account-strategy [focus]`, `/op-value-snapshot [period]`, `/op-accessibility-priorities`.
- **CI** — `.github/workflows/validate.yml` (runs `quick_validate.py` on pushes and PRs) and `.github/workflows/staleness-check.yml` (flags reference files whose `Last verified` date is aging), plus `.github/CODEOWNERS`.

### Added — Industry playbooks

- **`references/industries/`** — a directory of **7 vertical playbooks** plus an `index.md` router: retail / e-commerce, financial services & insurance, healthcare & life sciences, travel & hospitality, media & publishing, government & public sector, and education. Each maps the vertical's pains, applicable regulations, and seasonal / operational moments (e.g., retail's Black Friday) to concrete ObservePoint coverage.

### Added — Lifecycle

- **`references/lifecycle-and-maturity.md`** — a program maturity model and onboarding starter answering "where do we go next." This is **starter content**; the fuller lifecycle treatment is a v0.5.0 follow-up.

### Added — MarTech adjacency

- **`references/martech-adjacency.md`** — covers **12 platforms / topics** ObservePoint sits next to: GA4, Adobe Analytics, GTM, server-side GTM, Adobe Launch, Tealium iQ, Consent Mode v2, Meta CAPI, the broader Conversions API ecosystem, CDPs, attribution, and Privacy Sandbox. Each entry is honest about what ObservePoint can prove versus what it cannot.

### Added — Account / ROI / accessibility

- **`references/account-health-and-strategy.md`** — account diagnostics, common underuse patterns, and biggest-bang-for-buck next actions; powers `/op-account-strategy`.
- **`references/roi-and-renewal-framing.md`** — quantified value framing and a renewal narrative for a budget owner, **with no pricing**; powers `/op-value-snapshot`.
- **`references/accessibility-playbooks.md`** — accessibility prioritization, the ADA / Section 508 / WCAG / EAA landscape, and lawsuit-defense evidence; powers `/op-accessibility-priorities`.

### Changed

- **SKILL.md** — decision tree and reference index gained rows routing to the new industries / lifecycle / martech / account / ROI / accessibility content; the frontmatter `description` was expanded with v0.4.0 trigger keywords (industry verticals, program maturity / onboarding, MarTech-adjacency platforms, account focus, ROI / renewal, accessibility prioritization) while staying within Anthropic's 1,536-char cap.
- **`references/personas.md`** — added Customer Success Manager (CSM) and Accessibility Specialist personas.
- **`references/consulting-deliverables.md`** — added Value Snapshot, Renewal Narrative, and Accessibility Priority Report deliverables.
- **`references/glossary.md`** — added accessibility and ROI terms.
- **`references/solution-playbooks.md`** — added 3 playbooks tied to the new content.
- **Plugin and marketplace manifests** — both descriptions updated to surface the v0.4.0 surface area for marketplace-search discoverability.
- **`scripts/quick_validate.py`** — now also scans `commands/` for broken reference links; **`scripts/run_evals.py`** hardened against malformed JSON.

### Notes

- The lifecycle file ships as starter content with a dedicated v0.5.0 follow-up planned for the full treatment.
- `scripts/run_evals.py` stands in for the spec's `improve_description.py`: this is a clean public repo with no live-model access or secrets, so the full description-optimization loop (which needs a model and an eval harness) lives in Anthropic's `skill-creator`. `run_evals.py` provides the eval-listing / running half locally.
- Audience scope is unchanged: customer + internal-consulting / CSM. There is intentionally **no** sales, pre-sales, or prospect-research content.
- File totals: 26 reference files (18 top-level + 8 under `industries/`), 7 slash commands, 21 evals, and the SKILL.md remains well under Anthropic's 500-line ceiling.

## [0.3.0] — 2026-06-03

The "comprehensive privacy" release. The skill now credibly handles "anything website privacy" — every comprehensive privacy law that affects websites globally, every active litigation theory targeting tracking, every major signal and voluntary framework, with each regulation honestly mapped to what ObservePoint can prove (or can't). The MCP catalog is refreshed against the current live server.

### Added

- **New reference file: `privacy-litigation-defense.md` (222 lines)** — tort / litigation-driven privacy claims that v0.2.0 was silent on. Covers CIPA (Cal. Penal Code §§ 631 / 632 / 638.51 — the dominant 2024-2026 tracking-pixel litigation theory), VPPA (video-tracking pixels), BIPA (Illinois biometric), ECPA / federal Wiretap, state wiretap statutes (MA, PA, FL, WA), healthcare-tracking pixel claims (HIPAA + state torts), session-replay claims. Closing section on producing the evidence pack for counsel. Strong disclaimer framing throughout — technical evidence guidance, not legal advice.
- **U.S. comprehensive state law coverage** — all 19 in-force state privacy laws documented individually (California CCPA/CPRA, Colorado, Connecticut, Virginia, Utah, Texas, Oregon, Montana, Delaware, Iowa, Nebraska, NH, NJ, Minnesota, Maryland, Tennessee, Indiana, Kentucky, Rhode Island), with a U.S. state matrix table for at-a-glance comparison. v0.2.0 had these "mentioned only" in a single paragraph; v0.3.0 gives each a full entry with effective date, enforcement body, GPC stance, sensitive-data treatment, and ObservePoint coverage approach.
- **U.S. health-data-specific section** — Washington My Health My Data Act (with private right of action emphasized), Nevada SB 370, Connecticut health-data add-ons.
- **U.S. AI-specific section** — Colorado AI Act (effective Feb 2026, first U.S. state AI Act), Texas Responsible AI Governance Act, NYC Local Law 144.
- **U.S. kids-specific section** — California AADC (9th Circuit injunction context), KOSA (federal bill status), state student data privacy laws.
- **International expansion** — EU beyond GDPR (DSA, DMA, Data Act, NIS2), UK GDPR + DPA 2018 + DPDI Act + PECR, Latin America (Argentina, Mexico, Chile, Colombia in addition to LGPD), APAC (China PIPL, Singapore PDPA, Japan APPI, South Korea PIPA, Thailand, Philippines, Indonesia, Vietnam, Australia, NZ in addition to India DPDP), Canada (Quebec Law 25 added — strictest Canadian regime), new Middle East and Africa region (UAE, Saudi, Bahrain, Israel, South Africa POPIA, Kenya, Nigeria).
- **Signals expansion** — Universal Opt-Out Mechanism (UOOM), IAB Global Privacy Platform (GPP), Apple ATT, Privacy Sandbox status (Topics retired, CHIPS / FedCM / Protected Audience / Private State Tokens).
- **New Voluntary standards section** — PCI DSS 4.0 (Requirements 6.4.3 and 11.6.1 — script inventory and change detection on payment pages), NIST Privacy Framework, ISO/IEC 27701.
- **Comprehensive coverage matrix** — restructured from 11 rows to ~76 rows across 4 sub-tables (U.S. comprehensive, U.S. sectoral/health/AI/kids, International, Signals/frameworks/voluntary).
- **Out-of-scope laws section** — DSAR fulfillment, employee data, marketing email content (CAN-SPAM / CASL), telephone marketing (TCPA / DNC), Section 230, antitrust, securities disclosure, pure data-broker laws. Honest "this isn't us, here's where to go" routing.
- **~30 new glossary terms** — CIPA, VPPA, BIPA, ECPA, Wiretap Act, pen-register, trap-and-trace, session replay, DSA, DMA, NIS2, Data Act, PIPL, APPI, PIPA, GPP, UOOM, ATT, Privacy Sandbox, PCI DSS, NIST Privacy Framework, ISO 27701, MHMDA, AADC, KOSA, Colorado AI Act, RAIGA, UK GDPR, Quebec Law 25, POPIA, and more.
- **4 new solution playbooks** — "Defend a CIPA / VPPA / BIPA / wiretap claim", "Set up state-specific privacy monitoring", "Validate AI-Act / Colorado AI Act marketing transparency disclosures", "Maintain a multi-jurisdiction compliance program".
- **CONTRIBUTING.md MCP catalog refresh-cadence section** — codifies the quarterly (or per-MCP-server-release) refresh expectation.
- **TOC at the top of `privacy-and-compliance.md`** — file is now 1,030 lines; TOC required per Anthropic's >300-line guidance.

### Changed

- **`references/mcp-tools.md` refreshed against the current live MCP server** (377 → 537 lines). New tool families documented: PII scanning (`scan_audit_pii`, `scan_journey_pii`), cross-audit comparison (`compare_consent_states`, `compare_cookie_set`, `compare_domain_set`, `compare_tag_set`), anomaly / drift / coverage (`find_anomalies`, `get_metric_trend`, `find_coverage_gaps`, `find_first_observed`, `find_rare_observations`), analysis primitives (`analyze_journey_*`), inventory / data shape (`get_inventory`, `correlate_pages`, `profile_variable`, `get_pages_without_tag`), selector verification (`verify_selectors`). Expanded label-management surface, folder management, journey diagnostics, rule references. OneTrust flow documented as three-step with the idempotent `sync_onetrust_consent_categories` commit (fixes the re-import-orphans bug).
- **SKILL.md decision tree** routes litigation questions to `privacy-litigation-defense.md`; clarifies the privacy-and-compliance row is for comprehensive regulations with TOC navigation.
- **SKILL.md frontmatter description** expanded with new trigger keywords (CIPA, VPPA, BIPA, ECPA, HIPAA, PCI DSS, Colorado AI Act, EU AI Act, DSA, DMA, China PIPL, UK GDPR, Quebec Law 25, Washington MHMDA, 19+ U.S. state privacy laws, Apple ATT, Privacy Sandbox, PII leaks to ad networks). 975 chars, well under Anthropic's 1,536-char cap.
- **Plugin and marketplace manifests** — description rewritten to surface comprehensive privacy coverage and the new tool families for marketplace-search discoverability.
- **Privacy-and-compliance.md size** — 178 → 1,030 lines. Restructured around regional H2 sections so progressive disclosure can target one region without loading the whole file.

### Fixed

- v0.2.0's `Last verified` dates bumped to 2026-06-03 across touched files.
- v0.2.0 references to `export_audit_run` corrected to `export_report` (the former was removed from the MCP server).

### Removed

- `assign_audit_consent_categories`, `export_audit_run`, `get_audit_locations` references (all removed from the live MCP server since v0.2.0).
- Duplicate EU AI Act Article 50 entry from the signals section (full entry preserved in the EU regional section).

### Notes

- File totals: 13 reference files, ~3,830 lines of reference content, 127-line SKILL.md (still well under Anthropic's 500-line ceiling).
- ObservePoint MCP server posture unchanged from v0.2.0 — the plugin still does not ship a `.mcp.json`; MCP registration happens at the Claude environment level. The wrapper-detection pattern at runtime is unchanged.
- The litigation-defense file is sensitive content (active class-action waves); strong "coordinate with counsel" disclaimers framed throughout.

## [0.2.0] — 2026-05-28

### Changed

- **`references/mcp-tools.md` rewritten end-to-end** from the live ObservePoint MCP server's `get_api_docs`. The v0.1.0 placeholder (95 lines of `TBD pending GA` stubs) is replaced with a 377-line reference covering the real tool families (audits, journeys, action-sets, rules, alerts, consent categories + CMP integration, scheduling, grid reports, exports, escape hatches), the safety gates encoded in the wrappers (selector evidence, journey-shape, watch-usage, two-step CMP import, schedule sanitization, selector-type rewriting), and common multi-step patterns.
- **`SKILL.md` MCP section now names real wrappers** in examples (`list_audits`, `setup_compliance_monitoring`, `build_schedule`, `op_api_call`) and frames the MCP server as in active development with internal access today, not as a future possibility.
- **README MCP section** now documents the two install paths (Claude Desktop `.dxt` extension, Claude Code `claude mcp add`) for ObservePoint internal users with access, clarifies the skill works in knowledge-only mode for everyone else, and explains why the plugin does not bundle its own `.mcp.json` today (registration happens at the Claude environment level, not per-plugin).

### Fixed

- **Casing bug across SKILL.md, README, CHANGELOG, and `api-reference.md`**: v0.1.0 wrote the MCP tool prefix as `mcp__observepoint__` (all lowercase). The actual prefix is `mcp__ObservePoint__` (capital O, P). Five total occurrences corrected.

### Notes

- The ObservePoint MCP server remains in active development. The plugin does not ship a `.mcp.json` or `.mcp.json.example` — when the MCP server is registered in a user's Claude environment via either supported path, the skill picks up the tools automatically through Claude's runtime tool list. A future release will revisit plugin-level packaging once the MCP server is generally available.

## [0.1.0] — 2026-05-28

Initial release.

### Added

- Plugin and marketplace manifests at `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, matching Anthropic's first-party schema (`skill-creator`, `example-plugin`).
- `skills/observepoint-consultant/SKILL.md` — the dispatcher / persona / decision tree. Frontmatter contains only `name` and `description` per Anthropic spec; description is written in skill-creator's "pushy" style. Body is 121 lines, well under the 500-line ceiling.
- 12 reference files inside `skills/observepoint-consultant/references/` covering products, solution playbooks, API recipes, MCP extension pattern, privacy & compliance, competitive positioning, brand verbiage, platform limitations, integrations, consulting deliverables, personas, and glossary. Each file ends with a `Last verified: 2026-05-28` footer.
- Repository scaffolding: `LICENSE` (MIT), `LICENSE.txt` inside the skill directory, `.gitignore`, `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`, and `.github` issue and pull-request templates.

### Notes

- The ObservePoint MCP server is not yet generally available. The skill detects `mcp__ObservePoint__*` tools at runtime and prefers them when present; otherwise it falls back to REST API recipes documented in `references/api-reference.md`. The skill never invents MCP tool names.
- This is a community-built, MIT-licensed plugin. It is not an official ObservePoint product.

[0.5.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.5.0
[0.4.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.4.0
[0.3.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.3.0
[0.2.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.2.0
[0.1.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.1.0
