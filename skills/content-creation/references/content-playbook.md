# Content playbook — writing in the web-governance / ObservePoint domain

Load this when the user wants to **write or improve a piece of content** in the web-governance / ObservePoint domain — a blog post, a how-to guide, a one-pager, or a thought-leadership piece — and wants it to read like someone who actually knows the domain wrote it.

This is an OUTPUT skill: it produces a draft (or critiques one), it does not run the platform. The domain *facts* it leans on live in the specialist skills; this playbook owns the *craft* of turning those facts into publishable content that sounds like ObservePoint. The shape is different from the advisory specialists — those answer a question; this one produces an artifact and hands it back for editing.

## Contents

1. [House voice](#1-house-voice)
2. [Audience framing](#2-audience-framing)
3. [Content structures](#3-content-structures)
4. [Evidence and citation discipline](#4-evidence-and-citation-discipline)
5. [The no-fabrication rule](#5-the-no-fabrication-rule)
6. [Humanizer pairing](#6-humanizer-pairing)
7. [Giving feedback on a draft](#7-giving-feedback-on-a-draft)

## 1. House voice

The canonical voice lives in the shared `references/verbiage-and-messaging.md` — read it before drafting anything customer-facing, and defer to it on any conflict. The rules that matter most for content:

- **The category is "web governance platform."** Never "tag manager," "cookie scanner," or "analytics QA tool." The crisp short forms are "the web governance platform" and "automated web governance."
- **The core message is insights, automation, and compliance for the chaos of your website.** The "chaos" framing is ObservePoint's own and is load-bearing — it names the customer's reality (many teams, many vendors, many unknowns) without blaming them. Lead a piece with one of the three public outcomes:
  1. Catch hidden privacy violations before regulators do.
  2. Reduce ad spend wasted on broken tracking.
  3. Simplify compliance through automation rather than manual audits.
- **Capitalization is exact.** ObservePoint (one word). Web Audits, Journeys, Page Insights, Tag & Cookie Debugger, HAR Analyzer, LiveConnect, Tag & Variable Rules. Don't pluralize oddly ("running an Audit," not "running an Audits").
- **Outcome statements beat feature statements.** "Catch a broken purchase event the moment a release ships, not three weeks later when revenue reports look wrong" lands; "ObservePoint has a Rules engine" does not.
- **Use the customer's words** — your team, your stack, your domain, releases, releases that change tagging. Avoid condescending framings ("your tag mess," "manual processes are broken").
- **Frame limitations as routing, not apology.** Web-only, observes what the CMP exposes, synthetic browser — name these as honest scope, not weaknesses.
- **Regulatory language stays at "evidence and validation."** Never "achieves compliance"; compliance is decided by lawyers and regulators, not by a tool.

### Voice quick-reference

| Use this | Not this |
|---|---|
| Web governance platform | Tag manager / cookie scanner |
| Validates what your CMP claims to do | Replaces your CMP |
| Catch issues before regulators do | Catch issues before lawsuits |
| Evidence pack | Proof |
| Scheduled audits | Crawls |
| Synthetic browser | Robot / bot |
| Releases that change tagging | Your tag mess |

When in doubt, the table in `references/verbiage-and-messaging.md` is longer and authoritative.

## 2. Audience framing

Pitch every piece at a specific reader. The shared `references/personas.md` is the source of truth for who they are, what pains them, and the vocabulary to match. Pick one primary persona before you write a word — content addressed to "everyone" addresses no one. Quick framing per persona:

- **Analytics Manager / Analytics Engineer** — data-quality first. Lead with the broken-event-for-two-weeks fear; speak in events, data layer, releases, regressions. The engineer wants the Rule snippet and the API shape; don't hedge with them. Keep pure privacy jargon out unless they raise it.
- **Privacy / Compliance Officer (incl. Healthcare)** — evidence and risk, not endpoints. Talk quarterly evidence packs, every-page/every-device proof, consent states, PHI URL patterns. Keep regulatory claims at "evidence," never "compliance achieved." They know the regulation cold — don't lecture.
- **MarTech Operations / Digital Marketer** — campaign-launch fire drills. Make the mess survivable; show in-app workflows, not CI/CD gates (those are the engineer's world). The marketer wants the pre-launch checklist, not the architecture.
- **Web Developer / QA / InfoSec / CISO** — the technical impact of someone else's tag on their page, or their third-party-risk surface. Speak CLS/LCP/INP, render-blocking, third-party risk, vendor inventory, data egress. They don't speak in pixel; they speak in NIST and Lighthouse.
- **Chief Data Officer / CSM** — strategic. Trust, governance, data-quality SLA, value realization, renewal, maturity stage. Lead with the program; the tools support it.

When the user hasn't named an audience, ask which persona the piece is for before drafting — the structure, depth, and vocabulary all hinge on it. A blog for the CISO and a blog for the Digital Marketer on the "same" topic are two different pieces.

## 3. Content structures

Each format has a shape. The reusable skeletons live in this skill's `assets/` (`blog-template.md`, `one-pager-template.md`); pull the matching one and fill it. The structures:

### Blog post

Hook (a real, recognizable pain) → the problem in the reader's terms → the web-governance angle (why this is a *governance failure*, not a one-off bug) → how ObservePoint helps (named modules, an outcome, an honest scope note) → CTA (request a demo / read the deeper guide). 600–1,200 words, one persona, one takeaway. The web-governance angle is the part that separates an ObservePoint blog from a generic martech blog: every problem is reframed as "this keeps happening because no one is watching the website continuously."

### How-to guide

Goal stated up front → prerequisites → numbered steps with the exact product names and click-paths or Rule/API snippets → "how you know it worked" (the verification step) → limitations/caveats → next step. Grounded in the relevant specialist skill's mechanics; don't improvise click-paths or invent a setting. If the guide involves Rules, Journeys, or the API, pull the actual mechanics from `analytics-validation`, `journeys-testing`, or `api-strategy` rather than guessing.

### One-pager

Headline (the outcome, not the feature) → the problem (2–3 sentences) → the approach (how ObservePoint addresses it, named modules) → proof points (placeholder — real numbers or none) → CTA. Fits on one page; every line earns its place. This is the format most likely to be handed to a budget owner, so the no-fabrication rule (section 5) is strictest here.

### Thought-leadership

A point of view on where web governance is going — regulatory pressure, consent enforcement, accessibility litigation, AI-driven martech sprawl. Opens with a tension, argues a position, grounds it in the domain, lands a "so what." ObservePoint appears as the *lens*, not the hard sell — at most a soft close. The credibility comes from the domain depth, so this format leans hardest on the specialist skills for evidence.

## 4. Evidence and citation discipline

Every claim in a draft must be groundable. This skill does not invent domain facts — it pulls them from the specialist skills and cites ObservePoint capabilities accurately. Map the claim to its source:

- **Regulation claims** — does GDPR / CCPA / a U.S. state law apply, what it requires → ground in the `regulation` skill. Keep the framing at "evidence and validation."
- **Tag / pixel claims** — what a vendor is, its category, its risk tier → ground in the `tags` skill.
- **Analytics-correctness claims** — events, data layer, value integrity, dedup, the Rules that prove it → ground in the `analytics-validation` skill.
- **Consent / CMP claims** — does Reject-All block, Consent Mode v2 propagation, banner behavior, pre-consent firing → ground in the `consent-cmp` skill.
- **Litigation claims** — CIPA, VPPA, BIPA, ECPA, session-replay, healthcare-pixel → ground in the `litigation-defense` skill.
- **Accessibility claims** — WCAG, ADA, Section 508, EAA, impact ranking → ground in the `accessibility` skill.
- **Product capability and scope** — what a module does, and its honest limits → ground in the shared `references/products-and-modules.md` and `references/limitations.md`.

When you assert a capability, name the module the way the platform names it (section 1). When you assert a domain fact, it should trace to one of those skills, not to your own recall. If a piece spans several domains, consult each owning skill rather than improvising across them.

## 5. The no-fabrication rule

This is the hard line for an OUTPUT skill that produces external-facing content:

- **Never invent customers.** No named logos, no "Company X saw…" unless the user supplies a real, permitted reference. Default to "a Fortune 500 retailer" or "a large healthcare provider," matching `references/verbiage-and-messaging.md`.
- **Never invent pricing.** ObservePoint pricing is custom. Direct the reader to "request a demo" or "contact sales." No dollar figures, no "starting at," no tier names.
- **Never invent statistics.** No made-up percentages, ROI figures, breach counts, or "studies show." If a claim needs a number, mark it `[SOURCE NEEDED: …]` and leave the sourcing to a human with a real citation.
- **Never invent roadmap dates, MCP tool names, or unverifiable claims.** If you can't trace it to a specialist skill or a public ObservePoint source, flag it rather than write it as fact.

A draft that ships with `[SOURCE NEEDED]` markers is a success — it tells the human exactly what to verify. A draft with confident invented numbers is a liability. When the user pushes for a hard statistic you don't have, hold the line: offer the marker, not a guess.

## 6. Humanizer pairing

AI-drafted content carries tells — inflated symbolism, the rule of three, em-dash overuse, vague attributions ("studies suggest," "industry experts"), promotional adjectives, and negative parallelisms ("not just X, but Y"). After you produce a draft, **explicitly recommend running the `humanizer` skill** over it, and offer to do so. The workflow:

1. **Draft** from the matching `assets/` template, grounded in the specialist skills (section 4).
2. **Run `humanizer`** to strip the AI tells.
3. **Hand back** the de-AI-ed draft with any `[SOURCE NEEDED]` markers intact.

Note this pairing in the hand-off so the user knows the draft is a first pass, not a final. The `humanizer` step is a default part of the workflow, not an optional extra.

## 7. Giving feedback on a draft

When the user brings an existing draft instead of asking for a new one, critique against the same standards: voice (section 1), audience fit (section 2), structure (section 3), groundability (section 4), and the no-fabrication rule (section 5).

Flag every claim that can't be traced, every invented number or customer, every off-voice phrase ("tag manager," "achieves compliance"). Then offer to run `humanizer` on it. Be specific and quote the line: "tighten the intro" is not feedback; "this stat needs a `[SOURCE NEEDED]` marker — we don't have a public figure for it" is. Rank the fixes — voice and fabrication issues first (they're publish-blockers), structure and polish second.

*Last verified: 2026-06-04*
