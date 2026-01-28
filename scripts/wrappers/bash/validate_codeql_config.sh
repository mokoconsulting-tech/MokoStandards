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
SCRIPT_NAME="validate_codeql_config"
SCRIPT_PATH="scripts/validate/validate_codeql_config.py"
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

# Check if Python is available
check_python() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        log_error "Python is not installed or not in PATH"
        echo "Please install Python 3.7 or later"
        exit 1
    fi
}

# Main execution
main() {
    local repo_root
    repo_root=$(get_repo_root)
    
    local python_cmd
    python_cmd=$(check_python)
    
    local full_script_path="$repo_root/$SCRIPT_PATH"
    
    # Check if script exists
    if [ ! -f "$full_script_path" ]; then
        log_error "Python script not found: $full_script_path"
        exit 1
    fi
    
    # Setup logging directory
    local log_dir="$repo_root/logs/$SCRIPT_CATEGORY"
    mkdir -p "$log_dir"
    
    local timestamp
    timestamp=$(date +"%Y%m%d_%H%M%S")
    local log_file="$log_dir/${SCRIPT_NAME}_${timestamp}.log"
    
    # Execute Python script with all arguments
    log_info "Running $SCRIPT_NAME..."
    log_info "Log file: $log_file"
    
    if "$python_cmd" "$full_script_path" "$@" 2>&1 | tee "$log_file"; then
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
