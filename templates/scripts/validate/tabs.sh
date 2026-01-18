#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: Validation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/validate/tabs.sh
# VERSION: 01.00.00
# BRIEF: Validates that no literal tab characters exist in source files
# NOTE: Template script for validation

set -euo pipefail

echo "[INFO] Checking for literal tab characters..."

# Find files with tabs (excluding binary files and specific extensions)
TABS_FOUND=0

while IFS= read -r file; do
  if grep -P '\t' "$file" >/dev/null 2>&1; then
    echo "[ERROR] Tabs found in: $file"
    TABS_FOUND=1
  fi
done < <(git ls-files '*.php' '*.js' '*.css' '*.xml' '*.yml' '*.yaml' '*.md' 2>/dev/null || true)

if [ "$TABS_FOUND" -eq 0 ]; then
  echo "[OK] No tabs found in source files"
  exit 0
else
  echo "[FAIL] Tab characters detected. Use spaces instead."
  exit 1
fi
