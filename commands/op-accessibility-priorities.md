---
description: Rank accessibility findings by impact and surface the highest-impact fixes first
argument-hint: ""
allowed-tools: [Read, Glob, Grep]
---

# /op-accessibility-priorities

## Arguments

No arguments. $ARGUMENTS is ignored; assess the accessibility findings available in the session.

## Instructions

1. Load the **accessibility** skill and its deep accessibility-playbooks reference.
2. If `mcp__ObservePoint__*` tools are present in this session, pull the accessibility findings: `get_report_schema` (search for the accessibility-issues entity to discover column names), then `query_report` with `entityType=accessibility-issues` to retrieve the issues.
3. Apply the impact-prioritization framework from the reference (severity x reach x effort, WCAG conformance level, pages affected) to rank the findings.
4. Return the highest-impact fixes first, each with the WCAG criterion, the affected scope, and the remediation step.

### If the ObservePoint MCP server is not connected

Do not fabricate accessibility findings. Explain that pulling live issues requires the MCP server, then walk through the manual version (which accessibility reports to open in-app) and the impact-prioritization framework the ranking would apply. Cite the **accessibility** skill.

## Example Usage

```
/op-accessibility-priorities
```
