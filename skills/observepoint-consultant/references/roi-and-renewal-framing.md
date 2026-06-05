# ROI and renewal framing

Load this file when the conversation is about *demonstrating the value a customer already gets from ObservePoint* — renewal preparation, a quarterly business review, a budget-owner conversation, justifying the line item to a CFO or VP, or the `/op-value-snapshot` command. The audience is an existing customer and the CSM working with them, not a prospect. The job is to translate what the program has been quietly doing — catching incidents, accruing evidence, retiring risk — into a story a budget owner acts on.

> **This reference frames value; it never quotes prices. ObservePoint pricing is custom — direct any pricing question to the account team. Everything here is about demonstrating value, not cost.**

This is the value-framing companion to the `account-health` skill, which reads the account and ranks the next moves, and diagnoses the maturity stage and the arc between stages. This file takes their output — the incidents caught, the regressions detected, the stage the customer is at — and turns it into the renewal case. No sales motion, no prospecting: the customer already bought it, and the question is whether the value is visible to the person who signs the renewal.

## ROI framework

ObservePoint is not a revenue-generation tool, and framing it as one invites a comparison it will lose. It is a **risk-reduction + efficiency + revenue-protection** play. The honest framing is *what breaks, and what risk re-enters, without it* — the value is the cost of the bad outcomes it prevents, not new revenue it creates.

Three value pillars, in the order a budget owner cares about them:

| Pillar | The question it answers | What the value actually is |
|---|---|---|
| **Risk reduction** | What exposure does this retire? | Privacy/litigation exposure, regulator inquiry, and undocumented-vendor risk that would otherwise sit unmonitored until it becomes a demand letter or a fine. |
| **Revenue protection** | What revenue does this protect? | Conversion and purchase tracking that, when it silently breaks, corrupts the data the business steers on and wastes the ad spend pointed at it. |
| **Efficiency** | What does this save us doing by hand? | Audit automation and evidence generation that would otherwise be manual QA, manual audit-prep, and cross-team firefighting hours. |

The trap to avoid: trying to attribute a revenue *lift* to ObservePoint. It doesn't generate demand. What it does is keep the machinery that captures demand honest — so the framing is always *protection and avoidance*, expressed as the cost of the incident that didn't happen, the audit that didn't take three weeks of manual prep, and the leak that was caught before it was a complaint. Lead with risk retired and time-to-detect, anchored to the customer's own numbers from the account, never to a generic benchmark.

Two framing disciplines make the difference between a renewal case that lands and one that gets second-guessed:

- **Counterfactual, not hypothetical.** "This caught a broken purchase event on March 4" is a fact in the run history. "This could save you millions" is a number the budget owner will discount to zero. Stay on the counterfactual the account can prove — the incident that *was* caught and what its undetected version would have cost in the customer's own terms.
- **The budget owner's metric, not yours.** A CFO cares about revenue integrity and audit-defense cost; a privacy GC cares about litigation exposure; a VP of Marketing cares about ad-spend efficiency. The same audit history supports all three stories — pick the value categories below that map to whoever signs the renewal, and lead with those.

## Quantifiable value categories

Six categories. For each: **what to measure**, **how ObservePoint data evidences it** (the report or MCP tool that produces the proof), and **how to express it to a budget owner**. Every number must trace back to the customer's own account — a fabricated benchmark is worse than no number.

### 1. Incident avoidance — broken tracking caught early protects revenue

- **Measure:** incidents caught *before* they reached business impact — a broken purchase event, a doubled conversion pixel, a tag that stopped firing — and the gap between when ObservePoint flagged it and when it would otherwise have surfaced (the monthly-report lag, the complaint, the quarter-end reconciliation).
- **Evidence:** `find_anomalies` on the tags / broken-pages metrics flags the run where the metric moved; `get_metric_trend` shows the trajectory behind the flag; run history via `get_audit_runs` and `analyze_rule_results` dates the catch. `find_first_observed` pins when a change first appeared.
- **Express it:** "Our purchase-event Rule failed on the March 4 run and alerted the analytics owner the same day. Without the audit, that break surfaces in the monthly report — three weeks of corrupted conversion data steering ad spend and merchandising decisions in between." The value is the bad-data window that didn't happen.

### 2. Compliance evidence readiness — audit hours saved and fine-exposure reduction

