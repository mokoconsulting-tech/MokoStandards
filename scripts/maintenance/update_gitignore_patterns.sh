#!/usr/bin/env bash
# ============================================================================
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /scripts/update_gitignore_patterns.sh
# VERSION: 01.00.00
# BRIEF: Add or update .gitignore patterns for Sublime Text and SFTP config files
# ============================================================================

set -e  # Exit on any error

# Configuration
PATTERNS_TO_ADD=(
    "*.sublime*"
    "sftp-config*.json"
)

PATTERNS_TO_REMOVE=(
    "*.sublime-project"
    "*.sublime-workspace"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a pattern exists in .gitignore
pattern_exists() {
    local file="$1"
    local pattern="$2"
    
    if [ ! -f "$file" ]; then
        return 1
    fi
    
    # Check if pattern exists as a complete line
    grep -qxF "$pattern" "$file" 2>/dev/null
}

# Function to remove old patterns
remove_old_patterns() {
    local file="$1"
    local changed=0
    
    if [ ! -f "$file" ]; then
        return 0
    fi
    
    for pattern in "${PATTERNS_TO_REMOVE[@]}"; do
        if pattern_exists "$file" "$pattern"; then
            print_info "Removing old pattern: $pattern"
            # Use temporary file to safely remove pattern
            grep -vxF "$pattern" "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
            changed=1
        fi
    done
    
    return $changed
}

# Function to add new patterns
add_new_patterns() {
    local file="$1"
    local changed=0
    
    # Create .gitignore if it doesn't exist
    if [ ! -f "$file" ]; then
        print_warning ".gitignore not found, creating new file"
        touch "$file"
    fi
    
    # Find the right section to add patterns
    # Look for OS / Editor / IDE section or create it
    local section_marker="# OS / Editor / IDE cruft"
    local has_section=0
    
    if grep -q "$section_marker" "$file" 2>/dev/null; then
        has_section=1
    fi
    
    for pattern in "${PATTERNS_TO_ADD[@]}"; do
        if ! pattern_exists "$file" "$pattern"; then
            print_info "Adding pattern: $pattern"
            
            if [ $has_section -eq 1 ]; then
                # Add after the section marker
                sed -i "/^$section_marker/a $pattern" "$file"
            else
                # Add at the end with a comment header
                if [ ! -s "$file" ]; then
                    echo "$section_marker" >> "$file"
                else
                    echo "" >> "$file"
                    echo "$section_marker" >> "$file"
                fi
                echo "$pattern" >> "$file"
                has_section=1
            fi
            changed=1
        else
            print_info "Pattern already exists: $pattern"
        fi
    done
    
    return $changed
}

# Function to update .gitignore in a directory
update_gitignore() {
    local dir="$1"
    local gitignore_file="$dir/.gitignore"
    
    print_info "Processing: $gitignore_file"
    
    local changed=0
    
    # Remove old patterns
    if remove_old_patterns "$gitignore_file"; then
        changed=1
    fi
    
    # Add new patterns
    if add_new_patterns "$gitignore_file"; then
        changed=1
    fi
    
    if [ $changed -eq 1 ]; then
        print_success "Updated: $gitignore_file"
        return 0
    else
        print_info "No changes needed: $gitignore_file"
        return 1
    fi
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] [DIRECTORY]

Add *.sublime* and sftp-config*.json patterns to .gitignore files.
Removes old *.sublime-project and *.sublime-workspace patterns.

OPTIONS:
    -h, --help          Show this help message
    -r, --recursive     Process all .gitignore files recursively
    -d, --dry-run       Show what would be changed without making changes
    -v, --verbose       Verbose output

DIRECTORY:
    Path to directory containing .gitignore (default: current directory)
    With -r flag, searches recursively for all .gitignore files

EXAMPLES:
    # Update .gitignore in current directory
    $0

    # Update .gitignore in specific directory
    $0 /path/to/repo

    # Update all .gitignore files recursively
    $0 -r /path/to/repos

    # Dry run to see what would change
    $0 -r -d /path/to/repos

EOF
}

# Parse command line arguments
RECURSIVE=0
DRY_RUN=0
VERBOSE=0
TARGET_DIR="."

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -r|--recursive)
            RECURSIVE=1
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=1
            shift
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

# Validate target directory
if [ ! -d "$TARGET_DIR" ]; then
    print_error "Directory not found: $TARGET_DIR"
    exit 1
fi

print_info "Starting .gitignore update process"
print_info "Target directory: $TARGET_DIR"
print_info "Recursive mode: $RECURSIVE"
print_info "Dry run mode: $DRY_RUN"
echo ""

if [ $DRY_RUN -eq 1 ]; then
    print_warning "DRY RUN MODE - No changes will be made"
    echo ""
fi

# Process files
if [ $RECURSIVE -eq 1 ]; then
    print_info "Searching for .gitignore files recursively..."
    
    # Find all .gitignore files
    GITIGNORE_FILES=$(find "$TARGET_DIR" -name ".gitignore" -type f)
    
    if [ -z "$GITIGNORE_FILES" ]; then
        print_warning "No .gitignore files found"
        exit 0
    fi
    
    FILE_COUNT=$(echo "$GITIGNORE_FILES" | wc -l)
    print_info "Found $FILE_COUNT .gitignore file(s)"
    echo ""
    
    UPDATED_COUNT=0
    
    while IFS= read -r gitignore_file; do
        if [ $DRY_RUN -eq 0 ]; then
            gitignore_dir=$(dirname "$gitignore_file")
            if update_gitignore "$gitignore_dir"; then
                ((UPDATED_COUNT++))
            fi
        else
            print_info "Would process: $gitignore_file"
        fi
    done <<< "$GITIGNORE_FILES"
    
    echo ""
    if [ $DRY_RUN -eq 0 ]; then
        print_success "Updated $UPDATED_COUNT of $FILE_COUNT .gitignore file(s)"
    else
        print_info "Would update .gitignore files (dry run)"
    fi
else
    # Process single directory
    if [ $DRY_RUN -eq 0 ]; then
        if update_gitignore "$TARGET_DIR"; then
            print_success "Update complete"
        else
            print_info "No changes needed"
        fi
    else
        print_info "Would process: $TARGET_DIR/.gitignore"
    fi
fi

print_success "Process complete"
