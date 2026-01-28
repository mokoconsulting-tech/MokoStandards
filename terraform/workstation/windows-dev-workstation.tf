# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Terraform.DevWorkstation
# INGROUP: MokoStandards.Infrastructure
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: terraform/workstation/dev-workstation.tf
# VERSION: 01.00.00
# BRIEF: Terraform definition for Windows development workstation provisioning configuration

locals {
  dev_workstation_config = {
    metadata = {
      name            = "Windows Developer Workstation Configuration"
      version         = "1.0.0"
      description     = "Standardized configuration for Windows development workstations"
      platform        = "windows"
      last_updated    = "2026-01-27T00:00:00Z"
      maintainer      = "MokoStandards Team"
      documentation   = "docs/scripts/automation/dev-workstation-provisioner.md"
      source_script   = "scripts/automation/dev-workstation-provisioner.ps1"
    }

    # Workspace configuration
    workspace = {
      default_path      = "$env:USERPROFILE\\Documents\\Workspace"
      create_if_missing = true
      artifacts = [
        "winget-monthly-update.cmd",
        "logs",
        "scripts"
      ]
    }

    # Package management configuration
    winget = {
      update_schedule = {
        type      = "monthly"
        day       = 1
        time      = "09:00"
        task_name = "Winget Monthly Update (Exclude PHP and Python)"
      }

      upgrade_options = {
        mode                      = "all"
        silent                    = true
        accept_package_agreements = true
        accept_source_agreements  = true
      }

      # Packages to exclude from automatic updates
      excluded_packages = [
        {
          id     = "Python.Python.3.10"
          reason = "Pinned version for compatibility"
        },
        {
          id     = "PHP.PHP"
          reason = "Managed separately via WSL or manual install"
        }
      ]

      log_location = "C:\\Logs\\Winget"
    }

    # WSL (Windows Subsystem for Linux) configuration
    wsl = {
      enabled              = true
      default_distro       = "Ubuntu"
      require_confirmation = true

      features = {
        subsystem_linux = "Microsoft-Windows-Subsystem-Linux"
        virtual_machine = "VirtualMachinePlatform"
      }

      provisioning = {
        auto_install            = false # Requires user confirmation
        auto_reset              = false # Requires user confirmation
        provision_after_install = true
      }
    }

    # Ubuntu WSL configuration
    ubuntu_wsl = {
      distro_name = "Ubuntu"
      version     = "latest"

      # PHP configuration for development
      php = {
        version = "8.3"

        packages = [
          "php8.3-cli",
          "php8.3-common",
          "php8.3-opcache",
          "php8.3-mysql",
          "php8.3-curl",
          "php8.3-mbstring",
          "php8.3-intl",
          "php8.3-gd",
          "php8.3-zip",
          "php8.3-soap",
          "php8.3-imagick",
          "php8.3-apcu",
          "php8.3-imap"
        ]

        enabled_modules = [
          "curl",
          "mbstring",
          "intl",
          "gd",
          "zip",
          "soap",
          "imagick",
          "opcache",
          "mysqli",
          "pdo_mysql",
          "apcu",
          "imap"
        ]
      }

      provisioning_script = <<-BASH
        set -euo pipefail
        
        sudo apt update
        sudo apt install -y \
          php8.3-cli php8.3-common php8.3-opcache php8.3-mysql \
          php8.3-curl php8.3-mbstring php8.3-intl php8.3-gd php8.3-zip php8.3-soap \
          php8.3-imagick php8.3-apcu php8.3-imap
        
        sudo phpenmod -v 8.3 -s cli \
          curl mbstring intl gd zip soap imagick opcache mysqli pdo_mysql apcu imap
        
        php -v
        php -m | sort
      BASH
    }

    # Security and governance
    security = {
      require_admin              = true
      user_confirmation_required = true

      confirmation_gates = [
        {
          action  = "wsl_reset"
          message = "WSL is already installed. Do you want to RESET Ubuntu WSL?"
          title   = "WSL Detected"
          type    = "warning"
          default = "no"
        },
        {
          action  = "wsl_install"
          message = "WSL is not fully provisioned. Install WSL with Ubuntu?"
          title   = "WSL Not Installed"
          type    = "question"
          default = "no"
        }
      ]
    }

    # Operational parameters
    operations = {
      verbose_logging      = false
      log_to_file          = true
      create_restore_point = false

      validation_checks = [
        "admin_privileges",
        "winget_availability",
        "disk_space",
        "internet_connectivity"
      ]
    }

    # Pinned versions and compatibility
    runtime_versions = {
      python = {
        pinned_version = "3.10"
        update_policy  = "manual"
        reason         = "Application compatibility requirements"
      }

      php = {
        pinned_version = "8.3"
        update_policy  = "wsl_managed"
        reason         = "Managed via WSL Ubuntu for consistency"
      }
    }
  }
}

# Output the configuration for use by provisioning scripts
output "dev_workstation_config" {
  description = "Windows developer workstation configuration"
  value       = local.dev_workstation_config
}

# Output PowerShell command generation template
output "powershell_script_template" {
  description = "Template for generating PowerShell provisioning script"
  value = {
    winget_monthly_task = {
      task_name         = local.dev_workstation_config.winget.update_schedule.task_name
      schedule_day      = local.dev_workstation_config.winget.update_schedule.day
      schedule_time     = local.dev_workstation_config.winget.update_schedule.time
      excluded_packages = [for pkg in local.dev_workstation_config.winget.excluded_packages : pkg.id]
      log_root          = local.dev_workstation_config.winget.log_location
    }

    wsl_provisioning = {
      enabled      = local.dev_workstation_config.wsl.enabled
      distro       = local.dev_workstation_config.ubuntu_wsl.distro_name
      php_version  = local.dev_workstation_config.ubuntu_wsl.php.version
      php_packages = local.dev_workstation_config.ubuntu_wsl.php.packages
      setup_script = local.dev_workstation_config.ubuntu_wsl.provisioning_script
    }
  }
}

# Output validation rules
output "workstation_validation" {
  description = "Validation rules for workstation provisioning"
  value = {
    required_checks = local.dev_workstation_config.operations.validation_checks
    security_gates  = local.dev_workstation_config.security.confirmation_gates
    pinned_versions = local.dev_workstation_config.runtime_versions
  }
}
