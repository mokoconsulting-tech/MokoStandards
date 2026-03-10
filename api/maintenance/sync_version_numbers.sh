#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Maintenance Scripts
# INGROUP: MokoStandards
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: scripts/maintenance/sync_version_numbers.sh
# VERSION: 04.00.04
# BRIEF: Synchronize version numbers across all repository files

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Target version (canonical source: README.md)
TARGET_VERSION="04.00.04"

echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Version Number Synchronization Script${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Target version: ${YELLOW}${TARGET_VERSION}${NC}"
echo ""

# Count files before
echo "Analyzing repository..."
TOTAL_FILES=$(find . -type f \( -name "*.tf" -o -name "*.php" -o -name "*.yml" -o -name "*.yaml" -o -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" \) \
    ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*" | wc -l)

echo "Total files to scan: $TOTAL_FILES"
echo ""

# Find files with old version patterns
echo "Searching for version mismatches..."
OLD_VERSIONS=$(grep -r "04\.00\.0[0-2]" --include="*.tf" --include="*.php" --include="*.yml" --include="*.yaml" --include="*.py" --include="*.sh" --include="*.md" --include="*.json" \
    --exclude-dir=vendor --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=tests \
    2>/dev/null | wc -l || echo "0")

echo "Found $OLD_VERSIONS references to old versions (04.00.04, 04.00.04)"
echo ""

if [ "$OLD_VERSIONS" -eq 0 ]; then
    echo -e "${GREEN}✅ All versions are already synchronized to ${TARGET_VERSION}${NC}"
    exit 0
fi

# Perform replacement
echo "Synchronizing versions..."
UPDATED_COUNT=0

# Update Terraform files
for file in $(find . -name "*.tf" ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Update PHP files
for file in $(find . -name "*.php" ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Update YAML files
for file in $(find . \( -name "*.yml" -o -name "*.yaml" \) ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Update Python files
for file in $(find . -name "*.py" ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Update Shell scripts
for file in $(find . -name "*.sh" ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Update Markdown files
for file in $(find . -name "*.md" ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Update JSON files
for file in $(find . -name "*.json" ! -path "*/vendor/*" ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/tests/*"); do
    if grep -q "04\.00\.0[0-2]" "$file" 2>/dev/null; then
        sed -i 's/04\.00\.01/04.00.04/g; s/04\.00\.02/04.00.04/g' "$file"
        UPDATED_COUNT=$((UPDATED_COUNT + 1))
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Version Synchronization Complete${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Files updated: ${YELLOW}${UPDATED_COUNT}${NC}"
echo -e "Target version: ${YELLOW}${TARGET_VERSION}${NC}"
echo ""

# Verify synchronization
REMAINING=$(grep -r "04\.00\.0[0-2]" --include="*.tf" --include="*.php" --include="*.yml" --include="*.yaml" --include="*.py" --include="*.sh" --include="*.md" --include="*.json" \
    --exclude-dir=vendor --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=tests \
    2>/dev/null | wc -l || echo "0")

if [ "$REMAINING" -eq 0 ]; then
    echo -e "${GREEN}✅ Verification: All versions synchronized successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: ${REMAINING} version references still remain${NC}"
    echo "Run the following command to review:"
    echo "  grep -rn \"04\.00\.0[0-2]\" --include=\"*.tf\" --include=\"*.php\" --include=\"*.yml\" --include=\"*.yaml\""
fi

echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit changes: git add -A && git commit -m 'Sync version numbers to ${TARGET_VERSION}'"
echo "  3. Push changes: git push"
echo ""
