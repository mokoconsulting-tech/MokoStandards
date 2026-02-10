#!/usr/bin/env bash
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
# (./LICENSE.md).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/common.sh
# VERSION: 04.01.00
# BRIEF: Common shell utilities for MokoStandards scripts
# PATH: /scripts/lib/common.sh
# NOTE: Provides reusable functions for logging, error handling, and shell operations

# Common Shell Library for MokoStandards Scripts
#
# Provides reusable utilities for:
# - Standard file header generation
# - Logging and output formatting
# - Error handling and exit codes
# - Path and file operations
# - Repository introspection
#
# Usage:
#   source scripts/lib/common.sh

# ============================================================
# Constants
# ============================================================

# Fallback version if README.md cannot be read
# NOTE: This must be kept in sync with _FALLBACK_VERSION in common.py
# NOTE: This version is now sourced from README.md title line. The previous hardcoded
#       version (04.01.00) was out of sync with README.md (03.01.03). The README is
#       now the single source of truth for the repository version.
readonly _FALLBACK_VERSION="03.01.03"

# Extract version from README.md title line
# Searches for pattern: # README - <REPO> (VERSION: XX.YY.ZZ)
_get_version_from_readme() {
    local repo_root
    local current_dir
    local readme_path
    
    # Find repo root by looking for .git directory
    current_dir="$(pwd)"
    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/.git" ]]; then
            repo_root="$current_dir"
            break
        fi
        current_dir="$(dirname "$current_dir")"
    done
    
    # If we found repo root and README exists
    if [[ -n "$repo_root" ]]; then
        readme_path="$repo_root/README.md"
        if [[ -f "$readme_path" ]]; then
            # Extract version using grep and sed
            local version
            version=$(grep -E '^# .* \(VERSION:' "$readme_path" | head -n1 | sed -E 's/.*VERSION:\s*([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
            if [[ -n "$version" ]]; then
                echo "$version"
                return 0
            fi
        fi
    fi
    
    # Fallback version
    echo "$_FALLBACK_VERSION"
}

# Initialize MOKO_VERSION by reading from README
readonly MOKO_VERSION="$(_get_version_from_readme)"
readonly MOKO_REPO_URL="https://github.com/mokoconsulting-tech/MokoStandards"
readonly MOKO_COPYRIGHT="Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>"
readonly MOKO_LICENSE="GPL-3.0-or-later"

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_INVALID_ARGS=2
readonly EXIT_NOT_FOUND=3
readonly EXIT_PERMISSION=4

# ============================================================
# Logging and Output
# ============================================================

# Print an info message
log_info() {
    echo "ℹ️  $*"
}

# Print a success message
log_success() {
    echo "✅ $*"
}

# Print a warning message
log_warning() {
    echo "⚠️  $*"
}

# Print an error message to stderr
log_error() {
    echo "❌ $*" >&2
}

# Print a debug message if DEBUG is set
log_debug() {
    if [[ -n "${DEBUG:-}" ]]; then
        echo "🔍 $*" >&2
    fi
}

# Print a message without emoji
log_plain() {
    echo "$*"
}

# ============================================================
# Error Handling
# ============================================================

# Print an error message and exit
# Usage: die "error message" [exit_code]
die() {
    local message="$1"
    local exit_code="${2:-$EXIT_ERROR}"
    log_error "$message"
    exit "$exit_code"
}

# Ensure a command exists
# Usage: require_command "git" "Git is required"
require_command() {
    local cmd="$1"
    local message="${2:-Command required: $cmd}"

    if ! command -v "$cmd" &> /dev/null; then
        die "$message" "$EXIT_NOT_FOUND"
    fi
}

# Ensure a file exists
# Usage: require_file "/path/to/file" "Config file"
require_file() {
    local file_path="$1"
    local description="${2:-File}"

    if [[ ! -f "$file_path" ]]; then
        die "$description not found: $file_path" "$EXIT_NOT_FOUND"
    fi
}

# Ensure a directory exists
# Usage: require_dir "/path/to/dir" "Source directory"
require_dir() {
    local dir_path="$1"
    local description="${2:-Directory}"

    if [[ ! -d "$dir_path" ]]; then
        die "$description not found: $dir_path" "$EXIT_NOT_FOUND"
    fi
}

# ============================================================
# Repository Utilities
# ============================================================

# Find the repository root by looking for .git directory
# Returns: Absolute path to repository root
get_repo_root() {
    local current_dir
    current_dir="$(pwd)"

    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/.git" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir="$(dirname "$current_dir")"
    done

    die "Not in a git repository" "$EXIT_ERROR"
}

# Get relative path from repository root
# Usage: get_relative_path "/absolute/path/to/file"
get_relative_path() {
    local file_path="$1"
    local repo_root
    repo_root="$(get_repo_root)"

    # Remove repo root from path to get relative path
    echo "/${file_path#$repo_root/}"
}

# ============================================================
# Path Utilities
# ============================================================

# Ensure directory exists, creating it if necessary
# Usage: ensure_dir "/path/to/dir" "Build directory"
ensure_dir() {
    local dir_path="$1"
    local description="${2:-Directory}"

    if [[ ! -d "$dir_path" ]]; then
        mkdir -p "$dir_path" || die "Failed to create $description: $dir_path"
        log_info "Created $description: $dir_path"
    fi
}

# Check if a path should be excluded based on patterns
# Usage: is_excluded_path ".git" "exclusion1,exclusion2,..." && echo "excluded"
# Second parameter is optional comma-separated exclusions, defaults to common patterns
is_excluded_path() {
    local path="$1"
    local exclusions="${2:-node_modules,vendor,dist,build,target,__pycache__}"
    local basename
    basename="$(basename "$path")"

    # Exclude hidden files/directories
    [[ "$basename" =~ ^\. ]] && return 0

    # Exclude Python egg-info metadata directories/files
    [[ "$basename" == *".egg-info" ]] && return 0

    # Check against exclusion list
    IFS=',' read -ra EXCLUDE_ARRAY <<< "$exclusions"
    for exclude_pattern in "${EXCLUDE_ARRAY[@]}"; do
        if [[ "$basename" == "$exclude_pattern" ]]; then
            return 0
        fi
    done

    return 1
}

# ============================================================
# File Operations
# ============================================================

# Safely copy a file with backup
# Usage: safe_copy "source.txt" "dest.txt"
safe_copy() {
    local src="$1"
    local dest="$2"

    require_file "$src" "Source file"

    if [[ -f "$dest" ]]; then
        local backup="${dest}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$dest" "$backup" || die "Failed to create backup: $backup"
        log_info "Created backup: $backup"
    fi

    cp "$src" "$dest" || die "Failed to copy $src to $dest"
    log_success "Copied: $src -> $dest"
}

# ============================================================
# String Utilities
# ============================================================

# Trim whitespace from string
# Usage: trimmed=$(trim "  hello  ")
trim() {
    local var="$*"
    # Remove leading whitespace
    var="${var#"${var%%[![:space:]]*}"}"
    # Remove trailing whitespace
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}

# Convert string to lowercase
# Usage: lower=$(to_lower "HELLO")
to_lower() {
    echo "$*" | tr '[:upper:]' '[:lower:]'
}

# Convert string to uppercase
# Usage: upper=$(to_upper "hello")
to_upper() {
    echo "$*" | tr '[:lower:]' '[:upper:]'
}

# ============================================================
# Dry-Run Utilities
# ============================================================

# Global dry-run flag (default: false)
DRY_RUN=${DRY_RUN:-false}

# Execute command or print dry-run message
# Usage: run_cmd "command" "arg1" "arg2"
run_cmd() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would execute: $*"
    else
        "$@"
    fi
}

