#!/usr/bin/env python3
"""Generate Bash wrappers for all PHP CLI scripts in api/."""

import os

REPO        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASH_DIR    = os.path.join(REPO, "api", "wrappers", "bash")

SCRIPTS = [
    # (wrapper_name, script_path_from_repo_root, category)
    ("auto_detect_platform",       "api/validate/auto_detect_platform.php",          "validate"),
    ("check_changelog",            "api/validate/check_changelog.php",               "validate"),
    ("check_dolibarr_module",      "api/validate/check_dolibarr_module.php",         "validate"),
    ("check_enterprise_readiness", "api/validate/check_enterprise_readiness.php",    "validate"),
    ("check_joomla_manifest",      "api/validate/check_joomla_manifest.php",         "validate"),
    ("check_language_structure",   "api/validate/check_language_structure.php",      "validate"),
    ("check_license_headers",      "api/validate/check_license_headers.php",         "validate"),
    ("check_no_secrets",           "api/validate/check_no_secrets.php",              "validate"),
    ("check_paths",                "api/validate/check_paths.php",                   "validate"),
    ("check_php_syntax",           "api/validate/check_php_syntax.php",              "validate"),
    ("check_repo_health",          "api/validate/check_repo_health.php",             "validate"),
    ("check_structure",            "api/validate/check_structure.php",               "validate"),
    ("check_tabs",                 "api/validate/check_tabs.php",                    "validate"),
    ("check_version_consistency",  "api/validate/check_version_consistency.php",     "validate"),
    ("check_xml_wellformed",       "api/validate/check_xml_wellformed.php",          "validate"),
    ("scan_drift",                 "api/validate/scan_drift.php",                    "validate"),
    ("bulk_sync",                  "api/automation/bulk_sync.php",                   "automation"),
    ("deploy_sftp",                "api/deploy/deploy-sftp.php",                     "deploy"),
    ("fix_line_endings",           "api/fix/fix_line_endings.php",                   "fix"),
    ("fix_permissions",            "api/fix/fix_permissions.php",                    "fix"),
    ("fix_tabs",                   "api/fix/fix_tabs.php",                           "fix"),
    ("fix_trailing_spaces",        "api/fix/fix_trailing_spaces.php",                "fix"),
    ("pin_action_shas",            "api/maintenance/pin_action_shas.php",            "maintenance"),
    ("setup_labels",               "api/maintenance/setup_labels.php",               "maintenance"),
    ("sync_dolibarr_readmes",      "api/maintenance/sync_dolibarr_readmes.php",      "maintenance"),
    ("update_sha_hashes",          "api/maintenance/update_sha_hashes.php",          "maintenance"),
    ("update_version_from_readme", "api/maintenance/update_version_from_readme.php", "maintenance"),
    ("plugin_health_check",        "api/plugin_health_check.php",                    "plugin"),
    ("plugin_list",                "api/plugin_list.php",                            "plugin"),
    ("plugin_metrics",             "api/plugin_metrics.php",                         "plugin"),
    ("plugin_readiness",           "api/plugin_readiness.php",                       "plugin"),
    ("plugin_validate",            "api/plugin_validate.php",                        "plugin"),
]


def bash_wrapper(name: str, script_path: str, category: str) -> str:
    return (
        "#!/usr/bin/env bash\n"
        "# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>\n"
        "#\n"
        "# This file is part of a Moko Consulting project.\n"
        "#\n"
        "# SPDX-License-Identifier: GPL-3.0-or-later\n"
        "#\n"
        "# FILE INFORMATION\n"
        "# DEFGROUP: MokoStandards.Wrappers.Bash\n"
        "# INGROUP: MokoStandards.Wrappers\n"
        "# REPO: https://github.com/mokoconsulting-tech/MokoStandards\n"
        f"# PATH: /api/wrappers/bash/{name}.sh\n"
        "# VERSION: 04.00.15\n"
        f"# BRIEF: Bash wrapper for {script_path}\n"
        "\n"
        "set -euo pipefail\n"
        "\n"
        f'SCRIPT_NAME="{name}"\n'
        f'SCRIPT_PATH="{script_path}"\n'
        f'SCRIPT_CATEGORY="{category}"\n'
        "\n"
        "RED='\\033[0;31m'; GREEN='\\033[0;32m'; BLUE='\\033[0;34m'; NC='\\033[0m'\n"
        "\n"
        "log_info()    { echo -e \"${BLUE}[INFO]  $1${NC}\"; }\n"
        "log_success() { echo -e \"${GREEN}[OK]    $1${NC}\"; }\n"
        "log_error()   { echo -e \"${RED}[ERROR] $1${NC}\"; }\n"
        "\n"
        "get_repo_root() { git rev-parse --show-toplevel 2>/dev/null || pwd; }\n"
        "\n"
        "check_php() {\n"
        "  if command -v php &>/dev/null; then\n"
        "    echo php\n"
        "  else\n"
        "    log_error 'PHP is not installed or not in PATH'\n"
        "    echo 'Install PHP 8.1+: https://www.php.net/downloads'\n"
        "    exit 1\n"
        "  fi\n"
        "}\n"
        "\n"
        "main() {\n"
        "  local repo_root php_cmd full_path log_dir log_file timestamp exit_code\n"
        "  repo_root=$(get_repo_root)\n"
        "  php_cmd=$(check_php)\n"
        '  full_path="${repo_root}/${SCRIPT_PATH}"\n'
        "\n"
        '  if [[ ! -f "$full_path" ]]; then\n'
        '    log_error "Script not found: $full_path"\n'
        "    exit 1\n"
        "  fi\n"
        "\n"
        '  log_dir="${repo_root}/logs/${SCRIPT_CATEGORY}"\n'
        '  mkdir -p "$log_dir"\n'
        '  timestamp=$(date +"%Y%m%d_%H%M%S")\n'
        '  log_file="${log_dir}/${SCRIPT_NAME}_${timestamp}.log"\n'
        "\n"
        '  log_info "Running ${SCRIPT_NAME}..."\n'
        '  log_info "Log: ${log_file}"\n'
        "\n"
        "  set +e\n"
        '  "$php_cmd" "$full_path" "$@" 2>&1 | tee "$log_file"\n'
        "  exit_code=${PIPESTATUS[0]}\n"
        "  set -e\n"
        "\n"
        "  if [[ $exit_code -eq 0 ]]; then\n"
        '    log_success "${SCRIPT_NAME} completed successfully"\n'
        "  else\n"
        '    log_error "${SCRIPT_NAME} failed (exit ${exit_code}) — see ${log_file}"\n'
        "  fi\n"
        "  exit $exit_code\n"
        "}\n"
        "\n"
        'main "$@"\n'
    )


def main() -> None:
    count = 0
    for name, script_path, category in SCRIPTS:
        path = os.path.join(BASH_DIR, f"{name}.sh")
        with open(path, "w", newline="\n") as fh:
            fh.write(bash_wrapper(name, script_path, category))
        print(f"  {name}.sh")
        count += 1
    print(f"\nGenerated {count} Bash wrappers.")


if __name__ == "__main__":
    main()
