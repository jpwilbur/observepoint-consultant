# Contributing to observepoint-consultant

Thanks for considering a contribution. This skill is a living knowledge base — the most impactful contributions are usually new or refreshed entries in `skills/observepoint-consultant/references/`.

## Quick start

1. Fork the repo and create a feature branch off `main`:
   ```
   git checkout -b docs/add-<topic>
   ```
2. Make your change. Reference docs are plain markdown, one topic per file.
3. Update the `Last verified: YYYY-MM-DD` footer on any file you touched.
4. Open a PR using the provided template.

## Branch naming

We follow Conventional Commits and matching branch prefixes:

- `feat/<short-name>` — new behavior in `SKILL.md`
- `docs/<short-name>` — additions or edits to `references/`
- `fix/<short-name>` — corrections
- `chore/<short-name>` — meta changes (CI, docs, manifests)

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/). Examples:

```
docs(references): refresh privacy-and-compliance for India DPDPA
feat(skill): add MCP extension-point block to SKILL.md
fix(manifest): correct keyword spelling in marketplace.json
```

## Anthropic skill conventions we follow

This skill follows [Anthropic's first-party skill-creator patterns](https://github.com/anthropics/skills) verbatim. Specifically:

- `SKILL.md` frontmatter contains only `name` and `description`.
- The `description` is written in the "pushy" style Anthropic recommends to combat under-triggering — include the phrase `Use this skill whenever the user mentions …` with broad keyword coverage.
- SKILL.md body stays under 500 lines (Anthropic's stated ceiling). Long content lives in `references/`.
- Use imperative form. Explain *why*, don't lean on heavy-handed all-caps MUST/NEVER.
- Optional bundled directories follow Anthropic's anatomy: `scripts/` (executable), `references/` (loaded into context as needed), `assets/` (output templates).

## Style for reference docs

- One topic per file. Filename is kebab-case (e.g., `privacy-and-compliance.md`).
- Lead with a one-paragraph summary so Claude can decide whether to load deeper sections.
- Use tables for matrices (regulation × coverage, persona × playbook).
- Cite ObservePoint help-center URLs or official docs where possible.
- Add a `Last verified: YYYY-MM-DD` footer.

## Source rules

- **Public sources only** for facts about ObservePoint, its competitors, or its customers. The competitive doc has explicit rules of engagement at the top.
- **No internal pricing**, no roadmap inference, no claims sourced from confidential material.
- **No fabricated MCP tool names.** The MCP reference uses a `TBD pending GA` pattern; only add real tool names once they're verified against the published MCP server.

## PR review

A maintainer will check:

- Skill still installs and `/observepoint-consultant` appears in the picker.
- Smoke-test prompt grid still passes (see [`README.md`](./README.md) → Verification, once polished).
- `Last verified` dates updated on touched files.
- No license/trademark issues.

## Disclaimer

Contributions are accepted under the [MIT license](./LICENSE). By contributing you confirm you have the right to license your contribution under those terms and that nothing you contribute is confidential to ObservePoint, LLC or any other party.
