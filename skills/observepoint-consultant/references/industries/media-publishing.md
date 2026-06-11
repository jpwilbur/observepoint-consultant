# Industry playbook — media & publishing

Load this when the user is a news organization, digital publisher, streaming/OTT service, broadcaster, or B2B media company, or asks about programmatic ad-revenue protection, TCF/GPP consent-string validity, VPPA litigation exposure on video pages, paywall and subscription conversion tracking, or governing an ad stack that grows and changes faster than anyone can keep up with. The shape follows the retail playbook (context → use cases → regulations → vendors → Rule examples → pitfalls → CSM cadence), but the governing instinct is unique to media: where retail fights *sprawl* and financial services fights *leakage*, media fights *velocity* — an ad stack of dozens of pixels that changes weekly, where a single invalid consent string can break programmatic revenue and a single video pixel can invite a VPPA class action.

## Industry context

A media property is a content surface monetized two ways at once: programmatic advertising and reader/viewer subscriptions. The same article page that earns a fraction of a cent per impression from a header-bidding auction may also carry a paywall that converts a reader into a recurring subscription. Both revenue lines run through the browser, and both depend on tracking that has to be correct *and* consented.

The defining trait of the media stack is **heavy ad-tech**. Where a retailer runs five-plus retargeting pixels, a publisher runs *dozens* — an ad server (Google Ad Manager), a header-bidding wrapper (Prebid) calling out to a long roster of SSPs and DSPs, identity vendors, viewability and verification scripts, plus the analytics and engagement tools. That stack is not static: SSP/DSP partners are added and dropped constantly as the ad-ops team chases yield, often without the page-governance team ever hearing about it. The stack grows and churns by the week, which is exactly why a standing allowlist control matters more here than anywhere else.

The second defining trait is **VPPA exposure**. Any publisher with video content — and nearly all of them have it — sits in the path of the Video Privacy Protection Act litigation wave. A video pixel that ships the title or ID of the clip a reader is watching to Meta or TikTok is the precise fact pattern plaintiffs plead. Media is the epicenter of this wave; the VPPA deep-dive below is the industry-specific heart of this file.

The two revenue lines also pull the consent posture in opposite directions, and that tension is the source of much of the work. Advertising wants pixels to fire — yield depends on demand partners seeing the impression and the audience signal. Subscription and privacy want the minimum that consent allows, especially on the video surface where VPPA risk concentrates. The audit's job is to hold the line precisely where the consent state draws it: every ad pixel gated, the consent string valid before the stack reads it, and the video identifier never leaking — without breaking the programmatic revenue the consent is supposed to enable. Getting that balance right, run over run, as the ad stack churns, is the whole engagement.

## Top use cases

Each maps to a concrete ObservePoint capability.

- **TCF / GPP consent-string validity.** Programmatic revenue depends on a valid IAB consent string reaching the ad stack — an absent, malformed, or stale TC string means SSPs drop the bid or the publisher serves non-personalized ads at a fraction of the rate. Validate that a current-version TC string (and the right GPP sections) is present and well-formed *before* any IAB-vendor pixel fires. This is a revenue-quality use case as much as a compliance one.
- **VPPA litigation-defense readiness on video pages.** Prove that no video-tracking pixel sends the video title, URL, or ID to Meta, TikTok, or another third party without consent. Scope a Web Audit (or Journey, where playback is gated behind a click) to the video-bearing URLs and inspect the pixel payloads with `get_page_requests` and `query_report`. The VPPA deep-dive below is the canonical recipe.
- **Paywall / subscription conversion tracking.** The subscription line is the publisher's most durable revenue, and the conversion event (start-trial, subscribe, upgrade) is the number the growth team optimizes against. Prove it fires exactly once with the plan identifier and value populated — a Journey that hits the paywall and subscribes is the only way to observe an event that exists only after interaction.
- **Ad-stack governance.** Inventory every SSP, DSP, header-bidding partner, and identity vendor, and turn the approved-vendor allowlist into the standing control that flags the next unannounced addition. With dozens of pixels changing weekly, `find_first_observed` dating a newly-appeared ad domain is the difference between catching a rogue partner in a day and finding it in a quarterly review.
- **Recirculation / engagement analytics integrity.** Publishers live on engagement metrics — recirculation, scroll depth, time-on-page, content-recommendation clicks — fed by Chartbeat, Parse.ly, and the analytics platform. A broken or double-firing engagement event corrupts the editorial dashboards that drive content strategy, and because these metrics also inform what content gets commissioned, a silent data-quality break has a longer tail than a one-off reporting glitch. Validate the engagement events fire once and carry the article/section identifiers the editorial team reports on, and use `find_anomalies` to catch a sudden jump or drop in engagement-event volume that signals a tracking break rather than a real audience shift.

