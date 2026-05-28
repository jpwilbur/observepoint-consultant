# What ObservePoint cannot do — and the workaround

A working list of platform limits, with the recommended workaround for each. Load this file FIRST whenever a user asks "can ObservePoint do X?" — knowing the boundary matters more than knowing the capabilities.

The shape of every entry: **what's not supported**, **why**, **the workaround**, and **when to use a different tool entirely**.

## Native mobile app testing

**Not supported.** ObservePoint cannot scan, audit, or run tests against native iOS or Android applications. It is a web platform that drives a synthetic Chromium browser.

**Why.** App traffic is SSL-encrypted, mobile frameworks fragment across Swift, Kotlin, React Native, Flutter, and Xamarin, and reliable automation across the matrix would mean shipping a different product. ObservePoint has stated this is a deliberate boundary, not a roadmap gap.

**Workaround.**

1. Capture a HAR file from the device — Charles Proxy, mitmproxy, or any debugging proxy will export one.
2. Upload that HAR to the **HAR Analyzer** and run your Tag & Variable Rules against the captured requests.
3. For live interactive testing, use **LiveConnect** with the real device on your network. That gives you the request stream live but is ad-hoc, not scheduled.

**When to pick a different tool.** Firebase Test Lab, BrowserStack App Automate, or a vendor like AppsFlyer for in-app attribution. ObservePoint is not the right answer for native-app tracking validation as a scheduled process.

## Server-side tag execution

**Not supported.** ObservePoint cannot run server-side Google Tag Manager (sGTM), conversion APIs (Meta CAPI, Google Enhanced Conversions server-to-server), or any backend tag.

**Why.** The platform observes what a browser sees. Server-side tags fire on your servers, not in the browser.

**Workaround.**

- Observe the **client-side request** that triggers the server-side tag. If your sGTM tag fires when the browser POSTs to `/collect-events`, you can still validate that the browser made that POST, with the right payload, at the right time.
- Pair that with **server logs** — your sGTM endpoint should log every request it processes. ObservePoint validates the browser side; your logs validate the server side. Together they cover the full round-trip.

**When to pick a different tool.** Any backend observability platform (Datadog, New Relic, Honeycomb) is the right place to monitor server-side tags themselves.

## Single-page apps without `Prevent Navigation`

**Partially supported.** A Web Audit will load each URL and capture what happens on that initial load, which is correct. But a Journey that navigates *within* an SPA — clicking a link that changes the route without reloading — will miss subsequent tag firings unless you set the `Prevent Navigation` flag on the action.

**Why.** The Journey engine listens for navigation events. Browser route changes in SPAs aren't navigation events.

**Workaround.** Set `Prevent Navigation = true` on every click action inside an SPA Journey. The Journey engine will then continue treating the page as a single session and capture all tag firings.

Works with Angular, React, Vue, and Svelte equivalently.

## Audits are synthetic browsers, not real users

**Not a real-user view.** A Web Audit runs a synthetic Chromium browser from ObservePoint's infrastructure. That browser has no cookies from prior sessions, no AdBlock extensions, no specific geographic IP unless you geo-route, no user-specific A/B test bucket assignments unless your site sets them deterministically.

**Why.** Repeatable testing requires a clean environment.

**Workaround.**

- For consent and tag-firing correctness, the synthetic view is what you want — it's controlled.
- For real-user trends (load times that ad blockers create, regional variance, blocking by browser extensions), use **Page Insights** with the lightweight tag deployed on your live site.
- For a single user's reported issue, get a HAR from them and use the **HAR Analyzer**.

## Page Insights is sampled

**Not a complete population.** Page Insights pulls real-user telemetry, but it samples — it doesn't capture every visit. Treat its dashboards as trends, not authoritative counts.

**Workaround.** Cross-reference Page Insights trends with your primary analytics tool (GA4, Adobe Analytics) when you need exact numbers. Page Insights tells you direction and magnitude; your analytics tool tells you the exact value.

## Consent Management Platform (CMP) backend logic

**Not directly testable.** ObservePoint cannot reach into a CMP's server logic to validate the rules a privacy team configured. It can only see what the CMP exposes to the browser.

**Workaround.** Validate the **outcome** instead of the configuration: run separate audits with each consent state and assert that the right tags fire (or don't). If "Reject All" is supposed to block all advertising tags, write a Rule that asserts no advertising tags fire on a Reject-All audit. If that Rule passes, the CMP's backend logic worked, end-to-end.

OneTrust, TrustArc, Cookiebot, Didomi, Sourcepoint and other major CMPs are supported this way — see `references/integrations.md`.

## Gated content behind unusual auth

**Limited.** Standard username/password login forms work — configure a login flow in the Audit. CAPTCHA, MFA push, and OAuth redirect-heavy flows are harder.

**Workaround.**

- For MFA, set up a service account with MFA disabled (most enterprises allow this for non-production accounts used by automation).
- For CAPTCHA, ask the vendor for an IP allowlist that exempts ObservePoint's egress IPs.
- For OAuth, persist a session cookie via the login flow and reuse it.

If none of that works, consider running the audit only on the public marketing pages and using a HAR for the gated content.

## Email content rendering

**Not supported.** ObservePoint does not render email HTML in clients like Outlook, Apple Mail, or Gmail. It cannot tell you what an email looks like in Dark Mode in iOS Mail.

**What IS supported: Email Link Validation.** ObservePoint follows every link in an email and validates the destination — broken links, redirect chains, UTM correctness, landing-page tag firing. That's the use case it's built for.

**When to pick a different tool.** Litmus or Email on Acid for rendering across clients.

## Very large single audits

**Soft limit.** A single Web Audit has a default cap (around 100 pages by default; configurable upward with enterprise plans). For huge sites, split into multiple audits by section.

**Workaround.** Define audits per site section — `/shop/*`, `/blog/*`, `/account/*` — and orchestrate them via the REST API. This also makes alerting per section cleaner.

## Real-time blocking of pre-consent tags

**Not in scope.** ObservePoint observes; it does not intervene. It will not, by itself, prevent a tag from firing on your live site before consent.

**Workaround.** Use your CMP and tag manager (OneTrust + GTM, Tealium + Consent Manager, etc.) to do the actual blocking. ObservePoint then validates that the blocking worked. ObservePoint = detective control, CMP/TMS = preventive control.

## Pricing transparency

**Not published.** Pricing is custom and quote-based.

**Workaround.** Refer the customer to their account team or `sales@observepoint.com`. Do not invent or estimate pricing tiers — there's a free trial path at https://app.observepoint.com/sign-up if they want to try without a sales conversation.

## Things people *think* aren't supported but actually are

A handful of common false negatives:

- **Mobile-web testing.** Use a mobile user-agent string and viewport — supported.
- **Multi-region/geo testing.** Route the audit from different IPs — supported.
- **GPC (Global Privacy Control) signal.** Toggle "Send GPC Signal" on the audit — supported, and treated as a separate consent state.
- **Consent Mode v2.** Supported via consent-state audits; validate the Mode v2 categories (`ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`) with Rules.
- **Accessibility scanning.** Supported, with WCAG 2.1 AA coverage and the new Accessibility Highlight Report (2026).
- **SAML/OIDC SSO for the app itself.** Self-Serve SSO shipped in March 2026.

When in doubt, check the recent platform-additions list in `references/products-and-modules.md` before declining a request.

---

*Last verified: 2026-05-28*
