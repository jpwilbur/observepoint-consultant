# observepoint-consultant

> A Claude Code skill that turns Claude into the world's greatest [ObservePoint](https://www.observepoint.com/) and web-governance advisor.

Type `/observepoint-consultant` in Claude Code (or any Claude Code-compatible client) and get evidence-based, reference-backed answers about every aspect of the ObservePoint platform and the web-governance market it serves.

## What it knows

The skill ships 12 reference files inside one focused `SKILL.md` dispatcher. Topic coverage:

| Reference | What it covers |
|---|---|
| `products-and-modules.md` | Web Audits, Journeys, Page Insights, Touchpoints / JourneyStream / Prism, Tag & Cookie Debugger, HAR Analyzer, LiveConnect, Rules engine, Alerts, Reports |
| `solution-playbooks.md` | Recipes for analytics validation, consent enforcement, accessibility, performance, CMP-specific work, campaign launches, healthcare compliance, and program-building |
| `api-reference.md` | v3 REST API endpoints, auth, recipes for triggering audits, creating Rules, processing HARs, and wiring CI/CD gates |
| `mcp-tools.md` | Extension point for the forthcoming ObservePoint MCP server (auto-detected at runtime when GA) |
| `privacy-and-compliance.md` | Mapping GDPR, CCPA/CPRA, HIPAA, LGPD, PIPEDA, India DPDP, COPPA, GPC, TCF, Consent Mode v2, EU AI Act Article 50, WCAG to ObservePoint coverage |
| `competitive-positioning.md` | Honest, public-source-only comparisons against DataTrue, Tag Inspector, Tealium iQ Validate, OneTrust scanning, Crownpeak, Trackingplan |
| `verbiage-and-messaging.md` | Brand-correct phrasing, capitalization, do/don't language |
| `limitations.md` | What ObservePoint cannot do, with the recommended workaround for each |
| `integrations.md` | TMS, CMP, ticketing, comms, identity, CI/CD, BI plug-ins |
| `consulting-deliverables.md` | Hand-back templates: tag audit report, governance policy, RACI, release-gate checklist, evidence pack, QBR |
| `personas.md` | Tone and content tuning for nine common ObservePoint personas |
| `glossary.md` | Term reference |

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
/observepoint-consultant Write a Rule that catches OneTrust consent drift.
/observepoint-consultant What's the difference between an Audit and a Journey?
/observepoint-consultant Does ObservePoint test mobile apps?
/observepoint-consultant Draft a Web Governance Policy outline.
/observepoint-consultant How does ObservePoint compare to OneTrust scanning?
/observepoint-consultant I'm a Privacy Officer at a healthcare company. Where do I start?
/observepoint-consultant Build me a release-gate checklist for our analytics releases.
/observepoint-consultant Use the ObservePoint MCP to start an audit.
```

Each answer follows a fixed shape: restated goal → recommended approach with product names → concrete next steps → limitations → which reference file(s) were used.

## How the MCP server slots in

ObservePoint is building an official [Model Context Protocol](https://modelcontextprotocol.io/) server. It is **not yet generally available**.

When the server ships:

- Tools named `mcp__observepoint__*` will appear in your Claude session.
- This skill auto-detects them at runtime and prefers them over raw REST calls.
- Until then, the skill answers operational questions using the REST API and explicitly says MCP is coming.

The skill **never invents an MCP tool name.** See `skills/observepoint-consultant/references/mcp-tools.md` for the extension pattern.

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
