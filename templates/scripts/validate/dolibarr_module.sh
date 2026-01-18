#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Templates.Scripts
# INGROUP: MokoStandards.Templates
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/validate/dolibarr_module.sh
# VERSION: 01.00.00
# BRIEF: Dolibarr module validation script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==================================="
echo "Dolibarr Module Validation"
echo "==================================="
echo ""

ERRORS=0
WARNINGS=0

# Check for src directory
if [ ! -d "src" ]; then
    echo -e "${RED}✗${NC} Missing required directory: src/"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} Found src/ directory"
fi

# Check for core/modules directory
if [ ! -d "src/core/modules" ]; then
    echo -e "${RED}✗${NC} Missing required directory: src/core/modules/"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} Found src/core/modules/ directory"
fi

# Check for language files
if [ ! -d "src/langs" ]; then
    echo -e "${YELLOW}⚠${NC} Missing suggested directory: src/langs/"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✓${NC} Found src/langs/ directory"
fi

# Check for module descriptor
MODULE_DESCRIPTORS=$(find src/core/modules -name "mod*.class.php" 2>/dev/null || true)
if [ -z "$MODULE_DESCRIPTORS" ]; then
    echo -e "${RED}✗${NC} No module descriptor found (mod*.class.php)"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} Found module descriptor: $(basename $MODULE_DESCRIPTORS)"
fi

echo ""
echo "==================================="
echo "Validation Summary"
echo "==================================="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}✗ Validation failed${NC}"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠ Validation passed with warnings${NC}"
    exit 0
else
    echo -e "${GREEN}✓ Validation passed${NC}"
    exit 0
fi
