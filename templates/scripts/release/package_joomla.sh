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
# PATH: /templates/scripts/release/package_joomla.sh
# VERSION: 01.00.00
# BRIEF: Package building script for Joomla components

set -e

# Component name (customize this)
COMPONENT_NAME="${COMPONENT_NAME:-com_example}"
VERSION="${VERSION:-1.0.0}"

# Directories
BUILD_DIR="build"
DIST_DIR="dist"

echo "==================================="
echo "Joomla Component Package Builder"
echo "==================================="
echo "Component: $COMPONENT_NAME"
echo "Version: $VERSION"
echo ""

# Clean previous builds
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Copy component files
echo "Copying component files..."
cp -r site "$BUILD_DIR/"
cp -r admin "$BUILD_DIR/"

if [ -d "media" ]; then
    cp -r media "$BUILD_DIR/"
fi

if [ -d "language" ]; then
    cp -r language "$BUILD_DIR/"
fi

# Copy manifest
cp "${COMPONENT_NAME}.xml" "$BUILD_DIR/"

# Create package
echo "Creating package..."
cd "$BUILD_DIR"
zip -r "../$DIST_DIR/${COMPONENT_NAME}_${VERSION}.zip" .
cd ..

echo ""
echo "Package created: $DIST_DIR/${COMPONENT_NAME}_${VERSION}.zip"
echo "==================================="
