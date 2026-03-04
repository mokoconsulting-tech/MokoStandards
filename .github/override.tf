# Repository Health Check Override Configuration
# Location: .github/override.tf
# 
# This file allows repository-specific customization of health checks.
# It overrides the default configuration from MokoStandards.
# 
# MokoStandards Repository: This is the source repository for standards and templates.
# Configuration is customized to reflect its role as a template/standards repository.

locals {
  # Repository-specific metadata
  override_metadata = {
    repository_name = "MokoStandards"
    repository_type = "standards" # This is the standards/templates repository
    override_reason = "Source repository for organizational standards - custom health checks for template repository"
    last_updated    = "2026-03-03"
    auto_synced     = false # This repository is the source, not synced to
  }
  
  # Disable specific checks (by check ID)
  # Some checks don't apply to the standards repository itself
  disabled_checks = [
    # MokoStandards contains workflow TEMPLATES, not the actual workflows
    # that get synced TO other repositories, so disable checks for "live" workflows
    # "ci-workflow-present",  # We have templates/workflows, not .github/workflows for projects
  ]
  
  # Adjust point values for specific checks
  # Standards repository has different priorities
  custom_point_values = {
    # Documentation is critical for a standards repository
    # "docs-index-present" = 10
    # "docs-comprehensive" = 10
  }
  
  # Custom category point adjustments
  custom_category_points = {
    # Documentation and templates are more important for standards repo
    # documentation = 25
    # templates = 20
  }
  
  # Custom threshold percentages
  custom_thresholds = {
    # MokoStandards should maintain high quality standards
    excellent = 95  # High bar for the standards repository
    good      = 85
    fair      = 70
    poor      = 0
  }
  
  # Additional repository-specific checks for MokoStandards
  additional_checks = {
    api_scripts_present = {
      id          = "api-scripts-present"
      name        = "API Scripts Directory"
      description = "Check for api/ directory with validation and automation scripts"
      points      = 5
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Ensure api/ directory exists with subdirectories: validate, automation, build"
      parameters  = {
        directory_path = "api"
      }
    }
    
    templates_directory = {
      id          = "templates-directory-present"
      name        = "Templates Directory"
      description = "Check for templates/ directory with workflow and config templates"
      points      = 10
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Ensure templates/ directory exists with subdirectories: workflows, github, docs, configs"
      parameters  = {
        directory_path = "templates"
      }
    }
    
    definitions_present = {
      id          = "definitions-present"
      name        = "Repository Definitions"
      description = "Check for api/definitions/ directory with repository structure definitions"
      points      = 5
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Ensure api/definitions/ directory exists with .tf definition files"
      parameters  = {
        directory_path = "api/definitions"
      }
    }
    
    standards_definition_exists = {
      id          = "standards-definition-exists"
      name        = "Standards Repository Definition"
      description = "Check for standards-repository.tf definition file"
      points      = 3
      check_type  = "file-exists"
      category    = "required-files"
      required    = true
      remediation = "Create api/definitions/standards-repository.tf"
      parameters  = {
        file_path = "api/definitions/standards-repository.tf"
      }
    }
  }
  
  # File sync exclusions
  # MokoStandards is the SOURCE, so it doesn't receive syncs
  # But this documents what files are templates vs. actual configs
  sync_exclusions = [
    # These are specific to MokoStandards repository operations
    ".github/workflows/bulk-repo-sync.yml",
    ".github/workflows/standards-validation.yml",
    "api/automation/bulk_sync.php",
    "api/validate/auto_detect_platform.php",
  ]
  
  # Protected files
  # Files that should never be overwritten (MokoStandards specific)
  protected_files = [
    # Core repository configuration
    ".github/config.tf",
    ".github/override.tf",
    
    # MokoStandards-specific workflows
    ".github/workflows/bulk-repo-sync.yml",
    ".github/workflows/standards-compliance.yml",
    
    # Repository structure definitions
    "api/definitions/standards-repository.tf",
    "api/definitions/default-repository.tf",
    "api/definitions/crm-module.tf",
    "api/definitions/waas-component.tf",
    "api/definitions/generic-repository.tf",
    
    # Critical documentation
    "README.md",
    "ROADMAP.md",
    "docs/policy/*",
  ]
}

# Export overrides for consumption by health check validation
output "health_check_overrides" {
  description = "Repository-specific health check overrides for MokoStandards"
  value = {
    metadata          = local.override_metadata
    disabled_checks   = local.disabled_checks
    custom_points     = local.custom_point_values
    custom_categories = local.custom_category_points
    custom_thresholds = local.custom_thresholds
    additional_checks = local.additional_checks
    sync_exclusions   = local.sync_exclusions
    protected_files   = local.protected_files
  }
}

# Override configuration summary
output "override_summary" {
  description = "Summary of active overrides for MokoStandards repository"
  value = {
    total_disabled_checks    = length(local.disabled_checks)
    total_custom_points      = length(local.custom_point_values)
    total_custom_categories  = length(local.custom_category_points)
    total_additional_checks  = length(local.additional_checks)
    total_sync_exclusions    = length(local.sync_exclusions)
    total_protected_files    = length(local.protected_files)
    has_custom_thresholds    = length(local.custom_thresholds) > 0
    repository_role          = "standards-source"
  }
}
