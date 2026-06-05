# Account health and strategy

Load this file when the question is "what should I focus on in my account?", "where's the biggest bang for the buck?", or "give me an account review" — and when the `/op-account-strategy` command runs. The job here is to read an existing ObservePoint account, score how well it's being used, find the underused capabilities that would move the needle most, and hand back a prioritized plan. It's the renewal-health lens on top of the maturity diagnosis in `references/lifecycle-and-maturity.md` — that file tells you *which stage* a customer is in; this file tells you *the specific next moves* and *which ones pay off first*.

This is a diagnostic, not a sales motion. The output is a list of concrete account changes ranked by impact and effort, each tied to a tool call or in-app signal that proves the gap is real.

> **MCP-driven.** The diagnostics below assume the ObservePoint MCP server is connected — every detection step is a real tool call. If `mcp__ObservePoint__*` tools are not present in the session (the server is pre-GA; see `references/mcp-tools.md`), this becomes a *manual in-app review*: the same signals are all visible in the UI (audit list, Rules tab, Alerts page, consent-category attachments, saved reports), just read by hand instead of by tool. Don't fake tool calls — narrate the in-app equivalent.

## Account health diagnostic framework

Score the account across seven dimensions. Each is a 0–3 band: 0 absent, 1 token, 2 working, 3 mature. The point isn't the number — it's surfacing the lowest bands, which are where the next move lives.

| Dimension | What you're reading | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| **Coverage breadth** | How much of the real estate is watched | one audit | a few audits, key properties only | most revenue/risk properties | all properties, organized by tier |
| **Rule depth** | Whether inventory has pass/fail meaning | no Rules | Rules on one audit | Rules on key audits | Rule library tracking the threat landscape |
| **Alerting** | Whether failures find a human | no alerts | alerts but unrouted | alerts routed and owned | tuned, trusted, per-Rule ownership |
| **Consent-state coverage** | Whether opt-out is actually tested | default audit only | one consent variant | opt-out tested per key domain | default + opt-out + GPC per domain |
| **PII scanning** | Whether leaks are looked for | never run | run once, ad hoc | run on key audits | scheduled across PHI/PII-bearing properties |
| **Organization** | Whether the account rolls up cleanly | single folder, no labels | some folders | folders by team/domain | folders + labels + saved reports rolling up |
| **Freshness** | Whether what exists actually runs | stale, manual runs | sporadic | scheduled, mostly healthy | scheduled, all healthy, drift-monitored |

Read the bands off the account, don't ask the customer to self-report — the self-report and the data disagree more often than not. The fast reads: `get_usage_overview` for breadth and freshness, `list_audits` + `get_audit_health` per audit for what's actually working, `list_rules` / `get_audit_rules` for Rule depth, `list_alerts` for alerting, `get_audit_consent_categories` for consent coverage, `list_folders` + `list_labels` + `list_saved_reports` for organization. The next two sections turn the low bands into specific fixes.

## Common underuse patterns

The recurring ways an account leaves value on the table. For each: how to **detect** it (a specific tool call or in-app signal) and what **fixing** it unlocks. These map onto the maturity stuck-patterns in `references/lifecycle-and-maturity.md` — here the framing is "what to change in the account," there it's "how the program stalls."

**1. Single-folder organization at scale.** *Detect:* `list_folders` returns one (or none) while `list_audits` returns many — a flat account where everything lives together. In-app: the audit list is one long unfiltered scroll. *Unlocks:* folders by team / domain / risk tier plus labels (`create_folder`, `create_label`, `set_audit_labels`) make `get_inventory` roll up cleanly and let saved reports slice by tier. Organization is the precondition for executive reporting — you can't show a sponsor a coherent rollup of a flat list.

**2. Audits without Rules attached.** *Detect:* `get_audit_rules` returns empty (or near-empty) on audits that `get_audit` shows are running. The customer is collecting inventory nobody grades. *Unlocks:* converting the top failure modes into Rules (`create_rule` → `update_audit_rules`) turns raw inventory into pass/fail signal. Without Rules there's data but no verdict; with them, every run answers "did anything break?"

