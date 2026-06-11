# Account configuration — how to set up and structure an ObservePoint account

Load this when the user is asking *how to build the account*: how to organize audits into folders, what to name things, how to design the rule library and consent categories, where alerts should route, how often audits should run, and how to stand up the configuration that addresses a specific regulation or use case. This is the *set-up-and-structure* layer — distinct from *what the law requires or whether consent works* (the `privacy-compliance` skill), *what to focus on next* (the program health section of the `account-and-program` skill).

The discipline that defines this skill: I describe the blueprint and the click-path; the human applies it. Every tool named below is a real wrapper verified in the shared `references/mcp-tools.md`, and the config is only as good as the evidence the audits then produce — a tidy folder tree with no Rules attached governs nothing.

## Contents

1. [Best-practice account structure](#1-best-practice-account-structure)
2. [Naming and label strategy](#2-naming-and-label-strategy)
3. [Rule-library design](#3-rule-library-design)
4. [Consent-category design](#4-consent-category-design)
5. [Alert routing](#5-alert-routing)
6. [Schedule cadence](#6-schedule-cadence)
7. [Regulation → configuration mapping](#7-regulation--configuration-mapping)
8. [The admin/config MCP tools](#8-the-adminconfig-mcp-tools)
9. [The config_blueprint.py workflow](#9-the-config_blueprintpy-workflow)
10. [WHEN/EXPECT examples](#10-whenexpect-examples)

## 1. Best-practice account structure

An account that scales is organized before it is populated. The taxonomy is a two-level tree plus a cross-cutting label layer:

- **Folders** are the top-level organization — usually one per **business unit, brand, or region** (`Retail-NA`, `EU-Properties`, `Corporate`). A folder is the unit a CSM or admin hands to a team; keep it coarse. Create with `create_folder`, list with `list_folders`.
- **Sub-folders** group at the **domain or property** level inside a folder (`Retail-NA → shop.example.com`, `Retail-NA → checkout.example.com`). One sub-folder per domain keeps a property's audits, journeys, and reports together. Create with `create_subfolder`, list with `list_subfolders`.
- **Audits** live in the relevant sub-folder. The default shape is **one audit per (property × consent-state × purpose)** — a `shop.example.com` property under a CCPA mandate becomes three audits (Default / Opt-Out / GPC), not one. Resist the single mega-audit: it makes the consent-state diff impossible and buries per-purpose Rules.

A worked tree for a two-brand retailer under a CCPA mandate:

```
Retail-NA  (folder)
├── shop.example.com  (sub-folder)
│   ├── shop.example.com — Default Audit
│   ├── shop.example.com — Opt-Out Audit
│   └── shop.example.com — GPC Audit
└── checkout.example.com  (sub-folder)
    ├── checkout.example.com — Conversion Validation [Accept-All]
    └── checkout.example.com — Release Gate
EU-Properties  (folder)
└── eu.example.com  (sub-folder)
    ├── eu.example.com — Accept All Audit
    └── eu.example.com — Reject All Audit
```

The structural anti-patterns to catch on a health review: a flat account with no folders and 40 audits named by date; one audit crawling three domains so no per-domain owner can be assigned; consent-state audits that aren't paired, so `compare_consent_states` has nothing to diff.

**Folder vs. label — when to use which.** A folder answers *who owns this and where does it live* (one home per audit, hierarchical, coarse). A label answers *what cross-cutting thing is this* (many per audit, flat, spans folders). If you find yourself wanting two folders for the same audit ("it's both a `checkout` property and a `release-gate`"), the second axis is a label. Decide the tree before creating the first audit — re-parenting audits later is possible but error-prone, and saved reports, schedules, and labels that referenced the old location have to be reconciled by hand.

## 2. Naming and label strategy

Names are queried as substrings (`list_audits(search=...)`), so a disciplined naming convention is itself a feature. The convention that holds up:

```
<property> — <purpose> [<consent-state>]
shop.example.com — Conversion Validation [Accept-All]
shop.example.com — Privacy Sweep [Opt-Out]
checkout.example.com — Release Gate
```

`compare_consent_states` recognizes the `default` / `opt-out` / `gpc` state names that `setup_compliance_monitoring` emits — keep those exact state words in consent-audit names so the diff auto-discovers its pairs.

**Labels** (`create_label`, `list_labels`, `set_audit_labels`, `get_audit_labels`) are the cross-cutting axis that folders can't express, because a label spans folders. Design a small, controlled label vocabulary up front rather than letting it sprawl:

- **Lifecycle:** `prod`, `staging`, `release-gate`.
- **Regulation:** `ccpa`, `gdpr`, `hipaa` — so a privacy lead can pull every regulated audit across every brand in one filter.
- **Priority:** `tier-1` for revenue-critical properties whose alerts page someone.

A label vocabulary of a dozen controlled terms is governable; thirty free-text labels is noise. Labels also carry to journeys and saved reports (`add_journey_label`, `set_saved_report_labels`), so the same axis filters every entity type.

## 3. Rule-library design

Rules are where the account stops being an inventory and starts being governance. Design the **library** centrally, then attach Rules to audits — don't hand-author the same Rule on every audit.

- **Author and version Rules centrally** with `create_rule` / `update_rule`; list the library with `list_rules`. A Rule is a reusable definition; `find_rule_references` shows which audits and journeys use it before you change or `delete_rule` one.
- **Attach** the right Rules to each audit with `update_audit_rules` (read the current set with `get_audit_rules`). This is the step people forget — a Rule in the library that's attached to nothing governs nothing.
- **Theme the library** so coverage is legible:
  - *Presence* — the analytics/consent tag that **must** fire on every page (catches the tag that silently stopped).
  - *Absence* — the advertising/sale-share pixel that **must not** fire under opt-out (the consent-leak Rule).
  - *Variable correctness* — `purchase` carries a numeric `value > 0`, the account ID matches the property, the data-layer key is populated.
  - *Hygiene* — no duplicate/double-firing of a conversion tag, no tag firing before CMP interaction.

A repeatable library-build sequence: `list_rules` to see what already exists (don't duplicate), `create_rule` for each missing themed Rule, `find_rule_references` before editing a shared one to see its blast radius, then `get_audit_rules` → `update_audit_rules` per audit to attach the right subset. The Opt-Out audit gets the *absence* Rules; the conversion audit gets the *variable-correctness* Rules; every audit gets the relevant *presence* and *hygiene* Rules.

Build the WHEN/EXPECT mechanics with the `tag-and-analytics-quality` skill, which owns Rule authoring; this skill owns *which* Rules belong in the library and *which audits* they attach to. Examples in section 10.

## 4. Consent-category design

A consent category is the named bucket ObservePoint maps tags and cookies into so an audit can ask "did anything outside *Strictly Necessary* fire under opt-out?" Design them to mirror the CMP's own taxonomy:

- **Mirror the CMP, don't invent.** If OneTrust publishes Strictly Necessary / Performance / Functional / Targeting, build those exact categories so the audit's verdict speaks the CMP's language. Create with `create_consent_category`; manage with `update_consent_category` / `delete_consent_category`; list with `list_consent_categories`.
- **Populate the buckets.** Add the tags, cookies, request domains, and labels that belong to each category with `add_consent_category_tags`, `add_consent_category_cookies`, `add_consent_category_request_domains`, and `add_consent_category_labels` (each has a `remove_*` counterpart).
- **OneTrust shortcut.** Import the CMP's categories instead of hand-building them: `start_onetrust_consent_category_import`, then `poll_onetrust_consent_category_import`, then `sync_onetrust_consent_categories` keeps them current. This is the two-step import pattern the server encodes — don't fake a one-shot.
- **Attach to audits.** `set_audit_consent_categories` (or `add_` / `remove_audit_consent_categories`) decides which categories an audit evaluates. **The hard rule:** the Opt-Out and GPC audits get **Strictly Necessary only** — never assign a non-essential category to them, or the opt-out diff is meaningless. The Default/Accept-All audit gets all categories.

## 5. Alert routing

An audit that catches a break in silence isn't governance. Routing is the difference between a same-day fix and a quarter-end surprise.

- **Create alerts** with `create_alert` (manage with `update_alert` / `delete_alert`, list with `list_alerts`). `get_alert_metric_types` lists which metrics support an alert before you author one.
- **Route by severity, not volume.** A `tier-1` property's broken-purchase Rule pages the analytics owner; a low-priority hygiene finding emails a weekly digest. Routing everything to one channel trains the team to ignore it.
- **Own every alert.** Each alert names a destination that maps to a human or a team channel (Slack `#analytics-alerts`, a Jira project, an email list) — see `references/integrations.md` for the connector side. An alert with no owner is noise.
- **Run-level alerts** surface per run via `get_run_alerts`; the alert *definitions* are the standing config you set up here.

## 6. Schedule cadence

Cadence is a configuration decision with a cost/coverage trade-off. Match it to the property's volatility and role:

| Property role | Cadence | Why |
|---|---|---|
| Release-gate / staging | per deploy (triggered) | catch the regression before it ships |
| Tier-1 revenue / consent-critical | daily | a broken purchase event or consent leak can't sit a week |
| Standard production | weekly | the default for most properties |
| Stable / low-change | monthly | inventory + drift check without burning runs |

Build the schedule with `build_schedule`, never a hand-written RRULE — it validates the timezone, normalizes the recurrence, and warns when the timezone's recommended datacenter disagrees with the audit's location. Drop its output into `create_audit` / `update_audit`. `list_schedule_presets` gives the canonical preset names (`weekly`, `business-days`, `monthly`); `get_audit_frequencies` gives the allowed values; `get_schedule_calendar` shows the resulting run calendar so two heavy audits don't collide on the same morning.

## 7. Regulation → configuration mapping

This is where a legal mandate becomes an account shape. The legal *why* lives in the `privacy-compliance` skill (which laws apply, what they require, how ObservePoint evidences them, and whether the consent banner works); this section is the *what to build*. `config_blueprint.py` (section 9) emits these as JSON.

- **CCPA / CPRA → three audits.** Default (baseline, all categories) + Opt-Out (pre-audit CMP Reject-All, Strictly Necessary only) + GPC (`gpcEnabled` + `blockThirdPartyCookies`, Strictly Necessary only). Use `setup_compliance_monitoring(regulation="ccpa", domain=...)` — it creates all three with the correct pre-audit actions and consent assignments in one call. Rules: no advertising/sale-share pixels under opt-out, GPC honored. Never assign a non-essential category to the Opt-Out or GPC audit.
- **GDPR / ePrivacy → reject-all pair.** Accept-All (baseline) + Reject-All (Strictly Necessary only, the core evidence). The Reject-All audit proves no non-essential tag fired before consent — that's the finding regulators ask for. Rules: no non-essential tags pre-consent, vendor inventory, cookie classification.
- **HIPAA → PHI-URL audit.** A single audit scoped to patient-facing URL patterns, paired with `scan_audit_pii` on those URLs daily. Rules: no advertising tag on PHI URLs, portal CMP suppression. The finding here is an ad pixel on an authenticated health page, which is a far bigger problem than the same pixel on a marketing page.

For the consent-state mechanics — pre-audit `privacyoptout` actions, `blockThirdPartyCookies`, and whether the diff actually proves blocking — defer to the `privacy-compliance` skill. This skill stands up the audits; that skill proves they catch what they're supposed to.

## 8. The admin/config MCP tools

When `mcp__ObservePoint__*` tools are loaded, prefer the typed wrappers over `op_api_call` — they encode the schedule sanitization, two-step CMP import, and consent-assignment safety gates. All verified in `references/mcp-tools.md`; if no `mcp__ObservePoint__*` tools are present, the same setup is the UI click-path, with REST recipes in the `api-strategy` skill. Never invent a tool name.

**Identity and impersonation (admin/CSM):**

- `whoami` — confirm which account/identity the session is acting as **before** you configure anything. Always the first call when impersonation is in play.
- `find_account` — locate a customer account by name/URL.
- `login_as_account` — impersonate into that account to configure on the customer's behalf.
- `stop_impersonation` — return to your own identity when done. Pair every `login_as_account` with this.
- `get_account` — account-level info, plan tier, usage caps (does the plan allow the audit count this blueprint implies?).

**Structure and config wrappers** (covered in their sections above): `create_folder` / `create_subfolder`, `create_label` / `set_audit_labels`, `create_audit` / `update_audit`, `create_rule` / `update_audit_rules`, `create_consent_category` / `set_audit_consent_categories`, `create_alert`, `build_schedule`, and the one-shot `setup_compliance_monitoring`.

The disciplined sequence: `whoami` → (`find_account` → `login_as_account` if CSM) → `get_account` to confirm the plan → build the structure → attach Rules and consent categories → schedule → route alerts → `stop_impersonation`.

## 9. The config_blueprint.py workflow

`scripts/config_blueprint.py` is a deterministic lookup that emits the audit / consent-category / rule-theme blueprint for a regulation as JSON. It is **advisory** — it tells you what to build; the human applies it via `setup_compliance_monitoring`, the config wrappers, or the UI.

```bash
python3 scripts/config_blueprint.py ccpa
python3 scripts/config_blueprint.py gdpr example.com
```

Known regulations: `ccpa`, `gdpr`, `hipaa`. An unknown regulation exits non-zero with the known list, so a typo fails loudly rather than producing a wrong plan. The CCPA blueprint's own `note` points back at `setup_compliance_monitoring` for the one-call build. Run it at the **start** of a configuration conversation to anchor on the right shape, then translate the JSON into wrapper calls. It does not touch the account — it never creates anything.

## 10. WHEN/EXPECT examples

The Rule mechanics belong to the `tag-and-analytics-quality` skill; these show the *shape* of the Rules a well-structured account's library carries, themed per section 3.

- **Presence on a tier-1 property.** `WHEN page matches "shop.example.com/*"` → `EXPECT tag "Google Analytics 4" present`. Attach to the Default audit; alert routes to `#analytics-alerts`. Catches the analytics tag that silently stopped firing.
- **Absence under opt-out (the consent-leak Rule).** `WHEN audit = "Opt-Out"` → `EXPECT tag "Meta Pixel" NOT present`. Attach to the Opt-Out audit only. A Meta Pixel surviving Reject-All is the leak the CCPA mandate exists to catch.
- **Variable correctness.** `WHEN tag = "Google Analytics 4" AND event = "purchase"` → `EXPECT ecommerce.value is numeric AND > 0`. Attach to the conversion-validation audit on the checkout property; daily cadence.
- **PHI hygiene (HIPAA).** `WHEN page matches "/patient/*"` → `EXPECT no advertising-category tag present`. Attach to the PHI-URL audit; pair with a daily `scan_audit_pii` and a `tier-1` alert.

Each example names the audit it attaches to, the consent state it assumes, and the alert that fires — that triad is what turns a Rule from a definition into governance.

## Putting it together — a configuration walkthrough

The end-to-end shape for "set up `shop.example.com` for CCPA," as a CSM configuring on the customer's behalf:

1. **Confirm identity and plan.** `whoami`; if impersonating, `find_account` → `login_as_account` → `whoami` again to confirm. `get_account` to check the plan allows three new audits.
2. **Anchor on the blueprint.** `python3 scripts/config_blueprint.py ccpa shop.example.com` — the JSON names the three audits, the Strictly-Necessary-only consent rule for Opt-Out/GPC, and the rule themes.
3. **Build the structure.** `create_folder("Retail-NA")` → `create_subfolder` for `shop.example.com`.
4. **Create the audits.** `setup_compliance_monitoring(regulation="ccpa", domain="shop.example.com")` builds all three with the correct pre-audit actions and consent assignments in one call — preferred over three hand-built `create_audit` calls.
5. **Mirror consent categories.** Import from the CMP if it's OneTrust (`start_onetrust_consent_category_import` → `poll_…` → `sync_…`); otherwise `create_consent_category` per CMP bucket, then confirm `set_audit_consent_categories` left only Strictly Necessary on Opt-Out and GPC.
6. **Attach the rule library.** `create_rule` for each missing themed Rule, `update_audit_rules` to attach the absence Rules to Opt-Out and the presence/correctness Rules to Default.
7. **Schedule and route.** `build_schedule(presetName="daily", …)` → `update_audit`; `create_alert` routing the consent-leak Rule to `#privacy-alerts`.
8. **Label and hand off.** `set_audit_labels` with `ccpa` + `tier-1`; `stop_impersonation`.

Without MCP this is the same sequence as a UI click-path; the REST equivalents live in the `api-strategy` skill.

---

*Last verified: 2026-06-04*