- **Measure:** the hours a compliance or privacy team would otherwise spend assembling audit evidence by hand, plus the fine-exposure reduction from being able to demonstrate ongoing controls rather than a point-in-time scramble.
- **Evidence:** the quarterly evidence pack — `query_report` against rule-summary and run history, packaged with `create_saved_report` for the live view and exported as the artifact. The pack proves the audits ran as scheduled, what they caught, and how fast it was remediated.
- **Express it:** "The Q1 evidence pack assembled itself from the audit history — no week of manual screenshotting before the audit committee meeting. And when a regulator or auditor asks, we show a year of dated, scheduled runs instead of reconstructing the past from memory." The value is the readiness, not just the hours.

### 3. Ad-spend efficiency — clean conversion data means less wasted spend

- **Measure:** ad spend pointed at audiences or optimized against conversion signals that were silently broken or firing pre-consent — spend wasted because the platform was optimizing on corrupted data.
- **Evidence:** consent and conversion validation. `compare_consent_states` shows which ad/measurement tags fire on Accept-All but should be blocked on Reject-All; Rules on the conversion events catch a purchase pixel that stopped firing or double-fired; `query_report` against the tags/network-requests entities quantifies where the conversion signal is clean.
- **Express it:** "The Meta and Google conversion tags were double-firing on the iOS path for two weeks — the bid optimizer was learning on inflated conversions and overspending against that audience. The audit caught it; the spend correction is the value." The customer owns the wasted-spend figure; ObservePoint owns the catch.

### 4. Legal and fine-exposure reduction — privacy and CIPA defense readiness

- **Measure:** the litigation and fine exposure retired by being able to prove reasonable controls and a change history — CIPA/wiretap, VPPA, BIPA, and healthcare-pixel theories all turn on what data left to which third party, and when.
- **Evidence:** `scan_audit_pii` and `scan_journey_pii` produce the masked leak-path findings (what value matched which pattern, to which destination domain) without echoing the data; consent-state audits and `compare_consent_states` document whether opt-out actually blocks what it claims to. This is the evidence backbone described in the `litigation-defense` skill.
- **Express it:** "When the demand letter arrives, we can show counsel exactly what fired, to whom, under which consent state, on which date — a documented control history instead of a frantic forensic reconstruction." The value is the difference between a defensible posture and a discovery scramble. (Frame the customer's exposure generically; never quote ObservePoint's price against it.)

### 5. Operational efficiency — audit automation versus manual QA hours

- **Measure:** the QA and validation hours that scheduled audits replace — the manual tag-checking, the release-time spot checks, the "did anything break?" sweeps an analyst would otherwise run by hand.
- **Evidence:** scheduled audits versus manual testing. `get_usage_trends` and the run history via `get_audit_runs` show the cadence of automated coverage; `get_audit_health` shows it running reliably without a human triggering it. Each scheduled run is QA that no one had to perform.
- **Express it:** "Forty-plus scheduled audit runs a month, each one a full-site tag-and-consent check no analyst had to run by hand — and the release-gate audit means QA doesn't manually re-verify tagging on every deploy." The value is the analyst time redirected from checking to building.

### 6. Team-time savings — analytics, privacy, and dev hours not spent firefighting

- **Measure:** the cross-functional hours *not* spent reacting — analytics chasing a data discrepancy, privacy fielding a what-fired question, engineering bisecting a tagging regression — because the alert fired the day the change landed instead of weeks later.
- **Evidence:** the time-to-detect improvement is the proxy. `analyze_rule_results` and `get_run_alerts` show failures caught and routed at the run that introduced them; `find_first_observed` shows how fresh the catch was. A failure caught at the introducing run is a fraction of the firefight of one discovered downstream.
- **Express it:** "Catching the broken event at the deploy that caused it is a one-owner same-day fix. Discovering it three weeks later in a reconciliation is an all-hands forensic exercise across analytics, privacy, and engineering." The value is the firefight that became a ticket.

## Before / after framing templates

The cleanest way to show value to a budget owner is the contrast between the pre-ObservePoint state and the current state. Fill these with the customer's own incidents — the specifics are the persuasion.

