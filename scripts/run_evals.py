#!/usr/bin/env python3
"""Validate evals/evals.json and print the prompt grid grouped by area.

Usage: python3 scripts/run_evals.py
Does NOT call any model — evaluation is performed by running the prompts
against the installed skill in a Claude session. Exit 0 if structure valid.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVALS = REPO / "evals" / "evals.json"
REQUIRED = {"id", "area", "prompt", "expected_output_summary", "must_include", "must_not_include"}


def main():
    data = json.loads(EVALS.read_text())
    evals = data.get("evals", [])
    errors = []
    seen_ids = set()
    for e in evals:
        missing = REQUIRED - set(e)
        if missing:
            errors.append(f"eval {e.get('id', '?')} missing fields: {sorted(missing)}")
        if e.get("id") in seen_ids:
            errors.append(f"duplicate eval id: {e.get('id')}")
        seen_ids.add(e.get("id"))
        if not isinstance(e.get("must_include", []), list):
            errors.append(f"eval {e.get('id')}: must_include must be a list")
    if errors:
        print("EVALS INVALID:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    by_area = defaultdict(list)
    for e in evals:
        by_area[e["area"]].append(e)
    print(f"{len(evals)} evals across {len(by_area)} areas\n")
    for area in sorted(by_area):
        print(f"## {area}")
        for e in by_area[area]:
            print(f"  [{e['id']}] {e['prompt']}")
        print()
    sys.exit(0)


if __name__ == "__main__":
    main()
