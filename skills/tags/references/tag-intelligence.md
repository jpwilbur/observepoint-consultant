# Tag intelligence — what is this tag, and should it be here?

Load this when the user is holding a tag and asking a *judgment* question: "what is this pixel," "should it be on this page," "is this vendor authorized or risky," or "classify my whole inventory." This is the presence-and-governance layer. It answers identity (what the tag is), classification (which category it belongs to), risk (how much it should worry a governance team), and the should-it-be-here verdict (does this tag belong on *this* page, under *this* consent state, against *this* approved-vendor list).

The distinction that defines this skill: the sibling `martech` skill explains how a platform is *implemented* and `analytics-validation` proves whether its *data is correct*. Tag intelligence sits before both — it tells you what the thing on the wire actually is and whether it has any business being there. The authoritative catalog of tag *definitions* comes live from ObservePoint via `list_tags`; the value added here is the expert judgment layered on top.

## Contents

1. [Classification taxonomy — the nine categories](#1-classification-taxonomy--the-nine-categories)
2. [Risk-tier rubric](#2-risk-tier-rubric)
3. [The "should it be here?" decision procedure](#3-the-should-it-be-here-decision-procedure)
4. [The live catalog — how ObservePoint feeds the judgment](#4-the-live-catalog--how-observepoint-feeds-the-judgment)
5. [The classifier script](#5-the-classifier-script)
6. [Curated vendor reference](#6-curated-vendor-reference)
7. [Boundaries — where to defer](#7-boundaries--where-to-defer)

## 1. Classification taxonomy — the nine categories

Every tag a page fires falls into one of nine buckets. The category drives the risk tier and the governance posture, so classify first, judge second.

- **analytics** — measures behavior for the site's own reporting. GA4, Adobe Analytics, Amplitude, Mixpanel, Heap, Matomo. First-party-intent measurement: the site wants to understand its own traffic. Medium risk because it still collects behavioral data and in consent regimes is rarely "strictly necessary."
- **advertising** — built to target, retarget, or measure paid media, usually by setting third-party identifiers and sending data to an ad network's backend. Meta Pixel, Google Ads / Floodlight, TikTok, Criteo, The Trade Desk, Taboola. The highest-scrutiny category: third-party data sharing, retargeting cookies, the bulk of consent and wiretap-litigation exposure.
- **social** — share buttons, embeds, and the lighter-touch pixels from social platforms whose *primary* purpose on the page is engagement rather than ad-conversion. LinkedIn Insight, X/Twitter widgets, Pinterest tag. Medium risk: many double as advertising pixels, so read intent and destination.
- **session-replay** — records the actual user session: mouse movement, scroll, clicks, keystrokes, and DOM mutations, replayed later. FullStory, Hotjar, Contentsquare, Mouseflow, Glassbox, LogRocket. High risk: it is the canonical target of "interception/wiretap" class actions (CIPA, ECPA, state two-party-consent statutes) and the category most likely to capture PII or payment fields if masking is misconfigured.
- **fingerprinting** — identifies a device/browser without a cookie, by hashing signals (fonts, canvas, WebGL, audio, hardware). FingerprintJS and the device-intelligence/anti-fraud vendors. High risk: built to defeat the user's privacy controls, and explicitly named in several regulatory enforcement actions.
- **tag-manager** — the container that loads other tags rather than collecting data itself. Google Tag Manager, Adobe Launch/Tags, Tealium iQ, Ensighten. Low *intrinsic* risk, high *leverage*: it is the delivery mechanism for everything else, so its governance is where unauthorized tags get in.
- **consent** — the CMP and its machinery: the banner, the preference store, the signal it broadcasts. OneTrust, Cookiebot, TrustArc, Usercentrics, Didomi, Sourcepoint. Low risk and usually *required* to be present — its absence or misconfiguration is the finding, not its presence.
- **functional** — makes the site work: A/B testing and personalization (Optimizely, VWO, Adobe Target), live chat (Intercom, Drift, Zendesk), CDNs, error monitoring (Sentry), payment SDKs. Low-to-medium risk depending on what they collect; judged case by case.
- **unknown** — the classifier could not match a signature, or the tag is a custom/internal/first-party script with no public definition. Treated as high risk *until investigated* — an unknown tag firing on a checkout page is exactly the thing a governance program exists to catch.

## 2. Risk-tier rubric

Risk here means *governance and compliance* exposure, not whether the tag is technically broken. Three tiers:

- **High** — advertising, session-replay, fingerprinting, and (provisionally) unknown. These either share data with third parties, record the user directly, defeat privacy controls, or are unidentified. They carry the bulk of consent-leakage and litigation risk, so they are the categories that *must* be reviewed for authorization, consent gating, and placement.
- **Medium** — analytics and social. They collect behavioral data and frequently ride along with advertising use cases, but their core purpose is measurement/engagement rather than third-party targeting. Review them on sensitive pages and under denial; tolerate them more readily elsewhere.
- **Low** — tag-manager, consent, and most functional tags. These are infrastructure or are required to be present. The finding is usually their *absence*, *misconfiguration*, or *abuse* (e.g. a tag manager loading an unapproved vendor), not their presence.

Risk is a starting posture, not a verdict. A medium-risk analytics tag on a HIPAA-covered patient-portal page is a far bigger problem than a high-risk ad pixel on a public marketing homepage with consent. Page sensitivity and consent state modulate the tier — which is what the decision procedure does next.

## 3. The "should it be here?" decision procedure

"Should this tag be here?" is answered along four axes. Walk them in order; the first hard failure is the answer.

1. **Page type.** What is the page's sensitivity? Public marketing pages tolerate the most; authenticated, health, financial, children's, and checkout/payment pages tolerate the least. A session-replay tag on a marketing page is a review item; the same tag on a logged-in patient portal or a credit-card form is a likely incident.
2. **Consent state.** What did the user choose, and is the tag respecting it? A high- or medium-risk tag that fires *before* the banner is interacted with, or *survives a Reject-All*, is leakage regardless of how legitimate the vendor is. The honest framing: a perfectly authorized vendor firing under denial is still a violation.
3. **Approved-vendor list.** Is this vendor on the customer's sanctioned list for this property/region? A tag with no entry on the approved list is unauthorized by default — most often a marketer-added pixel through the tag manager, or a piggybacked vendor riding inside an approved tag.
4. **Destination domain.** Where is the data actually going? The vendor name on the tag and the host it sends to should agree. A tag labeled as one vendor POSTing to an unrelated ad-network domain is either misclassified or a piggyback — investigate the destination, not just the label.

Worked examples:

- *Meta Pixel on a public homepage, consent accepted, on the approved list, posting to `facebook.com`.* Page type OK, consent OK, authorized, destination matches. **Verdict: belongs.** Keep monitoring that it stays consent-gated.
- *FullStory on a logged-in account-settings page.* High-risk session-replay on an authenticated page that likely renders PII. Even if authorized, the question becomes: is field-masking configured, and is replay consented? **Verdict: review urgently** — high blast radius if masking is off.
- *An unrecognized pixel posting to `criteo.com` from a checkout page, not on the approved list, firing under Reject-All.* Fails three axes at once: sensitive page, unauthorized vendor, consent leakage. **Verdict: does not belong — escalate.** Classic piggyback or rogue marketer tag.
- *OneTrust on every page.* Consent category, required to be present. **Verdict: belongs** — its *absence* would be the finding.

## 4. The live catalog — how ObservePoint feeds the judgment

The judgment above is only as good as the evidence under it. ObservePoint supplies that evidence live (use the `mcp__ObservePoint__*` tools when they are loaded; otherwise the same reads are available from the UI and the REST recipes in the `api-strategy` skill — never invent a tool name). All tools below are verified in the shared `references/mcp-tools.md`.

- **`list_tags`** — the authoritative catalog of tag *definitions*: the vendor library ObservePoint matches network requests against. This is the source of truth for "what is this tag," and it is *live*, so it outranks any static list including the curated reference in section 6. When the catalog and a static guess disagree, the catalog wins.
- **`get_tag_inventory`** — what actually fired, and on which pages, in a given audit run. This is the population the should-it-be-here procedure runs against — the difference between "this vendor is defined" and "this vendor is on the wire here."
- **`get_tag_health`** — uptime and reliability of the tags that should be firing: are the *expected* tags present and stable, the inverse governance question to "is an unexpected tag present."
- **`find_first_observed`** — when a tag was first seen across the audit history. The answer to "when did this vendor appear?" — the trigger for investigating a newly-added, unauthorized, or piggybacked tag.
- **`find_rare_observations`** — low-frequency findings: a tag that fires on a handful of pages out of thousands. Rare presence is a strong signal for a rogue or test pixel that escaped governance.

The pattern: pull the authoritative identity from `list_tags`, the actual presence from `get_tag_inventory`, then apply the section-3 procedure. Use `find_first_observed` and `find_rare_observations` to surface the *new* and the *rare* — the two profiles most likely to be unauthorized.

## 5. The classifier script

`scripts/classify_tag_inventory.py` is a heuristic first pass for triage when you have an inventory export and want a fast category/risk/review breakdown before pulling the live catalog. It is *not* authoritative — `list_tags` and human judgment refine it.

Feed it a JSON list of `{"name", "domain"}` objects, the shape of a `get_tag_inventory` export:

```bash
python3 scripts/classify_tag_inventory.py inventory.json
```

It emits JSON: each tag annotated with `category`, `risk`, and a `review` boolean, plus a `summary` with totals and a per-category count. `review` is set for the categories that always warrant a governance look — advertising, session-replay, fingerprinting, and unknown. Use the `review_count` to size the work and the `by_category` map to spot a surprise (e.g. an `unknown` count higher than expected, or session-replay where none was sanctioned).

Limits to state plainly: it matches on substrings of name and domain, so a renamed or proxied tag (first-party-disguised, CNAME-cloaked) can slip to `unknown`, and a generic word in a vendor's name can over-match. Treat the output as a worklist, not a verdict — confirm every `review` item against `list_tags` and the four-axis procedure.

## 6. Curated vendor reference

The highest-impact and highest-risk vendors, grouped by category, with what each is, its risk tier, and a should-it-be-here note. The live `list_tags` catalog is authoritative and broader than this list; this is the fast human reference for the vendors that come up most. Where a vendor spans categories, it is filed under its dominant governance concern.

### Advertising (high risk)

- **Meta Pixel / Conversions API** (`facebook.net`, `facebook.com`) — Meta's ad-targeting and conversion pixel. The single most litigated tag (healthcare-pixel and wiretap class actions). Must be consent-gated; never on health, financial, or authenticated flows without explicit review of what parameters it carries.
- **Google Ads / gtag conversion** (`googleadservices.com`, `google.com/ads`) — paid-search conversion and remarketing. Belongs where a paid campaign drives traffic; consent-gate it and confirm it isn't on pages outside the campaign scope.
- **Google Floodlight / Campaign Manager 360 / DV360** (`doubleclick.net`, `fls.doubleclick.net`) — DoubleClick display/measurement. High third-party-cookie footprint; expect it only on properties running DCM/DV360 media.
- **Google Display / AdSense** (`googlesyndication.com`) — display ads and remarketing audiences. Often broader than intended; check it isn't blanketing the whole site.
- **The Trade Desk** (`adsrvr.org`) — programmatic DSP, Unified ID 2.0 identity. Heavy third-party identity sync; authorize per property and watch for piggybacked syncs.
- **Criteo** (`criteo.com`, `criteo.net`) — retargeting specialist, aggressive cookie-syncing. A frequent uninvited piggyback; if it appears without an entry on the approved list, investigate the source tag.
- **Taboola** (`taboola.com`) and **Outbrain** (`outbrain.com`) — content-recommendation / native ad networks. Belong on publisher properties running their widgets; surprising elsewhere.
- **TikTok Pixel** (`analytics.tiktok.com`, `tiktok.com`) — conversion and audience pixel. Rising litigation and regulatory scrutiny; consent-gate and keep off sensitive pages.
- **Microsoft Advertising / Bing UET** (`bat.bing.com`) — Microsoft Ads conversion tag. Expect it only where Microsoft Ads media runs.
- **Snap Pixel** (`sc-static.net`, `snapchat.com`) — Snapchat conversion pixel. Same posture as the other social-ad pixels.
- **Amazon Advertising** (`amazon-adsystem.com`) — Amazon DSP/affiliate measurement. Common on retail; confirm it's authorized.
- **Quantcast** (`quantserve.com`), **AppNexus/Xandr** (`adnxs.com`), **PubMatic** (`pubmatic.com`), **Rubicon/Magnite** (`rubiconproject.com`) — ad-exchange / SSP / DMP infrastructure, usually arriving via header bidding on publisher sites. High cookie-sync volume; on a non-publisher site their presence is a flag.
- **Yahoo / Verizon Media DOT** (`analytics.yahoo.com`), **AdRoll** (`adroll.com`), **Bing/Microsoft Clarity** — see Clarity under session-replay; AdRoll is retargeting and belongs only where its campaigns run.

### Analytics (medium risk)

- **Google Analytics 4** (`google-analytics.com`, `analytics.google.com`, `g/collect`) — the default web analytics tag. Belongs nearly everywhere measurement is wanted, but is *not* strictly necessary under most consent regimes, so it must respect consent and IP/identifier settings on sensitive pages.
- **Universal Analytics** (`google-analytics.com/collect`) — the retired GA predecessor. Its presence is now a *finding*: a still-firing UA tag is dead weight and a sign of stale tag-manager config.
- **Adobe Analytics / AppMeasurement** (`*.omtrdc.net`, `*.sc.omtrdc.net`, `2o7.net`) — enterprise analytics, eVars/props/events. Belongs on Adobe-stack properties; the legacy `2o7.net` domain firing is a stale-config flag.
- **Amplitude** (`amplitude.com`, `api.amplitude.com`) — product analytics. Common in product/app surfaces; confirm consent handling on logged-in pages.
- **Mixpanel** (`mixpanel.com`, `api.mixpanel.com`) — product/event analytics. Same posture as Amplitude.
- **Heap** (`heap.io`, `heapanalytics.com`) — autocapture analytics; records broad interaction data automatically, so it edges toward session-replay concerns — review what it captures on sensitive pages.
- **Matomo** (`matomo.cloud`, self-hosted) — privacy-forward, often self-hosted analytics. Lower third-party-sharing concern but still behavioral data.
- **Segment** (`segment.com`, `cdn.segment.io`) — see CDPs; it functions as an analytics ingestion point as well.
- **Pendo** (`pendo.io`), **FullStory analytics**, **Plausible** (`plausible.io`), **Snowplow** (collector domains) — product analytics / privacy-light measurement; judged on what they collect and where data lands.

### Social (medium risk)

- **LinkedIn Insight Tag** (`px.ads.linkedin.com`, `snap.licdn.com`) — B2B conversion and audience tag; effectively an advertising pixel, treat it as one on sensitive pages.
- **X / Twitter Pixel** (`static.ads-twitter.com`, `t.co`) — conversion/audience pixel and widgets. Consent-gate the pixel form.
- **Pinterest Tag** (`pintrk`, `pinterest.com`) — conversion pixel; belongs on commerce sites running Pinterest media.
- **Reddit Pixel** (`redditstatic.com`, `reddit.com`) — conversion pixel; same posture.
- **Facebook/Instagram social widgets** (`facebook.net` SDK, like/share) — distinct from the Meta Pixel; the embed itself still sets cookies and phones home, so it carries consent weight even when it isn't the conversion pixel.

### Session-replay (high risk)

- **FullStory** (`fullstory.com`, `fs.js`) — full DOM/session recording. The category's headline name in litigation. Demands field-masking on any page with PII or payment input, and explicit consent posture; never assume defaults are safe.
- **Hotjar** (`hotjar.com`, `static.hotjar.com`) — heatmaps + session recording. Same masking/consent scrutiny; common but frequently un-reviewed.
- **Contentsquare** (`contentsquare.net`, includes the former Clicktale) — enterprise experience analytics with replay. High capture surface; review masking config.
- **Microsoft Clarity** (`clarity.ms`) — free session replay + heatmaps from Microsoft. Its zero cost means it spreads without governance — a frequent "who added this?" find.
- **Mouseflow** (`mouseflow.com`), **LogRocket** (`logrocket.com`, `lr-ingest`), **Glassbox** (`glassbox` domains), **Quantum Metric** (`quantummetric.com`), **SessionCam / Smartlook** — all session-replay; all require masking review and a consent posture on any sensitive page. LogRocket in particular often sits inside web apps capturing application state.

### Fingerprinting (high risk)

- **FingerprintJS / Fingerprint Pro** (`fpjs.io`, `fpcdn.io`, `api.fpjs.io`) — device-identification by signal hashing, marketed for fraud/anti-bot. Legitimate fraud use exists, but it is built to identify users without consent, so its presence outside an authenticated/fraud-sensitive flow is a strong review item.
- **Device-intelligence / anti-fraud vendors** (Sift, Iovation, ThreatMetrix, Forter, Riskified) — fraud-prevention fingerprinting. Defensible on login/checkout for fraud control; a flag if found on general marketing pages where no fraud use case exists.

### Tag-manager (low intrinsic risk, high leverage)

- **Google Tag Manager** (`googletagmanager.com`, `gtm.js`) — the dominant container. Not a data-collector itself; its governance *is* the control point — an unauthorized tag almost always entered through here. Audit what it loads, not the container.
- **Adobe Launch / Adobe Tags** (`assets.adobedtm.com`) — Adobe's tag manager. Same leverage logic.
- **Tealium iQ** (`tags.tiqcdn.com`) — enterprise TMS with a data layer (UDH). Often the central control plane; its load order governs consent timing.
- **Ensighten** (`nexus.ensighten.com`), **Commanders Act** (`tagcommander`) — enterprise TMS, frequently chosen for consent-gating capability.

### Consent (low risk — absence is the finding)

- **OneTrust** (`cdn.cookielaw.org`, `onetrust.com`, `otSDKStub.js`) — the market-leading CMP. Its presence is expected; the finding is whether it actually *blocks* on Reject-All — that validation belongs to the `consent-cmp` skill.
- **Cookiebot** (`consent.cookiebot.com`, `cookiebot.com`) — CMP with prior-blocking auto-scan. Same posture.
- **TrustArc** (`consent.trustarc.com`), **Usercentrics** (`usercentrics.eu`, `app.usercentrics.eu`), **Didomi** (`sdk.privacy-center.org`, `didomi.io`), **Sourcepoint** (`sourcepoint.com`), **Osano** (`osano.com`), **Quantcast Choice / CMP** (`quantcast.mgr.consensu.org`) — all CMPs. Present-and-correct is the goal; presence alone is not validation.

### Functional (low-to-medium risk — judged case by case)

- **Optimizely** (`optimizely.com`, `cdn.optimizely.com`), **VWO** (`visualwebsiteoptimizer.com`), **Adobe Target** (`tt.omtrdc.net`, `at.js`) — A/B testing and personalization. They mutate the page and can collect behavioral data; review what they store and whether they delay consent-sensitive content.
- **Intercom** (`intercom.io`, `widget.intercom.io`), **Drift** (`drift.com`), **Zendesk / Zopim** (`zopim.com`, `zendesk.com`), **LiveChat** (`livechatinc.com`) — live chat. Functional, but they set cookies and can capture conversation PII; consent posture matters on regulated sites.
- **Sentry** (`sentry.io`, `browser.sentry-cdn.com`), **New Relic** (`nr-data.net`, `js-agent.newrelic.com`), **Datadog RUM** (`datadoghq.com`, `browser-intake`) — error/performance monitoring. Usually defensible as functional, but RUM tools capture interaction and sometimes URL/PII data — review on sensitive pages.
- **Stripe** (`js.stripe.com`), **Braintree / PayPal** (`braintreegateway.com`, `paypal.com`) — payment SDKs. Functional and required on checkout; the concern is *other* tags co-firing on the same payment page, not these.
- **Cloudflare / Akamai / Fastly** edge scripts, **reCAPTCHA** (`google.com/recaptcha`), **Google Maps / Fonts** — infrastructure and utility. Low concern individually; reCAPTCHA and Maps do set Google cookies, so they count toward consent on strict regimes.

### CDPs (medium risk — fan-out is the blind spot)

- **Segment** (`cdn.segment.io`, `api.segment.io`) — the common CDP ingest. ObservePoint sees the one client-side ingest call; the server-side fan-out to downstream destinations is invisible (a `martech` boundary). Govern what it ingests client-side and confirm it respects consent before the call fires.
- **Tealium AudienceStream / EventStream**, **mParticle** (`mparticle.com`), **Adobe Experience Platform Web SDK / Alloy** (`*.edge.adobedc.net`, `alloy.js`), **Rudderstack** (`rudderstack.com`) — CDP/collection layers. Same logic: the client-side collection call is observable, the downstream distribution is not.

## 7. Boundaries — where to defer

This skill answers identity, classification, risk, and should-it-be-here. It hands off when the question changes shape:

- **Implementation** — "how is GA4 / GTM / sGTM / a CAPI actually built, and what can ObservePoint observe of it" → the `martech` skill. Tag intelligence says *what* a tag is; martech says *how* its platform works.
- **Data correctness** — "is the `purchase` event carrying the right value, does this tag fire once on the right page, build me the validation Rules" → the `analytics-validation` skill. Tag intelligence says the tag *belongs*; analytics-validation proves its data is *sound*.
- **Consent wiring** — "does Reject-All actually block this tag, is the OneTrust/Cookiebot banner behaving, is Consent Mode v2 propagating" → the `consent-cmp` skill. Tag intelligence flags that a high-risk tag *must* be consent-gated; consent-cmp proves the gate works.
- **Litigation framing, regulation mapping, scanner limits** — defend a pixel/session-replay claim → the `litigation-defense` skill; map a privacy law to coverage → the `regulation` skill; what the scanner structurally cannot see → the shared `references/limitations.md`.

The shared foundation stays linked by plain filename: `references/mcp-tools.md` (tool catalog + REST fallback), `references/products-and-modules.md` (which module/Rule type covers tag governance), and `references/limitations.md` (the can't-see line — server-side fan-out, synthetic browsers).

---

*Last verified: 2026-06-04*
