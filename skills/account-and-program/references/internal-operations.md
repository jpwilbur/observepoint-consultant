# Internal operations — running ObservePoint across a book of accounts (CSM / solutions / support)

Load this when an INTERNAL ObservePoint user (CSM, solutions consultant, SE, support, services) is working ACROSS customer accounts rather than configuring one: "what's broken across my book right now," "who has access to this account," "who changed this audit," onboarding hygiene, QBR prep, or doing work inside a customer's account on their behalf. This is the internal across-the-book motion. For configuring a single account, see `references/account-config.md`; for the legal *why* of any finding, see `privacy-compliance`. **Strictly internal operations and pricing-free** — pricing, ROI math, and deal-scoping live in the separate internal `observepoint-revenue` tooling.

## 1. The motion: triage the book → focus → act safely

1. **Triage the portfolio** — find what needs attention across accounts.
2. **Read who's using it** — access and change review.
3. **Act safely in the account** — the impersonation lifecycle with the write-arming gate.

## 2. Portfolio triage — "what's broken right now"

- `get_account_health` is the weighted-severity digest of the most problematic audits (failed runs, triggered alerts, rule failures, broken pages, unapproved cookies). It is the FRONT DOOR — run it FIRST to find the audits that deserve a look, scoped to the whole account or a folder, instead of looping `get_audit_health` over every audit. Drop into `list_audits` + `get_audit_health(auditId)` only on what it flags. `get_audits_status` is the run-status companion.
- `find_account` resolves a customer by name/URL to the numeric id the impersonation lifecycle needs.

## 3. Account access & change review

These are the bread-and-butter governance reads for onboarding hygiene, QBR prep, security review, and "who broke this audit." Teach them as workflows, not a tool list:

- **Onboarding / access hygiene** — `review_account_access` lists who can reach the account; flag never-logged-in, stale (>90 days), and over-privileged admins, then `get_user` for detail on a flagged person.
- **Change attribution ("who changed this audit / when did this break")** — `query_user_events` returns the activity/event log filtered by item or time window. **It is attribution-only: it tells you who did what and when, NOT a before/after diff of the configuration.** Pair it with `get_file_changes` / `compare_audit_runs` when you need the actual delta.
- **QBR / security review** — combine `get_account_health` (program state) with `review_account_access` (access posture) to walk into the review with both the "is it working" and "is it governed" picture.

## 4. The safe impersonation lifecycle (admin)

Acting inside a customer's account is powerful and easy to misfire — a wrong-account write lands in real customer data. The lifecycle, every time:

1. `whoami` — confirm whose identity you're acting as BEFORE anything. The connector is one long-lived session, so a prior task may have left an impersonation active; never assume.
2. `find_account` → `login_as_account(accountId)` — enter the account. **Reads are live immediately; WRITES are blocked.**
3. `confirm_account_plan({plan})` — **the write-arming gate.** Call it ONLY after you have (a) told the user which account you're in and what you intend to do, and (b) gotten their explicit "proceed." It re-mints the token and arms writes for THAT plan. Re-confirm for each distinct piece of work; never carry one plan's confirmation into unrelated later work.
4. Do the work (the config sequence in `references/account-config.md`).
5. `stop_impersonation` — return to your own admin identity. Pair every `login_as_account` with it.

Impersonation also **auto-reverts after a short idle period** — after any gap, re-run `whoami` before assuming you're still in the account. The full operating doctrine (hard rules, lifecycle, re-confirmation) lives with the tools in `references/mcp-tools.md` — this section is the operating summary; that file is the authority.

## 5. Boundaries

- **Pricing, ROI math, deal-scoping, prospecting** → the separate internal `observepoint-revenue` plugin. Out of scope here.
- **Single-account configuration** → `references/account-config.md` (this file is the across-the-book layer above it).
- **Program health depth (seven-dimension score, underuse patterns, maturity)** → `references/account-health-and-strategy.md`.
- **What the law requires / does consent work** → `privacy-compliance`.
- **The MCP tool catalog + the impersonation operating doctrine + never-invent rule** → `references/mcp-tools.md` (runtime tool list always wins).

*Last verified: 2026-06-12*
