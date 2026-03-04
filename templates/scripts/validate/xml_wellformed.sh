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
# PATH: /templates/scripts/validate/xml_wellformed.sh
# VERSION: 01.00.00
# BRIEF: Validates XML files are well-formed
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
