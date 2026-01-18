#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: Fix
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/fix/line_endings.sh
# VERSION: 01.00.00
# BRIEF: Fixes line endings to LF
# NOTE: Template script for automated fixes

set -euo pipefail

echo "[INFO] Fixing line endings to LF..."

FIXED_COUNT=0

while IFS= read -r file; do
  if file "$file" | grep -q "CRLF"; then
    dos2unix "$file" 2>/dev/null || sed -i 's/\r$//' "$file"
    echo "[FIXED] $file"
    FIXED_COUNT=$((FIXED_COUNT + 1))
  fi
done < <(git ls-files '*.php' '*.js' '*.css' '*.xml' '*.sh' '*.md' 2>/dev/null || true)

echo "[INFO] Fixed $FIXED_COUNT files"
exit 0
