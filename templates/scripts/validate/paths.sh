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
# PATH: /templates/scripts/validate/paths.sh
# VERSION: 01.00.00
# BRIEF: Validates that path separators use forward slashes
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

echo "[INFO] Checking for backslash path separators..."

# Find files with backslash path separators
BACKSLASH_FOUND=0

while IFS= read -r file; do
  if grep -E '\\\\' "$file" | grep -vE '(\\\\n|\\\\t|\\\\r|\\\\"|\\\\\\|namespace)' >/dev/null 2>&1; then
    echo "[WARN] Potential backslash path separator in: $file"
    BACKSLASH_FOUND=1
  fi
done < <(git ls-files '*.xml' '*.json' '*.yml' '*.yaml' '*.md' 2>/dev/null || true)

if [ "$BACKSLASH_FOUND" -eq 0 ]; then
  echo "[OK] No backslash path separators found"
  exit 0
else
  echo "[WARN] Backslash separators detected. Review manually."
  exit 0
fi
