# observepoint-consultant

> A Claude Code skill that turns Claude into the world's greatest [ObservePoint](https://www.observepoint.com/) and web-governance advisor.

Type `/observepoint-consultant` in Claude Code (or any Claude Code-compatible client) and get evidence-based, reference-backed answers about every aspect of the ObservePoint platform and the web-governance market it serves.

## What it knows

The skill ships **13 reference files** inside one focused `SKILL.md` dispatcher. Topic coverage:

| Reference | What it covers |
|---|---|
| `products-and-modules.md` | Web Audits, Journeys, Page Insights, Touchpoints / JourneyStream / Prism, Tag & Cookie Debugger, HAR Analyzer, LiveConnect, Rules engine, Alerts, Reports |
| `solution-playbooks.md` | Recipes for analytics validation, consent enforcement, accessibility, performance, CMP-specific work, campaign launches, healthcare compliance, litigation defense, state-specific monitoring, AI-Act disclosure, multi-jurisdiction programs |
| `api-reference.md` | v3 REST API endpoints, auth, recipes for triggering audits, creating Rules, processing HARs, and wiring CI/CD gates |
| `mcp-tools.md` | 130+ MCP wrapper catalog organized by family (PII scanning, consent-state comparison, anomaly detection, analysis primitives, etc.) with the safety gates documented |
| `privacy-and-compliance.md` | **Comprehensive global privacy coverage** — 50+ regulations across all 19 U.S. comprehensive state laws (CCPA, CPA, CTDPA, VCDPA, UCPA, TDPSA, OCPA, MCDPA, DPDPA, …), sectoral (HIPAA, GLBA, COPPA, FERPA), U.S. health-data (Washington MHMDA, Nevada SB 370), U.S. AI (Colorado AI Act, Texas RAIGA, NYC LL 144), U.S. kids (CA AADC, KOSA), EU (GDPR, ePrivacy, EU AI Act, DSA, DMA, Data Act, NIS2), UK (UK GDPR, DPA 2018, PECR), Latin America, APAC (China PIPL, Japan APPI, Singapore PDPA, Korea PIPA, India DPDP, Australia, NZ), Canada (PIPEDA, Quebec Law 25), Middle East & Africa, browser signals (GPC, UOOM, TCF, GPP, Consent Mode v2, Apple ATT, Privacy Sandbox), voluntary standards (PCI DSS 4.0, NIST Privacy Framework, ISO/IEC 27701), accessibility (WCAG / EAA) |
| `privacy-litigation-defense.md` | **Tort / litigation-driven privacy claims** — CIPA pen-register theory, VPPA video-tracking, BIPA biometric, ECPA / federal Wiretap, state wiretap statutes (MA, PA, FL, WA), healthcare-tracking pixel claims, session-replay claims. Evidence-pack assembly for counsel. |
| `competitive-positioning.md` | Honest, public-source-only comparisons against DataTrue, Tag Inspector, Tealium iQ Validate, OneTrust scanning, Crownpeak, Trackingplan |
| `verbiage-and-messaging.md` | Brand-correct phrasing, capitalization, do/don't language |
| `limitations.md` | What ObservePoint cannot do, with the recommended workaround for each |
| `integrations.md` | TMS, CMP, ticketing, comms, identity, CI/CD, BI plug-ins |
| `consulting-deliverables.md` | Hand-back templates: tag audit report, governance policy, RACI, release-gate checklist, evidence pack, QBR |
| `personas.md` | Tone and content tuning for nine common ObservePoint personas |
| `glossary.md` | Term reference (~80 terms covering products, regulations, litigation theories, signals, frameworks) |

## Who it's for

- Analytics Managers and Analytics Engineers
- Privacy and Compliance Officers
- Marketing Operations and MarTech Engineers
- Web Developers and QA
- InfoSec / CISOs
- Chief Data Officers
- Healthcare and regulated-industry compliance leads
- Anyone evaluating, implementing, or consulting on ObservePoint

## Install

