---
description: Build a Day-1 onboarding checklist for an industry and domain
argument-hint: "<industry> <domain>"
allowed-tools: [Read, Glob, Grep]
---

# /op-onboarding-checklist

## Arguments

Two values from $ARGUMENTS: the customer's industry (e.g. retail-ecommerce, financial-services-insurance, media-publishing) and their primary domain. If the industry is ambiguous, ask before proceeding.

## Instructions

1. Load `skills/observepoint-consultant/references/lifecycle-and-maturity.md` and `skills/observepoint-consultant/references/industries/<industry>.md` (resolve `<industry>` to the matching reference file).
2. Combine the generic Day-1 onboarding milestones from the lifecycle reference with the industry-specific priorities (key audits, Rules, Privacy Reports, and use cases) from the industry reference.
3. Tailor the checklist to the supplied domain.
4. Return an ordered Day-1 checklist with each item's owner, the ObservePoint setup it produces, and the success criterion.

## Example Usage

```
/op-onboarding-checklist retail-ecommerce example.com
/op-onboarding-checklist financial-services-insurance bank.example.com
```
