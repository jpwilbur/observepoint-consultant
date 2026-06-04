#!/usr/bin/env python3
"""Diff a live `get_api_docs` dump against the documented MCP catalog.

Usage:
  python3 scripts/refresh_mcp_catalog.py < api_docs_dump.txt
  python3 scripts/refresh_mcp_catalog.py path/to/api_docs_dump.txt

Heuristic (the dump is free text), so it over-reports. Informational only;
never mutates files. Exists to make the quarterly refresh start from a diff.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "skills" / "observepoint-consultant" / "references" / "mcp-tools.md"

TOOL_RE = re.compile(r"mcp__ObservePoint__([a-z0-9_]+)")
BACKTICK_RE = re.compile(r"`([a-z][a-z0-9_]+)`")


def documented_tools():
    text = CATALOG.read_text()
    names = set(TOOL_RE.findall(text))
    names |= set(BACKTICK_RE.findall(text))
    return names


def dump_tools(dump_text):
    return set(re.findall(r"\b([a-z_]+_[a-z_]+)\b", dump_text))


def main():
    if len(sys.argv) > 1:
        dump_text = Path(sys.argv[1]).read_text()
    else:
        dump_text = sys.stdin.read()
    if not dump_text.strip():
        print("No input. Pipe `get_api_docs` output via stdin or pass a file path.")
        sys.exit(2)

    cat = documented_tools()
    dump = dump_tools(dump_text)

    missing_from_dump = sorted(t for t in cat if t not in dump)
    new_in_dump = sorted(t for t in dump if t not in cat and "_" in t)

    print("== Documented tools NOT found in dump (review for removal) ==")
    for t in missing_from_dump:
        print(f"  - {t}")
    print("\n== Tools in dump NOT documented (review for addition) ==")
    for t in new_in_dump:
        print(f"  + {t}")
    print("\nThis report is informational. Update mcp-tools.md by hand and bump its Last-verified date.")


if __name__ == "__main__":
    main()
