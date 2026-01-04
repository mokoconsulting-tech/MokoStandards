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
# INGROUP: Fix
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/fix/permissions.sh
# VERSION: 01.00.00
# BRIEF: Fixes file permissions (644 for files, 755 for directories and scripts)
# NOTE: Template script for automated fixes

set -euo pipefail

echo "[INFO] Fixing file permissions..."

# Fix directory permissions
find . -type d -not -path './.git/*' -exec chmod 755 {} \; 2>/dev/null || true

# Fix file permissions
find . -type f -not -path './.git/*' -exec chmod 644 {} \; 2>/dev/null || true

# Make scripts executable
find . -type f -name '*.sh' -not -path './.git/*' -exec chmod 755 {} \; 2>/dev/null || true

echo "[OK] Permissions fixed"
exit 0
