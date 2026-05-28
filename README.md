# observepoint-consultant

> A Claude Code skill that turns Claude into the world's greatest [ObservePoint](https://www.observepoint.com/) and web-governance advisor.

When installed, you can type `/observepoint-consultant` in Claude Code (or any Claude Code-compatible client) and get evidence-based, reference-backed answers about:

- **ObservePoint products & modules** — Web Audits, Journeys, Page Insights, Touchpoints / JourneyStream / Prism, the Tag & Cookie Debugger, HAR Analyzer, LiveConnect, and the Rules engine
- **The seven solution categories** — Web Privacy, Analytics Validation, WCAG Accessibility, CMP Validation, Email Link Validation, Landing Page Validation, Tag/Website Debugger
- **Writing Rules & API recipes** — Tag & Variable Rules with When/Expect logic, v3 REST API recipes, CI/CD integration
- **Privacy & compliance** — GDPR, CCPA/CPRA, HIPAA, LGPD, India DPDPA, TCF 2.3, Consent Mode v2, GPC, EU AI Act Article 50
- **Consulting deliverables** — Tag Audit Reports, Web Governance Policies, RACI matrices, Release-Gate checklists
- **The forthcoming ObservePoint MCP server** — auto-detects `mcp__observepoint__*` tools at runtime and prefers them when available; falls back to REST today

## Who it's for

- Analytics Managers and Analytics Engineers
- Privacy and Compliance Officers
- Marketing Operations and MarTech Engineers
- Web Developers and QA
- InfoSec and CISOs
- Chief Data Officers
- Healthcare and regulated-industry compliance leads
- Anyone consulting on, evaluating, or implementing ObservePoint

## Status

**v0.1.0 in development.** This README is a stub during the initial scaffold; full install instructions and example prompts will land at v0.1.0 release. Track progress in [CHANGELOG.md](./CHANGELOG.md).

## Install (preview)

Once v0.1.0 ships:

```
/plugin marketplace add jpwilbur/observepoint-consultant
/plugin install observepoint-consultant@observepoint-consultant
```

Then in any Claude Code session:

```
/observepoint-consultant How do I validate GA4 purchase events on a single-page app?
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). The easiest place to add value is in the `skills/observepoint-consultant/references/` directory — each file is self-contained markdown.

## License

[MIT](./LICENSE).

## Disclaimer

This is a **community-built** Claude Code skill. It is **not** an official ObservePoint product, and ObservePoint, LLC has not endorsed it. All information reflects publicly documented ObservePoint capabilities as of the `Last verified` date in each reference file. **Verify product behavior against current ObservePoint documentation before making procurement, compliance, or contractual decisions.** "ObservePoint" and product names referenced here are trademarks of ObservePoint, LLC.
