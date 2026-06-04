# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.3.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.3.0
[0.2.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.2.0
[0.1.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.1.0
