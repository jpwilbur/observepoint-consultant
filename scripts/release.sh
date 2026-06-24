#!/usr/bin/env bash
#
# release.sh — build the versioned .plugin and publish it to the shared drive.
# Safe to run by hand; also invoked by the git hook on a version bump.
#
# Usage: scripts/release.sh [--dry-run] [--force]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PLUGIN_SUBDIR="${PLUGIN_SUBDIR:-}"
DRIVE_FOLDER="${OP_PLUGIN_DRIVE_FOLDER:-ObservePoint Consultant}"
SLACK_NAME="${OP_RELEASE_DISPLAY_NAME:-ObservePoint Consultant}"
SLACK_FOLDER_URL="${OP_RELEASE_FOLDER_URL:-https://drive.google.com/drive/folders/1dxAAaaqFaQK2JCfZ_AMMsXPlmMeF65-e}"

DRY=""; FORCE=""
for a in "$@"; do
  case "$a" in
    --dry-run) DRY="--dry-run" ;;
    --force)   FORCE="--force" ;;
    *) echo "Unknown arg: $a" >&2; exit 2 ;;
  esac
done

PYTHON="${PYTHON:-/opt/homebrew/bin/python3}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python3

# 1. Build (writes dist/<name>-<version>.plugin).
PLUGIN_SUBDIR="$PLUGIN_SUBDIR" PYTHON="$PYTHON" bash "$ROOT/scripts/build_plugin.sh"

# 2. Resolve the artifact path from the manifest.
if [ -n "$PLUGIN_SUBDIR" ]; then MANIFEST="$PLUGIN_SUBDIR/.claude-plugin/plugin.json"; else MANIFEST=".claude-plugin/plugin.json"; fi
NAME="$("$PYTHON" -c "import json;print(json.load(open('$MANIFEST'))['name'])")"
VERSION="$("$PYTHON" -c "import json;print(json.load(open('$MANIFEST')).get('version','0.0.0'))")"
ARTIFACT="$ROOT/dist/${NAME}-${VERSION}.plugin"

# 3. Publish to the shared drive (and announce on Slack on a real publish).
"$PYTHON" "$ROOT/scripts/publish_to_drive.py" "$ARTIFACT" --folder "$DRIVE_FOLDER" \
  --notify --name "$SLACK_NAME" --folder-url "$SLACK_FOLDER_URL" $DRY $FORCE
