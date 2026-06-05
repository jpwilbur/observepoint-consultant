---
description: Walk through assembling technical evidence for a tracking-pixel class action or demand letter
argument-hint: "<statute> <domain>"
allowed-tools: [Read, Glob, Grep]
---

# /op-litigation-evidence-pack

## Arguments

Two values from $ARGUMENTS: the statute or theory at issue (e.g. CIPA, VPPA, wiretap, HIPAA-pixel) and the domain under scrutiny.

## Instructions

This produces technical evidence, not legal advice — coordinate with the customer's counsel.

1. Load the **litigation-defense** skill and its deep privacy-litigation-defense reference.
2. Locate the section for the supplied statute or theory and identify the relevant evidentiary signals (e.g. pen-register / wiretap data flows, video-pixel detection, PHI-bearing URLs).
3. Walk through assembling the technical evidence pack for the domain: which audits and Rules to run, which Privacy Reports and PII scans to export, and how to preserve audit history as a defensible timeline.
4. Return an ordered evidence-assembly plan, framing every artifact as technical findings to hand to counsel — never as a legal conclusion or outcome promise.

## Example Usage

```
/op-litigation-evidence-pack CIPA example.com
/op-litigation-evidence-pack VPPA video.example.com
```
