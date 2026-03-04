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
# INGROUP: Release
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/release/package.sh
# VERSION: 01.00.00
# BRIEF: Creates release package
# NOTE: Template script for release automation

set -euo pipefail

echo "[INFO] Creating release package..."

# Get version from manifest or git tag
VERSION="${1:-$(git describe --tags --abbrev=0 2>/dev/null || echo '0.0.0')}"
PACKAGE_NAME="${2:-package}"

# Create package directory
BUILD_DIR="build"
PACKAGE_DIR="${BUILD_DIR}/${PACKAGE_NAME}"

rm -rf "${BUILD_DIR}"
mkdir -p "${PACKAGE_DIR}"

# Copy files (customize based on project structure)
echo "[INFO] Copying files..."
cp -r src/* "${PACKAGE_DIR}/" 2>/dev/null || true
cp -r admin "${PACKAGE_DIR}/" 2>/dev/null || true
cp -r site "${PACKAGE_DIR}/" 2>/dev/null || true
cp ./*.xml "${PACKAGE_DIR}/" 2>/dev/null || true
cp LICENSE* "${PACKAGE_DIR}/" 2>/dev/null || true
cp CHANGELOG.md "${PACKAGE_DIR}/" 2>/dev/null || true

# Create archive
ARCHIVE="${BUILD_DIR}/${PACKAGE_NAME}-${VERSION}.zip"
echo "[INFO] Creating archive: ${ARCHIVE}"

cd "${BUILD_DIR}"
zip -r "$(basename ${ARCHIVE})" "${PACKAGE_NAME}" >/dev/null

echo "[OK] Package created: ${ARCHIVE}"
ls -lh "$(basename ${ARCHIVE})"

exit 0
