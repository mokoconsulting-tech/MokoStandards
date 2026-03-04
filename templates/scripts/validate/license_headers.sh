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
# PATH: /templates/scripts/validate/license_headers.sh
# VERSION: 01.00.00
# BRIEF: Validates license headers in source files
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

echo "[INFO] Checking for license headers..."

MISSING_HEADERS=0

while IFS= read -r file; do
  if ! head -n 20 "$file" | grep -q "SPDX-License-Identifier:"; then
    echo "[WARN] Missing SPDX license identifier: $file"
    MISSING_HEADERS=1
  fi
done < <(git ls-files '*.php' '*.js' '*.css' '*.sh' 2>/dev/null || true)

if [ "$MISSING_HEADERS" -eq 0 ]; then
  echo "[OK] All source files have license headers"
  exit 0
else
  echo "[WARN] Some files missing license headers (advisory)"
  exit 0
fi
