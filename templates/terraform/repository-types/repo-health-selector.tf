# Repository Health Configuration Selector
# This file provides a selector mechanism to choose the appropriate health configuration
# based on repository type
# 
# Usage: Pass repository_type variable to get the correct health configuration
# Supported types: standards, generic, terraform, nodejs, joomla, dolibarr

variable "repository_type" {
  description = "Type of repository (standards, generic, terraform, nodejs, joomla, dolibarr)"
  type        = string
  default     = "generic"
  
  validation {
    condition     = contains(["standards", "generic", "terraform", "nodejs", "joomla", "dolibarr"], var.repository_type)
    error_message = "Repository type must be one of: standards, generic, terraform, nodejs, joomla, dolibarr"
  }
}

locals {
  # Map of all available health configurations
  health_configs = {
    standards = {
      config    = try(output.repo_health_config.value, null)
      source    = "repo-health-standards.tf"
      points    = 103
      description = "Complete standards repository validation (MokoStandards itself)"
    }
    
    generic = {
      config    = try(output.generic_repo_health_config.value, null)
      source    = "repo-health-generic.tf"
      points    = 88
      description = "Generic libraries and projects"
    }
    
    terraform = {
      config    = try(output.terraform_repo_health_config.value, null)
      source    = "repo-health-terraform.tf"
      points    = 110
      description = "Terraform infrastructure repositories"
    }
    
    nodejs = {
      config    = try(output.nodejs_repo_health_config.value, null)
      source    = "repo-health-nodejs.tf"
      points    = 95
      description = "Node.js/JavaScript/TypeScript projects"
    }
    
    joomla = {
      config    = try(output.joomla_repo_health_config.value, null)
      source    = "repo-health-joomla.tf"
      points    = 98
      description = "Joomla extensions and components"
    }
    
    dolibarr = {
      config    = try(output.dolibarr_repo_health_config.value, null)
      source    = "repo-health-dolibarr.tf"
      points    = 96
      description = "Dolibarr modules and extensions"
    }
  }
  
  # Selected configuration based on repository_type variable
  selected_config = local.health_configs[var.repository_type]
  
  # Metadata about the selection
  selector_metadata = {
    repository_type = var.repository_type
    config_source   = local.selected_config.source
    total_points    = local.selected_config.points
    description     = local.selected_config.description
    version         = "04.00.04"
    last_updated    = "2026-02-27"
  }
  
  # Configuration summary
  config_summary = {
    for type, cfg in local.health_configs : type => {
      points      = cfg.points
      description = cfg.description
      source      = cfg.source
    }
  }
  
  # Override file location (standardized across all repository types)
  override_file_location = ".github/override.tf"
  
  # Common override instructions
  override_instructions = {
    file_location = local.override_file_location
    description   = "Repository-specific health check customizations"
    purpose       = "Override default health check configurations per repository"
    example = <<-EOT
      # Example .github/override.tf
      # Override health check configuration for this repository
      
      locals {
        # Disable specific checks
        disabled_checks = ["npm-publish-workflow", "deployment-secrets-documented"]
        
        # Adjust point values
        custom_points = {
          "ci-workflow-present" = 10  # Increase from default 5
        }
        
        # Custom thresholds
        custom_thresholds = {
          excellent = 95  # Raise bar for excellence
        }
      }
    EOT
  }
}

# Output the selected health configuration
output "selected_repo_health_config" {
  description = "Selected repository health configuration based on repository type"
  value = {
    metadata          = local.selector_metadata
    health_config     = local.selected_config.config
    override_location = local.override_file_location
    override_guide    = local.override_instructions
  }
}

# Output summary of all available configurations
output "available_health_configs" {
  description = "Summary of all available health configurations"
  value       = local.config_summary
}

# Output repository type mapping for reference
output "repository_type_mapping" {
  description = "Mapping of repository types to their health configurations"
  value = {
    standards = {
      name        = "MokoStandards Repository"
      points      = 103
      strictness  = "highest"
      use_case    = "The MokoStandards repository itself"
    }
    
    terraform = {
      name        = "Terraform Infrastructure"
      points      = 110
      strictness  = "highest"
      use_case    = "Infrastructure as Code repositories with cloud deployments"
    }
    
    joomla = {
      name        = "Joomla Extensions"
      points      = 98
      strictness  = "high"
      use_case    = "Joomla components, modules, plugins, and templates"
    }
    
    dolibarr = {
      name        = "Dolibarr Modules"
      points      = 96
      strictness  = "high"
      use_case    = "Dolibarr ERP/CRM modules and extensions"
    }
    
    nodejs = {
      name        = "Node.js Projects"
      points      = 95
      strictness  = "medium-high"
      use_case    = "Node.js, JavaScript, TypeScript libraries and applications"
    }
    
    generic = {
      name        = "Generic Libraries"
      points      = 88
      strictness  = "medium"
      use_case    = "General-purpose libraries and projects in any language"
    }
  }
}

# Output override configuration template
output "override_config_template" {
  description = "Template for creating .github/override.tf in target repositories"
  value = <<-EOT
    # Repository Health Check Override Configuration
    # Location: .github/override.tf
    # 
    # This file allows repository-specific customization of health checks.
    # It overrides the default configuration from MokoStandards.
    # 
    # Repository Type: ${var.repository_type}
    # Default Points: ${local.selected_config.points}
    # Configuration Source: ${local.selected_config.source}
    
    locals {
      # Repository-specific metadata
      override_metadata = {
        repository_name = "your-repo-name"
        override_reason = "Describe why overrides are needed"
        last_updated    = "2026-02-27"
      }
      
      # Disable specific checks (by check ID)
      disabled_checks = [
        # Example: "npm-publish-workflow",
        # Example: "deployment-secrets-documented",
      ]
      
      # Adjust point values for specific checks
      custom_point_values = {
        # Example: "ci-workflow-present" = 10
        # Example: "security-scan" = 15
      }
      
      # Custom category point adjustments
      custom_category_points = {
        # Example: ci_cd_status = 20
        # Example: security = 25
      }
      
      # Custom threshold percentages
      custom_thresholds = {
        # excellent = 95
        # good      = 80
        # fair      = 60
        # poor      = 0
      }
      
      # Additional repository-specific checks
      additional_checks = {
        # Add custom checks specific to this repository
        # Example:
        # custom_check = {
        #   id          = "custom-check"
        #   name        = "Custom Check"
        #   description = "Repository-specific validation"
        #   points      = 5
        #   check_type  = "file-exists"
        #   category    = "custom"
        #   required    = false
        #   remediation = "Add custom configuration"
        #   parameters  = {
        #     file_path = "custom.config"
        #   }
        # }
      }
    }
    
    # Export overrides for consumption by health check validation
    output "health_check_overrides" {
      description = "Repository-specific health check overrides"
      value = {
        metadata         = local.override_metadata
        disabled_checks  = local.disabled_checks
        custom_points    = local.custom_point_values
        custom_categories = local.custom_category_points
        custom_thresholds = local.custom_thresholds
        additional_checks = local.additional_checks
      }
    }
  EOT
}
