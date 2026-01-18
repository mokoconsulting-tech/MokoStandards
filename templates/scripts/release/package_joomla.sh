#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
