#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: Validation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/validate/changelog.sh
# VERSION: 01.00.00
# BRIEF: Validates CHANGELOG.md structure and format
# NOTE: Template script for validation

set -euo pipefail

echo "[INFO] Validating CHANGELOG.md..."

if [ ! -f "CHANGELOG.md" ]; then
  echo "[ERROR] CHANGELOG.md not found"
  exit 1
fi

# Check for required header
if ! grep -q "^# Changelog" CHANGELOG.md; then
  echo "[ERROR] CHANGELOG.md missing required '# Changelog' header"
  exit 1
fi

echo "[OK] CHANGELOG.md validation passed"
exit 0