This repo is a self-hosted Claude Code [marketplace](https://docs.claude.com/en/docs/claude-code/plugins). Two-step install:

```
/plugin marketplace add jpwilbur/observepoint-consultant
/plugin install observepoint-consultant@observepoint-consultant
```

The first command points Claude Code at this GitHub repo. The second installs the plugin from that marketplace.

After installing, restart Claude Code (or open a new session) and type `/` — you should see `/observepoint-consultant` in the picker.

### Local-development install

If you've cloned the repo and want to install from your working copy:

```
/plugin marketplace add /absolute/path/to/observepoint-consultant
/plugin install observepoint-consultant@observepoint-consultant
```

## Usage

Invoke with any question. Examples that exercise different parts of the skill:

```
/observepoint-consultant How do I validate GA4 purchase events on a single-page app?
/observepoint-consultant Map CCPA enforcement readiness to ObservePoint coverage.
/observepoint-consultant What's CIPA and how does ObservePoint help defend a class action?
/observepoint-consultant Set up Colorado CPA compliance monitoring.
/observepoint-consultant Do we need to honor GPC in Texas?
/observepoint-consultant Defend a VPPA class action — what evidence do I produce?
/observepoint-consultant Map China PIPL to ObservePoint coverage.
/observepoint-consultant Is PCI DSS 4.0 something ObservePoint helps with?
/observepoint-consultant What does my privacy program need for Washington My Health My Data?
/observepoint-consultant Write a Rule that catches OneTrust consent drift.
/observepoint-consultant What's the difference between an Audit and a Journey?
/observepoint-consultant Does ObservePoint test mobile apps?
/observepoint-consultant Draft a Web Governance Policy outline.
/observepoint-consultant How does ObservePoint compare to OneTrust scanning?
/observepoint-consultant I'm a Privacy Officer at a healthcare company. Where do I start?
/observepoint-consultant Build me a release-gate checklist for our analytics releases.
/observepoint-consultant Maintain a multi-jurisdiction compliance program across EU, US, APAC.
/observepoint-consultant Use the ObservePoint MCP to scan a journey for PII leaks.
```

Each answer follows a fixed shape: restated goal → recommended approach with product names → concrete next steps → limitations → which reference file(s) were used.

## How the MCP server slots in

The ObservePoint [MCP](https://modelcontextprotocol.io/) server is currently in active development. A small group of internal users has access today; broader release is expected in the coming months.

**For everyone:** the skill works in knowledge-only mode without the MCP server. Answers come from the bundled reference docs, with REST API recipes for operational tasks. This is the default experience.

**For ObservePoint internal users with access:** once the MCP server is registered in your Claude environment, the skill auto-detects `mcp__ObservePoint__*` tools at runtime and prefers them over the REST recipes. **No additional setup in this plugin is needed** — MCP registration happens at the Claude environment level, not per-plugin. This is why this repo does **not** ship a `.mcp.json`: it would either duplicate your existing registration or hard-code a non-portable local path.

Two real install paths today (refer to the MCP server's own README for the authoritative steps):

- **Claude Desktop**: install the `.dxt` extension and enter your API key when prompted. Restart Claude Desktop, start a new conversation.
- **Claude Code CLI**: register via `claude mcp add --scope user observepoint -- node /path/to/observepoint-mcp/build/index.js` with `-e OP_API_KEY=...` (required) and optionally `-e OP_BASE_URL=...` for non-default environments. Restart Claude Code.

The skill **never invents an MCP tool name.** When the tools aren't loaded in your session, the skill behaves as the knowledge-only advisor. See [`skills/observepoint-consultant/references/mcp-tools.md`](./skills/observepoint-consultant/references/mcp-tools.md) for the full tool catalog and the safety gates the wrappers enforce (selector evidence, journey-shape, watch-usage, two-step CMP import).

When the MCP server reaches general availability, this section will be updated with the public install path — likely a `.mcp.json` bundled in the plugin so installing this plugin alone is enough to set up both the skill and the MCP server.

## Versioning

Semantic versioning. v0.x is pre-production; APIs and reference doc structure may change.

See [CHANGELOG.md](./CHANGELOG.md) for the release history.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). The easiest place to add value is in [skills/observepoint-consultant/references/](./skills/observepoint-consultant/references/) — each file is self-contained markdown.

Especially welcome:

- Refreshes when ObservePoint ships new features (update the relevant reference file and bump its `Last verified` date).
- New playbooks in `solution-playbooks.md` for pains we haven't covered.
- Real MCP tool documentation once the server reaches GA.

## Anthropic skill conventions

This skill follows [Anthropic's first-party skill-creator patterns](https://github.com/anthropics/skills) verbatim:

- SKILL.md frontmatter contains only `name` and `description`.
- The `description` is written in skill-creator's "pushy" style to combat under-triggering.
- SKILL.md body stays under 500 lines; long content lives in `references/`.
- Imperative form, explains *why* not just steps.
- Optional directories follow Anthropic's anatomy (`scripts/`, `references/`, `assets/`); we use `references/` only.

See [CONTRIBUTING.md](./CONTRIBUTING.md#anthropic-skill-conventions-we-follow) for details.

## License

[MIT](./LICENSE).

## Disclaimer

This is a **community-built** Claude Code skill. It is **not** an official ObservePoint product, and ObservePoint, LLC has not endorsed it. All information reflects publicly documented ObservePoint capabilities as of the `Last verified` date in each reference file. **Verify product behavior against current ObservePoint documentation before making procurement, compliance, or contractual decisions.** "ObservePoint" and product names referenced here are trademarks of ObservePoint, LLC.
