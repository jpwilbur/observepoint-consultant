#!/usr/bin/env bash
#
# build_plugin.sh — build a Cowork-uploadable `.plugin` bundle from committed HEAD.
#
# Why this script exists:
#   A `.plugin` file is just a ZIP of the plugin directory with
#   `.claude-plugin/plugin.json` at the ZIP ROOT. (It is NOT a `.dxt` — that
#   format is for MCP servers / desktop extensions.) Cowork's "install plugin
#   via upload" path accepts this file.
#
#   THE TRAP: this repo is ALSO a self-hosted marketplace, so `.claude-plugin/`
#   contains BOTH `plugin.json` and `marketplace.json`. If `marketplace.json` is
#   left in the uploaded zip, Cowork (and `claude plugin validate`) classify the
#   artifact as a MARKETPLACE, not a plugin — and the upload fails with
#   "Plugin validation failed." So we export the committed tree, delete
#   `marketplace.json`, validate that it now reads as a plugin, then zip it.
#
# Usage:
#   scripts/build_plugin.sh [output-path]
#     output-path   optional; defaults to dist/<plugin-name>.plugin
#                   e.g. scripts/build_plugin.sh ~/Downloads/observepoint-consultant.plugin
#
# Notes:
#   - Builds from committed HEAD (reproducible release artifact), not the working
#     tree. Commit your changes first.
#   - An uploaded `.plugin` is a point-in-time copy and does NOT auto-update.
#     Re-run this and re-upload on each release, or use the org marketplace.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -f .claude-plugin/plugin.json ]; then
  echo "ERROR: .claude-plugin/plugin.json not found — run from inside the repo." >&2
  exit 1
fi

NAME="$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['name'])")"
VERSION="$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json')).get('version','0.0.0'))")"
OUT="${1:-$ROOT/dist/$NAME.plugin}"

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# 1. Export committed content (tracked files at HEAD; respects .gitignore, omits .git/)
git archive HEAD | tar -x -C "$STAGE"

# 2. Drop the marketplace manifest — it belongs to the GitHub-marketplace install
#    path only, and its presence makes the upload validate as a marketplace.
rm -f "$STAGE/.claude-plugin/marketplace.json"

# 3. Validate that it now reads as a PLUGIN (not a marketplace). Hard-fail otherwise.
if command -v claude >/dev/null 2>&1; then
  VALIDATION="$(claude plugin validate "$STAGE" 2>&1 || true)"
  echo "$VALIDATION"
  if ! grep -q "Validating plugin manifest" <<<"$VALIDATION"; then
    echo "ERROR: not classified as a plugin (did marketplace.json leak into the package?)." >&2
    exit 1
  fi
  if ! grep -q "Validation passed" <<<"$VALIDATION"; then
    echo "ERROR: plugin validation failed — see output above." >&2
    exit 1
  fi
else
  echo "WARN: 'claude' CLI not found on PATH; skipping validation step." >&2
fi

# 4. Package: zip the staged contents at root so .claude-plugin/plugin.json sits
#    at the ZIP root (required).
mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"
( cd "$STAGE" && zip -rq "$OUT" . -x '*.DS_Store' )

echo
echo "Built ${NAME} v${VERSION}"
echo "  -> ${OUT}"
echo
echo "Upload this file via Cowork's 'install plugin via upload'. Do NOT unzip or re-zip it."