# Execute command with message or print dry-run message
# Usage: run_with_msg "Creating file" "touch" "file.txt"
run_with_msg() {
    local message="$1"
    shift
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] $message"
        echo "[DRY-RUN] Would execute: $*"
    else
        log_info "$message"
        "$@"
    fi
}

# ============================================================
# Validation Utilities
# ============================================================

# Check if a variable is set and not empty
# Usage: is_set "$MY_VAR" || die "MY_VAR is required"
is_set() {
    [[ -n "${1:-}" ]]
}

# Check if running as root
# Usage: is_root && die "Do not run as root"
is_root() {
    [[ $EUID -eq 0 ]]
}

# Check if a port is in use
# Usage: is_port_in_use 8080 && die "Port 8080 is already in use"
is_port_in_use() {
    local port="$1"
    if command -v lsof &> /dev/null; then
        lsof -i ":$port" &> /dev/null
    elif command -v netstat &> /dev/null; then
        netstat -tuln | grep -q ":$port\( \|$\)"
    else
        log_warning "Cannot check port usage (lsof/netstat not available)"
        return 1
    fi
}

# ============================================================
# Git Utilities
# ============================================================

# Get current git branch name
# Usage: branch=$(get_git_branch)
get_git_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

# Get current git commit hash
# Usage: commit=$(get_git_commit)
get_git_commit() {
    git rev-parse HEAD 2>/dev/null || echo "unknown"
}

