---
description: Summarize the current state of a domain — recent audits, issues, and changes
argument-hint: "<domain>"
allowed-tools: [Read, Glob, Grep]
---

# /op-state-of-play

## Arguments

The domain to summarize: $ARGUMENTS. Treat it as the search key for finding the relevant audits.

## Instructions

1. Load the **account-health** skill and its deep account-health-and-strategy reference.
2. If `mcp__ObservePoint__*` tools are present in this session, run the state-of-play workflow for the domain: `list_audits` (search by the domain) -> `get_audit_runs` for the most recent runs -> `find_anomalies` to surface spikes and drops -> `get_file_changes` to flag what shifted since the last run.
3. Synthesize a concise status report: most recent runs and their pass/fail posture, notable anomalies, and what changed.
4. Recommend the next action for any issue that warrants attention.

### If the ObservePoint MCP server is not connected

Do not fabricate audit data. Explain that the live status pull requires the MCP server, then outline the manual version (which in-app reports and run-comparison views to open) and what the workflow would surface. Cite the **account-health** skill.

## Example Usage

```
/op-state-of-play example.com
/op-state-of-play shop.example.com
```
