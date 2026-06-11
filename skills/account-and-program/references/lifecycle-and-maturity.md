# Lifecycle and maturity

Load this file when the conversation is about *where a customer is and where they go next*, not about a single technical task. The triggers: maturity questions ("how mature is our program?", "are we doing this right?"), onboarding ("we just bought ObservePoint — now what?"), expansion ("we have audits running, what's the next level?"), and the open-ended "where do we go from here?" The shape here is a maturity model plus the operational rhythms that move a customer up it. It pairs with the "Build a Web Governance program from scratch" playbook in `references/solution-playbooks.md` — that playbook is the month-by-month build sequence; this file is the diagnostic and the longer arc around it.

> **Starter content.** This file establishes the framework. Customer-size-aware
> timelines (SMB vs. mid-market vs. enterprise) and ObservePoint's actual internal
> program processes need a dedicated working session to integrate — that's a planned
> v0.6.0 follow-up. Treat the timelines here as illustrative defaults, not commitments.

## Web Governance Maturity Model

Four stages: **crawl → walk → run → fly.** This is the same framing the "Build a Web Governance program from scratch" playbook in `references/solution-playbooks.md` uses for its phased build — Phase 1 inventory is the crawl entry point, Phase 4 expansion lands a customer in run/fly. Use that playbook for the *build* steps; use this section to *diagnose* which stage a customer is actually in, which is rarely the stage they think they're in.

The diagnosis is not a survey. You read it off the account: how many audits exist, whether they run on a schedule, whether Rules are attached, whether alerts route to a human, and whether anyone outside the analytics team has ever seen the output. The MCP tools make this fast — `get_usage_overview` and `list_audits` tell you the breadth, `get_audit_health` tells you whether what exists is actually working, and `find_coverage_gaps` tells you what's missing from what should be there.

### Crawl — one audit, manual, reactive

**Diagnostic indicators.** `list_audits` returns one or a few audits. `get_usage_overview` shows low, sporadic usage — runs cluster around incidents, not a schedule. `get_audit_rules` on the audits returns few or no Rules. No alerts configured (`list_alerts` is empty or near-empty). The customer runs an audit when something breaks, reads the result, and closes the tab. There is no recurring cadence and no second viewer.

**What "good" looks like at this stage.** A single broad Web Audit across the site that actually completes and returns a clean tag-and-cookie inventory. `get_audit_health` is green for that one audit. The customer can answer "what tags and vendors are on our site?" from the inventory rather than from memory. That baseline inventory is the foundation everything else builds on — getting it right matters more than getting more.

**Common stuck-at-this-stage patterns.** The classic is "bought it but only ran one audit" — the tool was purchased to answer one question, the question got answered, and it went dormant. The other is treating ObservePoint as a one-off debugging console: run, look, leave, with nothing scheduled and nothing remembered between incidents. Both leave the customer paying for a platform they touch quarterly.

