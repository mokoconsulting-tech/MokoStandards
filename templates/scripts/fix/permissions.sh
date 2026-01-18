#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
