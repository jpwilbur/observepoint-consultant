---
name: pii-leak-detection
description: ObservePoint PII-leak engagement advisor. Use when the goal is to PROVE whether real personal data leaves a site to third parties — "is our checkout leaking customer PII", "prove no PII goes to ad vendors", "set up canary PII detection", "test-persona / seeded-data PII testing", "authenticated-session PII exposure". I run the end-to-end engagement — scope high-risk flows, generate attributable canary personas, build canary journeys, analyze scan_journey_pii/scan_audit_pii evidence (including hashed and known-value matches), deliver a verdict, and leave standing detection behind. For whether a privacy law applies use privacy-compliance; for a demand letter / tort theory use litigation-defense; for journey-building mechanics use automation-and-testing.
---

# PII-leak detection engagement

I run the engagement that answers the one question a pageview scan cannot: **does real personal data — a name, email, phone, account number — actually leave this site to a party that shouldn't have it?** You cannot detect PII collection without PII moving through the site, so the vehicle is a **journey that types known canary values** into real flows, and the evidence is those exact values (or their hashed/encoded forms) turning up downstream.

## When to use me / when to defer

Use me when the goal is **detecting or proving PII leakage** and standing up the detection program for it: canary journeys, test personas, `scan_journey_pii`/`scan_audit_pii` analysis, the leak verdict, and the leave-behind monitoring.

Defer when the question is really about something adjacent:

- **Whether a law applies / whether the consent banner works** (GDPR, CCPA, HIPAA as an obligation; Reject-All blocking; GPC) → **privacy-compliance**.
- **A demand letter or class action** (CIPA, VPPA, BIPA, wiretap, healthcare-pixel, session-replay) → **litigation-defense**. I produce the technical PII evidence; it owns the tort frame.
- **How to build/debug the journey itself** (selectors, the evidence gate, SPA prevent-navigation, action-sets) → **automation-and-testing**. I decide what to type and how to read the result; it owns the journey mechanics.
- **Consent-category / audit configuration** → **privacy-compliance** and **account-and-program**.

## How I answer

The deep engagement content lives in this skill's `references/pii-engagement-playbook.md`. Every engagement walks six phases:

1. **Scope & tier flows** — inventory the flows that submit or render PII; tier by risk (authenticated + payment first, then lead/signup forms, then search/preferences). Deliberately not "50 journeys" — maintenance is a scoping input.
2. **Seed** — generate one **canary persona per flow** with `scripts/canary_persona.py` (unique-after-normalization name / E.164 phone / address / account id; per-flow email uniqueness only when inbox sub-addressing is confirmed). Provision **one** `PII-CANARY` inbox for the account (reuse if it exists — never create a second); the default `shared` email mode uses that one address for every flow, with attribution resting on the distinct name/phone. The playbook has the guardrail and the sub-addressing option.
3. **Build** — a journey per flow that types the persona's values, through automation-and-testing's selector-evidence gate. Size the trailing `waitDuration` to the longest expected delayed egress, or late beacons/`sendBeacon` calls are missed (verified 2026-07-14).
4. **Analyze** — `scan_journey_pii` (JSON mode) over each run. It catches the canary **and its hashed/encoded forms** — a SHA-256/percent/base64 hit is *stronger* evidence than plaintext, because it proves active identity-resolution processing (Meta CAPI / Google Enhanced Conversions style). Use `knownValues` to trace a masked field's plaintext or a logged-in test account's server-rendered profile — but only in captured surfaces (requests/cookies/tag variables); server-rendered DOM no tag consumes is invisible, so a no-hit is not proof of absence. Check the inbox for received mail (independent propagation proof), and run `scan_audit_pii` + the cookie/request privacy reports site-wide.
5. **Deliver** — a masked verdict (what leaked, to which third party, in which form) with a coverage matrix that names what could NOT be inspected (opaque payloads, masked fields, uncaptured surfaces). Never let an incomplete scan read as clean.
6. **Leave behind** — schedule the canary journeys + the audits, keep the inbox listening, and use Rules ONLY for presence assertions (consent tag present, GPC honored). Rules cannot detect an unwanted occurrence — standing PII detection is scheduled journeys + periodic re-scan + inbox canaries, not an inverted rule.

## MCP tools I use

When `mcp__ObservePoint__*` tools are loaded (requires the ObservePoint connector ≥ v0.6.70 for `knownValues` + `format:"json"` + variant catching):

- `mcp__ObservePoint__scan_journey_pii` — the core: canary + known-value + hashed/encoded-variant PII tracing over a journey run, masked, with a `format:"json"` evidence mode.
- `mcp__ObservePoint__scan_audit_pii` — the site-wide regex + OP-IP counterpart (no canary — audits type nothing).
- `mcp__ObservePoint__create_journey` / `update_journey_actions` / `run_journey` — build and run the canary journeys (through automation-and-testing's evidence gate).
- `mcp__ObservePoint__list_email_inboxes` / `create_email_inbox` / `get_email_inbox_messages` — provision the ONE canary inbox and read received-mail propagation proof.
- `mcp__ObservePoint__get_request_privacy_report` / `get_cookie_privacy_report` / `compare_consent_states` — audit-side consent/party context.

If no `mcp__ObservePoint__*` tools are loaded, the user doesn't have MCP access — fall back to the REST recipes (see **automation-and-testing** and the shared `references/mcp-tools.md`). Never invent a tool name; only call tools that actually appear.

## Shared foundation

These live in the meta-skill and stay linked by their plain `references/` filename:

- `references/mcp-tools.md` — the MCP tool catalog + REST fallback.
- `references/limitations.md` — what the scanner cannot see (server-side tags, synthetic browsers, native mobile) — name these before a customer is surprised.
- `references/solution-playbooks.md` — the end-to-end recipes this engagement draws on.

## What I can't do

- **Prove absence.** A no-hit means the value didn't reach a captured surface in this run — not that the site never leaks it. Server-rendered DOM, opaque payloads, and server-side tags are blind spots I name explicitly.
- **Handle raw PII.** All findings are masked; a hashed-variant hit is reported as its form, never the hash itself.
- **Replace counsel or a privacy assessment.** I produce technical leak evidence; whether it's a violation is privacy-compliance / litigation-defense / the customer's lawyers.
- **Build the journeys' selectors for you.** The journey mechanics + the live-DOM evidence gate are automation-and-testing's job; I decide what to seed and how to read the result.

*Last verified: 2026-07-14*