## Business-model breakout

The four media business models are not minor variations — they change which revenue line dominates, how much VPPA exposure the property carries, and what the consent stakes are. Pin the model down in the first conversation; it sets the whole audit design.

| | **Ad-supported news** | **Subscription / paywall** | **Streaming / OTT** | **B2B media** |
|---|---|---|---|---|
| **Revenue line** | Almost entirely programmatic advertising — the heaviest ad stack of the four; yield is everything. | Subscription revenue dominates; a lighter ad stack (or ad-free for subscribers) and a metered or hard paywall. | Subscription and/or ad-supported (AVOD/FAST); video is the entire product. | Lead-gen and sponsored content; gated whitepapers and webinars; a lighter ad stack, heavier marketing-automation. |
| **VPPA exposure** | Moderate — embedded video on article pages; exposure scales with how much video is published. | Moderate — video behind or alongside the paywall; the subscriber identity makes re-identification easier, which plaintiffs note. | **Highest** — video *is* the product, every page is a video page, and viewing history is the core data the pixel can leak. | Lower — webinars and product video, but a smaller surface; still real where a gated video ships a pixel. |
| **Consent stakes** | Highest programmatic stakes — an invalid TC string directly cuts ad revenue across the whole property. | Mixed audience (logged-in subscribers + anonymous metered readers) complicates the consent state; the string must be right for both. | Consent must gate ad and measurement pixels on the video surface where VPPA risk concentrates. | EU/cross-border B2B audiences pull in GDPR; the marketing-automation cookies are the consent watch point. |
| **Audit emphasis** | TC/GPP-string validity Rules + the ad-stack allowlist; programmatic-revenue protection. | Paywall-conversion Journey + consent-state coverage for both audience states; subscription-event integrity. | VPPA-pattern Rules on every page + `scan_audit_pii` on the video surface; the strictest video-pixel scrutiny. | Lead-form PII scrutiny + GDPR consent on the gated-content funnel; lighter ad-stack governance. |

For streaming/OTT especially, treat every page as a video page: the VPPA-pattern Rule below is not a subset of the audit, it *is* the audit. For ad-supported news, the TC/GPP-string Rule is the revenue-protection control — an invalid string isn't a compliance footnote, it's lost money on every impression.

## Regulations that hit media hardest

Media's programmatic-ad density and video content put it squarely in the path of both the consent-framework regimes and the video-privacy litigation wave. Do not restate effective dates or enforcement detail here — those live in the **privacy-compliance** skill and the `litigation-defense` skill. The media-specific angle:

- **IAB TCF + GPP.** Not law itself, but the technical contract through which a publisher signals consent to the entire programmatic ad ecosystem. A valid TC string is the precondition for personalized-ad demand; the GPP string carries the U.S. state and global sections. Getting these wrong is both a compliance gap *and* a direct revenue hit, which makes media the vertical where consent-string validity has a dollar figure attached. See the **privacy-compliance** skill, IAB Transparency and Consent Framework (TCF) and IAB Global Privacy Platform (GPP).
- **VPPA — the defining media litigation risk.** The Video Privacy Protection Act is the single most consequential regulation for a publisher with video. The litigation wave targets exactly the publisher fact pattern: a Meta or TikTok pixel on a video page that discloses what the reader watched. This is the media epicenter — route any video-bearing property to the `litigation-defense` skill → VPPA, and see the VPPA deep-dive below.
- **GDPR + ePrivacy (EU/UK).** Any publisher with European readers is in scope, and the ad-tech pixels that drive programmatic revenue are precisely the non-essential trackers ePrivacy requires consent for before they fire. The TCF string is how a European publisher operationalizes this. See the **privacy-compliance** skill, GDPR and ePrivacy Directive.
- **Google Consent Mode v2.** The technical bridge between the consent state and Google Ad Manager / Google's ad demand. A publisher monetizing through Google's stack must propagate Consent Mode v2 signals correctly or the ad and measurement behavior degrades. See the **privacy-compliance** skill, Google Consent Mode v2.
- **CIPA and the wiretap theories.** Session-replay, chat, and engagement-analytics vendors on a media property are targets for the pen-register and wiretap class actions hitting consumer-facing sites — and a media property with comment sections, newsletter sign-ups, and account flows has plenty of interaction surface. See the `litigation-defense` skill → CIPA.

