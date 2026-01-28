#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# REQUIRED FILE: This file must be present in all MokoStandards-compliant repositories
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Required
# INGROUP: MokoStandards.Setup
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/required/setup-labels.sh
# VERSION: 03.01.00
# BRIEF: REQUIRED label deployment script for all repositories
# NOTE: This file must be copied to scripts/maintenance/setup-labels.sh in your repository

set -euo pipefail

# =============================================================================
# REQUIRED LABEL DEPLOYMENT SCRIPT
# =============================================================================
# This script creates standard labels required for all MokoStandards repos.
# Copy this file to: scripts/maintenance/setup-labels.sh
# Usage: ./scripts/maintenance/setup-labels.sh [--dry-run]
# =============================================================================

# Dry-run flag (default: false)
DRY_RUN=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--dry-run] [--help]"
            echo ""
            echo "REQUIRED SCRIPT: Deploy standard labels to repository"
            echo ""
            echo "Options:"
            echo "  --dry-run    Show what would be created without actually creating labels"
            echo "  --help       Show this help message"
            echo ""
            echo "Prerequisites:"
            echo "  - GitHub CLI (gh) must be installed"
            echo "  - Must be authenticated: gh auth login"
            echo "  - Must have admin access to repository"
            echo ""
            echo "Installation:"
            echo "  curl -fsSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/required/setup-labels.sh > scripts/maintenance/setup-labels.sh"
            echo "  chmod +x scripts/maintenance/setup-labels.sh"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

if [ "$DRY_RUN" = true ]; then
    log_info "Running in DRY-RUN mode - no labels will be created"
fi

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    log_error "GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    log_error "Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
log_info "Setting up labels for repository: $REPO"

# Function to create or update a label
create_label() {
    local name=$1
    local color=$2
    local description=$3

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would create label: $name (color: #$color, description: $description)"
    else
        if gh label create "$name" --color "$color" --description "$description" --force 2>/dev/null; then
            log_success "Created/updated label: $name"
        else
            log_warning "Failed to create label: $name"
        fi
    fi
}

echo ""
log_info "Creating REQUIRED project type labels..."

# REQUIRED: Project Type Labels
create_label "joomla" "7F52FF" "Joomla extension or component"
create_label "dolibarr" "FF6B6B" "Dolibarr module or extension"
create_label "generic" "808080" "Generic project or library"

echo ""
log_info "Creating REQUIRED language labels..."

# REQUIRED: Language Labels
create_label "php" "4F5D95" "PHP code changes"
create_label "javascript" "F7DF1E" "JavaScript code changes"
create_label "typescript" "3178C6" "TypeScript code changes"
create_label "python" "3776AB" "Python code changes"
create_label "css" "1572B6" "CSS/styling changes"
create_label "html" "E34F26" "HTML template changes"

echo ""
log_info "Creating REQUIRED component labels..."

# REQUIRED: Component Labels
create_label "documentation" "0075CA" "Documentation changes"
create_label "ci-cd" "000000" "CI/CD pipeline changes"
create_label "docker" "2496ED" "Docker configuration changes"
create_label "tests" "00FF00" "Test suite changes"
create_label "security" "FF0000" "Security-related changes"
create_label "dependencies" "0366D6" "Dependency updates"
create_label "config" "F9D0C4" "Configuration file changes"
create_label "build" "FFA500" "Build system changes"

echo ""
log_info "Creating REQUIRED workflow labels..."

# REQUIRED: Workflow/Process Labels
create_label "automation" "8B4513" "Automated processes or scripts"
create_label "mokostandards" "B60205" "MokoStandards compliance"
create_label "needs-review" "FBCA04" "Awaiting code review"
create_label "work-in-progress" "D93F0B" "Work in progress, not ready for merge"
create_label "breaking-change" "D73A4A" "Breaking API or functionality change"

echo ""
log_info "Creating REQUIRED priority labels..."

# REQUIRED: Priority Labels
create_label "priority: critical" "B60205" "Critical priority, must be addressed immediately"
create_label "priority: high" "D93F0B" "High priority"
create_label "priority: medium" "FBCA04" "Medium priority"
create_label "priority: low" "0E8A16" "Low priority"

echo ""
log_info "Creating REQUIRED type labels..."

# REQUIRED: Type Labels
create_label "type: bug" "D73A4A" "Something isn't working"
create_label "type: feature" "A2EEEF" "New feature or request"
create_label "type: enhancement" "84B6EB" "Enhancement to existing feature"
create_label "type: refactor" "F9D0C4" "Code refactoring"
create_label "type: chore" "FEF2C0" "Maintenance tasks"

echo ""
log_info "Creating REQUIRED status labels..."

# REQUIRED: Status Labels
create_label "status: pending" "FBCA04" "Pending action or decision"
create_label "status: in-progress" "0E8A16" "Currently being worked on"
create_label "status: blocked" "B60205" "Blocked by another issue or dependency"
create_label "status: on-hold" "D4C5F9" "Temporarily on hold"
create_label "status: wontfix" "FFFFFF" "This will not be worked on"

echo ""
log_info "Creating REQUIRED size labels..."

# REQUIRED: Size Labels (based on lines changed)
create_label "size/xs" "C5DEF5" "Extra small change (1-10 lines)"
create_label "size/s" "6FD1E2" "Small change (11-30 lines)"
create_label "size/m" "F9DD72" "Medium change (31-100 lines)"
create_label "size/l" "FFA07A" "Large change (101-300 lines)"
create_label "size/xl" "FF6B6B" "Extra large change (301-1000 lines)"
create_label "size/xxl" "B60205" "Extremely large change (1000+ lines)"

echo ""
log_info "Creating REQUIRED health labels..."

# REQUIRED: Repository Health Labels
create_label "health: excellent" "0E8A16" "Health score 90-100"
create_label "health: good" "FBCA04" "Health score 70-89"
create_label "health: fair" "FFA500" "Health score 50-69"
create_label "health: poor" "FF6B6B" "Health score below 50"

echo ""
echo "============================================================"
if [ "$DRY_RUN" = true ]; then
    log_info "[DRY-RUN] Label deployment simulation completed"
    echo ""
    log_info "To apply these labels, run:"
    echo "  $0"
else
    log_success "Label deployment completed successfully!"
    echo ""
    log_info "Summary:"
    echo "  - Project Types: 3 labels"
    echo "  - Languages: 6 labels"
    echo "  - Components: 8 labels"
    echo "  - Workflow: 5 labels"
    echo "  - Priority: 4 labels"
    echo "  - Type: 5 labels"
    echo "  - Status: 5 labels"
    echo "  - Size: 6 labels"
    echo "  - Health: 4 labels"
    echo "  - TOTAL: 46 labels"
fi
echo "============================================================"
echo ""

# Next steps
if [ "$DRY_RUN" = false ]; then
    log_info "Next steps:"
    echo "  1. Configure auto-labeling by adding .github/labeler.yml"
    echo "  2. Setup label automation workflow in .github/workflows/"
    echo "  3. Verify labels in repository settings"
    echo ""
    log_info "For more information:"
    echo "  https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guides/label-deployment.md"
fi

exit 0
