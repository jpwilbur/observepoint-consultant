#!/usr/bin/env python3
"""Classify an ObservePoint tag inventory into category + risk + review flag.

Usage: python3 classify_tag_inventory.py inventory.json
inventory.json is a list of {"name": str, "domain": str} (e.g. from
get_tag_inventory). Output (stdout) is JSON: {"tags": [...], "summary": {...}}.
This is a heuristic first pass — the live authoritative catalog is list_tags;
the tags skill applies judgment on top. Categories: analytics, advertising,
social, session-replay, fingerprinting, tag-manager, consent, functional,
unknown. review=True for categories that warrant governance review.
"""
import json
import sys

SIGNATURES = [
    ("google-analytics", "analytics"),
    ("googletagmanager", "tag-manager"),
    ("analytics", "analytics"),
    ("adobe", "analytics"),
    ("omtrdc", "analytics"),
    ("facebook", "advertising"),
    ("fbcdn", "advertising"),
    ("doubleclick", "advertising"),
    ("googlesyndication", "advertising"),
    ("googleadservices", "advertising"),
    ("tiktok", "advertising"),
    ("criteo", "advertising"),
    ("taboola", "advertising"),
    ("bing", "advertising"),
    ("twitter", "social"),
    ("linkedin", "social"),
    ("pinterest", "social"),
    ("fullstory", "session-replay"),
    ("hotjar", "session-replay"),
    ("contentsquare", "session-replay"),
    ("mouseflow", "session-replay"),
    ("fingerprint", "fingerprinting"),
    ("onetrust", "consent"),
    ("cookielaw", "consent"),
    ("cookiebot", "consent"),
    ("trustarc", "consent"),
    ("usercentrics", "consent"),
]

RISK = {
    "advertising": "high",
    "session-replay": "high",
    "fingerprinting": "high",
    "social": "medium",
    "analytics": "medium",
    "tag-manager": "low",
    "consent": "low",
    "functional": "low",
    "unknown": "high",
}
REVIEW_CATEGORIES = {"advertising", "session-replay", "fingerprinting", "unknown"}


def classify_one(tag):
    hay = f"{tag.get('name','')} {tag.get('domain','')}".lower()
    category = "unknown"
    for sub, cat in SIGNATURES:
        if sub in hay:
            category = cat
            break
    return {
        "name": tag.get("name", ""),
        "domain": tag.get("domain", ""),
        "category": category,
        "risk": RISK[category],
        "review": category in REVIEW_CATEGORIES,
    }


def main():
    if len(sys.argv) != 2:
        print("usage: classify_tag_inventory.py inventory.json", file=sys.stderr)
        sys.exit(2)
    inv = json.loads(open(sys.argv[1]).read())
    tags = [classify_one(t) for t in inv]
    summary = {"total": len(tags), "review_count": sum(1 for t in tags if t["review"]), "by_category": {}}
    for t in tags:
        summary["by_category"][t["category"]] = summary["by_category"].get(t["category"], 0) + 1
    print(json.dumps({"tags": tags, "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
