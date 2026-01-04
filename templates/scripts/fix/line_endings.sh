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
