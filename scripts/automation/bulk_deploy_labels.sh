#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Automation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /scripts/automation/bulk_deploy_labels.sh
# VERSION: 03.00.00
# BRIEF: Deploy standard labels to all repositories in an organization
# NOTE: Requires GitHub CLI (gh) to be installed and authenticated

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SETUP_LABELS_SCRIPT="$REPO_ROOT/scripts/maintenance/setup-labels.sh"

# Default configuration
DRY_RUN=false
ORGANIZATION=""
REPO_FILTER=""
PARALLEL=false
MAX_PARALLEL=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

log_section() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Deploy standard labels to all repositories in a GitHub organization.

OPTIONS:
    -o, --org ORG           GitHub organization name (required)
    -f, --filter PATTERN    Filter repositories by name pattern (optional)
    --dry-run               Show what would be done without making changes
    --parallel              Deploy to repositories in parallel (faster)
    --max-parallel N        Maximum parallel deployments (default: 5)
    -h, --help              Show this help message

EXAMPLES:
    # Deploy to all repositories in organization (dry run)
    $0 --org mokoconsulting-tech --dry-run

    # Deploy to all repositories
    $0 --org mokoconsulting-tech

    # Deploy only to repositories matching pattern
    $0 --org mokoconsulting-tech --filter "moko*"

    # Deploy in parallel for faster execution
    $0 --org mokoconsulting-tech --parallel --max-parallel 10

REQUIREMENTS:
    - GitHub CLI (gh) must be installed and authenticated
    - User must have admin access to repositories
    - setup-labels.sh script must be present

EOF
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--org)
            ORGANIZATION="$2"
            shift 2
            ;;
        -f|--filter)
            REPO_FILTER="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --max-parallel)
            MAX_PARALLEL="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$ORGANIZATION" ]; then
    log_error "Organization name is required"
    show_usage
    exit 1
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

# Check if setup-labels.sh exists
if [ ! -f "$SETUP_LABELS_SCRIPT" ]; then
    log_error "setup-labels.sh not found at: $SETUP_LABELS_SCRIPT"
    exit 1
fi

# Make setup-labels.sh executable
chmod +x "$SETUP_LABELS_SCRIPT"

log_section "Bulk Label Deployment"

if [ "$DRY_RUN" = true ]; then
    log_warning "DRY-RUN mode enabled - no changes will be made"
fi

log_info "Organization: $ORGANIZATION"
if [ -n "$REPO_FILTER" ]; then
    log_info "Filter: $REPO_FILTER"
fi

# Get list of repositories
log_info "Fetching repositories..."

if [ -n "$REPO_FILTER" ]; then
    REPOS=$(gh repo list "$ORGANIZATION" --limit 1000 --json name -q ".[].name" | grep "$REPO_FILTER" || true)
else
    REPOS=$(gh repo list "$ORGANIZATION" --limit 1000 --json name -q ".[].name")
fi

if [ -z "$REPOS" ]; then
    log_error "No repositories found"
    exit 1
fi

REPO_COUNT=$(echo "$REPOS" | wc -l)
log_success "Found $REPO_COUNT repositories"

# Function to deploy labels to a single repository
deploy_to_repo() {
    local repo_name=$1
    local full_repo="$ORGANIZATION/$repo_name"
    
    log_info "Processing: $full_repo"
    
    # Clone or update repository directory
    local temp_dir="/tmp/label-deploy-$$-$(echo "$repo_name" | tr '/' '-')"
    
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would deploy labels to: $full_repo"
        return 0
    fi
    
    # Clone repository to temp directory
    if gh repo clone "$full_repo" "$temp_dir" -- --depth 1 &> /dev/null; then
        cd "$temp_dir"
        
        # Run setup-labels.sh in repository context
        if "$SETUP_LABELS_SCRIPT" &> "/tmp/label-deploy-$repo_name.log"; then
            log_success "Deployed labels to: $full_repo"
            rm -rf "$temp_dir"
            return 0
        else
            log_error "Failed to deploy labels to: $full_repo (check /tmp/label-deploy-$repo_name.log)"
            rm -rf "$temp_dir"
            return 1
        fi
    else
        log_error "Failed to clone: $full_repo"
        return 1
    fi
}

# Deploy labels
log_section "Deploying Labels"

SUCCESS_COUNT=0
FAILED_COUNT=0
SKIPPED_COUNT=0

if [ "$PARALLEL" = true ]; then
    log_info "Deploying in parallel (max $MAX_PARALLEL concurrent)"
    
    # Use GNU parallel if available, otherwise fall back to xargs
    if command -v parallel &> /dev/null; then
        echo "$REPOS" | parallel -j "$MAX_PARALLEL" deploy_to_repo {}
    else
        echo "$REPOS" | xargs -P "$MAX_PARALLEL" -I {} bash -c "deploy_to_repo {}"
    fi
else
    # Sequential deployment
    while IFS= read -r repo; do
        if deploy_to_repo "$repo"; then
            ((SUCCESS_COUNT++))
        else
            ((FAILED_COUNT++))
        fi
    done <<< "$REPOS"
fi

# Summary
log_section "Deployment Summary"

if [ "$DRY_RUN" = true ]; then
    log_info "[DRY-RUN] Would deploy labels to: $REPO_COUNT repositories"
else
    log_info "Total repositories: $REPO_COUNT"
    log_success "Successful: $SUCCESS_COUNT"
    if [ $FAILED_COUNT -gt 0 ]; then
        log_error "Failed: $FAILED_COUNT"
    fi
    if [ $SKIPPED_COUNT -gt 0 ]; then
        log_warning "Skipped: $SKIPPED_COUNT"
    fi
fi

echo ""
log_success "Bulk label deployment completed!"

exit 0
