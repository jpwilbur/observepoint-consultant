---
description: Produce a quantified ObservePoint value summary for a budget owner
argument-hint: "[period]"
allowed-tools: [Read, Glob, Grep]
---

# /op-value-snapshot

## Arguments

Optional reporting period: $ARGUMENTS (e.g. "last quarter", "trailing 90 days", "YTD"). If omitted, default to the trailing quarter.

## Instructions

This snapshot never quotes pricing — it quantifies value delivered, not cost.

1. Load the `roi` skill, which carries the ROI and renewal-value framing.
2. If `mcp__ObservePoint__*` tools are present in this session, gather the value signals for the period: `get_usage_overview` / `get_usage_summary` / `get_usage_trends` for activity, plus issue-detection and remediation evidence (rule violations caught, anomalies flagged, coverage gaps closed).
3. Map the raw activity to the ROI framing from the reference (risk avoided, time saved, revenue protected).
4. Return a budget-owner-ready value snapshot: headline outcomes, the quantified metrics behind each, and the renewal narrative — with no mention of pricing or cost.

### If the ObservePoint MCP server is not connected

Do not fabricate usage numbers. Explain that the quantified pull requires the MCP server, then outline the manual version (which usage and issue reports to export) and the ROI framing the snapshot would apply. Cite the `roi` skill.

## Example Usage

```
/op-value-snapshot
/op-value-snapshot "last quarter"
/op-value-snapshot YTD
```
