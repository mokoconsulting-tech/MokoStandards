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
# PATH: /templates/scripts/maintenance/sync_dolibarr_readmes.sh
# VERSION: XX.YY.ZZ
# BRIEF: Keeps root README.md and src/README.md in sync for Dolibarr module repositories
# NOTE: Root README.md targets developers/contributors; src/README.md targets end users.
#       This script copies the end-user sections from root to src and updates the module
#       version in both files to match the FILE INFORMATION VERSION in root README.md.
#       Copy to api/maintenance/ or scripts/maintenance/ in the target Dolibarr module repo.

set -euo pipefail

# ── Colour helpers ─────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
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
			echo "  --dry-run   Preview changes without writing"
			echo "  --path DIR  Dolibarr module repo root (default: two levels above this script)"
			echo ""
			echo "What this script does:"
			echo "  1. Reads VERSION from root README.md FILE INFORMATION block"
			echo "  2. Updates the version badge in root README.md (if stale)"
			echo "  3. Regenerates src/README.md with:"
			echo "     - The same FILE INFORMATION header (audience: end-user)"
			echo "     - Module name and description pulled from root README.md"
			echo "     - Installation, Configuration, and Usage sections from root README.md"
			echo "     - Updated version reference"
			echo "  4. Updates the version badge in src/README.md"
			exit 0
			;;
		*) echo -e "${RED}Unknown option: $1${NC}"; exit 2 ;;
	esac
done

ROOT_README="${REPO_ROOT}/README.md"
SRC_README="${REPO_ROOT}/src/README.md"

# ── Validate ────────────────────────────────────────────────────────────────
if [ ! -f "$ROOT_README" ]; then
	echo -e "${RED}✗ Root README.md not found at ${ROOT_README}${NC}"
	exit 1
fi

if [ ! -d "${REPO_ROOT}/src" ]; then
	echo -e "${RED}✗ src/ directory not found — is this a Dolibarr module repository?${NC}"
	exit 1
fi

# ── Extract version from root README.md ────────────────────────────────────
VERSION=$(grep -oP '^\s*VERSION:\s*\K[0-9]{2}\.[0-9]{2}\.[0-9]{2}' "$ROOT_README" | head -1)
if [ -z "$VERSION" ]; then
	echo -e "${RED}✗ Could not find VERSION in root README.md FILE INFORMATION block${NC}"
	exit 1
fi

# ── Extract key fields from root README.md ─────────────────────────────────
# Module name: first H1 heading after the closing -->
MODULE_NAME=$(awk '/^-->/{found=1; next} found && /^# /{print substr($0,3); exit}' "$ROOT_README")
MODULE_NAME="${MODULE_NAME:-$(basename "$REPO_ROOT")}"

# REPO field from FILE INFORMATION block
REPO_URL=$(grep -oP '^\s*REPO:\s*\K\S+' "$ROOT_README" | head -1)
REPO_URL="${REPO_URL:-https://github.com/mokoconsulting-tech}"

# DEFGROUP for src README (end-user variant)
DEFGROUP=$(grep -oP '^\s*DEFGROUP:\s*\K.+' "$ROOT_README" | head -1)
DEFGROUP="${DEFGROUP:-MokoStandards.Module}"

# INGROUP
INGROUP=$(grep -oP '^\s*INGROUP:\s*\K.+' "$ROOT_README" | head -1)
INGROUP="${INGROUP:-MokoStandards}"

# BRIEF from root README (reuse for src)
BRIEF=$(grep -oP '^\s*BRIEF:\s*\K.+' "$ROOT_README" | head -1)
BRIEF="${BRIEF:-${MODULE_NAME} end-user documentation}"

# ── Extract shareable sections from root README.md ─────────────────────────
# Extract content between specific H2 headings that are relevant to end users.
# Sections copied: Installation, Configuration, Usage, Support (if present).
extract_section() {
	local heading="$1"
	local file="$2"
	# Extract from "## $heading" up to (but not including) the next "## " heading
	awk "
		/^## ${heading}/{found=1; print; next}
		found && /^## /{exit}
		found{print}
	" "$file"
}

INSTALL_SECTION=$(extract_section "Installation" "$ROOT_README")
CONFIG_SECTION=$(extract_section "Configuration" "$ROOT_README")
USAGE_SECTION=$(extract_section "Usage" "$ROOT_README")
SUPPORT_SECTION=$(extract_section "Support" "$ROOT_README")

