#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: Validation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/validate/version_alignment.sh
# VERSION: 01.00.00
# BRIEF: Validates version alignment across manifest files
# NOTE: Template script for validation

set -euo pipefail

echo "[INFO] Checking version alignment..."

# Extract versions from XML manifests
VERSIONS=()

while IFS= read -r file; do
  if grep -q "<extension" "$file" 2>/dev/null; then
    VERSION=$(grep -oP '<version>\K[^<]+' "$file" 2>/dev/null || true)
    if [ -n "$VERSION" ]; then
      VERSIONS+=("$file:$VERSION")
    fi
  fi
done < <(git ls-files '*.xml' 2>/dev/null || true)

if [ "${#VERSIONS[@]}" -eq 0 ]; then
  echo "[OK] No version manifests found (skipping)"
  exit 0
fi

# Check if all versions match
FIRST_VERSION=""
MISMATCH=0

for entry in "${VERSIONS[@]}"; do
  VERSION="${entry#*:}"
  if [ -z "$FIRST_VERSION" ]; then
    FIRST_VERSION="$VERSION"
  elif [ "$VERSION" != "$FIRST_VERSION" ]; then
    echo "[ERROR] Version mismatch: $entry (expected $FIRST_VERSION)"
    MISMATCH=1
  fi
done

if [ "$MISMATCH" -eq 0 ]; then
  echo "[OK] All versions aligned: $FIRST_VERSION"
  exit 0
else
  echo "[FAIL] Version alignment errors detected"
  exit 1
fi