- **Broken-tracking detection.** *Before:* broken purchase tracking discovered in the monthly report, three weeks of bad data already steering spend and decisions. *After:* caught within one audit cycle, alerted to the owner the same day, fixed before the next reporting period.
- **Consent compliance.** *Before:* "we think Reject All blocks the ad tags" — an assumption no one had tested. *After:* `compare_consent_states` proves it every cycle, and the one time it regressed, the audit caught the leak before a complaint did.
- **Vendor sprawl.** *Before:* a third-party vendor list maintained from memory, last reconciled "a while ago." *After:* every third-party domain receiving data is inventoried each run, and a new one that appears between change freezes gets a first-observed date and a question.
- **Audit / regulator readiness.** *Before:* a week of manual evidence-gathering and screenshotting before every audit-committee meeting. *After:* the evidence pack exports from the run history on demand, dated and complete.
- **Release safety.** *Before:* tagging regressions shipped to production and were found by whoever noticed the numbers looked wrong. *After:* the release-gate audit blocks the deploy when a critical Rule fails on staging.

Keep each contrast to one before and one after sentence. A budget owner reads the delta, not the prose around it.

## Renewal narrative templates

The value story that lands depends on where the customer is in the maturity arc covered by the `account-health` skill (crawl → walk → run → fly). A crawl-stage customer can't tell a fly-stage story, and a fly-stage customer is insulted by a crawl-stage one. Match the narrative to the diagnosed stage, not the stage the customer claims.

**Crawl — one audit, manual, reactive.** The narrative is *foundation and the catch that paid for it.* The program is young, so lead with the single concrete thing the one audit surfaced that the customer didn't know — the undocumented vendors on the inventory, the tag that wasn't firing where it should. "We've already found X; here's what we'd see with the monitoring actually running." Renewal here is about protecting the foundation and funding the next step, not defending a mature operation. Pair with the crawl→walk transition checklist so the renewal buys a trajectory, not a static tool.

**Walk — scheduled audits, Rules attached, reviewed by a person.** The narrative is *the system is catching real things on its own.* Now there's a run history to point at: Rules firing on real runs (`analyze_rule_results`), regressions caught on a cadence. "Over the last two quarters the audits caught N regressions; here's the one that would have been three weeks of bad data." Renewal is straightforward — the evidence is accumulating — but flag the missing alert layer as the gap the next year closes.

**Run — alerts routed, ownership defined, program operating.** The narrative is *measured protection with a time-to-detect to prove it.* This customer has incidents caught, routed, and resolved on an SLA, plus a recurring evidence pack. Lead with the numbers: incidents detected, time-to-detect P50/P90, regressions caught before impact, the evidence pack the privacy team relies on. The renewal case is the quantified track record. The one risk to name: if there's no executive sponsor, recruit one *before* renewal — the `account-health` skill flags sponsor absence as the leading renewal risk and treats it as a first-class signal.

**Fly — governance program, executive-owned, continuously improving.** The narrative is *this is infrastructure, and removing it regresses the business.* The program is a standing function with a sponsor and a budget line; the renewal conversation is about continuity and the cost of the gap if it lapsed. Lead with the program's maturity — the QBR cadence, the policy and RACI, the coverage that onboards new properties by default — and frame the renewal as protecting an established control, not buying a tool. The price-of-not-renewing framing below is sharpest here.

## Common budget-owner objections + rebuttals

Each rebuttal is grounded in a real ObservePoint capability, not a sales line. Stay in value framing — never counter a budget objection with a pricing claim.

| Objection | Rebuttal grounded in capability |
|---|---|
| **"It's a nice-to-have."** | It's the only thing watching whether the tracking the business steers on still works. The day a purchase event breaks silently, it stops being nice-to-have — and the evidence pack and incident history show it has already caught exactly that. Reframe from "extra" to "the smoke detector for revenue and consent data." |
| **"We'll just do this manually."** | Manual QA covers the pages someone remembers to check, on the days they remember to check them. Scheduled audits cover every page every cycle, `compare_consent_states` diffs opt-out automatically, and `scan_audit_pii` looks for leaks no human eyeballs catch. The manual equivalent is the operational-efficiency hours in the value categories above — and it still misses the slow drift `find_anomalies` is built to catch. |
| **"OneTrust / our CMP already does this."** | A CMP *collects and stores* consent; it doesn't *verify the tags obey it.* ObservePoint tests whether Reject All actually blocks what it's supposed to (`compare_consent_states`) and whether tags fire pre-consent — the gap between what the CMP promises and what the site does. The two are complementary, not redundant; see `references/competitive-positioning.md` for the full framing. The CMP is the policy; ObservePoint is the audit of the policy. |
| **"We haven't had an incident."** | You haven't had a *caught* incident — that's survivorship bias. Before monitoring, a broken event or a consent leak surfaces weeks later as a data discrepancy or a complaint, not as "an incident on a date." The run history shows what was caught and when; the absence of surprises is the product working, not the risk being absent. |
| **"Budget is tight this year."** | Tight budget is exactly when an undetected broken-tracking incident or a privacy demand letter hurts most — both are far more expensive than the monitoring that prevents them. Frame the renewal against the cost of one incident the program has already caught this year, drawn from the account's own history, not against a discretionary line. (Direct any actual pricing discussion to the account team.) |

