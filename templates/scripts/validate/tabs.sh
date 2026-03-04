#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
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

DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

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
