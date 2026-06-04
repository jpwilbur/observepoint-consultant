#!/usr/bin/env python3
"""Structural validation for the observepoint-consultant plugin.

Runs in CI on every PR. Exit 0 on success, 1 on any failure.
Optional: --staleness-days N prints (does not fail) reference files whose
Last-verified date is older than N days.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "skills" / "observepoint-consultant"
REFS = SKILL_DIR / "references"

REMOVED_TOOLS = [
    "assign_audit_consent_categories",
    "export_audit_run",
    "get_audit_locations",
]

errors = []


def check_manifests():
    for rel in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]:
        p = REPO / rel
        if not p.exists():
            errors.append(f"manifest missing: {rel}")
            continue
        try:
            json.loads(p.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"manifest invalid JSON {rel}: {e}")


def check_skill_frontmatter():
    p = SKILL_DIR / "SKILL.md"
    text = p.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append("SKILL.md: no frontmatter block found")
        return
    fm = m.group(1)
    keys = sorted(re.findall(r"^([A-Za-z0-9_-]+):", fm, re.MULTILINE))
    if keys != ["description", "name"]:
        errors.append(f"SKILL.md frontmatter keys must be exactly [description, name], got {keys}")
    desc_m = re.search(r"^description:\s*(.*)$", fm, re.MULTILINE)
    if desc_m and len(desc_m.group(1)) > 1536:
        errors.append(f"SKILL.md description {len(desc_m.group(1))} chars > 1536 cap")
    body = text[m.end():]
    body_lines = len(body.splitlines())
    if body_lines > 500:
        errors.append(f"SKILL.md body {body_lines} lines > 500 ceiling")


def check_footers():
    footer_re = re.compile(r"\*Last verified:\s*\d{4}-\d{2}-\d{2}\*")
    for p in sorted(REFS.rglob("*.md")):
        if not footer_re.search(p.read_text()):
            errors.append(f"missing 'Last verified: YYYY-MM-DD' footer: {p.relative_to(REPO)}")


def check_removed_tools():
    for p in sorted(SKILL_DIR.rglob("*.md")):
        text = p.read_text()
        for tool in REMOVED_TOOLS:
            if tool in text:
                errors.append(f"removed MCP tool '{tool}' referenced in {p.relative_to(REPO)}")


def check_tool_prefix_casing():
    for p in sorted(SKILL_DIR.rglob("*.md")):
        if "mcp__observepoint__" in p.read_text():
            errors.append(f"lowercase 'mcp__observepoint__' in {p.relative_to(REPO)} (use mcp__ObservePoint__)")


def check_cross_references():
    ref_re = re.compile(r"references/([A-Za-z0-9_./<>-]+\.md)")
    scan_dirs = [SKILL_DIR, REPO / "commands"]
    for base in scan_dirs:
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            for ref in ref_re.findall(p.read_text()):
                if "<" in ref or ">" in ref:
                    continue  # placeholder like references/industries/<industry>.md
                target = REFS / ref
                if not target.exists():
                    errors.append(f"broken cross-reference 'references/{ref}' in {p.relative_to(REPO)}")


def check_staleness(days):
    today = date.today()
    date_re = re.compile(r"\*Last verified:\s*(\d{4})-(\d{2})-(\d{2})\*")
    for p in sorted(REFS.rglob("*.md")):
        m = date_re.search(p.read_text())
        if not m:
            continue
        y, mo, d = (int(x) for x in m.groups())
        age = (today - date(y, mo, d)).days
        if age > days:
            print(f"STALE ({age}d): {p.relative_to(REPO)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--staleness-days", type=int, default=None)
    args = parser.parse_args()
    if args.staleness_days is not None:
        check_staleness(args.staleness_days)

    check_manifests()
    check_skill_frontmatter()
    check_footers()
    check_removed_tools()
    check_tool_prefix_casing()
    check_cross_references()
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("All checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
