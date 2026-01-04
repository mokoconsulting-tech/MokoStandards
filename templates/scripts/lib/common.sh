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

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
  echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

log_fatal() {
  echo -e "${RED}[FATAL]${NC} $*" >&2
  exit 1
}

# Check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Require command
require_command() {
  if ! command_exists "$1"; then
    log_fatal "Required command not found: $1"
  fi
}

# Get git root directory
get_git_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}

# Check if running in git repository
is_git_repo() {
  git rev-parse --git-dir >/dev/null 2>&1
}

# Get current git branch
get_current_branch() {
  git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

# Export functions
export -f log_info log_warn log_error log_fatal
export -f command_exists require_command
export -f get_git_root is_git_repo get_current_branch
