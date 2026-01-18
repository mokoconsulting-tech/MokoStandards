#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
