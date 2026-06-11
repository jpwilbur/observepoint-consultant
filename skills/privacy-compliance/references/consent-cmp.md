# Consent & CMP validation — does the consent setup actually work?

Load this when the question is whether a consent setup *works on the wire*, not what the law requires and not how a platform is wired. The recurring trigger shapes: **does Reject-All actually block tracking**, **is Google Consent Mode v2 propagating** from the CMP to the Google tags, **is the CMP banner behaving** (firing a default before tags load, honoring the user's choice), and **are non-essential tags firing before consent**. ObservePoint runs the page in a real Chromium browser under a chosen consent state and reads the result, so it is the truth-source for the does-it-work question that a CMP's own admin console can't answer.

This layer sits between two siblings. The **regulation** skill owns what the law *requires* (GDPR, CCPA, the 19 U.S. state laws, GPC recognition, the TCF/GPP legal frameworks). The **tag-and-analytics-quality** skill owns how the platform is *implemented* (the Consent Mode v2 CMP-to-gtag wiring, the `gcs`/`gcd` parameters, server-side GTM). This file is the *technical validation* in the middle: prove, from the browser, that the banner does what it claims and the consent signal reaches the tags it's supposed to gate.

## Contents

1. [The CMP landscape ObservePoint supports](#1-the-cmp-landscape-observepoint-supports)
2. [The consent-state audit pattern](#2-the-consent-state-audit-pattern)
3. [Consent Mode v2 validation](#3-consent-mode-v2-validation)
4. [Pre-consent firing detection](#4-pre-consent-firing-detection)
5. [OneTrust import / sync](#5-onetrust-import--sync)
6. [Consent-leak triage workflow](#6-consent-leak-triage-workflow)
7. [What this is NOT](#7-what-this-is-not)

## 1. The CMP landscape ObservePoint supports

A consent management platform is the source of truth for a visitor's choice: it renders the banner, records the decision, and signals the tag layer what may fire. The technical validation question is always the same regardless of vendor — *did the choice the banner recorded actually reach the wire?* — but ObservePoint can drive some CMPs automatically, which makes the Reject-All / Accept-All audits far cheaper to run.

**Detecting and enumerating CMPs.**

- `detect_cmp` — given a page, identifies which CMP is present. Use it first when a customer isn't sure what they're running, or to confirm the banner you expect is actually the one deployed (multi-brand sites routinely run different CMPs per property).
- `list_supported_cmps` — returns the CMPs ObservePoint can drive *natively*, i.e. the ones the `privacyoptin` / `privacyoptout` pre-audit actions can accept-all or reject-all without hand-written click selectors. This is the list that decides whether a consent audit is one config flag or a brittle scripted banner-click.

**The CMPs that matter.** OneTrust (the enterprise default, and the one with a dedicated import flow — see section 5); Cookiebot, now part of **Usercentrics** (the merged consent suite common in EU mid-market); TrustArc; Didomi (strong in EU/French-speaking markets, deep TCF integration); and Sourcepoint (publisher-heavy, TCF-native). Always verify the live `list_supported_cmps` output rather than asserting a given CMP is natively drivable — native support is the thing that changes between releases, and the `privacyoptout` shortcut only applies to CMPs on that list.

**Why native support is the load-bearing detail.** When a CMP is natively supported, you drive it with a `privacyoptout` pre-audit action and ObservePoint clicks Reject-All through the CMP's own SDK — stable across banner redesigns. When it isn't, you fall back to a scripted Journey that clicks the banner by selector, which breaks the moment the banner's markup changes. The first question on any consent engagement is therefore: *is this CMP on the supported list, or are we scripting the banner by hand?*

**TCF / GPP-backed CMPs.** Many of these CMPs (Didomi, Sourcepoint, Cookiebot/Usercentrics, OneTrust) implement the IAB **TCF** (Transparency & Consent Framework) string and the **GPP** (Global Privacy Platform) string — the standardized consent payloads vendors read. Those frameworks are *legal/industry constructs*, owned by the **regulation** skill; what matters for validation is that a TCF/GPP CMP encodes the user's choice into a consent string that downstream tags are supposed to honor. ObservePoint's job is unchanged: prove that whatever the CMP encoded actually suppressed the tags on the wire. The consent string is a means; the firing behavior is the test.

## 2. The consent-state audit pattern

This is the core motion of the whole skill. A consent setup can only be validated by *comparing* what fires across consent states — a single audit tells you what fired, but not whether it should have. The pattern is to run the same pages under several consent states and diff them.

**The consent states.**

- **Default** — the page loaded with no interaction (the pre-banner window). Nothing non-essential should fire here.
- **Accept-All** — the user granted everything. This is the permissive baseline: it shows the *full* set of tags the site is capable of firing.
- **Reject-All** — the user refused all non-essential processing. The opt-out audit. Drive it with a `privacyoptout` pre-audit action on a natively supported CMP.
- **GPC** — the Global Privacy Control signal is asserted at the browser level (paired with third-party-cookie blocking). The machine-readable opt-out that 12 of the 19 U.S. state laws mandate honoring; the **regulation** skill owns *which* states require it.

The cleanest one-shot setup is `setup_compliance_monitoring(regulation="ccpa", domain=...)`, which builds the three-audit shape (Default + Opt-Out + GPC) designed for California and reused across most state laws. Never assign non-essential consent categories to the Opt-Out or GPC audits — those audits exist to prove non-essential tags *don't* fire.

**`compare_consent_states` — the core diagnostic.** This is the single most important tool in the skill. It diffs the tag set between two consent-state audits on the same domain and answers the question every privacy team actually has: **what fires on Accept-All but not on Reject-All?** Anything in that delta is a tag that the opt-out was supposed to suppress and didn't — the literal definition of a consent leak.

```
compare_consent_states(domain="example.com", leftState="default", rightState="opt-out")
compare_consent_states(domain="example.com", leftState="default", rightState="gpc")
```

It auto-discovers the audit pair by domain and state name (it recognizes the naming the compliance setup produces), and you can override with explicit audit IDs for finer control. The output *is* the finding: the tags and vendors that survived the opt-out. Back it with `get_cookie_privacy_report` (which cookies were set under each state, categorized by consent compliance) and `get_request_privacy_report` (which vendors and geographies received data under each state) for the cookie-level and vendor-level evidence artifacts.

The discipline: **counting requests is the wrong test.** Under denied consent, well-behaved Google tags still fire — as cookieless pings (section 3). The right test is the *delta in identified tag behavior* between states, which is exactly what `compare_consent_states` surfaces.

**Reject-All vs GPC — why you run both.** They are not redundant. Reject-All exercises the **CMP's own opt-out path** (the user clicked "Reject All" in the banner), proving the banner's reject button is wired through to the tags. GPC exercises a **browser-level signal** asserted before the banner is even touched (paired with third-party-cookie blocking), proving the site detects and honors a machine-readable opt-out a privacy-conscious browser sends automatically. A site can pass Reject-All and fail GPC (it honors the button but ignores the header) or vice versa. For a multi-state U.S. program the GPC audit is effectively mandatory because 12 of the 19 state laws require honoring it — one GPC audit proves the technical signal works for the whole portfolio.

**Antipatterns this audit pattern catches.**

- A tag in the Accept-All / Reject-All delta — the opt-out fired but the tag survived (the canonical leak).
- A tag firing identically under all four states — the consent state has no effect on it at all, so the tag is consent-blind.
- The Reject-All audit passing while the GPC audit fails (or the reverse) — partial opt-out coverage.
- A non-essential consent category mistakenly assigned to the Opt-Out or GPC audit, so the audit "passes" only because it was told the leaking tag was allowed.

## 3. Consent Mode v2 validation

Consent Mode v2 is where a privacy program most often *believes* it's compliant while the wire disagrees. The **tag-and-analytics-quality** skill owns the implementation deep-dive — the CMP-to-gtag wiring, the meaning of every bit in `gcs`/`gcd`, advanced vs basic mode. This section is the *validation companion*: how to prove, from ObservePoint, that the signal propagated from the CMP into the Google tags correctly.

**The four signals to validate.** Consent Mode v2 carries four consent types, and a v2-compliant implementation must set all four:

- **`ad_storage`** — cookies/identifiers for advertising.
- **`analytics_storage`** — cookies/identifiers for analytics.
- **`ad_user_data`** — whether user data may be sent to Google for advertising (new in v2).
- **`ad_personalization`** — whether data may be used for personalization / remarketing (new in v2).

If `ad_user_data` and `ad_personalization` are absent, the implementation is still Consent Mode **v1** — non-compliant for Google advertising features in the EEA. That absence is itself a finding.

**Default vs updated.** A correct implementation sets a **default** consent state *before* any Google tag loads (for EEA users this should be `denied` for the ad/analytics signals), then issues an **update** when the user interacts with the banner. The common failure is a missing or late default, so tags fire under the wrong assumption in the pre-interaction window.

**Cookieless pings under denied.** When a signal is `denied`, advanced-mode Google tags don't go silent — they send **cookieless pings**: requests that set no identifiers and carry no cookies, used for conversion modeling. So "consent is respected" does not mean "no request fires" — it means the request that fires is the cookieless-ping shape with the consent flags signaling denial, *not* a full identified hit. (In basic mode the tags are blocked entirely until consent, so under Reject-All nothing fires at all — know which mode the customer implemented before writing the Rule.)

**Validating propagation from CMP → Google tags.** Run an Accept-All and a Reject-All audit, then read the consent parameters off the resulting Google requests. The `gcs` parameter encodes the granted/denied bits (e.g. `G100` = leading bits denied); the `gcd` parameter is the v2 descriptor carrying the `ad_user_data` / `ad_personalization` state.

```
# Under Reject-All, the Google tag request must signal denial — not a full hit
WHEN page is crawled under the Reject-All (opt-out) consent state
  AND a request fires to "google-analytics.com" OR "googleadservices.com" OR "google.com/pagead"
EXPECT
  the "gcs" parameter encodes ad_storage = denied (e.g. value "G100")
  the "gcd" parameter is present (the v2 descriptor carrying ad_user_data / ad_personalization)
  the request is the cookieless-ping shape — no analytics cookie (_ga / _ga_*) set or sent on it
  (NOT a full identified hit carrying a client_id from a persistent cookie)
```

Then `compare_consent_states(domain, leftState="default", rightState="opt-out")` to surface any Google tag that fires identified on Accept-All but should be cookieless or absent on Reject-All. For basic-mode implementations, invert the expectation: under Reject-All, expect *no* Google request at all.

**Consent Mode v2 antipatterns this catches.**

- No default set before tags load — the CMP only ever calls `update`, so the pre-interaction window ran under Google's implicit assumption instead of a `denied` default.
- The `update` firing too late — a full identified hit goes out *before* the consent update lands.
- Wrong signals on Reject-All — the user rejected, but `gcs`/`gcd` still encode `granted` (the CMP-to-gtag wiring is broken).
- A full identified hit instead of a cookieless ping under denied (advanced mode) — the tag ignored the consent signal.
- The v2 signals missing entirely — `ad_user_data` / `ad_personalization` never set, so the implementation is still v1 and non-compliant for EEA Google advertising.

## 4. Pre-consent firing detection

The single most consequential consent finding: a non-essential tag firing in the **default** window, before the user has interacted with the banner at all. This is the literal regulatory violation under ePrivacy / PECR (consent required *before* a non-essential cookie or tracker fires) and the technical fact behind most consent-leak class actions.

Validate it with a Web Audit running in the **default** state (no consent given), with a Rule asserting that nothing non-essential fires. The only thing that should appear on the wire in this state is the CMP itself.

```
WHEN page is crawled under the default (no-interaction) consent state
EXPECT
  no advertising-category tag fires
  no analytics-category tag fires
  the only tag present is the CMP / consent banner itself
```

The success metric is exact: pass rate on the no-consent variant stays at **100%**. Anything less is a leak. Schedule it daily for high-traffic properties — a single tag-manager publish can introduce a pre-consent tag overnight, and `find_first_observed` will tell you exactly which run it first appeared on. Use `compare_consent_states(domain, leftState="default", rightState="opt-out")` to confirm the default state is at least as strict as the opt-out state (it should be — default is the most restrictive window of all).

## 5. OneTrust import / sync

OneTrust is the enterprise CMP default, and ObservePoint has a dedicated three-step importer that pulls OneTrust's cookie-category definitions into ObservePoint consent categories, so the audits classify cookies the same way OneTrust does. The three steps are deliberately *not* collapsed into one — committing cookie-to-category mappings without showing the user what's about to change is exactly the failure mode the staged flow prevents.

**The three-step flow.**

1. `start_onetrust_consent_category_import` — kicks off the import; returns import-request IDs and the cookies the CMP detected.
2. `poll_onetrust_consent_category_import` — shows what was detected and what will be committed.
3. `sync_onetrust_consent_categories` — performs the create / update / delete commit. It's idempotent: it always writes the full CMP identity, so a re-import updates in place rather than orphaning categories.

**dryRun-first discipline.** Always run the third step with `dryRun: true` first to preview the plan, then again with `dryRun: false` only after the user confirms. The full safety rationale lives in the shared `references/mcp-tools.md` (the OneTrust importer safety-gate note) — the short version is that the dryRun preview is the gate between "here's what I'd change" and actually mutating the customer's consent-category configuration.

For multi-brand or multi-region orgs running OneTrust separately per property, pair the importer with per-instance audits so configuration drift across instances is caught — and validate the *result* with the consent-state audit pattern in section 2. The importer makes ObservePoint's classification match OneTrust's intent; the audits prove OneTrust's intent actually holds on the wire.

**Validating OneTrust category-by-category.** Once the categories are imported, the validation question becomes per-category: does denying a specific OneTrust category actually suppress the cookies and tags mapped to it? OneTrust's standard category IDs (`C0001` Strictly Necessary, `C0002` Performance, `C0003` Functional, `C0004` Targeting, `C0005` Social Media) are the unit of assertion.

```
# When a OneTrust category is denied, its cookies and tags must not appear
WHEN OneTrust category "C0004 — Targeting Cookies" = denied
EXPECT no advertising-category cookie mapped to C0004 is set
WHEN OneTrust category "C0002 — Performance Cookies" = denied
EXPECT no analytics-category tag mapped to C0002 fires
```

Route failures to both the privacy team and the OneTrust admin — a category-mapping failure is usually a OneTrust-side configuration problem (a cookie left unclassified, so it defaults to firing), not a tag-manager problem, and the admin is the one who fixes it.

## 6. Consent-leak triage workflow

When a customer reports "we think something is leaking," run the states top-down so each step narrows the cause:

1. **`detect_cmp`** on a representative page — confirm which CMP is live and that it matches what the customer believes is deployed.
2. **Default audit** — is anything non-essential firing before interaction? If yes, that's the most severe finding (pre-consent leak); fix it first.
3. **`compare_consent_states(leftState="default", rightState="opt-out")`** — what survives Reject-All? Each tag in the delta is a leak candidate.
4. **`compare_consent_states(leftState="default", rightState="gpc")`** — does the GPC path behave the same as the button path? A divergence means partial opt-out coverage.
5. **`get_cookie_privacy_report` + `get_request_privacy_report`** under the failing state — turn the tag-level delta into the cookie-level and vendor-level evidence artifact privacy needs.
6. For Google tags specifically, read `gcs`/`gcd` on the surviving request (section 3) to distinguish a true leak (full identified hit) from an expected cookieless ping.

The order matters: a pre-consent leak (step 2) is a worse finding than a Reject-All leak (step 3), because it fires before the user could have chosen anything at all.

## 7. What this is NOT

This skill is the technical does-it-work layer. Three things it deliberately does not own:

- **The legal requirement.** Whether your site *must* honor GPC in a given state, what counts as a "sale" or "share," which consent basis a regulation demands, the TCF/GPP legal frameworks — that's the **regulation** skill. This skill proves the technical signal works; the regulation skill says whether the law required it.
- **The platform implementation architecture.** How the CMP is wired to the Google tags, what each bit of `gcs`/`gcd` means, advanced vs basic Consent Mode, server-side GTM consent propagation — that's the **tag-and-analytics-quality** skill. This skill validates the *output*; tag-and-analytics-quality explains the *wiring*.
- **Whether a vendor is authorized to be there at all.** "Should this pixel exist on this page, is this vendor on our allowlist" — that's the tag-governance question. This skill asks whether a tag *respects consent*, not whether it's *supposed to be present*.

And the standard ObservePoint boundary applies throughout: ObservePoint sees the browser, and only the browser. It reads the consent signal the CMP put on the wire and the tag behavior that resulted — it cannot read the CMP's internal consent-record database, and it cannot confirm what a server-side container did with a consent signal after the client-to-server hop. Pair it with the CMP's own logs and the vendors' debug tools for the server side.

*Last verified: 2026-06-04*
