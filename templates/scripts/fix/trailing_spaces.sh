#!/usr/bin/env bash
# Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Remove trailing whitespace from files
#
# MokoStandards Policy Compliance:
# - File formatting: Enforces organizational coding standards
# - Reference: docs/policy/file-formatting.md

set -euo pipefail

# Default values
DRY_RUN=0
VERBOSE=1
FILE_TYPE=""
EXTENSIONS=()
FILES=()

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
Usage: $0 [OPTIONS] [FILES...]

Remove trailing whitespace from files.

OPTIONS:
    --type TYPE         Type of files to fix (yaml, python, shell, markdown, all)
    --ext EXT           Specific file extension (can be repeated)
    --dry-run           Show what would be changed without modifying files
    --quiet             Suppress verbose output
    -h, --help          Show this help message

EXAMPLES:
    # Fix all YAML files
    $0 --type yaml

    # Fix specific extensions
    $0 --ext .yml --ext .py

    # Fix specific files
    $0 file1.yml file2.py

    # Dry run
    $0 --type all --dry-run

EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --type)
            FILE_TYPE="$2"
            shift 2
            ;;
        --ext)
            EXTENSIONS+=("$2")
            shift 2
            ;;
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --quiet)
            VERBOSE=0
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            FILES+=("$1")
            shift
            ;;
    esac
done

# Function to get files by type
get_files_by_type() {
    local type="$1"
    local patterns=()

    case "$type" in
        yaml)
            patterns=("*.yml" "*.yaml")
            ;;
        python)
            patterns=("*.py")
            ;;
        shell)
            patterns=("*.sh" "*.bash")
            ;;
        markdown)
            patterns=("*.md" "*.markdown")
            ;;
        all)
            patterns=("*.yml" "*.yaml" "*.py" "*.sh" "*.bash" "*.md" "*.markdown")
            ;;
        *)
            echo "Unknown type: $type"
            exit 1
            ;;
    esac

    git ls-files "${patterns[@]}" 2>/dev/null || true
}

# Function to get files by extensions
get_files_by_extensions() {
    local patterns=()
    for ext in "${EXTENSIONS[@]}"; do
        patterns+=("*${ext}")
    done
    git ls-files "${patterns[@]}" 2>/dev/null || true
}

# Function to fix trailing spaces in a file
fix_trailing_spaces() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        [[ $VERBOSE -eq 1 ]] && echo "File not found: $file"
        return 1
    fi

    # Check if file has trailing whitespace
    if ! grep -q '[[:space:]]$' "$file"; then
        [[ $VERBOSE -eq 1 ]] && echo "Already clean: $file"
        return 0
    fi

    if [[ $DRY_RUN -eq 1 ]]; then
        [[ $VERBOSE -eq 1 ]] && echo -e "${YELLOW}Would fix: $file${NC}"
        return 0
    fi

    # Remove trailing whitespace
    sed -i 's/[[:space:]]*$//' "$file"
    [[ $VERBOSE -eq 1 ]] && echo -e "${GREEN}Fixed: $file${NC}"
}

# Main logic
TARGETS=()

if [[ ${#FILES[@]} -gt 0 ]]; then
    # Use provided files
    TARGETS=("${FILES[@]}")
elif [[ ${#EXTENSIONS[@]} -gt 0 ]]; then
    # Get files by extensions
    mapfile -t TARGETS < <(get_files_by_extensions)
elif [[ -n "$FILE_TYPE" ]]; then
    # Get files by type
    mapfile -t TARGETS < <(get_files_by_type "$FILE_TYPE")
else
    # Default: all supported types
    mapfile -t TARGETS < <(get_files_by_type "all")
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
    [[ $VERBOSE -eq 1 ]] && echo "No files to process"
    exit 0
fi

if [[ $VERBOSE -eq 1 ]]; then
    if [[ $DRY_RUN -eq 1 ]]; then
        echo "DRY RUN: Checking ${#TARGETS[@]} file(s)..."
    else
        echo "Fixing ${#TARGETS[@]} file(s)..."
    fi
    echo
fi

# Process files
MODIFIED=0
for file in "${TARGETS[@]}"; do
    if grep -q '[[:space:]]$' "$file" 2>/dev/null; then
        fix_trailing_spaces "$file"
        ((MODIFIED++)) || true
    else
        [[ $VERBOSE -eq 1 ]] && echo "Already clean: $file"
    fi
done

# Summary
[[ $VERBOSE -eq 1 ]] && echo

if [[ $DRY_RUN -eq 1 ]]; then
    echo "Would modify $MODIFIED file(s)"
else
    echo "Modified $MODIFIED file(s)"
fi
