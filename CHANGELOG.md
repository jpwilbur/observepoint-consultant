# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.2.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.2.0
[0.1.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.1.0
