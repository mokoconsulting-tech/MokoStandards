#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Wrappers.Bash
# INGROUP: MokoStandards.Wrappers
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /api/wrappers/bash/fix_tabs.sh
# VERSION: 04.00.15
# BRIEF: Bash wrapper for api/fix/fix_tabs.php

set -euo pipefail

SCRIPT_NAME="fix_tabs"
SCRIPT_PATH="api/fix/fix_tabs.php"
SCRIPT_CATEGORY="fix"

RED='\033[0;31m'; GREEN='\033[0;32m'; BLUE='\033[0;34m'; NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]  $1${NC}"; }
log_success() { echo -e "${GREEN}[OK]    $1${NC}"; }
log_error()   { echo -e "${RED}[ERROR] $1${NC}"; }

get_repo_root() { git rev-parse --show-toplevel 2>/dev/null || pwd; }

check_php() {
  if command -v php &>/dev/null; then
    echo php
  else
    log_error 'PHP is not installed or not in PATH'
    echo 'Install PHP 8.1+: https://www.php.net/downloads'
    exit 1
  fi
}

main() {
  local repo_root php_cmd full_path log_dir log_file timestamp exit_code
  repo_root=$(get_repo_root)
  php_cmd=$(check_php)
  full_path="${repo_root}/${SCRIPT_PATH}"

  if [[ ! -f "$full_path" ]]; then
    log_error "Script not found: $full_path"
    exit 1
  fi

  log_dir="${repo_root}/logs/${SCRIPT_CATEGORY}"
  mkdir -p "$log_dir"
  timestamp=$(date +"%Y%m%d_%H%M%S")
  log_file="${log_dir}/${SCRIPT_NAME}_${timestamp}.log"

  log_info "Running ${SCRIPT_NAME}..."
  log_info "Log: ${log_file}"

  set +e
  "$php_cmd" "$full_path" "$@" 2>&1 | tee "$log_file"
  exit_code=${PIPESTATUS[0]}
  set -e

  if [[ $exit_code -eq 0 ]]; then
    log_success "${SCRIPT_NAME} completed successfully"
  else
    log_error "${SCRIPT_NAME} failed (exit ${exit_code}) — see ${log_file}"
  fi
  exit $exit_code
}

main "$@"
