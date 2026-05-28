# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-28

Initial release.

### Added

- Plugin and marketplace manifests at `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, matching Anthropic's first-party schema (`skill-creator`, `example-plugin`).
- `skills/observepoint-consultant/SKILL.md` — the dispatcher / persona / decision tree. Frontmatter contains only `name` and `description` per Anthropic spec; description is written in skill-creator's "pushy" style. Body is 121 lines, well under the 500-line ceiling.
- 12 reference files inside `skills/observepoint-consultant/references/` covering products, solution playbooks, API recipes, MCP extension pattern, privacy & compliance, competitive positioning, brand verbiage, platform limitations, integrations, consulting deliverables, personas, and glossary. Each file ends with a `Last verified: 2026-05-28` footer.
- Repository scaffolding: `LICENSE` (MIT), `LICENSE.txt` inside the skill directory, `.gitignore`, `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`, and `.github` issue and pull-request templates.

### Notes

- The ObservePoint MCP server is not yet generally available. The skill detects `mcp__observepoint__*` tools at runtime and prefers them when present; otherwise it falls back to REST API recipes documented in `references/api-reference.md`. The skill never invents MCP tool names.
- This is a community-built, MIT-licensed plugin. It is not an official ObservePoint product.

[0.1.0]: https://github.com/jpwilbur/observepoint-consultant/releases/tag/v0.1.0