**Transition checklist (crawl → walk).** Confirm the baseline inventory audit is complete and healthy (`get_audit_health`). Put that audit on a schedule (`build_schedule` → `update_audit`). Draft the first three to five Rules covering the most painful known failure modes (start from the customer's actual incident history, not a generic list). Run `find_coverage_gaps` against the inventory to find the obvious holes — pages that should carry the analytics tag but don't, vendors that appear on some pages and not others.

### Walk — scheduled audits, Rules attached, results reviewed

**Diagnostic indicators.** `list_audits` shows several audits on a schedule (visible in their config). `get_usage_overview` shows steady, regular consumption rather than incident spikes. `get_audit_rules` returns a real Rule library on the key audits. Someone reviews results on a rhythm — but alerts may still be missing, so review is a person remembering to look rather than the system telling them. `list_alerts` is thin or empty.

**What "good" looks like at this stage.** Scheduled audits run reliably, Rules catch the regressions they were written for, and a named person reviews the output on a known cadence. `analyze_rule_results` across recent runs shows Rules actually firing and being acted on, not sitting dormant. The customer can answer "did anything break this week?" from the audit history instead of from a complaint.

**Common stuck-at-this-stage patterns.** "Audits but no Rules" — scheduled scans run, producing inventory nobody reads, because without Rules there's no pass/fail signal, just data. And "Rules but no alerts" — the Rules exist and fail correctly, but nobody is notified, so a failure sits in the dashboard until someone happens to look. Both stall the program at "we have data" without reaching "we get told when something's wrong."

**Transition checklist (walk → run).** Wire alerts on the high-stakes Rules (`create_alert`) and route them to the channel the responsible team actually watches. Define ownership per Rule — who gets paged when it fails. Establish a recurring review meeting so the cadence survives the person. Expand coverage with Journeys for the interactive funnels a Web Audit can't exercise. Stand up the first saved report (`create_saved_report`) so trends accumulate before anyone needs them.

### Run — alerts routed, ownership defined, program operating

**Diagnostic indicators.** `list_alerts` shows alerts on the important Rules, routed to real destinations. Coverage spans Web Audits *and* Journeys. `get_usage_overview` and `get_usage_trends` show consistent, growing usage that tracks the program's scope rather than incidents. Saved reports exist (`list_saved_reports`). Failures route to an owner and get resolved with a visible time-to-resolve, not just logged. The program runs whether or not any one person is paying attention this week.

**What "good" looks like at this stage.** Failures are caught by the system, routed to an owner, and resolved on an SLA. `find_anomalies` and `get_metric_trend` are part of the weekly rhythm, catching drift before it becomes an incident. The customer produces a recurring evidence artifact — a quarterly pack the privacy or analytics team relies on. Time-to-detect for a broken purchase event or a consent leak is measured in hours, not "discovered by the CFO."

**Common stuck-at-this-stage patterns.** "Alerts but noisy" — too many alerts, thresholds too tight, or alerts on Rules that flap, so the team learns to ignore them and the signal drowns. And the strategic ceiling: "a healthy program but no executive sponsor" — the operation runs well at the practitioner level but has no business owner, which is the single biggest renewal risk because nobody above the analyst can articulate the program's value when budget season comes. The account-health diagnostics in `references/account-health-and-strategy.md` treat this stuck pattern as a first-class renewal signal.

**Transition checklist (run → fly).** Tune alert thresholds against history (`find_anomalies` lookback, `get_metric_trend`) so alerts mean something — kill or widen the flappy ones. Tie the program's output to a business metric an executive cares about (ad-spend efficiency, incident reduction, audit-defense readiness) and name an executive sponsor. Move from a static evidence pack to a live saved-report dashboard the sponsor can open themselves. Establish the quarterly business review cadence. Bring CI/CD release gates and cross-functional coverage (privacy, analytics, marketing) under one program rather than several disconnected audits.

### Fly — governance program, executive-owned, continuously improving

**Diagnostic indicators.** Coverage is broad and intentional — audits and Journeys organized in folders by team, region, or risk tier, with consistent labels so reports roll up cleanly. `get_usage_trends` shows mature, predictable consumption. `get_inventory` gives a clean cross-audit roll-up. Alerts are tuned and trusted. Saved reports feed a recurring executive review. The program has a named business owner and a budget line. New properties are onboarded into the program by default, not bolted on after an incident.

**What "good" looks like at this stage.** Web governance is a standing program, not a tool. There's a policy and a RACI (see `references/consulting-deliverables.md`), an executive sponsor who reviews it quarterly, and a continuous-improvement loop — new failure modes become new Rules, new properties get onboarded into the existing cadence, and the evidence pack is a routine export rather than a fire drill. The program survives reorganizations because it's owned at the business level, not the individual level.

**Common stuck-at-this-stage patterns.** Complacency — the program runs so smoothly that nobody adds new Rules for emerging risks (a new privacy statute, a new vendor category, a new litigation theory), and coverage silently ages out of relevance. And sponsor attrition — the executive sponsor moves on and isn't replaced, quietly demoting the program back toward "run" without anyone noticing until renewal. The fly stage is maintained, not achieved once.

**Transition checklist (staying at fly).** Schedule a recurring coverage review against the current risk landscape — new regulations (the **privacy-compliance** skill), new vendor categories, new site properties. Confirm the executive sponsor is current and engaged; re-recruit on any leadership change. Keep the Rule library growing with the threat landscape rather than frozen. Treat the evidence pack and QBR as non-negotiable recurring commitments.

## Onboarding workflow

The milestone arc for a new customer, from kickoff to the first maturity transition. **Real timelines depend heavily on customer size** — an SMB on a single domain compresses these into days; a multi-brand enterprise with dozens of properties stretches them across quarters (the starter banner above applies). Treat the named intervals as the *sequence and dependencies*, not fixed dates.

**Day 1 — kickoff, scope, baseline audit.** Run the discovery conversation: which properties, which regions, which regulations, which data-layer spec, who owns what. (The per-industry files carry vertical-specific discovery questions — e.g. `references/industries/retail-ecommerce.md`.) Agree on the initial scope — start narrower than the customer asks for; a clean audit on the core properties beats a sprawling one that times out. Kick off the baseline Web Audit (`create_audit`, then `run_audit`) across that scope so the inventory is collecting from day one.

**Week 1 — interpret first results, draft initial Rules.** The baseline run is done; now read it together. Walk the tag inventory (`get_tag_inventory`), the cookie inventory (`get_cookie_inventory`), and the obvious gaps (`find_coverage_gaps`). This is where the customer first sees their own site clearly — usually with surprises. Translate the worst findings into the first three to five Rules (`create_rule`), and attach them to the baseline audit (`update_audit_rules`). The goal of week 1 is one healthy, Rule-bearing audit, not full coverage.

**Month 1 — scheduled audits live, alerts wired.** Move from manual to scheduled (`build_schedule` → `update_audit`) on a cadence that matches risk — weekly for most, daily for high-stakes funnels or PHI-bearing pages. Wire alerts on the Rules that matter (`create_alert`) and route them to the team's real channel. By the end of month 1 the customer is at the **walk** stage: the system runs on its own and tells someone when a known failure mode trips.

**Quarter 1 — full program, first evidence pack.** Expand coverage: Journeys for the interactive funnels (`create_journey`, `design_journey`), consent-state audits per region where privacy is in scope (`setup_compliance_monitoring`), and CI/CD release gates if the customer ships frequently. Stand up the first saved-report dashboard (`create_saved_report`) and produce the first quarterly evidence pack via `query_report` and `export_report`. This is the **run** stage and the first deliverable an executive sees.

**Year 1 — maturity transition, QBR cadence, renewal-prep groundwork.** By the one-year mark the program should be at **run** and reaching toward **fly**: tuned alerts, a named owner, a recurring quarterly business review, and an evidence trail that demonstrates value. Year 1 is also where renewal preparation begins in earnest — not as a sales motion but as the natural output of a program that's been accumulating evidence of its own worth. The **roi** skill covers how to frame that value; `references/account-health-and-strategy.md` covers reading whether the account is actually on track for it.

## CSM operational cadences

The recurring rhythms that keep a program at its stage and move it up. Each cadence has a job and a small set of tools.

**Weekly — incident triage on failed runs.** The fast loop. Check which scheduled runs failed and which Rules tripped. `check_run_status` and `get_run_alerts` surface what fired; `analyze_rule_results` interprets the pass/fail pattern across the week; `get_audit_health` flags audits that are failing to *run* (a config or auth problem) versus audits that ran and *caught* something. Triage, route to owners, confirm the genuine failures are tickets and the noise gets the alert tuned. The weekly cadence is where a "run"-stage program earns its keep.

**Monthly — trend review.** Step back from individual runs to the shape of the month. `find_anomalies` (per metric: tags, cookies, pages, request-domains) catches drift the weekly triage missed because it accreted slowly rather than spiking. `get_metric_trend` shows the trajectory. `find_first_observed` answers "when did this new vendor / cookie / domain first appear?" — the monthly review is the natural place to catch an unauthorized addition that slipped in between freezes. Bring the month's anomalies to the customer with a recommendation, not just a chart.

**Quarterly — business review and evidence pack.** The strategic loop. Produce the evidence pack: `query_report` against the rule-summary and run history for the quarter, packaged via `create_saved_report` for the live view and `export_report` for the artifact. The QBR shows the sponsor what the program caught, what it prevented, how fast it detected and resolved, and where coverage should expand next quarter. This is also the renewal-health checkpoint — `references/account-health-and-strategy.md` covers how to read the signals, and the **roi** skill covers how to frame the value the pack demonstrates.

**Annual — strategic planning and renewal prep.** The longest loop. Review the program against the year's risk landscape: new regulations, new properties, new vendor categories, organizational changes. Confirm the executive sponsor is current. Set the next year's coverage and maturity goals. Renewal prep is the natural byproduct — a program with a year of evidence packs and a present, engaged sponsor renews on its track record. The **roi** skill is the companion for building that case.

## Common stuck patterns

The recurring places programs stall, each with a detection method and a specific break-through play. These overlap with the diagnostics in `references/account-health-and-strategy.md` (treat that as the deeper, renewal-focused treatment) — here the focus is the operational unstick.

**"Bought it but only one audit."** *Detect:* `list_audits` returns one or a handful; `get_usage_overview` shows sporadic, incident-clustered usage with no schedule. *Break-through:* don't sell more audits — make the one audit recurring. Schedule it (`build_schedule` → `update_audit`), attach three Rules drawn from the customer's own incident history, and book the week-1 results review. The unlock is turning a one-time answer into a standing signal.

**"Audits but no Rules."** *Detect:* scheduled audits exist (visible in config) but `get_audit_rules` returns empty or near-empty across them. The customer is collecting inventory nobody reads. *Break-through:* run `find_coverage_gaps` and `get_tag_inventory` on the live data to surface the obvious failure modes, then convert the top few into Rules (`create_rule` → `update_audit_rules`). Inventory becomes pass/fail; data becomes signal.

**"Rules but no alerts."** *Detect:* `get_audit_rules` shows a real library, `analyze_rule_results` shows Rules failing on real runs, but `list_alerts` is empty. Failures sit in the dashboard until someone looks. *Break-through:* wire alerts on the high-stakes Rules (`create_alert`), route to the team's real channel, and assign an owner per alert. The unlock is moving from "we can see failures" to "failures find us."

**"Alerts but noisy."** *Detect:* `list_alerts` is full, but the team has stopped reacting — a tell you'll often hear in conversation before any tool confirms it. `find_anomalies` and `get_metric_trend` show many alerts firing on metrics that flap within normal range, or thresholds set tighter than the data's natural variance. *Break-through:* tune against history — widen or kill the flappy thresholds using the `find_anomalies` lookback to set realistic bands, and reserve alerts for the failures that actually warrant a human. Fewer, truer alerts restore trust in the channel.

**"Program but no exec sponsor."** *Detect:* the operation is healthy (`get_usage_trends` steady, alerts tuned, saved reports exist) but no one above the practitioner can name the program's business value — and it never appears in a leadership review. This is mostly an in-app-and-conversation signal, not a single tool reading. *Break-through:* tie the program's output to a metric an executive owns (ad-spend efficiency, incident reduction, litigation-defense readiness), build a saved-report dashboard the sponsor can open themselves, and book the first QBR. `references/account-health-and-strategy.md` treats sponsor absence as a leading renewal risk; the **roi** skill covers the value framing that recruits the sponsor.

## Maturity-driven roadmap

Concrete transition plans, one per stage gap. **Timelines scale with customer size** (per the starter banner) — the day counts below fit a mid-market customer on a focused set of properties; compress for SMB, extend for enterprise. The *order* of moves holds regardless of size.

**Crawl → walk, ~30 days.** Week 1: confirm the baseline audit is complete and healthy (`get_audit_health`), then schedule it (`build_schedule` → `update_audit`). Week 2: draft three to five Rules from the customer's incident history and attach them (`create_rule` → `update_audit_rules`). Week 3: run `find_coverage_gaps` and close the obvious holes (missing tags, partial coverage). Week 4: book the recurring results review and confirm the schedule has fired cleanly at least once. *Exit criteria:* scheduled, Rule-bearing audit with a human reviewing output on a cadence.

**Walk → run, ~90 days.** Month 1: wire alerts on the high-stakes Rules (`create_alert`), route them, and assign per-Rule ownership. Month 2: expand coverage — add Journeys for the interactive funnels (`design_journey`, `create_journey`) and consent-state audits per region where privacy is in scope (`setup_compliance_monitoring`). Month 3: stand up the first saved-report dashboard (`create_saved_report`) and produce a first evidence pack via `query_report` / `export_report`. *Exit criteria:* failures route to an owner and resolve on an SLA; coverage spans audits and Journeys; trends are accumulating in a saved report.

**Run → fly, ~180 days.** Months 1–2: tune alert thresholds against history (`find_anomalies`, `get_metric_trend`) so the channel is trusted. Months 3–4: name an executive sponsor and tie the program to a business metric the sponsor owns; move from a static export to a live dashboard. Months 5–6: organize coverage into folders/labels by team or risk tier for clean roll-ups (`get_inventory` for the cross-audit view), bring CI/CD gates and all cross-functional audits under one program, and run the first formal quarterly business review. *Exit criteria:* an executive-owned, continuously improving governance program with a tuned alert layer, a recurring QBR, and an evidence trail. The **roi** skill covers turning that evidence into the renewal case.

---

*Last verified: 2026-06-04*