# Get short git commit hash
# Usage: short_commit=$(get_git_commit_short)
get_git_commit_short() {
    git rev-parse --short HEAD 2>/dev/null || echo "unknown"
}

# Check if git working directory is clean
# Usage: is_git_clean || die "Git working directory is not clean"
is_git_clean() {
    [[ -z "$(git status --porcelain 2>/dev/null)" ]]
}

# ============================================================
# Script Initialization
# ============================================================

# Initialize script with common settings
# Usage: init_script
init_script() {
    # Enable strict mode
    set -euo pipefail

    # Set IFS to default (space, tab, newline)
    IFS=$' \t\n'

    log_debug "Script initialized with strict mode"
}

# Print script header
# Usage: print_header "Script Name" "Description"
print_header() {
    local name="$1"
    local description="${2:-}"

    echo "========================================================================"
    echo "$name"
    if [[ -n "$description" ]]; then
        echo "$description"
    fi
    echo "========================================================================"
    echo
}

# Print script footer
# Usage: print_footer
print_footer() {
    echo
    echo "========================================================================"
    log_success "Completed successfully"
    echo "========================================================================"
}

# ============================================================
# Main (for testing)
# ============================================================

# If script is executed directly (not sourced), run tests
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "MokoStandards Common Shell Library v$MOKO_VERSION"
    echo "========================================================================"
    echo

    # Test logging functions
    echo "Testing logging functions:"
    log_info "This is an info message"
    log_success "This is a success message"
    log_warning "This is a warning message"
    log_error "This is an error message (stderr)"
    echo

    # Test repository utilities
    echo "Testing repository utilities:"
    if repo_root=$(get_repo_root 2>/dev/null); then
        echo "Repository root: $repo_root"
        echo "Current directory: $(pwd)"
        rel_path=$(get_relative_path "$(pwd)")
        echo "Relative path: $rel_path"
    else
        echo "Not in a git repository"
    fi
    echo

    # Test string utilities
    echo "Testing string utilities:"
    echo "trim '  hello  ' = '$(trim "  hello  ")'"
    echo "to_lower 'HELLO' = '$(to_lower "HELLO")'"
    echo "to_upper 'hello' = '$(to_upper "hello")'"
    echo

    # Test git utilities
    if command -v git &> /dev/null; then
        echo "Testing git utilities:"
        echo "Branch: $(get_git_branch)"
        echo "Commit: $(get_git_commit_short)"
        if is_git_clean; then
            echo "Working directory: clean"
        else
            echo "Working directory: modified"
        fi
        echo
    fi

    log_success "Common shell library loaded successfully"
fi
