#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts.Maintenance
# INGROUP: MokoStandards
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /api/maintenance/sync_version_numbers.sh
# VERSION: XX.YY.ZZ
# BRIEF: Synchronize version numbers across all repository files from README.md (single source of truth)
# NOTE: Version is read dynamically from the FILE INFORMATION block in README.md.
#       Version format is zero-padded semver: XX.YY.ZZ (e.g. 04.00.03). All regex patterns
#       enforce exactly two digits per component by design.
#       For automated propagation on merge, see .github/workflows/sync-version-on-merge.yml

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
		--dry-run)      DRY_RUN=true; shift ;;
		--path)         REPO_ROOT="$2"; shift 2 ;;
		--help|-h)
			echo "Usage: $0 [--dry-run] [--path <repo-root>]"
			echo ""
			echo "  --dry-run   Show what would change without writing files"
			echo "  --path DIR  Repository root (default: auto-detected)"
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
	echo "  Expected format:  VERSION: XX.YY.ZZ"
	exit 1
fi

# ── Banner ─────────────────────────────────────────────────────────────────
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Version Number Synchronization${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Source:  ${YELLOW}README.md${NC} (single source of truth)"
echo -e "Version: ${YELLOW}${TARGET_VERSION}${NC}"
echo -e "Root:    ${YELLOW}${REPO_ROOT}${NC}"
if $DRY_RUN; then
	echo -e "${YELLOW}  DRY RUN — no files will be written${NC}"
fi
echo ""

# ── Badge pattern (Markdown) ────────────────────────────────────────────────
BADGE_PATTERN='s|\(https://img\.shields\.io/badge/MokoStandards-[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]-|(https://img.shields.io/badge/MokoStandards-'"${TARGET_VERSION}"'-|g'

# ── VERSION field patterns (per file type) ──────────────────────────────────
# Markdown/YAML/Shell:  VERSION: OLD  →  VERSION: NEW
VERSION_GENERIC='s|^\(\s*VERSION:\s*\)[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]|\1'"${TARGET_VERSION}"'|'
# PHP:  * VERSION: OLD  →  * VERSION: NEW
VERSION_PHP='s|^\(\s*\*\s*VERSION:\s*\)[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]|\1'"${TARGET_VERSION}"'|'
# composer.json:  "version": "OLD"  →  "version": "NEW"
VERSION_JSON='s|"version":\s*"[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]"|"version": "'"${TARGET_VERSION}"'"|'

UPDATED_COUNT=0

# ── Helper: update a single file ───────────────────────────────────────────
update_file() {
	local file="$1"
	local before
	before=$(md5sum "$file" 2>/dev/null | awk '{print $1}')

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
		*)
			return
			;;
	esac

	local after
	after=$(md5sum "$file" 2>/dev/null | awk '{print $1}')
	if [ "$before" != "$after" ]; then
		UPDATED_COUNT=$((UPDATED_COUNT + 1))
		echo -e "  ${GREEN}✓${NC} ${file#"${REPO_ROOT}/"}"
	fi
}

update_file_dry() {
	local file="$1"
	local rel="${file#"${REPO_ROOT}/"}"
	local ext="${file##*.}"
	local has_version=false

	case "$ext" in
		md)
			grep -qP '^\s*VERSION:\s*[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && has_version=true
			grep -qP 'img\.shields\.io/badge/MokoStandards-[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && has_version=true
			;;
		php)
			grep -qP '^\s*\*\s*VERSION:\s*[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && has_version=true
			;;
		yml|yaml|sh|ps1|py|tf)
			grep -qP '^\s*#\s*VERSION:\s*[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$file" 2>/dev/null && has_version=true
			;;
		json)
			grep -qP '"version":\s*"[0-9]{2}\.[0-9]{2}\.[0-9]{2}"' "$file" 2>/dev/null && has_version=true
			;;
	esac

	if $has_version; then
		UPDATED_COUNT=$((UPDATED_COUNT + 1))
		echo -e "  ${YELLOW}~${NC} ${rel}  (would update)"
	fi
}

# ── Walk the repo ───────────────────────────────────────────────────────────
EXCLUDES=(-not -path "*/vendor/*" -not -path "*/.git/*" \
          -not -path "*/node_modules/*" -not -path "*/logs/*")

while IFS= read -r -d '' file; do
	if $DRY_RUN; then
		update_file_dry "$file"
	else
		update_file "$file"
	fi
done < <(find "$REPO_ROOT" -type f \
	\( -name "*.md" -o -name "*.php" -o -name "*.yml" -o -name "*.yaml" \
	   -o -name "*.sh" -o -name "*.ps1" -o -name "*.py" -o -name "*.tf" \
	   -o -name "*.json" -o -name "*.md.template" -o -name "*.yml.template" \
	   -o -name "*.sh.template" \) \
	"${EXCLUDES[@]}" -print0)

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
if $DRY_RUN; then
	echo -e "${GREEN}  Dry Run Complete${NC}"
	echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
	echo ""
	echo -e "Files that would be updated: ${YELLOW}${UPDATED_COUNT}${NC}"
	echo ""
	echo "To apply changes, run without --dry-run:"
	echo "  $0 --path ${REPO_ROOT}"
else
	echo -e "${GREEN}  Version Synchronization Complete${NC}"
	echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
	echo ""
	echo -e "Files updated: ${YELLOW}${UPDATED_COUNT}${NC}"
	echo -e "Version:       ${YELLOW}${TARGET_VERSION}${NC}"
	echo ""
	echo "Next steps:"
	echo "  1. Review changes: git diff"
	echo "  2. Commit:         git add -A && git commit -m \"chore(version): sync to ${TARGET_VERSION}\""
	echo "  3. Push:           git push"
fi
echo ""
