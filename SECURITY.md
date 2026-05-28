# Security Policy

## Supported Versions

This is a knowledge-only Claude Code skill — it ships markdown documentation, not executable code. There is no runtime attack surface inside the skill itself. We still take security reporting seriously for the repository and its contents.

| Version | Supported |
|---------|-----------|
| `main`  | ✅        |
| Tagged releases (`v0.x`) | Latest only |

## Reporting a Vulnerability

If you find a security issue — for example, a malicious markdown payload, an outdated reference doc that leaks information, or a supply-chain concern — please report it privately:

- Email: **jarrod.wilbur@observepoint.com**
- Or open a [private GitHub Security Advisory](https://github.com/jpwilbur/observepoint-consultant/security/advisories/new)

Please do **not** open a public issue for security reports. We aim to acknowledge within 3 business days.

## What's out of scope

- Vulnerabilities in ObservePoint products themselves — report those to ObservePoint via [trust.observepoint.com](https://trust.observepoint.com/).
- Vulnerabilities in Claude Code itself — report those to Anthropic via [anthropic.com/security](https://www.anthropic.com/security).
- Vulnerabilities in the (forthcoming) ObservePoint MCP server — report those to ObservePoint.

## Secrets policy

This repository must never contain:

- API keys, tokens, or credentials of any kind
- Personally identifiable information
- Confidential ObservePoint customer data, pricing, or roadmap material

If you spot any such content in the repo, please report it via the channels above.
