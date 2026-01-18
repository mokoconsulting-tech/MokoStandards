#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: Validation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/validate/xml_wellformed.sh
# VERSION: 01.00.00
# BRIEF: Validates XML files are well-formed
# NOTE: Template script for validation

set -euo pipefail

echo "[INFO] Validating XML files..."

XMLLINT_ERRORS=0

while IFS= read -r file; do
  if ! xmllint --noout "$file" 2>/dev/null; then
    echo "[ERROR] XML validation failed: $file"
    XMLLINT_ERRORS=1
  fi
done < <(git ls-files '*.xml' 2>/dev/null || true)

if [ "$XMLLINT_ERRORS" -eq 0 ]; then
  echo "[OK] All XML files are well-formed"
  exit 0
else
  echo "[FAIL] XML validation errors detected"
  exit 1
fi
