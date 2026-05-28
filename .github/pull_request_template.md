## What & why

<!-- One paragraph: what does this PR change and why? Link related issues. -->

Closes #

## Scope

- [ ] `SKILL.md`
- [ ] Reference file(s): `references/...`
- [ ] Manifests (`plugin.json` / `marketplace.json`)
- [ ] Docs (`README.md`, `CONTRIBUTING.md`, etc.)
- [ ] Chore / meta

## Reference doc hygiene

- [ ] Updated `Last verified: YYYY-MM-DD` on every reference file I touched
- [ ] Sources cited are public (no internal-only or confidential material)
- [ ] No fabricated MCP tool names (any new MCP tool entry is marked `TBD pending GA` unless verified against the published server)

## Install test

Ran locally:

```
/plugin marketplace add /path/to/repo
/plugin install observepoint-consultant@observepoint-consultant
```

- [ ] `/plugin list` shows the plugin enabled
- [ ] Typing `/` shows `/observepoint-consultant` with the expected description
- [ ] A smoke-test prompt returns the canonical answer shape (goal → recommendation → next steps → limitations → citation)

## Notes for reviewer

<!-- Anything reviewers should focus on. -->
