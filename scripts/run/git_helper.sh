#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts.Utility
# INGROUP: MokoStandards.Scripts
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/run/git_helper.sh
# VERSION: 02.00.00
# BRIEF: Helper script for common git operations
# PATH: /scripts/run/git_helper.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to display help
show_help() {
    cat << EOF
Git Helper Script - Common Git Operations

Usage: $0 <command> [options]

Commands:
  status          Show repository status with summary
  clean           Clean untracked files and directories (interactive)
  sync            Sync with remote (fetch and pull)
  branch          List branches with last commit dates
  stash           Stash changes with description
  unstash         List and apply stashes
  history         Show commit history (last 10 commits)
  search          Search commit messages
  undo-commit     Undo last commit (keeps changes)
  diff-stats      Show diff statistics
  conflicts       Show files with merge conflicts

Options:
  -h, --help      Show this help message

Examples:
  $0 status
  $0 clean
  $0 branch
  $0 search "fix bug"
  $0 history

EOF
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
}

# Show enhanced status
cmd_status() {
    print_info "Repository Status"
    echo "===================="
    
    # Current branch
    branch=$(git rev-parse --abbrev-ref HEAD)
    print_info "Current branch: $branch"
    
    # Remote tracking
    remote=$(git config branch.$branch.remote 2>/dev/null || echo "none")
    print_info "Remote: $remote"
    
    # Commit status
    echo ""
    print_info "Recent commits:"
    git log --oneline -5
    
    # Status
    echo ""
    print_info "Working tree status:"
    git status --short
    
    # Statistics
    echo ""
    modified=$(git status --short | grep -c "^ M" || echo 0)
    added=$(git status --short | grep -c "^A" || echo 0)
    deleted=$(git status --short | grep -c "^D" || echo 0)
    untracked=$(git status --short | grep -c "^??" || echo 0)
    
    print_info "Summary: $modified modified, $added added, $deleted deleted, $untracked untracked"
}

# Clean untracked files
cmd_clean() {
    print_warning "This will show what would be removed"
    git clean -nfd
    
    echo ""
    read -p "Do you want to remove these files? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git clean -fd
        print_success "Cleaned untracked files"
    else
        print_info "Cancelled"
    fi
}

# Sync with remote
cmd_sync() {
    print_info "Fetching from remote..."
    git fetch --all --prune
    
    branch=$(git rev-parse --abbrev-ref HEAD)
    print_info "Pulling $branch..."
    
    if git pull --rebase; then
        print_success "Successfully synced with remote"
    else
        print_error "Failed to sync. Check for conflicts."
        exit 1
    fi
}

# List branches with dates
cmd_branch() {
    print_info "Branches (sorted by last commit date)"
    echo "=========================================="
    
    git for-each-ref --sort=-committerdate refs/heads/ \
        --format='%(HEAD) %(color:yellow)%(refname:short)%(color:reset) - %(color:green)%(committerdate:relative)%(color:reset) - %(contents:subject) - %(authorname)'
}

# Stash with description
cmd_stash() {
    if [ -z "$1" ]; then
        print_error "Please provide a stash description"
        echo "Usage: $0 stash <description>"
        exit 1
    fi
    
    git stash push -m "$1"
    print_success "Stashed changes: $1"
}

# List and apply stashes
cmd_unstash() {
    print_info "Available stashes:"
    git stash list
    
    echo ""
    read -p "Enter stash number to apply (or press Enter to cancel): " stash_num
    
    if [ -n "$stash_num" ]; then
        git stash apply stash@{$stash_num}
        print_success "Applied stash@{$stash_num}"
    else
        print_info "Cancelled"
    fi
}

# Show commit history
cmd_history() {
    count=${1:-10}
    print_info "Last $count commits:"
    echo "===================="
    
    git log --oneline --graph --decorate -$count
}

# Search commit messages
cmd_search() {
    if [ -z "$1" ]; then
        print_error "Please provide a search term"
        echo "Usage: $0 search <term>"
        exit 1
    fi
    
    print_info "Searching for: $1"
    echo "===================="
    
    git log --all --grep="$1" --oneline
}

# Undo last commit
cmd_undo_commit() {
    print_warning "This will undo the last commit but keep your changes"
    
    read -p "Continue? (y/N) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git reset --soft HEAD~1
        print_success "Last commit undone (changes preserved)"
    else
        print_info "Cancelled"
    fi
}

# Show diff statistics
cmd_diff_stats() {
    print_info "Diff statistics:"
    echo "===================="
    
    git diff --stat
    
    if [ -z "$(git diff --stat)" ]; then
        print_info "No changes in working directory"
        
        echo ""
        print_info "Staged changes:"
        git diff --cached --stat
    fi
}

# Show merge conflicts
cmd_conflicts() {
    conflicts=$(git diff --name-only --diff-filter=U)
    
    if [ -z "$conflicts" ]; then
        print_success "No merge conflicts"
    else
        print_warning "Files with conflicts:"
        echo "$conflicts"
        
        echo ""
        print_info "To resolve:"
        echo "  1. Edit the conflicted files"
        echo "  2. git add <file>"
        echo "  3. git commit"
    fi
}

# Main script
check_git_repo

case "${1:-}" in
    status)
        cmd_status
        ;;
    clean)
        cmd_clean
        ;;
    sync)
        cmd_sync
        ;;
    branch)
        cmd_branch
        ;;
    stash)
        cmd_stash "$2"
        ;;
    unstash)
        cmd_unstash
        ;;
    history)
        cmd_history "$2"
        ;;
    search)
        cmd_search "$2"
        ;;
    undo-commit)
        cmd_undo_commit
        ;;
    diff-stats)
        cmd_diff_stats
        ;;
    conflicts)
        cmd_conflicts
        ;;
    -h|--help|help)
        show_help
        ;;
    "")
        print_error "No command specified"
        echo ""
        show_help
        exit 1
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
