#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/ .
#
# FILE INFORMATION
# DEFGROUP: Release
# INGROUP: Moko-Cassiopeia
# PATH: scripts/release/update_dates.sh
# VERSION: 03.05.00
# BRIEF: Normalize dates in release files

set -euo pipefail

# Dry-run flag
DRY_RUN=false

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Restore positional parameters
set -- "${POSITIONAL_ARGS[@]+"${POSITIONAL_ARGS[@]}"}"

# Accept date and version as arguments (after filtering out --dry-run)
TODAY="${1:-$(date +%Y-%m-%d)}"
VERSION="${2:-unknown}"

# Validate date format (YYYY-MM-DD)
if ! [[ "${TODAY}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "ERROR: Invalid date format '${TODAY}'. Expected YYYY-MM-DD format."
  exit 1
fi

echo "Date normalization script running..."
echo "TODAY: ${TODAY}"
echo "VERSION: ${VERSION}"

# Escape special regex characters in VERSION for safe use in grep and sed
# Escapes: ] \ / $ * . ^ [
VERSION_ESCAPED=$(printf '%s\n' "${VERSION}" | sed 's/[][\/$*.^]/\\&/g')

# Update CHANGELOG.md - replace the date on the version heading line
if [ -f "CHANGELOG.md" ]; then
  # Match lines like "## [03.05.00] 2026-01-04" and update the date
  if grep -q "^## \[${VERSION_ESCAPED}\] " CHANGELOG.md; then
    if [ "$DRY_RUN" = true ]; then
      echo "[DRY-RUN] Would update CHANGELOG.md version [${VERSION}] date to ${TODAY}"
    else
      sed -i "s/^## \[${VERSION_ESCAPED}\] [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/## [${VERSION_ESCAPED}] ${TODAY}/" CHANGELOG.md
      echo "✓ Updated CHANGELOG.md version [${VERSION}] date to ${TODAY}"
    fi
  else
    echo "⚠ Warning: CHANGELOG.md does not contain version [${VERSION}] heading"
  fi
else
  echo "⚠ Warning: CHANGELOG.md not found"
fi

# Update src/templates/templateDetails.xml - replace the <creationDate> tag
if [ -f "src/templates/templateDetails.xml" ]; then
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would update src/templates/templateDetails.xml creationDate to ${TODAY}"
  else
    sed -i "s|<creationDate>[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}</creationDate>|<creationDate>${TODAY}</creationDate>|" src/templates/templateDetails.xml
    echo "✓ Updated src/templates/templateDetails.xml creationDate to ${TODAY}"
  fi
else
  echo "⚠ Warning: src/templates/templateDetails.xml not found"
fi

# Update updates.xml - replace the <creationDate> tag
if [ -f "updates.xml" ]; then
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would update updates.xml creationDate to ${TODAY}"
  else
    sed -i "s|<creationDate>[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}</creationDate>|<creationDate>${TODAY}</creationDate>|" updates.xml
    echo "✓ Updated updates.xml creationDate to ${TODAY}"
  fi
else
  echo "⚠ Warning: updates.xml not found"
fi

echo "Date normalization complete."
