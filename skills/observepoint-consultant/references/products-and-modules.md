# Products & modules

The canonical map of every ObservePoint product and module: what it does, when to use it, and how it fits with the rest of the platform. When a user asks "what is X?" or "which product solves Y?", load this file first.

## At a glance

ObservePoint is a **web governance platform** — an automated browser-based scanner that audits, validates, and monitors websites for analytics accuracy, privacy compliance, accessibility, and operational health. Everything in the platform shares one engine (a real Chromium browser running scripted page loads and interactions) and one rules system.

The product family breaks into two layers:

1. **Scanners** — the things that visit your website and produce data: Web Audits, Journeys, the Tag & Cookie Debugger, the HAR Analyzer, and LiveConnect.
2. **Insights** — the things that interpret that data: Rules, Alerts, Reports, and Page Insights.

Touchpoints, JourneyStream, and Prism — acquired from Strala in February 2020 — sit alongside as a separate measurement and attribution layer.

## Scanners

### Web Audits

The core scanner. A Web Audit crawls a list of URLs (or a domain, sitemap, or starting page with link-following) using a synthetic Chromium browser. For each page visited, the engine captures:

- Every network request (tags, pixels, beacons, third-party scripts)
- Every cookie set
- The full data layer at load time and after a configurable wait
- Console errors, page-load timing, status codes
- Visible HTML structure for accessibility checks

A Web Audit can be:

- One-shot or scheduled (hourly, daily, weekly, monthly, custom cron)
- Run with any user-agent string (so you can test mobile-web rendering by impersonating an iOS Safari UA, for example)
- Bound to one or more **consent states** (test "accept all," "reject all," and the GPC signal as separate audit variants)
- Geo-routed (test from US, EU, etc. — handy for region-targeted content and consent banners)
- Behind login (configure a login flow that runs once before the crawl)

Web Audits are the right choice for **most things**. If the question is "what is happening on this set of pages?", start here.

### Journeys

A Journey is a scripted multi-step user flow — click here, type here, scroll there, submit this form — that the synthetic browser replays. Journeys are how you validate:

- Add-to-cart and checkout flows
- Lead-gen and signup forms
- Login-gated content
- Multi-step funnels where tag firing depends on what the user did

Compared to a Web Audit, a Journey is:

- More expensive per run (slower, harder to schedule frequently)
- More fragile (selectors break when the page changes)
- Required for any Single-Page App or any flow where state matters

**Single-page apps need the `Prevent Navigation` flag.** Without it, the Journey engine treats client-side route changes as page reloads and misses tag firing.

### Tag & Cookie Debugger (Chrome extension)

A free Chrome extension. Installs in any analyst's browser and shows, on whatever page they're viewing right now:

- Every tag and pixel firing, with the request details
- Every cookie being set, including the new Cookie Report (October 2025) with consent classification
- Data layer state
- Accessibility highlights (added in early 2026)

The Debugger is the analyst's daily tool — it's the in-browser version of what the cloud platform does at scale. Use it for live debugging; don't try to use it for compliance reporting.

### HAR Analyzer

Upload a HAR file (HTTP archive — the standard export from Chrome DevTools, Charles, Fiddler, or any modern proxy) and the HAR Analyzer runs your Tag & Variable Rules against the captured requests.

Use cases:

- Audit a mobile app's network traffic (capture the HAR from the device, then process it — this is the supported workaround for the lack of native mobile app testing)
- Audit a partner's site you can't crawl directly
- Audit a single problematic user session a customer sent you

The HAR Analyzer is decoupled from LiveConnect; you can buy and use it standalone.

### LiveConnect

A proxy-based testing harness. Connect a real device — iPhone, Android phone or tablet, Windows or Mac desktop, Apple TV, other OTT devices — to LiveConnect over Wi-Fi, and every request that device makes goes through the proxy where you can see it live.

This is the only way to validate behavior on a **real device** in real-time. The free tier ships 30 sessions per year (modern UI refresh completed 2025).

LiveConnect is for ad-hoc debugging and pre-launch QA. It's not a scheduled-monitoring tool.

## Insights

### Rules engine — "Tag & Variable Rules"

Rules are the heart of validation. A Rule has a `WHEN` condition (tag X fires) and an `EXPECT` condition (and the value Y matches, or doesn't fire when it shouldn't). Concrete examples:

- `WHEN tag = "Google Analytics 4" AND event = "purchase" EXPECT ecommerce.value is numeric AND > 0`
- `WHEN page contains "checkout/confirmation" EXPECT tag "Meta Pixel" fires exactly once`
- `WHEN consent state = "Reject All" EXPECT no third-party advertising tags fire`

Rules can be attached to Web Audits, Journeys, and HAR Analyzer runs. They're how a passing/failing report gets generated.

Rule features worth knowing:

