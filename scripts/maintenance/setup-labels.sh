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
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Setup
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /scripts/setup-labels.sh
# VERSION: 01.00.00
# BRIEF: Script to create standard labels in a GitHub repository
# NOTE: Requires GitHub CLI (gh) to be installed and authenticated

set -euo pipefail

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
    
    if gh label create "$name" --color "$color" --description "$description" --force 2>/dev/null; then
        log_success "Created/updated label: $name"
    else
        log_warning "Failed to create label: $name"
    fi
}

echo ""
log_info "Creating project type labels..."

# Project Type Labels
create_label "joomla" "7F52FF" "Joomla extension or component"
create_label "dolibarr" "FF6B6B" "Dolibarr module or extension"
create_label "generic" "808080" "Generic project or library"

echo ""
log_info "Creating language labels..."

# Language Labels
create_label "php" "4F5D95" "PHP code changes"
create_label "javascript" "F7DF1E" "JavaScript code changes"
create_label "typescript" "3178C6" "TypeScript code changes"
create_label "python" "3776AB" "Python code changes"
create_label "css" "1572B6" "CSS/styling changes"
create_label "html" "E34F26" "HTML template changes"

echo ""
log_info "Creating component labels..."

# Component Labels
create_label "documentation" "0075CA" "Documentation changes"
create_label "ci-cd" "000000" "CI/CD pipeline changes"
create_label "docker" "2496ED" "Docker configuration changes"
create_label "tests" "00FF00" "Test suite changes"
create_label "security" "FF0000" "Security-related changes"
create_label "dependencies" "0366D6" "Dependency updates"
create_label "config" "F9D0C4" "Configuration file changes"
create_label "build" "FFA500" "Build system changes"

echo ""
log_info "Creating workflow labels..."

# Workflow/Process Labels
create_label "automation" "8B4513" "Automated processes or scripts"
create_label "mokostandards" "B60205" "MokoStandards compliance"
create_label "needs-review" "FBCA04" "Awaiting code review"
create_label "work-in-progress" "D93F0B" "Work in progress, not ready for merge"
create_label "breaking-change" "D73A4A" "Breaking API or functionality change"

echo ""
log_info "Creating priority labels..."

# Priority Labels
create_label "priority: critical" "B60205" "Critical priority, must be addressed immediately"
create_label "priority: high" "D93F0B" "High priority"
create_label "priority: medium" "FBCA04" "Medium priority"
create_label "priority: low" "0E8A16" "Low priority"

echo ""
log_info "Creating type labels..."

# Type Labels
create_label "type: bug" "D73A4A" "Something isn't working"
create_label "type: feature" "A2EEEF" "New feature or request"
create_label "type: enhancement" "84B6EB" "Enhancement to existing feature"
create_label "type: refactor" "F9D0C4" "Code refactoring"
create_label "type: chore" "FEF2C0" "Maintenance tasks"

echo ""
log_info "Creating status labels..."

# Status Labels
create_label "status: pending" "FBCA04" "Pending action or decision"
create_label "status: in-progress" "0E8A16" "Currently being worked on"
create_label "status: blocked" "B60205" "Blocked by another issue or dependency"
create_label "status: on-hold" "D4C5F9" "Temporarily on hold"
create_label "status: wontfix" "FFFFFF" "This will not be worked on"

echo ""
log_info "Creating size labels..."

# Size Labels (based on lines changed)
create_label "size/xs" "C5DEF5" "Extra small change (1-10 lines)"
create_label "size/s" "6FD1E2" "Small change (11-30 lines)"
create_label "size/m" "F9DD72" "Medium change (31-100 lines)"
create_label "size/l" "FFA07A" "Large change (101-300 lines)"
create_label "size/xl" "FF6B6B" "Extra large change (301-1000 lines)"
create_label "size/xxl" "8B0000" "Huge change (1000+ lines)"

echo ""
log_info "Creating repository health labels..."

# Repository Health Labels
create_label "repository-health" "5319E7" "Repository health and maintenance"
create_label "good-first-issue" "7057FF" "Good for newcomers"
create_label "help-wanted" "008672" "Extra attention is needed"
create_label "duplicate" "CFD3D7" "This issue or PR already exists"
create_label "invalid" "E4E669" "This doesn't seem right"
create_label "question" "D876E3" "Further information is requested"

echo ""
log_success "Label setup complete for $REPO"
log_info "You can view all labels at: https://github.com/$REPO/labels"