The U.S. comprehensive state privacy laws apply across the property's footprint and feed the GPP string's U.S. sections; route to the **privacy-compliance** skill for the state matrix where the audience reaches it.

What makes the media regulatory surface distinctive is that two of these — the IAB frameworks and VPPA — sit on opposite ends of the same content. The TCF/GPP string is the *enabler* of programmatic revenue; the VPPA exposure is the *liability* attached to the video that revenue runs against. A single video page is therefore both a revenue surface that needs a valid consent string and a litigation surface that needs the video identifier kept off the pixel. The Rules below are built to hold both at once.

## Common vendor patterns

The typical media stack is the densest ad-tech surface of any vertical, by layer:

- **Ad server.** Google Ad Manager (GAM) is the near-universal default — it decides which creative serves in each slot and is the hub the rest of the demand stack feeds. The GAM tags are where the ad-revenue data flow originates.
- **Header bidding.** Prebid.js (client-side, sometimes alongside or replaced by server-side Prebid Server) runs the pre-auction that lets multiple SSPs bid before GAM's ad call. The Prebid configuration is where the SSP/DSP roster actually lives.
- **SSPs and DSPs.** Dozens of supply- and demand-side platforms — Magnite, PubMatic, Index Exchange, OpenX, Xandr, The Trade Desk, and many more — each firing their own pixel and receiving bid-request data. This is where the sprawl concentrates and where the allowlist control earns its keep.
- **CMP.** A consent-management platform that emits the IAB TCF string (and GPP string) — Sourcepoint, OneTrust, Didomi, and Quantcast Choice are common in publishing. The CMP is what the consent-string-validity Rules exercise; confirm it actually emits a current-version, well-formed string *before* the ad stack reads it.
- **Video players and their pixels.** JW Player and Brightcove are the common players; each ships its own analytics and ad pixels, and the video-ad stack (VAST/VPAID tags, often a separate set of SSPs) rides alongside. These pixels are the VPPA watch list — they're the ones positioned to leak the video identifier.
- **Subscription / paywall platforms.** Piano and Zephr are the common entitlement-and-paywall engines; they decide who sees the wall, meter free articles, and fire the subscription conversion events. The conversion-event Rules assert against whatever these emit.
- **Analytics and engagement.** GA4 or Adobe Analytics as the primary platform, plus the publishing-specific engagement tools — Chartbeat and Parse.ly — that the editorial team lives in for recirculation and real-time content performance.
- **Identity and addressability.** With third-party cookies deprecating, publishers increasingly run identity vendors (UID2, RampID/LiveRamp, ID5, publisher-provided IDs) to keep audiences addressable for programmatic demand. These pass identifiers into the bid stream and are a consent-and-PII watch point — confirm they're gated and that they're not propagating a hashed email built from a logged-in subscriber without consent.

**A server-side blind spot.** Header bidding increasingly moves server-side (Prebid Server), and some publishers route the ad and measurement stack through a server-side container to trim the browser surface. That's a genuine performance and governance gain, but it also moves the data flow out of sight of a naive client-side scan — the SSP still receives the bid request, it just leaves from a first-party collection endpoint rather than a visible browser pixel. Audit the collection endpoint and the outbound server-to-vendor requests, not just the browser tags, or a server-side demand path reads as "clean" while the data still flows. Extend the allowlist and consent Rules to cover the server-side endpoint.

For the full module-by-module breakdown of how ObservePoint audits each of these, see `references/products-and-modules.md`.

## Industry-specific Rule examples

Concrete `WHEN / EXPECT` Rules, in the style of `references/solution-playbooks.md`. Attach them to a Web Audit on the relevant URL pattern, or to a Journey step.

**1. A valid TC string is present before any IAB-vendor ad pixel fires.** The programmatic-revenue-protection Rule — an absent or malformed TC string means lost or non-personalized demand on every impression.

```
WHEN page loads AND any IAB-registered ad vendor pixel is about to fire
EXPECT
  an IAB TCF consent string (current TCF version) is present
  the string is well-formed (decodes to a valid TC string, not empty/placeholder)
  the string is set BEFORE the first IAB-vendor ad request leaves the page
```

