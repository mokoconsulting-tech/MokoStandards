#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