**3. Rules without alerts.** *Detect:* `list_rules` / `get_audit_rules` show a real library and `analyze_rule_results` shows Rules failing on real runs, but `list_alerts` is empty. Failures sit in the dashboard until someone happens to look. *Unlocks:* `create_alert` on the high-stakes Rules, routed to the channel the owning team watches, moves the program from "we can see failures" to "failures find us." This is usually the single highest-leverage fix in a walk-stage account.

**4. Alerts to one person's email.** *Detect:* `list_alerts` / `get_alert` show every alert routing to a single individual's address rather than a team channel or distribution list — a bus-factor risk. In-app: the alert recipients column is one name across the board. *Unlocks:* re-routing to a shared channel or distribution list (`update_alert`) plus per-Rule ownership means a failure still gets seen when that one person is on vacation or has left. The program survives the person.

**5. No PII scanning.** *Detect:* there's no evidence `scan_audit_pii` or `scan_journey_pii` has ever run — no PII findings in any report, no customRegex configured, and the customer can't say whether email or MRN-style identifiers leak to third parties. *Unlocks:* a `scan_audit_pii` sweep across the PII/PHI-bearing properties surfaces leak paths (masked values, named destinations) before they become a CIPA/healthcare-pixel exposure. For regulated industries this is often the finding that justifies the whole program — see `references/privacy-litigation-defense.md`.

**6. No consent-state coverage.** *Detect:* `get_audit_consent_categories` shows only a default/baseline audit per domain, and `compare_consent_states` has nothing to compare — there's no opt-out or GPC variant to diff against. In-app: a single audit per domain, no "Reject All" or GPC sibling. *Unlocks:* standing up the three-audit consent pattern (`setup_compliance_monitoring` with regulation "ccpa" creates default + opt-out + GPC) makes `compare_consent_states` answer the question that actually matters — "does our Reject All block what it's supposed to?" A default-only account is testing presence, not compliance.

**7. No anomaly detection wired.** *Detect:* `find_anomalies` has never been used and there's no monitoring cadence — drift is caught by a complaint, not by the system. In-app: no monthly trend review, no one watching `get_metric_trend`. *Unlocks:* a monthly `find_anomalies` pass (per metric: tags, cookies, pages, request-domains) paired with `get_metric_trend` and `find_first_observed` catches the slow drift and the silently-added vendor that the weekly Rule triage misses. This is the difference between catching a change and being surprised by it.

**8. No labels or saved reports.** *Detect:* `list_saved_reports` is empty and `list_labels` is empty — nothing aggregates across audits, so there's no way to show a trend or roll up to a sponsor. *Unlocks:* `create_saved_report` (built after `get_report_schema` to discover columns) plus labels gives the program a live dashboard and an exportable evidence artifact. Without saved reports, every executive conversation starts from a blank page; with them, the trend is already accumulating before anyone asks for it.

## Biggest-bang-for-buck rubric

Prioritize the fixes by impact × effort. Impact = how much risk it retires or value it exposes; effort = how much configuration and change management it takes. Work the high-impact / low-effort quadrant first — those are the moves that change the account in an afternoon.

