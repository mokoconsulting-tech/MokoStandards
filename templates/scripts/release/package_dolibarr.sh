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
# PATH: /templates/scripts/release/package_dolibarr.sh
# VERSION: 01.00.00
# BRIEF: Package building script for Dolibarr modules

set -e

# Module name (customize this)
MODULE_NAME="${MODULE_NAME:-mokomodule}"
VERSION="${VERSION:-1.0.0}"

# Directories
SRC_DIR="src"
BUILD_DIR="build"
DIST_DIR="dist"

echo "==================================="
echo "Dolibarr Module Package Builder"
echo "==================================="
echo "Module: $MODULE_NAME"
echo "Version: $VERSION"
echo ""

# Clean previous builds
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Copy module source files
echo "Copying module files..."
if [ -d "$SRC_DIR" ]; then
    cp -r "$SRC_DIR/"* "$BUILD_DIR/"
else
    echo "Error: src/ directory not found"
    exit 1
fi

# Create package
echo "Creating package..."
cd "$BUILD_DIR"
zip -r "../$DIST_DIR/${MODULE_NAME}_${VERSION}.zip" .
cd ..

echo ""
echo "Package created: $DIST_DIR/${MODULE_NAME}_${VERSION}.zip"
echo "==================================="
