# observepoint-consultant

> A Claude Code skill that turns Claude into the world's greatest [ObservePoint](https://www.observepoint.com/) and web-governance advisor.

Type `/observepoint-consultant` in Claude Code (or any Claude Code-compatible client) and get evidence-based, reference-backed answers about every aspect of the ObservePoint platform and the web-governance market it serves.

## What it knows

The plugin ships as **a hub skill plus 6 focused advisors**. The `observepoint-consultant` hub is a thin router and shared foundation — when a question is squarely in one advisor's lane it hands off to that skill; when a question spans domains or sits above any single lane, the hub answers it directly. Each advisor owns its own deep reference; the shared foundation (~11 files: products, MCP tools, verbiage, limitations, glossary, competitive positioning, personas, consulting deliverables, solution playbooks, integrations, and the industries directory) lives under the hub and every advisor links back to it.

## Skills

All 7 skills auto-trigger from their `description` whenever a question matches their lane — you usually don't need to invoke one by name. You can also call any of them explicitly with the slash command shown.

| Skill | Invoke | What it's for |
|---|---|---|
| **observepoint-consultant** (hub) | `/observepoint-consultant` | Router + general advisor + shared foundation. Answers cross-cutting questions and routes the rest to an advisor. |
| privacy-compliance | `/observepoint-consultant:privacy-compliance` | Whether a **privacy or marketing law applies** and how to evidence it, AND whether the **consent banner / CMP actually blocks tracking** — GDPR, CCPA/CPRA, 19+ U.S. state laws, HIPAA, GLBA, PIPL; Reject-All, Consent Mode v2, GPC, OneTrust/Cookiebot/TrustArc/Didomi. |
| litigation-defense | `/observepoint-consultant:litigation-defense` | **Technical evidence for a tracking class action or demand letter** — CIPA, VPPA, BIPA, ECPA, state wiretap, healthcare-pixel, session-replay. Evidence packs for counsel. |
| accessibility | `/observepoint-consultant:accessibility` | **Accessibility** law and prioritization — ADA Title II/III, Section 508, WCAG 2.1/2.2, EAA, highest-impact-fix sequencing, lawsuit-defense evidence. |
| tag-and-analytics-quality | `/observepoint-consultant:tag-and-analytics-quality` | **What a tag is and whether it should be here** (vendor risk, authorization), AND **whether the analytics data is correct** — GA4/Adobe events, values, data-layer, attribution; how adjacent platforms are built and what ObservePoint sees (GA4, Adobe, GTM, sGTM, Tealium, Meta CAPI, CDPs, Privacy Sandbox). |
| account-and-program | `/observepoint-consultant:account-and-program` | How to **set up or structure the account** (audits, Rules, consent categories, alerts, schedules) AND **program health / maturity / onboarding / "what's next"** — saved reports, dashboards, charts. |
| automation-and-testing | `/observepoint-consultant:automation-and-testing` | **REST/MCP automation and CI/CD audit gates**, AND building or debugging **multi-step Journeys** — LiveConnect, HAR Analyzer, selector-evidence/journey-shape/watch-usage safety gates. |

Two boundaries worth knowing: *does Reject-All actually block this tag?* → **privacy-compliance**; *is this tag's data correct?* → **tag-and-analytics-quality**.

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

## Updating

When a new version is pushed to this repo, Claude Code does **not** auto-detect it — it only knows about the copy of this marketplace it pulled when you first added it. To get the latest, run **both** of these in the Claude Code terminal (note the first is `update`, *not* `add` — re-adding or "syncing" reuses the stale cache and is the #1 reason the Update button stays greyed out):

```
/plugin marketplace update observepoint-consultant
/plugin update observepoint-consultant@observepoint-consultant
```

Then restart Claude Code or start a new session. The first command re-pulls this repo so Claude Code can see the new version; the second installs it. After the marketplace is refreshed, the **Update** button in the `/plugin` UI also becomes active and does the same thing as the second command.

**Stuck on an old version (Update button greyed out, "last updated" weeks ago)?** You're on a stale marketplace cache. Clear it and re-pull:

```
rm -rf ~/.claude/plugins/cache/observepoint-consultant
```

then run the two commands above again.

### Cowork

**Cowork is a separate distribution channel from the terminal — it does _not_ read `~/.claude/plugins/`.** Cowork tracks plugins through an Anthropic **cloud-hosted snapshot** of this repo, which only re-syncs when that cloud marketplace record is refreshed. As a result, updating in the terminal (above) has **no effect** on Cowork, and Cowork can stay frozen on an old version with the Update button greyed out — a known limitation for personal / third-party GitHub marketplaces in Cowork.

To get the latest version into Cowork, in order of preference:

1. **Org marketplace (recommended).** An organization owner adds this repo under **Claude → Organization settings → Plugins** and turns on **"Sync automatically."** New pushes to `main` then propagate to every member's Cowork on their next session (up to ~30 min) — no per-person action and no greyed button. See [Manage Cowork plugins for your organization](https://support.claude.com/en/articles/13837433-manage-claude-cowork-plugins-for-your-organization).
2. **Per-user refresh.** In Cowork, **remove** the `observepoint-consultant` marketplace and **re-add** it to force a fresh snapshot. This is per-person and may need repeating on each release.
3. **Use the Desktop "Code" tab or terminal** for this plugin, where the update path above works reliably.

### Optional: org-wide auto-update (admin)

If your organization deploys [managed settings](https://docs.claude.com/en/docs/claude-code/settings) (e.g. via MDM), an admin can set `autoUpdate` on this marketplace so Claude Code re-pulls it on startup and offers the update without anyone running `marketplace update`. Add to the managed `managed-settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "observepoint-consultant": {
      "source": { "source": "github", "repo": "jpwilbur/observepoint-consultant" },
      "autoUpdate": true
    }
  }
}
```

This is the only way to get true "it just updates" behavior — it's an administrator-deployed setting, not something each user can flip in their personal `~/.claude/settings.json`. Without it, the two-command refresh above is the supported path for everyone.

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
/observepoint-consultant What's the ObservePoint playbook for a retail site preparing for Black Friday?
/observepoint-consultant Map the GLBA Safeguards Rule to ObservePoint coverage for a financial services site.
/observepoint-consultant Set up the Consent Mode v2 wiring between OneTrust and GTM — what should ObservePoint check?
/observepoint-consultant Server-side GTM — what can ObservePoint validate and what can't it?
/observepoint-consultant What should I focus on in my ObservePoint account? Where's the biggest bang for buck?
/observepoint-consultant From our accessibility data, what's the highest-impact fix to target first?
/observepoint-consultant We got an ADA web-accessibility demand letter — what evidence can ObservePoint produce?
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

See [CONTRIBUTING.md](./CONTRIBUTING.md). The easiest place to add value is in a skill's `references/` directory — the shared foundation lives under [skills/observepoint-consultant/references/](./skills/observepoint-consultant/references/), and each advisor owns its deep reference under `skills/<advisor>/references/`. Each file is self-contained markdown.

Especially welcome:

- Refreshes when ObservePoint ships new features (update the relevant reference file and bump its `Last verified` date).
- New playbooks in the hub's `solution-playbooks.md` for pains we haven't covered.
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
