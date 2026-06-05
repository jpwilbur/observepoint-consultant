---
description: Diagnose an ObservePoint account's health and surface the biggest-bang-for-buck next actions
argument-hint: "[focus: privacy|analytics|accessibility|performance]"
allowed-tools: [Read, Glob, Grep]
---

# /op-account-strategy

## Arguments

Optional focus area: $ARGUMENTS (one of privacy, analytics, accessibility, performance). If omitted, assess the whole account.

## Instructions

1. Load the **account-health** skill and its deep account-health-and-strategy reference.
2. If `mcp__ObservePoint__*` tools are present in this session, run the account-health diagnostic workflow from that file: `list_audits` -> `get_audit_health` per audit -> `get_usage_overview` / `get_usage_summary` / `get_usage_trends` -> `find_coverage_gaps` -> `find_anomalies` -> `get_inventory`. Score the account against the underuse-pattern checklist.
3. If the focus argument is set, scope the diagnostic to that dimension.
4. Return a prioritized list of next actions using the biggest-bang-for-buck rubric (impact x effort), each with the specific ObservePoint setup that addresses it.

### If the ObservePoint MCP server is not connected

Do not fabricate account data. Explain that the live diagnostic requires the MCP server, walk through the manual version (which reports to pull in-app), and outline what the diagnostic would surface. Cite the **account-health** skill.

## Example Usage

```
/op-account-strategy
/op-account-strategy privacy
/op-account-strategy accessibility
```
