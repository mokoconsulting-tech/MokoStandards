# Outputs for Terraform schema configuration


locals {
  # Metadata for this configuration
  config_metadata = {
    name            = "Outputs"
    description     = "Output definitions for Terraform configuration"
    version         = "2.0.0"
    last_updated    = "2026-01-28"
    maintainer      = "MokoStandards Team"
    schema_version  = "2.0"
    repository_url  = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type = "standards"
    format          = "terraform"
  }
}

output "schema_version" {
  description = "Current schema version"
  value       = var.schema_version
}

output "repository_types" {
  description = "List of supported repository types"
  value = [
    "default",
    "library",
    "application"
  ]
}
