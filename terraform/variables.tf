# Variables for repository schema configuration

locals {
  # Metadata for this configuration
  config_metadata = {
    name           = "Repository Schema Variables"
    description    = "Variable definitions for MokoStandards repository schemas and health thresholds"
    version        = "2.0.0"
    last_updated   = "2026-01-28"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type = "standards"
    format          = "terraform"
  }
}

variable "schema_version" {
  description = "Version of the schema specification"
  type        = string
  default     = "2.0"
}

variable "enable_strict_validation" {
  description = "Enable strict validation mode"
  type        = bool
  default     = false
}

variable "custom_health_thresholds" {
  description = "Custom health score thresholds (overrides defaults)"
  type = map(object({
    level          = string
    min_percentage = number
    max_percentage = number
    indicator      = string
    description    = string
  }))
  default = {}
}
