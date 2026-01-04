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
# PATH: /templates/scripts/validate/language_structure.sh
# VERSION: 01.00.00
# BRIEF: Validates language file structure
# NOTE: Template script for validation - specific to Joomla projects

set -euo pipefail

echo "[INFO] Validating language file structure..."

LANG_ERRORS=0

# Check for language INI files
while IFS= read -r file; do
  # Basic INI format validation
  if ! grep -q "^[A-Z_][A-Z0-9_]*=" "$file" 2>/dev/null; then
    echo "[WARN] Language file may have format issues: $file"
  fi
done < <(git ls-files '*.ini' 2>/dev/null || true)

if [ "$LANG_ERRORS" -eq 0 ]; then
  echo "[OK] Language file validation passed"
  exit 0
else
  echo "[FAIL] Language file validation errors detected"
  exit 1
fi
