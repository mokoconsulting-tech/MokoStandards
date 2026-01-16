#!/bin/bash
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Templates.Scripts
# INGROUP: MokoStandards.Templates
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/validate/structure.sh
# VERSION: 01.00.00
# BRIEF: Repository structure validation script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==================================="
echo "Repository Structure Validation"
echo "==================================="
echo ""

# Check required directories
REQUIRED_DIRS=("docs" "scripts" ".github/workflows")
MISSING_DIRS=()

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        MISSING_DIRS+=("$dir")
        echo -e "${RED}✗${NC} Missing required directory: $dir"
    else
        echo -e "${GREEN}✓${NC} Found directory: $dir"
    fi
done

# Check required files
REQUIRED_FILES=("README.md" "LICENSE" "CHANGELOG.md" "CONTRIBUTING.md" "SECURITY.md")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
        echo -e "${RED}✗${NC} Missing required file: $file"
    else
        echo -e "${GREEN}✓${NC} Found file: $file"
    fi
done

echo ""
echo "==================================="
echo "Validation Summary"
echo "==================================="

if [ ${#MISSING_DIRS[@]} -eq 0 ] && [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All required directories and files are present${NC}"
    exit 0
else
    echo -e "${RED}✗ Validation failed${NC}"
    echo ""
    if [ ${#MISSING_DIRS[@]} -gt 0 ]; then
        echo "Missing directories: ${MISSING_DIRS[*]}"
    fi
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        echo "Missing files: ${MISSING_FILES[*]}"
    fi
    exit 1
fi
