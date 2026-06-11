# Integrations

Where ObservePoint plugs into the rest of the customer's stack. Load this when the user asks "how does ObservePoint connect to X?" or wants to set up alerts, ticketing, identity, or pipelines.

The shape of every entry: **what the integration does**, **the auth model**, **the typical use**, **the gotcha**.

## Tag managers

### Google Tag Manager (GTM)

**What it does.** ObservePoint detects GTM containers on every audited page, identifies which tags GTM has fired, and validates the data layer pushes GTM consumes.

**Auth.** None on ObservePoint's side — the audit observes GTM passively as part of the page.

**Typical use.** Validate that the GTM container ID on production matches what's deployed, that the tags inside are firing per the data layer spec, that the consent gates configured inside GTM are honored.

**Gotcha.** Server-side GTM (sGTM) fires on your servers; ObservePoint can only see the client-side request that triggers it. See `references/limitations.md` → "Server-side tag execution."

### Tealium iQ

**What it does.** Bi-directional integration. ObservePoint can be triggered when Tealium publishes a new container version (validate the published version before traffic hits it).

**Auth.** Webhook from Tealium to ObservePoint, plus the ObservePoint API key for the callback.

**Typical use.** Block a problematic Tealium publish before it propagates everywhere.

**Gotcha.** Specific to the Tealium iQ workflow. Custom Tealium implementations may need a more bespoke wiring.

### Adobe Launch / Adobe Tags

**What it does.** Adobe Launch tags are detected and validated through the same audit mechanism as any other tag. ObservePoint includes templates for common Adobe Analytics rules.

**Auth.** None on the audit side. If wiring Adobe Launch's publishing pipeline into ObservePoint, use the same webhook pattern as Tealium.

**Typical use.** Validate Adobe Analytics eVar and event mapping on every release.

**Gotcha.** Adobe Launch's library reload patterns can sometimes look like missing tags to a basic scanner. The Rules engine handles this correctly with a small wait configured on the Audit.

## Consent Management Platforms (CMPs)

### OneTrust

**What it does.** ObservePoint's CMP validation has explicit support for OneTrust — automated "Accept All" and "Reject All" interaction in audits, plus the Bulk OneTrust Updates feature shipped in March 2026 for managing multiple OneTrust instances at once.

**Auth.** None for validation. The Bulk Updates feature uses an admin API key from the OneTrust side.

**Typical use.** Validate that OneTrust correctly suppresses non-essential tags under "Reject All." Bulk-update consent banner copy or vendor configurations across regional sites.

**Gotcha.** OneTrust's preview / staging cookie banner is sometimes scriptable; production almost always is.

### Cookiebot (by Usercentrics)

**What it does.** Standard CMP validation. ObservePoint runs the audit with the Cookiebot banner present, simulating consent choices.

**Auth.** None on ObservePoint's side.

**Typical use.** Same audit-per-consent-state pattern as OneTrust.

### TrustArc

**What it does.** Same audit-per-consent-state validation.

**Auth.** None on ObservePoint's side.

### Didomi, Sourcepoint, and generic CMPs

**What it does.** Most modern CMPs follow the IAB Transparency and Consent Framework. ObservePoint can interact with the CMP using a custom selector configuration if a CMP isn't natively recognized.

**Auth.** None.

**Gotcha.** Selectors break when the CMP vendor updates their banner. Re-validate when you see a wave of failures on a previously-stable audit.

## Ticketing and incident management

### Jira

**What it does.** Failed audits and Rule violations can create Jira tickets automatically. Useful when the failure-resolution workflow already lives in Jira.

**Auth.** API token from Jira plus a service account.

**Typical use.** Wire critical Rule failures to a "Site Quality" Jira project; non-critical failures go to email.

**Gotcha.** Don't wire every Rule to Jira on day one — you'll create ticket noise. Start with the top 5 Rules, expand as the team's signal-to-noise ratio improves.

### ServiceNow

**What it does.** Same pattern as Jira via webhooks.

**Auth.** Webhook + ServiceNow inbound integration.

## Communications

### Slack

**What it does.** Posts audit results and alerts into channels.

**Auth.** Slack incoming webhook URL configured in the ObservePoint alert.

**Typical use.** Dedicated `#analytics-alerts` and `#privacy-compliance` channels. Route each Rule to the right team's channel.

**Gotcha.** Slack channel routing tied to specific Rules pays off; one giant channel for "all alerts" gets muted within a quarter.

### Microsoft Teams

**What it does.** Same as Slack via the Teams incoming webhook.

### Email / SMS

**What it does.** Standard alert channels for individual recipients.

**Typical use.** SMS for genuinely-paging events (purchase tracking broken in production). Email for digests. Slack/Teams for everything in between.

## Identity and SSO

### Self-Serve SSO (March 2026)

**What it does.** Lets enterprise customers configure SAML / OIDC SSO for the ObservePoint app themselves, without needing ObservePoint support to provision it.

**Auth.** Standard SAML / OIDC metadata exchange.

**Typical use.** Onboard new ObservePoint users via your IdP (Okta, Azure AD, Google Workspace) instead of password-based local accounts.

**Gotcha.** If you provisioned SSO before March 2026, it's still managed the old way until you migrate.

### Username/password

**What it does.** Available for individual contributors and smaller teams.

**Typical use.** Quick start; enterprise teams should move to SSO.

## CI/CD

### GitHub Actions

**What it does.** Run audits as a release gate. The `automation-and-testing` skill carries a working workflow ("Recipe: CI/CD gate with GitHub Actions").

**Auth.** ObservePoint API key in a repository secret.

### GitLab CI, Jenkins, Bamboo, Circle CI, Azure DevOps

**What it does.** Same pattern. Any CI system that can run shell commands and `jq` can drive the ObservePoint REST API.

**Typical use.** Pre-deploy audit on the staging URL pattern; block the deploy if any critical Rule fails.

**Gotcha.** Don't gate every PR on a slow Web Audit. Use a fast targeted audit (a single key page or a Journey) for PR gates; full-site audits run on the deploy job after merge.

## Analytics and BI

### Google Sheets

**What it does.** Export audit results and Rule reports.

**Auth.** Google OAuth.

### CSV export

**What it does.** Every report supports CSV export, suitable for ingesting into a warehouse or BI tool.

**Typical use.** Push to Snowflake, BigQuery, Redshift via a small ETL — Looker / Tableau / Power BI dashboards on top.

## Webhooks (general purpose)

**What it does.** ObservePoint POSTs to a URL you control on audit-run completion. The payload identifies the audit, the run, the status, and key result metadata.

**Auth.** Whatever you configure on your receiver. Validate the source IP / signature if you're treating it as security-sensitive.

**Typical use.** Custom integrations to anywhere that isn't a first-party integration. Roll your own routing logic.

## The forthcoming MCP server

When the ObservePoint MCP server ships, it joins this list. See `references/mcp-tools.md` for the extension pattern. Treat it as an additional transport, not a replacement for any of the above.

---

*Last verified: 2026-05-28*
