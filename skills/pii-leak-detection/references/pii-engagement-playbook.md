# PII-leak detection engagement playbook

The operational depth behind the six phases in `SKILL.md`. This is a consulting/SE runbook, not legal advice.

## Contents
- Phase 1 — Scope & tier flows
- Phase 2 — Seed canary personas (+ the one-inbox guardrail)
- Phase 3 — Build the canary journeys
- Phase 4 — Baseline & analyze
- Phase 5 — Deliver the verdict
- Phase 6 — Leave behind standing detection
- Journey-maintenance strategy
- Production side-effects & etiquette

## Phase 1 — Scope & tier flows
Inventory every flow that SUBMITS personal data (forms) or RENDERS it (authenticated pages). Tier by risk:
- **Tier 1** — authenticated account areas + payment/checkout. The server sends real PII down to the browser here, so leaks happen without the journey typing anything; these need known-value tracing.
- **Tier 2** — lead / quote / signup / contact forms.
- **Tier 3** — search, preferences, chat.
Output: a customer-approved tiered flow list. Keep it small — maintenance cost is a scoping input, not an afterthought (see Journey-maintenance strategy).

## Phase 2 — Seed canary personas (+ the one-inbox guardrail)
Generate one persona per flow:
```
python3 scripts/canary_persona.py checkout,signup,quote <PII-CANARY-inbox-address> --seed 1
```
Each persona is unique after normalization (name / email / E.164 phone / address / account id) so hashed-variant matching stays collision-free.

**The one-inbox guardrail (hard rule):**
1. `list_email_inboxes` — if an inbox labeled `PII-CANARY` exists, reuse its address.
2. Only if none exists, `create_email_inbox` **once** and label it `PII-CANARY`.
3. **Never create a second canary inbox for the account.** Per-flow uniqueness is sub-addressing (`base+checkout@…`), not more inboxes.

Email mode: **shared** is the default (set from the 1768 sub-addressing verification). In `subaddress` mode each flow gets `base+flow@…`; confirm at build time that the target form accepts a `+` in the email field — if a specific form rejects it, switch that flow to the bare base address (`--email-mode shared`) and rely on the persona name/phone for attribution. In `shared` mode all flows use the bare base address; a received email proves propagation at account granularity and attribution rests on the typed name/phone.

## Phase 3 — Build the canary journeys
One journey per flow, built through **automation-and-testing** (selector-evidence gate, SPA prevent-navigation, action-sets for shared steps). Type the persona's values via `input`/`maskedinput`. For Tier 1, add the login steps and pass the account's known profile via `knownValues` on the scan. **Size the trailing `waitDuration`** on the last action to the longest expected delayed egress — late `sendBeacon`/post-load requests are only captured within the action's wait window (verified 2026-07-14: a 15s beacon is missed at `waitDuration=3`, caught at `20`).

## Phase 4 — Baseline & analyze
Run every journey, then:
- `scan_journey_pii` with `format:"json"` (requires connector ≥ v0.6.70). It catches the canary AND its hashed/percent/base64 forms — a digest hit is STRONGER evidence (active identity-resolution processing). Pass `knownValues` for masked fields and Tier-1 server-rendered profiles; remember the captured-surfaces-only boundary.
- Check `get_email_inbox_messages` for mail received at the canary address — independent, out-of-band propagation proof.
- `scan_audit_pii` + `get_request_privacy_report` / `get_cookie_privacy_report` / `compare_consent_states` for the site-wide and consent-context picture.
Record the JSON as the baseline for later re-scan diffing.

## Phase 5 — Deliver the verdict
A masked verdict: what leaked, to which third-party registrable domain, in which form (plaintext vs hashed). Include a **coverage matrix** naming what could NOT be inspected — opaque/undecodable payloads, masked fields without `knownValues`, uncaptured surfaces (server-side tags, server-rendered DOM). Never let a truncated or errored scan read as a clean "no PII" — the JSON `coverage.truncated`/`lowerBound` flags carry this; surface them.

## Phase 6 — Leave behind standing detection
- Schedule the canary journeys and the site-wide audit.
- Keep the `PII-CANARY` inbox listening; make inbox checks part of the periodic review.
- Use **Rules for presence assertions only** (consent tag present, GPC honored). Rules assert that expected things happen — they cannot detect an unwanted occurrence, and the inverted "always-fail" hack is unmaintainable and misses untagged requests. Standing PII detection = scheduled journeys + periodic re-scan (diff against the baseline) + inbox canaries.

## Journey-maintenance strategy
The adoption blocker is "now I maintain 50 journeys." Mitigate: tier ruthlessly (build Tier 1 first, expand only with demonstrated value); share common steps via **action-sets** (login, cookie-accept); set a re-verification cadence (selectors drift when the site redesigns); let journey-failure notifications catch breakage loudly.

## Production side-effects & etiquette
Canary journeys submit real forms — they create real leads, orders, and emails. Coordinate with the customer: use a provisioned TEST account for Tier 1, agree on CRM hygiene and suppression lists, and confirm who owns cleanup. The canary values are synthetic, but the submissions are real events in the customer's systems.