**2. No video-tracking pixel sends the video title/URL/id to Meta or TikTok without consent.** The VPPA Rule — the single most important Rule for a publisher with video. See the VPPA deep-dive below.

```
WHEN page URL matches /\/video|\/watch|\/play|\/episode/ AND consent state = "default (pre-consent)"
EXPECT
  no request to Meta (facebook.com / connect.facebook.net) contains the video title, URL, or video id
  no request to TikTok (analytics.tiktok.com) contains the video title, URL, or video id
  no advertising pixel fires before consent on the video surface
```

**3. The GPP string sections match the user's actual consent state.** The GPP string carries the U.S. state and global sections; a string whose sections disagree with what the user chose is both a compliance gap and a signal the CMP is misconfigured.

```
WHEN page loads with a GPP string present
EXPECT
  the GPP string contains the section(s) expected for the user's region (e.g., usnat / us-ca)
  the section's opt-out / sale-share flags reflect the actual consent choice
  the GPP string is not stale (matches the current consent selection, not a prior one)
```

**4. Under Reject-All, no advertising or SSP pixel fires.** The consent-enforcement Rule across the whole ad stack — opt-out has to actually stop the programmatic pixels, not just set a cookie.

```
WHEN consent state = "Reject All"
EXPECT
  no tags in category "Advertising" fire
  no SSP / DSP / header-bidding request domain receives data
    (Magnite, PubMatic, Index Exchange, OpenX, The Trade Desk, etc.)
  no video-ad (VAST/VPAID) call leaves the page
```

**5. The paywall / subscription conversion event fires once with plan + value.** The subscription-revenue integrity Rule — a missing plan or value, or a double-fire, corrupts the growth team's conversion reporting.

```
WHEN event = "subscribe" / "start_trial" / "purchase" on the subscription confirmation
EXPECT
  the conversion event fires exactly once
  plan_id (or plan_name) is a non-empty string
  value is numeric AND > 0
  currency matches /^[A-Z]{3}$/
```

**6. A newly-appeared SSP/DSP domain triggers an alert.** The ad-stack-velocity control — the one Rule that keeps a constantly-churning demand roster governable.

```
WHEN find_first_observed reports a request domain first seen in the latest run
  AND the domain is an advertising / SSP / DSP endpoint
EXPECT the domain is on the approved-vendor allowlist; otherwise raise an alert
```

Pair Rule 4 with `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` to produce the side-by-side evidence of exactly which ad pixels leak past the opt-out, and pair Rule 6 with `find_first_observed` to date precisely when an unrecognized SSP/DSP first appeared so it traces to a specific ad-ops change.

These six Rules sort into two homes. Rules 1, 3, 4, and 6 — TC/GPP-string validity, Reject-All enforcement, and the SSP/DSP allowlist watch — are static checks that attach to a standing Web Audit scoped across the article and video page types, run on a schedule so the whole property is covered every run. Rules 2 and 5 — the VPPA video-pixel check and the paywall conversion — depend on interaction (a play click, a metered-wall trigger, a subscribe), so they attach to the Journey in the worked example below. Build both; the Audit gives breadth across thousands of pages, the Journey gives depth through the events that only exist after a reader acts.

**A note on "video page" and "page type."** Rules 2 and 5 key off page type (video page, subscription confirmation), but the audit doesn't know a page is a video page unless something tells it. Target one of two ways: a URL pattern (`/video/`, `/watch/`, `/episode/`) when the site's URLs are clean, or a data-layer value (`page.type = "video"`, `content.hasVideo = true`) when they aren't. Prefer the data-layer value where it exists — URL patterns drift as a CMS is re-templated, and a Rule keyed to a stale pattern silently stops matching, which reads as a pass. Confirm the page-type signal during discovery before writing these.

## VPPA deep-dive — why media is the epicenter

Media is the center of the Video Privacy Protection Act litigation wave, and the reason is structural: a publisher with video content has both halves of the fact pattern plaintiffs plead. There is video content a reader watches, and there is an advertising or analytics pixel — most often the Meta Pixel, sometimes TikTok or Google Analytics — positioned to observe what was watched and send it to a third party that can tie it back to an identity. The statute's core prohibition is the disclosure of a consumer's video-viewing information without the specific, informed consent VPPA requires; the publisher's video page is where that disclosure happens if the pixel is configured to send the video title, URL, or identifier.

