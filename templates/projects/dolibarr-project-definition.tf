/**
 * Dolibarr Module Project Template
 * Standard project configuration for Dolibarr ERP/CRM module development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Dolibarr Module Project"
      description = "Standard project template for Dolibarr ERP/CRM module development"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "dolibarr"
    }

    custom_fields = [
      {
        name        = "Status"
        type        = "single_select"
        description = "Current lifecycle state of the task"
        options     = ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done", "Blocked", "Cancelled"]
      },
      {
        name        = "Priority"
        type        = "single_select"
        description = "Urgency and importance of the task"
        options     = ["Critical", "High", "Medium", "Low"]
      },
      {
        name        = "Size/Effort"
        type        = "single_select"
        description = "Estimated complexity and work effort"
        options     = ["XS - 1-2 hours", "S - 2-4 hours", "M - 1-2 days", "L - 3-5 days", "XL - 1-2 weeks", "XXL - 2+ weeks"]
      },
      {
        name        = "Sprint"
        type        = "text"
        description = "Sprint or iteration identifier"
      },
      {
        name        = "Target Version"
        type        = "text"
        description = "Target release version (semantic versioning)"
      },
      {
        name        = "Blocked Reason"
        type        = "text"
        description = "Description of what is blocking progress"
      },
      {
        name        = "Acceptance Criteria"
        type        = "text"
        description = "List of criteria that must be met for task completion"
      },
      {
        name        = "Dolibarr Version"
        type        = "single_select"
        description = "Target Dolibarr version for compatibility"
        options     = ["16.0", "17.0", "18.0", "19.0", "20.0", "Multiple"]
      },
      {
        name        = "Module Number"
        type        = "number"
        description = "Unique Dolibarr module number (100000-999999)"
      },
      {
        name        = "Database Changes"
        type        = "single_select"
        description = "Type of database changes required"
        options     = ["None", "Schema Only", "Data Migration", "Both", "TBD"]
      },
      {
        name        = "Module Descriptor"
        type        = "text"
        description = "Path to module descriptor file (modMyModule.class.php)"
      },
      {
        name        = "Module Version"
        type        = "text"
        description = "Current module version number (semantic versioning)"
      },
      {
        name        = "PHP Minimum"
        type        = "single_select"
        description = "Minimum PHP version required"
        options     = ["7.4", "8.0", "8.1", "8.2", "8.3"]
      },
      {
        name        = "Requires Sudo"
        type        = "single_select"
        description = "Does installation/upgrade require sudo privileges?"
        options     = ["Yes", "No", "Optional"]
      },
      {
        name        = "Module Family"
        type        = "single_select"
        description = "Dolibarr module family/category"
        options     = ["CRM", "Financial", "HR", "Projects", "Products/Services", "Interfaces", "Other"]
      },
      {
        name        = "Has Triggers"
        type        = "single_select"
        description = "Does the module implement triggers?"
        options     = ["Yes", "No"]
      },
      {
        name        = "Has Hooks"
        type        = "single_select"
        description = "Does the module use hooks?"
        options     = ["Yes", "No"]
      },
      {
        name        = "Has Widgets"
        type        = "single_select"
        description = "Does the module provide dashboard widgets?"
        options     = ["Yes", "No"]
      },
      {
        name        = "Migration Script"
        type        = "text"
        description = "Path to migration/upgrade SQL scripts"
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "Comprehensive view of all items"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Assignees", "Sprint", "Dolibarr Version", "Module Family"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          },
          {
            field     = "Status"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Sprint Board"
        type        = "board"
        description = "Kanban board for current sprint"
        group_by    = "Status"
        filter = {
          field    = "Sprint"
          operator = "is_not_empty"
          value    = ""
        }
        columns = ["Title", "Priority", "Size/Effort", "Assignees", "Dolibarr Version"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Release Roadmap"
        type        = "roadmap"
        description = "Timeline view of module releases"
        group_by    = "Target Version"
        filter = {
          field    = "Status"
          operator = "not_equals"
          value    = "Cancelled"
        }
        columns = ["Title", "Status", "Priority", "Module Family"]
        sort = [
          {
            field     = "Target Version"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Blocked Items"
        type        = "table"
        description = "All blocked items requiring attention"
        filter = {
          field    = "Status"
          operator = "equals"
          value    = "Blocked"
        }
        columns = ["Title", "Priority", "Blocked Reason", "Assignees", "Sprint"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Module Compatibility Matrix"
        type        = "table"
        description = "View by Dolibarr version compatibility"
        group_by    = "Dolibarr Version"
        columns     = ["Title", "Module Family", "Status", "Module Version", "PHP Minimum"]
        sort = [
          {
            field     = "Module Family"
            direction = "asc"
          },
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Database Migration Tracker"
        type        = "table"
        description = "Track database schema changes and data migrations"
        group_by    = "Database Changes"
        filter = {
          field    = "Database Changes"
          operator = "not_equals"
          value    = "None"
        }
        columns = ["Title", "Database Changes", "Status", "Migration Script", "Target Version"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
    ]

    workflows = [
      {
        name    = "Auto-status on PR creation"
        trigger = "pull_request_opened"
        actions = [
          {
            set_field = "Status"
            value     = "In Review"
          }
        ]
      },
      {
        name    = "Auto-status on PR merge"
        trigger = "pull_request_merged"
        actions = [
          {
            set_field = "Status"
            value     = "Testing"
          }
        ]
      },
      {
        name    = "Update Module Version on release"
        trigger = "release_published"
        actions = [
          {
            action  = "extract_version_from_tag"
            target  = "Module Version"
          }
        ]
      },
      {
        name    = "Database changes validation"
        trigger = "field_changed"
        field   = "Database Changes"
        actions = [
          {
            action = "check_migration_script_exists"
          },
          {
            notify = "assignees"
            condition = "script_missing"
          }
        ]
      },
    ]

    metadata = {
      version = "1.0.0"
      created = "2026-01-04"
      author  = "Moko Consulting"
      license = "GPL-3.0-or-later"
    }
  }
}

output "dolibarr_project_config" {
  description = "Dolibarr Module project template configuration"
  value       = local.project_config
}
