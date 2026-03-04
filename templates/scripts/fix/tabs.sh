#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Convert tabs to spaces in files
#
# MokoStandards Policy Compliance:
# - File formatting: Enforces organizational coding standards
# - Reference: docs/policy/file-formatting.md
# - YAML/Python/Shell: tabs → spaces (4 spaces default, 2 for YAML)
# - Makefiles: tabs preserved (required by Make syntax)

set -euo pipefail

# Default values
DRY_RUN=false
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

Convert tabs to spaces in files.

OPTIONS:
    --type TYPE         Type of files to fix (yaml, python, shell, all)
    --ext EXT           Specific file extension (can be repeated)
    --dry-run           Show what would be changed without modifying files
    --quiet             Suppress verbose output
    -h, --help          Show this help message

EXAMPLES:
    # Fix all YAML files (tabs → 2 spaces)
    $0 --type yaml

    # Fix all Python files (tabs → 4 spaces)
    $0 --type python

    # Fix specific extensions
    $0 --ext .yml --ext .py

    # Fix specific files
    $0 file1.yml file2.py

    # Dry run
    $0 --type all --dry-run

NOTE: Makefiles are automatically detected and tabs are preserved.

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
            DRY_RUN=true
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

# Function to check if file is a Makefile
is_makefile() {
    local file="$1"
    local basename
    basename=$(basename "$file" | tr '[:upper:]' '[:lower:]')

    [[ "$basename" == "makefile" ]] || \
    [[ "$basename" == "gnumakefile" ]] || \
    [[ "$basename" == makefile.* ]]
}

# Function to get number of spaces for file type
get_spaces_for_file() {
    local file="$1"
    local ext="${file##*.}"

    case "$ext" in
        yml|yaml)
            echo 2
            ;;
        py|sh|bash)
            echo 4
            ;;
        *)
            echo 4
            ;;
    esac
}

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
        all)
            patterns=("*.yml" "*.yaml" "*.py" "*.sh" "*.bash")
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

# Function to fix tabs in a file
fix_tabs() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        [[ $VERBOSE -eq 1 ]] && echo "File not found: $file"
        return 1
    fi

    # Skip Makefiles
    if is_makefile "$file"; then
        [[ $VERBOSE -eq 1 ]] && echo "Skipped (Makefile): $file"
        return 0
    fi

    # Check if file has tabs
    if ! grep -q $'\t' "$file"; then
        [[ $VERBOSE -eq 1 ]] && echo "Already clean: $file"
        return 0
    fi

    local num_spaces
    num_spaces=$(get_spaces_for_file "$file")
    local tab_count
    tab_count=$(grep -o $'\t' "$file" | wc -l)

    if [ "$DRY_RUN" = true ]; then
        [[ $VERBOSE -eq 1 ]] && echo -e "${YELLOW}Would fix: $file ($tab_count tabs → $num_spaces spaces)${NC}"
        return 0
    fi

    # Replace tabs with spaces
    if [[ "$num_spaces" -eq 2 ]]; then
        sed -i 's/\t/  /g' "$file"
    else
        sed -i 's/\t/    /g' "$file"
    fi

    [[ $VERBOSE -eq 1 ]] && echo -e "${GREEN}Fixed: $file ($tab_count tabs → $num_spaces spaces)${NC}"
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
    if [ "$DRY_RUN" = true ]; then
        echo "DRY RUN: Checking ${#TARGETS[@]} file(s)..."
    else
        echo "Fixing ${#TARGETS[@]} file(s)..."
    fi
    echo
fi

# Process files
MODIFIED=0
for file in "${TARGETS[@]}"; do
    if ! is_makefile "$file" && grep -q $'\t' "$file" 2>/dev/null; then
        fix_tabs "$file"
        ((MODIFIED++)) || true
    else
        if is_makefile "$file"; then
            [[ $VERBOSE -eq 1 ]] && echo "Skipped (Makefile): $file"
        else
            [[ $VERBOSE -eq 1 ]] && echo "Already clean: $file"
        fi
    fi
done

# Summary
[[ $VERBOSE -eq 1 ]] && echo

if [ "$DRY_RUN" = true ]; then
    echo "Would modify $MODIFIED file(s)"
else
    echo "Modified $MODIFIED file(s)"
fi
