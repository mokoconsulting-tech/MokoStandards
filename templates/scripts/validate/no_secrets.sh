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
# PATH: /templates/scripts/validate/no_secrets.sh
# VERSION: 01.00.00
# BRIEF: Checks for potential secrets in committed files
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

echo "[INFO] Checking for potential secrets..."

SECRETS_FOUND=0

# Check for common secret patterns
while IFS= read -r file; do
  if grep -iE '(password|api[_-]?key|secret|token|private[_-]?key)\s*[:=]\s*["\x27][^\x27"]{8,}' "$file" >/dev/null 2>&1; then
    echo "[WARN] Potential secret pattern in: $file"
    SECRETS_FOUND=1
  fi
done < <(git ls-files 2>/dev/null | grep -vE '\.(jpg|jpeg|png|gif|pdf|zip|tar|gz)$' || true)

if [ "$SECRETS_FOUND" -eq 0 ]; then
  echo "[OK] No obvious secrets detected"
  exit 0
else
  echo "[WARN] Potential secrets detected. Review manually."
  exit 0
fi
