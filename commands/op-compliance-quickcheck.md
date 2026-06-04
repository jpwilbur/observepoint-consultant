---
description: Audit a URL for the privacy regulations applicable to its jurisdiction
argument-hint: "<url>"
allowed-tools: [Read, Glob, Grep]
---

# /op-compliance-quickcheck

## Arguments

The URL to check: $ARGUMENTS. Infer the applicable jurisdictions from the domain, any country/region signals, and the user's stated operating footprint.

## Instructions

1. Load `skills/observepoint-consultant/references/privacy-and-compliance.md`.
2. Identify which privacy regulations apply to the URL's jurisdiction(s) and map each to the ObservePoint coverage that demonstrates readiness (the three-audit pattern: Default / Opt-Out / GPC, plus the relevant Privacy Reports and Rules).
3. If `mcp__ObservePoint__*` tools are present in this session, look up an existing audit for the URL via `list_audits` (search by domain), then pull the latest run with `get_audit_runs` and check consent behavior with `compare_consent_states`. Do not create new audits without confirmation.
4. Return a per-regulation readiness summary: what applies, what ObservePoint already covers, and the gaps to close.

### If the ObservePoint MCP server is not connected

Do not fabricate audit results. Explain that the live lookup requires the MCP server, then provide the knowledge-only mapping: which regulations apply to the URL and the ObservePoint setup that would prove compliance. Cite `references/privacy-and-compliance.md`.

## Example Usage

```
/op-compliance-quickcheck https://www.example.com
/op-compliance-quickcheck example.de
```