**What ObservePoint detects.** This is technical evidence, not legal advice — ObservePoint produces the data; counsel decides what it means for a claim.

- **The video identifier in the pixel payload.** `get_page_requests` on a video page surfaces the full network log, including the exact requests Meta Pixel and TikTok make. If the request URL, query string, or POST body carries the video title, the page URL, or a video id, that is the evidentially-relevant signal. `query_report` against the `network-requests` entity scales the same inspection across every video page in the audit, so the finding is "this pattern appears on 1,400 video pages," not "I checked one."
- **Pre-consent firing.** A Web Audit run in the default (no-consent) state with Rule 2 attached proves whether the video pixel fired *before* consent was given — the central question in a VPPA claim.
- **PII on the video surface.** `scan_audit_pii` (or `scan_journey_pii` where playback is gated behind a click) on the video URLs catches direct user-identifier leakage alongside the video data.
- **Timing.** `find_first_observed` dates when a video pixel first appeared on the video surface — useful when a complaint alleges a specific period.

**Why presence isn't the whole answer.** VPPA demands a specific, informed consent — distinct from a general terms-of-service acceptance — before video-viewing data may be disclosed. That means two things for the audit. First, the relevant question isn't only "did the pixel fire," it's "did the video *identifier* travel in the payload" — a Meta Pixel that fires a generic PageView without the video title or id is a different evidentiary posture than one sending `video_title` as an event parameter, and `get_page_requests` is what tells the two apart. Second, the consent state matters: Rule 2 run pre-consent establishes whether the disclosure happened before any consent at all, which is the strongest version of the plaintiff's fact pattern and the first thing to rule out.

Frame the output as: here is what was firing on the named video pages, here is whether it carried the video identifier, here is the consent state under which it fired, and here is when it first appeared. That is technical evidence for counsel — route the litigation framing, the consent-adequacy question, and the damages analysis to the `litigation-defense` skill → VPPA, which carries the statutory detail and the evidence-pack workflow. ObservePoint produces the record; it does not opine on liability.

## Common pitfalls

The failure modes that recur in media specifically. Each is pitfall → how ObservePoint catches it → the fix.

- **Ad pixels firing before the TC string is set.** *Pitfall:* the ad stack initializes faster than the CMP, so SSP and GAM calls leave the page before a valid TC string exists — the publisher serves non-personalized (low-rate) ads or drops the bid entirely, and it's also a consent violation. *Catch:* Rule 1 fails when an IAB-vendor pixel fires ahead of a well-formed TC string; the request waterfall in `get_page_requests` shows the ordering. *Fix:* gate the ad-stack initialization on the CMP's consent-ready signal (the standard IAB `tcloaded`/`useractioncomplete` event), and re-audit to confirm the string precedes the first ad call.
- **A new header-bidding partner added without governance.** *Pitfall:* ad-ops adds an SSP/DSP to the Prebid config to chase yield and never tells the page-governance team; the new partner's pixel fires, receives bid-request data, and may not be consent-gated. *Catch:* the approved-vendor allowlist Rule (Rule 6) turns each new arrival into an alert; `find_first_observed` dates exactly when the domain first appeared. *Fix:* route every Prebid-config change through the allowlist as a standing control, and confirm the new partner is consent-gated before it stays.
- **Video pixel leaking titles (VPPA).** *Pitfall:* the Meta or TikTok pixel on a video page is configured to send the video title or URL as event metadata, disclosing viewing history to a third party — the exact VPPA fact pattern. *Catch:* `get_page_requests` / `query_report` shows the video identifier in the pixel payload; Rule 2 fails when it appears pre-consent; `scan_audit_pii` catches accompanying identifier leakage. *Fix:* strip the video metadata from the pixel's event parameters (or stop firing the pixel on video pages until consent), and gate it behind explicit video-data consent — re-audit to confirm the identifier no longer escapes.
- **Paywall conversion double-counting.** *Pitfall:* the subscription confirmation re-fires on refresh, or two platforms (the paywall engine and the analytics platform) both report the conversion, inflating subscription numbers in the growth dashboard. *Catch:* the "fires exactly once" guard in Rule 5 fails the instant a second firing appears. *Fix:* add a transaction-id idempotency guard so a refresh doesn't re-send, or suppress the duplicate platform's conversion event; re-run the paywall Journey to confirm a single fire.
- **Consent string present but stale or invalid.** *Pitfall:* a TC or GPP string is on the page — so a shallow check passes — but it's a placeholder, an expired version, or reflects a prior consent choice rather than the current one, so the ad stack reads a string that doesn't match what the user actually chose. *Catch:* Rule 1's well-formedness check and Rule 3's section-matching check fail on a string that's present-but-wrong, where a mere presence check would pass. *Fix:* confirm the CMP regenerates the string on every consent change and emits the current TCF version; re-audit under multiple consent states to confirm the string tracks the choice.

