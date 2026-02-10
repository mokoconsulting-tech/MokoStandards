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
# INGROUP: Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /templates/scripts/lib/common.sh
# VERSION: 01.00.00
# BRIEF: Common utility functions for scripts
# NOTE: Template library script

# ============================================================
# Constants
# ============================================================

# Fallback version if README.md cannot be read
# NOTE: This must be kept in sync with _FALLBACK_VERSION in common.py
readonly _FALLBACK_VERSION="03.01.05"

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
            # More strict: line must start with "# README" and contain VERSION
            local version
            version=$(grep -E '^# README .* \(VERSION:' "$readme_path" | head -n1 | sed -E 's/.*VERSION:\s*([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
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

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
  echo "ℹ️  $*"
}

log_success() {
  echo "✅ $*"
}

log_warn() {
  echo "⚠️  $*"
}

log_warning() {
  echo "⚠️  $*"
}

log_error() {
  echo "❌ $*" >&2
}

log_fatal() {
  echo "❌ $*" >&2
  exit 1
}

log_debug() {
  if [[ -n "${DEBUG:-}" ]]; then
    echo "🔍 $*" >&2
  fi
}

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

# ============================================================
# Git Utilities
# ============================================================

# Get current git branch name
# Usage: branch=$(get_git_branch)
get_current_branch() {
  git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

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
# Utility Functions
# ============================================================

# Check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Get git root directory
get_git_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}

# Check if running in git repository
is_git_repo() {
  git rev-parse --git-dir >/dev/null 2>&1
}

# Export functions
export -f log_info log_success log_warn log_warning log_error log_fatal log_debug log_plain
export -f die require_command require_file require_dir
export -f get_repo_root get_relative_path ensure_dir
export -f get_current_branch get_git_branch get_git_commit get_git_commit_short is_git_clean
export -f command_exists get_git_root is_git_repo