# ── Banner ──────────────────────────────────────────────────────────────────
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Dolibarr README Sync${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Module:  ${CYAN}${MODULE_NAME}${NC}"
echo -e "Version: ${YELLOW}${VERSION}${NC}"
echo -e "Root:    ${YELLOW}${ROOT_README}${NC}"
echo -e "Src:     ${YELLOW}${SRC_README}${NC}"
$DRY_RUN && echo -e "${YELLOW}  DRY RUN — no files will be written${NC}"
echo ""

# ── Step 1: Update version badge + VERSION in root README.md ───────────────
echo -e "${CYAN}Step 1:${NC} Update root README.md badges and VERSION field..."

_update_root_readme() {
	local tmp
	tmp=$(mktemp)
	sed \
		-e 's|\(https://img\.shields\.io/badge/MokoStandards-\)[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]|\1'"${VERSION}"'|g' \
		-e 's|^\(\s*VERSION:\s*\)[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]|\1'"${VERSION}"'|' \
		"$ROOT_README" > "$tmp"
	if ! diff -q "$tmp" "$ROOT_README" > /dev/null 2>&1; then
		if $DRY_RUN; then
			echo -e "  ${YELLOW}~${NC} root README.md (would update version fields)"
		else
			mv "$tmp" "$ROOT_README"
			echo -e "  ${GREEN}✓${NC} root README.md updated"
		fi
	else
		echo -e "  ${GREEN}✓${NC} root README.md already current"
		rm -f "$tmp"
	fi
}

_update_root_readme

# ── Step 2: Generate / update src/README.md ────────────────────────────────
echo -e "${CYAN}Step 2:${NC} Sync src/README.md..."

TODAY=$(date -u '+%Y-%m-%d')

# Build the new src/README.md content
NEW_SRC_README=$(cat <<SRCREADME
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: ${DEFGROUP}
INGROUP: ${INGROUP}
REPO: ${REPO_URL}
PATH: /src/README.md
VERSION: ${VERSION}
BRIEF: ${BRIEF} — end-user documentation deployed with the module
NOTE: This file is auto-generated by sync_dolibarr_readmes.sh from root README.md.
      Edit the source sections in root README.md; do not edit this file directly.
      Last synced: ${TODAY}
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-${VERSION}-blue)](${REPO_URL})

# ${MODULE_NAME}

> **End-user documentation.** For developer and contributor documentation, see the root \`README.md\`.

SRCREADME
)

# Append extracted sections (skip empty ones)
if [ -n "$INSTALL_SECTION" ]; then
	NEW_SRC_README="${NEW_SRC_README}
${INSTALL_SECTION}"
fi

if [ -n "$CONFIG_SECTION" ]; then
	NEW_SRC_README="${NEW_SRC_README}
${CONFIG_SECTION}"
fi

if [ -n "$USAGE_SECTION" ]; then
	NEW_SRC_README="${NEW_SRC_README}
${USAGE_SECTION}"
fi

if [ -n "$SUPPORT_SECTION" ]; then
	NEW_SRC_README="${NEW_SRC_README}
${SUPPORT_SECTION}"
fi

NEW_SRC_README="${NEW_SRC_README}
---

*Documentation generated from root \`README.md\` — do not edit this file directly.*
"

# Compare with existing src/README.md
if [ -f "$SRC_README" ]; then
	EXISTING=$(cat "$SRC_README")
	if [ "$EXISTING" = "$NEW_SRC_README" ]; then
		echo -e "  ${GREEN}✓${NC} src/README.md already current"
	else
		if $DRY_RUN; then
			echo -e "  ${YELLOW}~${NC} src/README.md (would regenerate)"
			echo ""
			echo "  Diff preview:"
			diff <(echo "$EXISTING") <(echo "$NEW_SRC_README") | head -30 | sed 's/^/    /'
		else
			mkdir -p "$(dirname "$SRC_README")"
			echo "$NEW_SRC_README" > "$SRC_README"
			echo -e "  ${GREEN}✓${NC} src/README.md regenerated"
		fi
	fi
else
	if $DRY_RUN; then
		echo -e "  ${YELLOW}~${NC} src/README.md (would create — file does not exist)"
	else
		mkdir -p "$(dirname "$SRC_README")"
		echo "$NEW_SRC_README" > "$SRC_README"
		echo -e "  ${GREEN}✓${NC} src/README.md created"
	fi
fi

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
if $DRY_RUN; then
	echo -e "${GREEN}  Dry Run Complete${NC}"
	echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
	echo "Run without --dry-run to apply changes."
else
	echo -e "${GREEN}  Dolibarr README Sync Complete${NC}"
	echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
	echo -e "Module version: ${YELLOW}${VERSION}${NC}"
	echo ""
	echo "Next steps:"
	echo "  git diff && git add README.md src/README.md"
	echo "  git commit -m \"docs(readme): sync src/README.md from root for version ${VERSION}\""
fi
echo ""