- Templates for common platforms (GA4, GTM, Adobe Analytics, Meta Pixel, etc.)
- Regex matching on variable values
- Multi-variable AND/OR logic
- "Create rule from tag" — discover a tag, click to generate a rule that asserts it
- Audit Rules Report (new in March 2026) — audit-level rule results separate from page-level

### Alerts

A failing Rule can route an alert to:

- Email
- Slack
- Microsoft Teams
- SMS
- Jira (create a ticket)
- Webhook (anywhere else)

Alerts support threshold logic ("only alert if more than 5% of pages fail") and frequency caps ("once per occurrence, not on every recurring run").

### Reports

Each scanner produces a set of reports. The ones you'll work with most:

- **Page Summary** — pages scanned, issues per page
- **Tag & Variable Rules Report** — pass/fail by Rule
- **Audit Rules Report** — new in 2026; audit-level rule results
- **Cookies Privacy Compliance Report** — cookie inventory with consent classification
- **Domains & Geo Privacy Report** — vendor and country data flow
- **Accessibility Report / Accessibility Highlight Report** — WCAG violations, severity-graded (new in 2026)
- **Consents Report** — banner presence and implementation quality across the domain
- **Email Link Validation Report** — broken links in marketing emails
- **Landing Page Performance** — page load, missing elements, tracking completeness

All reports export to CSV; aggregation row functionality landed in March 2026.

### Page Insights

A separate dashboard that ingests real-user telemetry (via a lightweight tag deployed on your site) and surfaces:

- Average page load time
- Duplicate tag requests
- Broken pages
- Most-active pages by traffic

Page Insights complements the synthetic Audit data: Audits tell you what the browser engine sees, Page Insights tells you what your actual visitors are experiencing. Treat Page Insights as **sampled** — it's not a complete population view.

## Strala-acquired measurement layer

In February 2020, ObservePoint acquired Strala Technologies. Three products came over and remain in the platform:

### Touchpoints

Standardizes data across online and offline customer touchpoints and unifies them for attribution analysis. Use it when "did this campaign work?" requires data from sources outside the web (call centers, CRM, point-of-sale) merged with web behavior.

### JourneyStream

Automates campaign-tracking and touchpoint management. Sits between Touchpoints and your campaign tooling.

### Prism

Deep attribution and ROI analysis across marketing channels. Roughly: the analyst-facing reporting layer that consumes Touchpoints + JourneyStream data.

These are less commonly discussed in day-to-day ObservePoint conversations because most customers start with web audits and adopt the measurement layer later.

## Choosing between products

When a user describes a problem, this is the routing heuristic:

| Problem | Use |
|---|---|
| "I want to know what tags fire on my site" | **Web Audit** |
| "Tags don't fire when I add to cart" | **Journey** |
| "Single-page app — tags missing on route change" | **Journey** with `Prevent Navigation` |
| "Help me debug this one weird tag right now" | **Tag & Cookie Debugger** |
| "I have a HAR from the customer; tell me what's wrong" | **HAR Analyzer** |
| "Test on a real iPhone in front of me" | **LiveConnect** |
| "Audit my native iOS app" | Not supported. HAR Analyzer with a HAR captured from the app is the workaround. See `references/limitations.md`. |
| "Watch real-user performance trends" | **Page Insights** |
| "Did this campaign actually drive revenue?" | **Touchpoints / Prism** |
| "Catch a tag firing pre-consent" | **Web Audit** with multiple consent-state variants, plus Rules |
| "Catch broken purchase tracking before the release ships" | **Web Audit or Journey** triggered from CI/CD via the REST API |

## Audit vs. Journey — when each wins

| Dimension | Web Audit | Journey |
|---|---|---|
| Scale (pages per run) | Hundreds to thousands | Tens to low hundreds |
| Frequency | Hourly to monthly, comfortably | Daily/weekly, more cost |
| Coverage | Every page in scope | Only what the script touches |
| User behavior | None — direct URL loads | Full multi-step interaction |
| SPA support | Limited to initial load | Full, with `Prevent Navigation` |
| Login-gated | Yes (configure a login flow once) | Yes (built into the script) |
| Common use | Compliance + inventory + analytics validation across the site | Funnel validation, form testing, event-tracking validation |

Default to Web Audit unless the problem demands user interaction. Pair them when both apply.

## Recent platform additions (2025–2026)

Stay current. Recently shipped:

- **Self-Serve SSO** (March 2026)
- **Bulk OneTrust updates** (March 2026) — apply changes across multiple OneTrust instances
- **Audit Rules Report** (March 2026)
- **Accessibility in the Debugger** (March 2026)
- **New Cookie Report in the Debugger** (October 2025)
- **GPC signal enhancement** (September 2025)
- **Email Link Validation refresh** (June 2025)
- **LiveConnect modern UI refresh + free tier** (2025)
- **Aggregation rows, tooltip and column improvements across all reports** (March 2026)

When the user asks "does ObservePoint have X?", check this list before saying no.

---

*Last verified: 2026-05-28*