## The price of NOT renewing

The sharpest renewal framing is the honest one: what regresses, and what risk re-enters, the day ObservePoint is switched off. Walk the budget owner through what the lapse actually does.

- **Monitoring goes dark.** Scheduled audits stop. There is no longer anything checking whether tags fire, whether the conversion pixel works, whether a new vendor appeared. The site keeps changing; nothing watches it.
- **Drift returns undetected.** The slow accretion `find_anomalies` and `find_first_observed` were catching — the silently-added vendor, the gradually-degrading tag coverage — goes back to surfacing only when someone happens to notice. Time-to-detect resets from hours to "whenever."
- **Compliance evidence stops accruing.** The dated, scheduled run history that made the evidence pack a routine export stops growing. When the next audit or regulator inquiry comes, there's a gap in the record exactly where the lapse was — and a gap in a control history is its own kind of exposure.
- **Consent verification stops.** `compare_consent_states` is no longer confirming Reject All blocks what it should. A consent regression — the kind that drives CIPA and wiretap claims per the `litigation-defense` skill — can ship and sit live, undetected.
- **The next incident is found by the CFO, not the alert.** This is the whole framing in one line. With the program running, a broken purchase event is a same-day alert to an owner. Without it, it's a discrepancy the CFO spots in the quarter-end numbers — after weeks of corrupted data and wasted spend, and after the chance to catch it cheaply has passed.

The value of renewing is the inverse of this list. Frame the lapse as the regression it is, in the customer's own terms, never as a pricing threat.

## Building the value snapshot

The value snapshot is the screenshot-ready artifact a budget owner skims in thirty seconds — the proof, condensed. The `/op-value-snapshot` command produces this. Use the Value Snapshot and Renewal Narrative templates in `references/consulting-deliverables.md` for the format rather than inventing one (those specific templates are being added there alongside this reference).

What goes in it, all drawn from the account over the renewal period:

- **Incidents caught** — count and a one-line example of the most consequential one (the broken-event catch, the consent leak), with the date and the time-to-detect. From `analyze_rule_results`, `get_run_alerts`, run history via `get_audit_runs`.
- **Regressions detected** — drift and anomalies flagged before they became incidents. From `find_anomalies`, `get_metric_trend`, `find_first_observed`.
- **Vendors inventoried** — the third-party footprint tracked, and any new vendors caught appearing. From `get_inventory` and `get_request_privacy_report`.
- **Compliance evidence produced** — evidence packs generated, consent states verified, PII scans run. From the saved-report exports, `compare_consent_states`, `scan_audit_pii`.
- **Coverage and cadence** — audits running, scheduled runs completed, properties watched, over the period. From `get_usage_trends` and `get_audit_health`.

**Pulling the numbers.** A repeatable sequence for assembling the snapshot from the account, run over the renewal period:

```
get_usage_trends                          // coverage + cadence: runs completed, audits active over the period
get_audit_runs(auditId)                   // run history per key audit — dates the catches
analyze_rule_results(auditId)             // which Rules fired on real runs, and when
get_run_alerts(auditId, runId)            // incidents that routed to an owner
find_anomalies(auditId, metric="tags")    // regressions caught before they became incidents
find_first_observed(auditId)              // new vendors / cookies caught appearing, with dates
get_inventory                             // third-party footprint inventoried across audits
compare_consent_states(domain=...)        // consent verification evidence
query_report(entityType="rules", ...)     // package the rule-summary trend for the period
create_saved_report(...)                  // the live view the sponsor can open
```

If the MCP server isn't loaded this is the same read by hand from the UI — run history, Rules tab, Alerts page, saved reports — narrate the in-app equivalent rather than faking a tool call.

Follow the deliverable discipline in `references/consulting-deliverables.md`: numbers before prose, severity-ranked, dated, sourced to an ObservePoint report. One page, screenshot-ready, every figure traceable to the account. The snapshot doesn't argue the value — it shows it, and lets the budget owner reach the conclusion.

---

*Last verified: 2026-06-04*
