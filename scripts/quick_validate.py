#!/usr/bin/env python3
"""Structural validation for the observepoint-consultant plugin (multi-skill aware).

Discovers every skills/*/SKILL.md. Validates each skill's frontmatter and body
size, footers on every reference across all skills, the removed-tool guard and
casing across all skills + commands, and cross-reference resolution that accepts
either the owning skill's own references/ or the shared meta-skill references/.
Exit 0 on success, 1 on any failure. --staleness-days N prints (does not fail)
references older than N days.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
COMMANDS_DIR = REPO / "commands"
META_REFS = SKILLS_DIR / "observepoint-consultant" / "references"

REMOVED_TOOLS = [
    "assign_audit_consent_categories",
    "export_audit_run",
    "get_audit_locations",
]

errors = []


def skill_dirs():
    if not SKILLS_DIR.exists():
        return []
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def all_markdown():
    md = []
    if SKILLS_DIR.exists():
        md += list(SKILLS_DIR.rglob("*.md"))
    if COMMANDS_DIR.exists():
        md += list(COMMANDS_DIR.rglob("*.md"))
    return sorted(set(md))


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
    for d in skill_dirs():
        p = d / "SKILL.md"
        text = p.read_text()
        rel = p.relative_to(REPO)
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            errors.append(f"{rel}: no frontmatter block found")
            continue
        fm = m.group(1)
        keys = sorted(re.findall(r"^([A-Za-z0-9_-]+):", fm, re.MULTILINE))
        if keys != ["description", "name"]:
            errors.append(f"{rel}: frontmatter keys must be exactly [description, name], got {keys}")
        desc_m = re.search(r"^description:\s*(.*)$", fm, re.MULTILINE)
        if desc_m and len(desc_m.group(1)) > 1536:
            errors.append(f"{rel}: description {len(desc_m.group(1))} chars > 1536 cap")
        body = text[m.end():]
        if len(body.splitlines()) > 500:
            errors.append(f"{rel}: body {len(body.splitlines())} lines > 500 ceiling")


def check_footers():
    footer_re = re.compile(r"\*Last verified:\s*\d{4}-\d{2}-\d{2}\*")
    for d in skill_dirs():
        refs = d / "references"
        if not refs.exists():
            continue
        for p in sorted(refs.rglob("*.md")):
            if not footer_re.search(p.read_text()):
                errors.append(f"missing 'Last verified: YYYY-MM-DD' footer: {p.relative_to(REPO)}")


def check_removed_tools():
    for p in all_markdown():
        text = p.read_text()
        for tool in REMOVED_TOOLS:
            if tool in text:
                errors.append(f"removed MCP tool '{tool}' referenced in {p.relative_to(REPO)}")


def check_tool_prefix_casing():
    for p in all_markdown():
        if "mcp__observepoint__" in p.read_text():
            errors.append(f"lowercase 'mcp__observepoint__' in {p.relative_to(REPO)} (use mcp__ObservePoint__)")


def _owning_refs(p):
    """The references/ dir of the skill that contains file p, or None."""
    for d in skill_dirs():
        try:
            p.relative_to(d)
            return d / "references"
        except ValueError:
            continue
    return None


def check_cross_references():
    ref_re = re.compile(r"references/([A-Za-z0-9_./<>-]+\.md)")
    for p in all_markdown():
        owning = _owning_refs(p)
        for raw in ref_re.findall(p.read_text()):
            if "<" in raw or ">" in raw:
                continue  # placeholder like references/industries/<industry>.md
            bases = []
            if owning is not None:
                bases.append(owning)
            bases.append(META_REFS)
            if not any((b / raw).exists() for b in bases):
                errors.append(f"broken cross-reference 'references/{raw}' in {p.relative_to(REPO)}")


def check_staleness(days):
    today = date.today()
    date_re = re.compile(r"\*Last verified:\s*(\d{4})-(\d{2})-(\d{2})\*")
    for d in skill_dirs():
        refs = d / "references"
        if not refs.exists():
            continue
        for p in sorted(refs.rglob("*.md")):
            m = date_re.search(p.read_text())
            if not m:
                continue
            y, mo, dd = (int(x) for x in m.groups())
            age = (today - date(y, mo, dd)).days
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
