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
# PATH: /templates/scripts/validate/changelog.sh
# VERSION: 01.00.00
# BRIEF: Validates CHANGELOG.md structure and format
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

echo "[INFO] Validating CHANGELOG.md..."

if [ ! -f "CHANGELOG.md" ]; then
  echo "[ERROR] CHANGELOG.md not found"
  exit 1
fi

# Check for required header (new format: # CHANGELOG - RepoName (VERSION: X.Y.Z))
if ! grep -qE "^# CHANGELOG - .+ \(VERSION: [0-9]+\.[0-9]+\.[0-9]+\)" CHANGELOG.md; then
  echo "[ERROR] CHANGELOG.md missing required '# CHANGELOG - RepoName (VERSION: X.Y.Z)' header"
  exit 1
fi

# Check for [Unreleased] section
if ! grep -q "^## \[Unreleased\]" CHANGELOG.md; then
  echo "[ERROR] CHANGELOG.md missing required '## [Unreleased]' section"
  exit 1
fi

echo "[OK] CHANGELOG.md validation passed"
exit 0
