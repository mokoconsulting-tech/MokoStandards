#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Shell wrapper template for Python scripts
# This wrapper provides a convenient way to call Python scripts with proper error handling

set -euo pipefail

# Script Configuration - UPDATE THESE FOR EACH WRAPPER
SCRIPT_NAME="auto_detect_platform"
SCRIPT_PATH="scripts/validate/auto_detect_platform.php"
SCRIPT_CATEGORY="validation"  # automation, validation, maintenance, etc.

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

# Get repository root
get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null || pwd
}

# Check if PHP is available
check_php() {
    if command -v php &> /dev/null; then
        echo "php"
    else
        log_error "PHP is not installed or not in PATH"
        echo "Please install PHP 7.4 or later"
        exit 1
    fi
}

# Main execution
main() {
    local repo_root
    repo_root=$(get_repo_root)
    
    local php_cmd
    php_cmd=$(check_php)
    
    local full_script_path="$repo_root/$SCRIPT_PATH"
    
    # Check if script exists
    if [ ! -f "$full_script_path" ]; then
        log_error "PHP script not found: $full_script_path"
        exit 1
    fi
    
    # Setup logging directory
    local log_dir="$repo_root/var/logs/$SCRIPT_CATEGORY"
    mkdir -p "$log_dir"
    
    local timestamp
    timestamp=$(date +"%Y%m%d_%H%M%S")
    local log_file="$log_dir/${SCRIPT_NAME}_${timestamp}.log"
    
    # Execute PHP script with all arguments
    log_info "Running $SCRIPT_NAME..."
    log_info "Log file: $log_file"
    
    if "$php_cmd" "$full_script_path" "$@" 2>&1 | tee "$log_file"; then
        log_success "$SCRIPT_NAME completed successfully"
        exit 0
    else
        local exit_code=$?
        log_error "$SCRIPT_NAME failed with exit code: $exit_code"
        log_info "Check log file for details: $log_file"
        exit $exit_code
    fi
}

# Run main with all arguments
main "$@"
