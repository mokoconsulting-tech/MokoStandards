# Variables for repository schema configuration

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