| | **Low effort** | **High effort** |
|---|---|---|
| **High impact** | **Do first.** Wire alerts on existing Rules (#3). Re-route single-recipient alerts to a team channel (#4). Schedule a `scan_audit_pii` sweep on PII/PHI properties (#5). Run `find_anomalies` monthly (#7). | **Plan & resource.** Stand up the three-audit consent pattern per domain (#6). Build the Rule library from incident history where audits have none (#2). |
| **Low impact** | **Quick wins / fill-in.** First saved report + labels for rollup (#8). | **Defer.** Reorganize a sprawling flat account into folders/labels at scale (#1) — real value, but it's tedious and best done once coverage and Rules are settled. |

How to read the quadrants:

- **Do first (high impact / low effort).** Mostly turning on capability that's already half-built. Rules exist but don't alert; audits exist but PII was never scanned. Low change-management cost, immediate risk reduction.
- **Plan & resource (high impact / high effort).** Worth doing, but they need scope and a change window — building a Rule library or adding two consent-variant audits per domain touches configuration and someone's review cadence.
- **Quick wins (low impact / low effort).** The first saved report costs little and pays back the moment a sponsor asks for a trend. Good filler between the bigger moves.
- **Defer (low impact / high effort).** Reorganizing a flat account is real value but rarely urgent; do it once the program's Rules and coverage have stabilized, so you reorganize once rather than twice.

The order isn't rigid — a regulated-industry account with active litigation exposure promotes the PII sweep and consent coverage above everything else regardless of effort. Use the quadrant as the default, then let the customer's risk profile reorder it.

## MCP-tool diagnostic workflows

The concrete tool sequences that produce the health read. Each is a sequence, what it teaches you, and the action it points to. Run the ones that target the dimensions scoring lowest in the framework above.

**Account audit — score the whole account.**
```
list_audits                        // full inventory of audits
get_audit_health(auditId)          // per audit: is it running clean?
get_audit_rules(auditId)           // per audit: does it grade anything?
```
*What you learn:* breadth (how many audits, covering what), freshness (which are healthy vs. failing to run), and Rule depth (which audits are graded vs. raw inventory). *Action:* score the coverage / freshness / Rule-depth dimensions; the failing-to-run audits are a config/auth fix, the Rule-less ones feed underuse pattern #2.

**Usage trend — is consumption tracking the program or the incidents?**
```
get_usage_overview                 // current consumption snapshot
get_usage_summary                  // breakdown by audit/journey
get_usage_trends                   // trajectory over time
```
*What you learn:* whether usage is steady (a running program) or spiky (incident-driven, a stuck-at-crawl tell). *Action:* spiky low usage points to the "bought it but only one audit" unstick in `references/lifecycle-and-maturity.md`; steady growth confirms a healthy run/fly account worth a renewal-value conversation.

**Coverage gap analysis — what's missing from what should be there.**
```
find_coverage_gaps(auditId)        // pages missing expected tags, domains never seen
find_rare_observations(auditId)    // low-frequency findings worth a look
```
*What you learn:* the holes — pages that should carry the analytics tag but don't, vendors appearing on some pages and not others, and the rare observations that are either edge cases or early signs of an unauthorized addition. *Action:* the gaps become new Rules (close the "should be everywhere but isn't" hole) and a coverage-expansion recommendation.

**Anomaly / drift review — what changed and when.**
```
find_anomalies(auditId, metric="tags", thresholdPct=25, lookbackRuns=10)
get_metric_trend(auditId, metric="tags")   // the trajectory behind the flag
find_first_observed(auditId)                // when did this vendor/cookie/domain appear?
```
*What you learn:* runs where a metric jumped (scope-normalized, so a scan-size change doesn't masquerade as a spike), the trend behind the flag, and the first-seen date of anything new. *Action:* wire this as the monthly cadence (underuse pattern #7); a first-observed date that lands between change freezes is an unauthorized addition to chase down.

**Vendor inventory — who's receiving data, and is it allowed.**
```
get_inventory                              // cross-audit vendor/tag roll-up
query_report(entityType="network-requests", ...)   // request-domains across the account
get_request_privacy_report(auditId, runId)          // vendor / geo data-flow detail
```
*What you learn:* the full third-party footprint across audits, the distinct request-domains receiving data, and the geo/privacy shape of those flows. *Action:* reconcile against the approved-vendor list; undocumented vendors feed the tag-audit deliverable and a vendor-review recommendation. (Use `get_report_schema(entityType="network-requests", search="domain")` first to discover the columns before building the query.)

**PII exposure sweep — what personal data leaks, and to whom.**
```
list_audits(search="<key property>")       // find the PII/PHI-bearing audits
scan_audit_pii(auditId, customRegex=[...])  // per audit: leak paths, masked values
```
*What you learn:* which leak paths (tag-variable values, cookie values, request query strings) carry data matching email or your custom patterns, and which destination domains receive it — values masked, destinations named. *Action:* every finding to a third-party destination is an active leak to remediate; this is underuse pattern #5 and the evidence backbone for `references/privacy-litigation-defense.md`. Run `scan_journey_pii` on the equivalent funnels for the canary-mode signal on data the user actually typed.

## Recommended next-action templates keyed to maturity stage

Cross-reference the stage diagnosis in `references/lifecycle-and-maturity.md`, then apply the stage-specific next actions below. Diagnose the stage first (it's rarely the stage the customer thinks they're in), then run the matching plays.

**Crawl (one audit, manual, reactive) — make the one audit a standing signal.**
- Confirm the baseline audit is healthy (`get_audit_health`), then schedule it (`build_schedule` → `update_audit`).
- Draft three to five Rules from the customer's own incident history (`create_rule` → `update_audit_rules`) — underuse pattern #2.
- Run `find_coverage_gaps` and close the obvious holes.
- *Biggest bang:* the schedule + first Rules. Turns a one-time answer into a recurring verdict.

**Walk (scheduled audits, Rules attached, reviewed by a person) — make failures find a human.**
- Wire alerts on the high-stakes Rules (`create_alert`) and route to the team's real channel — underuse pattern #3, the top do-first move.
- Check alert routing for the single-recipient bus-factor risk (`get_alert` → `update_alert`) — underuse pattern #4.
- Add consent-state coverage where privacy is in scope (`setup_compliance_monitoring`) — underuse pattern #6.
- Stand up the first saved report (`get_report_schema` → `create_saved_report`) — underuse pattern #8.
- *Biggest bang:* alerting. A walk-stage account's failures are already being caught by Rules; they just aren't being announced.

**Run (alerts routed, ownership defined, program operating) — tune, monitor, and report up.**
- Tune flappy alert thresholds against history (`find_anomalies` lookback, `get_metric_trend`) so the channel stays trusted.
- Wire the monthly anomaly/drift review (`find_anomalies`, `find_first_observed`) — underuse pattern #7.
- Schedule PII sweeps across PII/PHI properties (`scan_audit_pii`) — underuse pattern #5.
- Move from a static export to a live saved-report dashboard a sponsor can open.
- *Biggest bang:* the move toward an executive sponsor. The lifecycle file flags sponsor absence as the leading renewal risk — tie the program's output to a metric an executive owns.

**Fly (governance program, executive-owned, continuously improving) — keep coverage current, don't let it age out.**
- Run a recurring coverage review against the current risk landscape — new regulations (the **regulation** skill), new vendor categories, new properties.
- Keep `get_inventory` rolling up cleanly; organize new properties into the existing folder/label scheme on day one (underuse pattern #1 in reverse — stay organized).
- Confirm the executive sponsor is current and engaged; re-recruit on any leadership change.
- Keep the Rule library growing with the threat landscape rather than frozen.
- *Biggest bang:* sponsor continuity and Rule-library freshness — the two ways a fly-stage account quietly slides back to run.

## How to deliver this to the customer

The health read becomes a deliverable. The structures live in `references/consulting-deliverables.md` — use them rather than inventing a format.

- **Account Health Check.** Frame the diagnostic as a short, ranked artifact: the seven-dimension scores up top, then the prioritized fix list from the bang-for-buck rubric, each fix tied to the tool-call evidence that proves the gap. Borrow the **Tag Audit Report** skeleton's discipline from `references/consulting-deliverables.md` — executive summary, top three findings ranked by severity, recommendations split into immediate / near-term / strategic. Two pages, numbers before prose, dated and signed.
- **Tie it to the maturity arc.** Pair the health check with the stage diagnosis and the relevant transition checklist from `references/lifecycle-and-maturity.md` so the customer sees not just the gaps but the path out of them.
- **Value framing.** Translating "we caught 23 undocumented vendors" or "Reject All leaks 4 tags" into a business case the sponsor acts on is the job of the ROI and renewal framing (a dedicated reference is planned for a later release). Until then, frame value in prose: lead with the risk retired (litigation exposure, ad-spend waste, regulator inquiry avoided) and the time-to-detect improvement, anchored to the numbers the diagnostic surfaced.

Deliver the ranked fix list, not the raw scores. The scores justify the ranking; the ranking is what the customer acts on.

---

*Last verified: 2026-06-04*
