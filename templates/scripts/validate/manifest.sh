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
# PATH: /templates/scripts/validate/manifest.sh
# VERSION: 01.00.00
# BRIEF: Validates Joomla manifest structure
# NOTE: Template script for validation - specific to Joomla projects

set -euo pipefail

echo "[INFO] Validating Joomla manifests..."

MANIFEST_ERRORS=0

# Find Joomla manifest files
while IFS= read -r file; do
  if grep -q "<extension" "$file" 2>/dev/null; then
    # Check for required elements
    if ! grep -q "<version>" "$file"; then
      echo "[ERROR] Missing <version> in: $file"
      MANIFEST_ERRORS=1
    fi
    if ! grep -q "<description>" "$file"; then
      echo "[WARN] Missing <description> in: $file"
    fi
  fi
done < <(git ls-files '*.xml' 2>/dev/null || true)

if [ "$MANIFEST_ERRORS" -eq 0 ]; then
  echo "[OK] Manifest validation passed"
  exit 0
else
  echo "[FAIL] Manifest validation errors detected"
  exit 1
fi
