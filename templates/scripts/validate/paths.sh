#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
