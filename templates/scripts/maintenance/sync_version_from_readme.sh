#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Templates.Scripts
# INGROUP: MokoStandards.Templates
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/maintenance/sync_version_from_readme.sh
# VERSION: XX.YY.ZZ
# BRIEF: Reads VERSION from README.md and propagates it to all badges and FILE INFORMATION headers
# NOTE: README.md is the single source of truth for the project version.
#       Copy this script to api/maintenance/ or scripts/maintenance/ in the target repo.
#       For automated on-merge propagation, pair with the sync-version-on-merge.yml.template workflow.

set -euo pipefail

# ── Colour helpers ─────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ── Options ────────────────────────────────────────────────────────────────
DRY_RUN=false
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

while [[ $# -gt 0 ]]; do
	case $1 in
		--dry-run)  DRY_RUN=true; shift ;;
		--path)     REPO_ROOT="$2"; shift 2 ;;
		--help|-h)
			echo "Usage: $0 [--dry-run] [--path <repo-root>]"
			echo ""
			echo "  --dry-run   Show what would change without writing files"
			echo "  --path DIR  Repository root (default: two levels above this script)"
			exit 0
			;;
		*) echo -e "${RED}Unknown option: $1${NC}"; exit 2 ;;
	esac
done

README="${REPO_ROOT}/README.md"

# ── Extract version from README.md ─────────────────────────────────────────
if [ ! -f "$README" ]; then
	echo -e "${RED}✗ README.md not found at ${README}${NC}"
	exit 1
fi

TARGET_VERSION=$(grep -oP '^\s*VERSION:\s*\K[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$README" | head -1)

if [ -z "$TARGET_VERSION" ]; then
	echo -e "${RED}✗ Could not find VERSION in README.md FILE INFORMATION block${NC}"
	echo "  Expected format:  VERSION: XX.YY.ZZ  (inside the <!-- --> comment)"
	exit 1
fi

# ── Banner ─────────────────────────────────────────────────────────────────
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Version Sync from README${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Source:  ${YELLOW}README.md${NC} (single source of truth)"
echo -e "Version: ${YELLOW}${TARGET_VERSION}${NC}"
$DRY_RUN && echo -e "${YELLOW}  DRY RUN — no files will be written${NC}"
echo ""

# ── Replacement patterns ────────────────────────────────────────────────────
# Markdown badge
BADGE_PATTERN='s|\(https://img\.shields\.io/badge/MokoStandards-[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]-|(https://img.shields.io/badge/MokoStandards-'"${TARGET_VERSION}"'-|g'
# FILE INFORMATION VERSION (generic: Markdown, YAML, Shell, Python, Terraform)
VERSION_GENERIC='s|^\(\s*VERSION:\s*\)[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]|\1'"${TARGET_VERSION}"'|'
# FILE INFORMATION VERSION (PHP:  * VERSION: OLD)
VERSION_PHP='s|^\(\s*\*\s*VERSION:\s*\)[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]|\1'"${TARGET_VERSION}"'|'
# composer.json "version" key
VERSION_JSON='s|"version":\s*"[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]"|"version": "'"${TARGET_VERSION}"'"|'

UPDATED_COUNT=0

# ── Helpers ─────────────────────────────────────────────────────────────────
_checksum() { md5sum "$1" 2>/dev/null | awk '{print $1}'; }

update_file() {
	local file="$1" before after
	before=$(_checksum "$file")
	case "${file##*.}" in
		md)
			sed -i "${VERSION_GENERIC}" "$file"
			sed -i "${BADGE_PATTERN}" "$file"
			;;
		php)
			sed -i "${VERSION_PHP}" "$file"
			;;
		yml|yaml|sh|ps1|py|tf)
			sed -i "${VERSION_GENERIC}" "$file"
			;;
		json)
			sed -i "${VERSION_JSON}" "$file"
			;;
		*) return ;;
	esac
	after=$(_checksum "$file")
	if [ "$before" != "$after" ]; then
		UPDATED_COUNT=$((UPDATED_COUNT + 1))
		echo -e "  ${GREEN}✓${NC} ${file#"${REPO_ROOT}/"}"
	fi
}

preview_file() {
	local file="$1" ext="${1##*.}" hit=false
	case "$ext" in
		md)
			grep -qP '^\s*VERSION:\s*[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && hit=true
			grep -qP 'img\.shields\.io/badge/MokoStandards-[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && hit=true
			;;
		php)
			grep -qP '^\s*\*\s*VERSION:\s*[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && hit=true
			;;
		yml|yaml|sh|ps1|py|tf)
			grep -qP '^\s*#\s*VERSION:\s*[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && hit=true
			;;
		json)
			grep -qP '"version":\s*"[0-9]{2}\.[0-9]{2}\.[0-9]{2}"' "$file" 2>/dev/null && hit=true
			;;
	esac
	if $hit; then
		UPDATED_COUNT=$((UPDATED_COUNT + 1))
		echo -e "  ${YELLOW}~${NC} ${file#"${REPO_ROOT}/"}"
	fi
}

# ── Walk the repo ───────────────────────────────────────────────────────────
EXCLUDES=(-not -path "*/vendor/*" -not -path "*/.git/*" \
          -not -path "*/node_modules/*" -not -path "*/logs/*")

while IFS= read -r -d '' file; do
	if $DRY_RUN; then
		preview_file "$file"
	else
		update_file "$file"
	fi
done < <(find "$REPO_ROOT" -type f \
	\( -name "*.md"  -o -name "*.php" -o -name "*.yml"  -o -name "*.yaml" \
	   -o -name "*.sh" -o -name "*.ps1" -o -name "*.py"  -o -name "*.tf" \
	   -o -name "*.json" -o -name "*.md.template" -o -name "*.yml.template" \) \
	"${EXCLUDES[@]}" -print0)

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
if $DRY_RUN; then
	echo -e "${GREEN}  Dry Run Complete${NC}"
	echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
	echo -e "Files that would be updated: ${YELLOW}${UPDATED_COUNT}${NC}"
	echo ""
	echo "Run without --dry-run to apply changes."
else
	echo -e "${GREEN}  Sync Complete${NC}"
	echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
	echo -e "Files updated: ${YELLOW}${UPDATED_COUNT}${NC}"
	echo -e "Version:       ${YELLOW}${TARGET_VERSION}${NC}"
	echo ""
	echo "Next steps:"
	echo "  git diff && git add -A && git commit -m \"chore(version): sync to ${TARGET_VERSION}\""
fi
echo ""
