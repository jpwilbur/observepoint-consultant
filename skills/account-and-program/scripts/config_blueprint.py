#!/usr/bin/env python3
"""Emit an ObservePoint account-configuration blueprint for a regulation.

Usage: python3 config_blueprint.py <regulation> [domain]
Prints JSON describing the audits, consent categories, and rule themes to set
up. Deterministic lookup; advisory only (the human applies it via the app/API).
"""
import json
import sys

BLUEPRINTS = {
    "ccpa": {
        "audits": [
            {"name": "Default Audit", "consent": "all categories", "purpose": "baseline"},
            {"name": "Opt-Out Audit", "consent": "Strictly Necessary only", "purpose": "pre-audit CMP Reject All"},
            {"name": "GPC Audit", "consent": "Strictly Necessary only", "purpose": "gpcEnabled + blockThirdPartyCookies"},
        ],
        "rule_themes": ["no advertising tags under opt-out", "GPC honored", "no sale/share pixels under opt-out"],
        "note": "Use setup_compliance_monitoring(regulation='ccpa') to create this three-audit pattern automatically.",
    },
    "gdpr": {
        "audits": [
            {"name": "Accept All Audit", "consent": "all categories", "purpose": "baseline"},
            {"name": "Reject All Audit", "consent": "Strictly Necessary only", "purpose": "pre-consent firing check"},
        ],
        "rule_themes": ["no non-essential tags before consent", "vendor inventory", "cookie classification"],
        "note": "ePrivacy + GDPR: the Reject-All audit is the core evidence.",
    },
    "hipaa": {
        "audits": [
            {"name": "PHI-URL Audit", "consent": "n/a", "purpose": "scan patient-facing URL patterns"},
        ],
        "rule_themes": ["no advertising tag on PHI URLs", "scan_audit_pii daily", "portal CMP suppression"],
        "note": "Pair with scan_audit_pii on patient-facing URLs.",
    },
}


def main():
    if len(sys.argv) < 2:
        print("usage: config_blueprint.py <regulation> [domain]", file=sys.stderr)
        sys.exit(2)
    reg = sys.argv[1].lower()
    domain = sys.argv[2] if len(sys.argv) > 2 else None
    if reg not in BLUEPRINTS:
        print(f"unknown regulation '{reg}'. known: {', '.join(sorted(BLUEPRINTS))}", file=sys.stderr)
        sys.exit(1)
    out = {"regulation": reg, "domain": domain, **BLUEPRINTS[reg]}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