## Worked example — the article-to-subscribe Journey

The conversion and consent Rules above are only as good as the path that exercises them. A Web Audit loads URLs directly; it never plays a video, hits a metered paywall, or completes a subscription, so it can't observe the events that fire *as a result of* reader actions. **Video playback, the paywall trigger, and the subscription event only exist after interaction — which is why the conversion half of this is a Journey, not an Audit.** (For the full Audit-vs-Journey decision, see `references/products-and-modules.md` → "Audit vs. Journey — when each wins.")

Script a single Journey through the canonical reader path and attach Rules step by step:

| Step | Action | Rules that attach | Why here |
|---|---|---|---|
| **1. Article** | Land on an article page in default (no-consent) state | CMP banner present; Rule 1 — valid TC string before any ad pixel; no ad/SSP pixel ahead of the string | Establishes the consent + ad-stack baseline before any interaction. |
| **2. Video play** | Click play on an embedded video | Rule 2 — no video title/URL/id reaches Meta or TikTok pre-consent; `scan_journey_pii` on this step | The VPPA-sensitive moment; the pixel observes the play. |
| **3. Paywall hit** | Read past the metered limit until the wall appears | Paywall fires once; no subscriber PII leaks to a third party; consent state still honored | The metering/entitlement boundary the paywall engine controls. |
| **4. Subscribe** | Complete a subscription (test account) | Rule 5 — `subscribe` event fires exactly once with `plan_id` + `value` + currency | The recurring-revenue conversion the growth team runs on. |

Run the same Journey a second time with the CMP in Reject-All state and attach Rule 4 to every step — that is the consent-leak evidence across the ad stack and the video surface. Use a *test* subscription account, never a real reader's. For the broad-surface complement, run a Web Audit scoped across article / video / paywall page types with Rules 1, 3, and 4 attached so the static checks (TC/GPP-string validity, Reject-All enforcement) cover the whole property while the Journey covers the interactive conversions. For the persona-led version of this recipe (pain → approach → alert routing → success metric), see `references/solution-playbooks.md`.

**Streaming/OTT variation.** For an all-video product, the path collapses to browse → play → (paywall or registration wall) → subscribe, and step 2 is the dominant risk surface rather than one moment among several — every content page is a video page, so the VPPA Rule (2) and the `scan_journey_pii` check on the play step carry most of the weight. Script the Journey through the actual player interaction (the play click, not a direct URL load) so the audit observes the pixel that fires on playback, which is exactly the request a VPPA claim turns on.

**SPA caveat.** Many modern publishing front-ends are single-page apps. Set the `Prevent Navigation` flag on the Journey or the engine treats client-side route changes as reloads and misses the tag firing — see `references/products-and-modules.md` → Journeys.

## Reporting and the evidence artifacts

Two saved-report artifacts carry most of the value for a media account, and both are worth standing up early so the data accumulates before anyone needs it.

**The programmatic consent-health dashboard.** Build a saved report with `create_saved_report` over the article/video audit, scoped to the consent-string Rules (Rules 1 and 3) and the Reject-All Rule (4), so ad-ops can see at a glance, per scheduled run, whether a valid TC string preceded the ad stack on every page type and whether the opt-out actually stopped the SSP/DSP pixels. Use `get_report_schema` (with the `search` parameter) to find the exact column names before building it — don't guess column names. Because an invalid consent string is a direct revenue hit in media, this dashboard is the one ad-ops should open daily during any yield-chasing change: a red TC-string row is lost money on every impression, not a compliance footnote. Pair it with `find_first_observed` so each newly-appeared SSP/DSP domain carries a "first seen" date, turning the ad-stack-velocity question into a lookup.

