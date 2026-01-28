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
# PATH: /templates/scripts/validate/php_syntax.sh
# VERSION: 01.00.00
# BRIEF: Validates PHP syntax
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

echo "[INFO] Validating PHP syntax..."

PHP_ERRORS=0

while IFS= read -r file; do
  if ! php -l "$file" >/dev/null 2>&1; then
    echo "[ERROR] PHP syntax error: $file"
    PHP_ERRORS=1
  fi
done < <(git ls-files '*.php' 2>/dev/null || true)

if [ "$PHP_ERRORS" -eq 0 ]; then
  echo "[OK] All PHP files have valid syntax"
  exit 0
else
  echo "[FAIL] PHP syntax errors detected"
  exit 1
fi
