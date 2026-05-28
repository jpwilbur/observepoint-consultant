# Glossary

Terms used across ObservePoint, web governance, privacy, and the wider MarTech stack. Load this when the user uses a term you're not sure about, or when an answer needs a quick definition.

Alphabetical. Cross-references in **bold**.

## A

**Accessibility Highlight Report.** An ObservePoint report (new in 2026) that surfaces WCAG 2.1 AA violations by severity and type. Companion to the broader Accessibility Report.

**Audit.** In ObservePoint specifically, a **Web Audit** — a configured scan of a defined set of URLs by the synthetic Chromium engine. See `references/products-and-modules.md` → Web Audits.

**Alert.** A notification routed when a Rule fails or a threshold is crossed. Routes to Slack, Microsoft Teams, email, SMS, Jira, or a custom webhook.

## B

**BAA (Business Associate Agreement).** A HIPAA-specific contract between a covered entity and a vendor that handles PHI. ObservePoint generally avoids being a Business Associate by not handling patient data directly.

**Beacon.** A small image or request used to transmit tracking data. Often used synonymously with "pixel."

## C

**CCPA (California Consumer Privacy Act).** The California privacy law. **CPRA** is its amendment effective from 2023, expanding scope.

**CMP (Consent Management Platform).** The system that captures user consent and signals it to tags. Examples: OneTrust, Cookiebot, TrustArc, Didomi, Sourcepoint.

**Consent Mode v2.** Google's consent signaling mechanism. Four categories: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`. Used by Google tags to determine how to behave under various consent states.

**Cookie.** A small piece of state stored in the browser. Subject to privacy regulation when used for tracking.

**CrUX (Chrome User Experience report).** Google's field-data source for Core Web Vitals. Not an ObservePoint product but referenced when discussing performance.

## D

**Data layer.** A standardized JavaScript object on a page that holds structured information about the user, the page, and events. Tag managers read from it. ObservePoint validates it.

**DPDP (Digital Personal Data Protection) Act.** India's comprehensive privacy law. Rules finalized late 2025, active enforcement entering 2026.

**DSAR (Data Subject Access Request).** A request from an individual to see, correct, or delete their personal data. Workflow-level, owned by privacy programs — not an ObservePoint feature directly.

## E

**EAA (European Accessibility Act).** EU directive extending accessibility obligations across member states.

**EU AI Act.** European regulation governing artificial intelligence systems, with marketing-relevant transparency obligations under Article 50 taking effect 2026.

**ePrivacy Directive.** EU directive covering electronic communications privacy, including the cookie consent requirements that precede GDPR.

## F

**FERPA (Family Educational Rights and Privacy Act).** U.S. law protecting student education records.

## G

**GA4 (Google Analytics 4).** Current generation of Google Analytics. Event-based model. Replaced Universal Analytics.

**GDPR (General Data Protection Regulation).** The European Union's comprehensive privacy regulation.

**GLBA (Gramm-Leach-Bliley Act).** U.S. law governing financial institutions and customer data.

**GPC (Global Privacy Control).** A browser-level "do not sell or share" signal honored as a valid opt-out under multiple U.S. state privacy laws. Toggle in ObservePoint as "Send GPC Signal" on an audit.

**GTM (Google Tag Manager).** Google's tag management system, both client-side and server-side variants.

## H

**HAR (HTTP Archive).** A standard JSON file format capturing the network requests a browser made on a page. Exportable from Chrome DevTools, Charles, Fiddler, mitmproxy. Processable by ObservePoint's **HAR Analyzer**.

**HIPAA (Health Insurance Portability and Accountability Act).** U.S. law governing health information privacy and security.

**Hydration.** A pattern in modern JS frameworks (React, Vue) where the page is server-rendered then "hydrated" with client-side interactivity. A common cause of tag firing inconsistencies; the **Journey** with **Prevent Navigation** is the workaround.

## I

**IAB (Interactive Advertising Bureau).** Industry body publishing the **TCF** consent framework.

**INP (Interaction to Next Paint).** A Core Web Vitals metric. Captures interaction responsiveness.

## J

**Journey.** In ObservePoint specifically, a scripted multi-step user flow run by the synthetic browser. See `references/products-and-modules.md` → Journeys.

**JourneyStream.** One of the Strala-acquired products. Automates campaign tracking and touchpoint management.

## L

**LCP (Largest Contentful Paint).** A Core Web Vitals metric. Captures perceived load time.

**LGPD (Lei Geral de Proteção de Dados).** Brazil's comprehensive privacy law. GDPR-style framework.

**LiveConnect.** ObservePoint product for connecting real devices via proxy for live network inspection.

## M

**MCP (Model Context Protocol).** Anthropic's open protocol for connecting AI systems to external tools. The ObservePoint MCP server is in development. See `references/mcp-tools.md`.

## P

**Page Insights.** ObservePoint's real-user telemetry dashboard, fed by a lightweight tag deployed on the customer's site.

**Pixel.** A tag used for ad attribution or analytics, originally implemented as a 1x1 image request. Used loosely to mean any analytics or advertising request.

**PHI (Protected Health Information).** Health information that identifies an individual. Under HIPAA, very strictly regulated.

**PIPEDA (Personal Information Protection and Electronic Documents Act).** Canada's federal private-sector privacy law.

**Prism.** One of the Strala-acquired products. Attribution and ROI analysis layer.

## R

**RACI.** A framework for assigning roles to activities — Responsible, Accountable, Consulted, Informed. Template in `references/consulting-deliverables.md`.

**Rule.** In ObservePoint specifically, a Tag & Variable Rule — `WHEN` condition + `EXPECT` condition. The mechanism by which audit findings turn into pass/fail signals.

## S

**sGTM (Server-side Google Tag Manager).** A GTM container that runs on the customer's own servers rather than in the browser. ObservePoint observes the client-side request that triggers it, not the server execution. See `references/limitations.md`.

**SOC 2.** A security and operational controls audit framework. Common enterprise procurement requirement.

**SPA (Single-Page Application).** A web app where navigation happens without full page reloads. Examples: React, Vue, Angular, Svelte apps. Requires **Journey** + **Prevent Navigation** for full coverage.

**Strala.** The company ObservePoint acquired in February 2020. Brought **Touchpoints**, **JourneyStream**, and **Prism**.

## T

**Tag.** A small piece of code that runs on a page to collect data or render content. Analytics tags, advertising tags, functional tags, and so on.

**TCF (Transparency and Consent Framework).** The IAB's standard for encoding consent strings. **TCF 2.3** is the current version; non-compliant strings became invalid February 28, 2026.

**TMS (Tag Management System).** GTM, Tealium iQ, Adobe Launch, Ensighten, etc. ObservePoint is vendor-neutral across TMS choices.

**Touchpoints.** One of the Strala-acquired products. Standardizes and unifies online and offline customer touchpoint data.

## U

**UTM (Urchin Tracking Module) parameters.** Query-string parameters (`utm_source`, `utm_medium`, etc.) used to attribute traffic to campaigns. Predates Google's acquisition of Urchin; the name stuck.

## W

**WCAG (Web Content Accessibility Guidelines).** The W3C standard for web accessibility. WCAG 2.1 Level AA is the conformance level most commonly enforced.

**Web Audit.** See **Audit**.

**Web governance.** The category ObservePoint operates in. Continuous, automated validation that a website behaves correctly for analytics, privacy, accessibility, and operational quality. See `references/verbiage-and-messaging.md`.

---

*Last verified: 2026-05-28*