**The VPPA evidence pack.** For any publisher with video, the recurring privacy/legal ask is "prove no video pixel is leaking what readers watch." Keep the `get_page_requests` / `query_report` output showing whether the video identifier appears in the Meta/TikTok payload, the masked `scan_audit_pii` / `scan_journey_pii` findings for the video surface, the Domains & Geo Privacy Report (`get_request_privacy_report`) for the video pages, and the `compare_consent_states` diffs (default vs. opt-out) on the video subset. `query_report` against the rule-summary lets you pull the pass/fail history for Rule 2 across the period — the run-over-run record that the video-pixel control held — without re-running anything. Bundled, that's the "reasonable practices" record counsel wants if a VPPA demand letter arrives — see the evidence-pack workflow in the `litigation-defense` skill → VPPA.

The point of standing both up early: evidence you didn't collect before the incident can't be back-filled with the same fidelity. In a vertical where one revenue line runs on consent-string validity and the other carries active litigation exposure, the accumulated audit history is the deliverable.

## CSM cadence

The recommended rhythm for a media account, built around the reality that the ad stack changes constantly:

- **Weekly baseline.** Weekly audits across the article / video / paywall page types, with the TC/GPP-string Rules (1, 3), the Reject-All Rule (4), and the VPPA Rule (2) live on every run. Run `find_anomalies` (metric `tags` and `request-domains`) after each run to catch ad-stack drift early — anomaly detection is scope-aware, so a traffic-driven page-count change doesn't masquerade as a tag spike.
- **Pre-deploy on ad-stack changes.** Any change to the Prebid config, the GAM setup, the CMP, or the video-player configuration runs a targeted audit as a release gate before it ships — the ad stack changes far more often than the editorial CMS, so this gate fires often. See the CI/CD release-gate recipe in `references/solution-playbooks.md`.
- **Continuous allowlist watch.** Keep Rule 6 (`find_first_observed` on new SSP/DSP domains) live on every run so an unannounced demand partner surfaces as an alert within a day, not at a quarterly review. This is the single highest-value standing control in media — the ad stack churns faster than any change-management process can track, so the only durable defense is detection that runs every time and flags the delta. Treat a flagged new domain as a question for ad-ops ("did you add this, is it consent-gated, is it on the approved list?"), not an automatic failure; the goal is governance with a paper trail, not blocking yield.
- **Alert routing.** TC/GPP-string-validity and ad-stack-allowlist failures route to **ad-ops** (it's their revenue and their roster); VPPA / video-pixel and consent-leak failures route to **privacy**; paywall-conversion and engagement-analytics failures route to **analytics + the growth team**. Escalate routing around a major ad-stack migration so a broken consent string pages a human same-day rather than waiting for the weekly review.

## Discovery checklist

Before designing anything, nail down the five facts that determine the whole audit shape:

1. **Which business model?** Ad-supported news, subscription/paywall, streaming/OTT, or B2B media — this picks the table row above and sets which revenue line, VPPA exposure, and consent stakes dominate.
2. **How much video, and where does it live?** Embedded clips on article pages, a dedicated video section, or an all-video OTT product — this scopes the VPPA Rule and decides whether video pages are a subset of the audit or the whole of it.
3. **Which CMP, and does it emit TCF and GPP?** The consent-string Rules depend on knowing which CMP is deployed and whether it emits a current-version TC string and the right GPP sections; confirm both early.
4. **What's the ad stack, and who owns Prebid?** Identify the ad server, the header-bidding setup, and the SSP/DSP roster — and who in ad-ops changes the Prebid config — so the allowlist control has a current sanctioned set and a clear owner to route alerts to.
5. **Which paywall/subscription platform, and what's the conversion event?** Piano, Zephr, or a custom entitlement engine — get the conversion event name and the plan/value field spec before writing Rule 5, since the Rules assert against whatever the platform actually emits.

The honest scope boundary to set in the same conversation: ObservePoint validates the *web* surface. The following are out of scope for direct scanning:

- A native iOS/Android news or streaming app — the in-app ad and measurement SDKs don't run in a scannable browser.
- A connected-TV (CTV/OTT) app on a smart-TV or set-top platform, and the server-side ad-insertion (SSAI) and CTV measurement tags (Nielsen/Comscore-style) that ride with it.
- The server-side ad-decisioning back-end and any demand path that never touches the browser.

A HAR captured from the app is the supported workaround for app traffic — see `references/limitations.md`. For a streaming service whose audience is mostly on CTV devices, say this plainly so the customer doesn't expect the web audit to cover the whole viewing surface; the web property is one slice of the measurement story, and the engagement is honest about which slice.

---

*Last verified: 2026-06-04*
