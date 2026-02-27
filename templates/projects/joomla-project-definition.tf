/**
 * Joomla Extension Project Template
 * Standard project configuration for Joomla extension development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Joomla Extension Project"
      description = "Standard project template for Joomla extension development (components, modules, plugins, libraries, packages, templates)"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "joomla"
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
        description = "Sprint or iteration identifier (e.g., Sprint 23, 2026-Q1-Sprint-3)"
      },
      {
        name        = "Target Version"
        type        = "text"
        description = "Target release version (semantic versioning, e.g., 1.2.3)"
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
        name        = "Joomla Version"
        type        = "single_select"
        description = "Target Joomla version for compatibility"
        options     = ["3.10", "4.4", "5.0", "5.1", "Multiple"]
      },
      {
        name        = "Extension Type"
        type        = "single_select"
        description = "Type of Joomla extension being developed"
        options     = ["Component", "Module", "Plugin", "Library", "Package", "Template"]
      },
      {
        name        = "Marketplace Status"
        type        = "single_select"
        description = "Current status in Joomla Extensions Directory (JED)"
        options     = ["Not Published", "In Review", "Published", "Rejected", "Not Applicable"]
      },
      {
        name        = "Update Server URL"
        type        = "text"
        description = "URL to the extension's update XML file"
      },
      {
        name        = "Extension Version"
        type        = "text"
        description = "Current extension version number (semantic versioning)"
      },
      {
        name        = "PHP Minimum"
        type        = "single_select"
        description = "Minimum PHP version required"
        options     = ["7.4", "8.0", "8.1", "8.2", "8.3"]
      },
      {
        name        = "Installation Type"
        type        = "single_select"
        description = "Type of installation supported"
        options     = ["Fresh Install", "Update", "Migration", "All"]
      },
      {
        name        = "Manifest File"
        type        = "text"
        description = "Path to the extension manifest XML file"
      },
      {
        name        = "Has Frontend"
        type        = "single_select"
        description = "Does the extension have frontend components?"
        options     = ["Yes", "No"]
      },
      {
        name        = "Has Backend"
        type        = "single_select"
        description = "Does the extension have backend/admin components?"
        options     = ["Yes", "No"]
      },
      {
        name        = "Has API"
        type        = "single_select"
        description = "Does the extension provide API endpoints?"
        options     = ["Yes", "No"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "Comprehensive view of all items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Assignees", "Sprint", "Joomla Version", "Extension Type"]
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
        description = "Kanban board for current sprint work"
        group_by    = "Status"
        filter = {
          field    = "Sprint"
          operator = "is_not_empty"
          value    = ""
        }
        columns = ["Title", "Priority", "Size/Effort", "Assignees", "Joomla Version"]
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
        description = "Timeline view of releases and versions"
        group_by    = "Target Version"
        filter = {
          field    = "Status"
          operator = "not_equals"
          value    = "Cancelled"
        }
        columns = ["Title", "Status", "Priority", "Extension Type"]
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
        name        = "Extension Compatibility Matrix"
        type        = "table"
        description = "View by Joomla version compatibility"
        group_by    = "Joomla Version"
        columns     = ["Title", "Extension Type", "Status", "Extension Version", "PHP Minimum"]
        sort = [
          {
            field     = "Extension Type"
            direction = "asc"
          },
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Marketplace Pipeline"
        type        = "board"
        description = "Track JED submission and review process"
        group_by    = "Marketplace Status"
        filter = {
          field    = "Marketplace Status"
          operator = "not_equals"
          value    = "Not Applicable"
        }
        columns = ["Title", "Extension Version", "Status", "Assignees"]
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
        name    = "Update Extension Version on release"
        trigger = "release_published"
        actions = [
          {
            action  = "extract_version_from_tag"
            target  = "Extension Version"
          }
        ]
      },
      {
        name    = "Stale blocker detection"
        trigger = "schedule_daily"
        actions = [
          {
            action = "find_items"
            query  = "Status=Blocked AND updated_at < 7 days ago"
          },
          {
            add_label = "stale-blocker"
          },
          {
            notify = "assignees"
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

output "joomla_project_config" {
  description = "Joomla Extension project template configuration"
  value       = local.project_config
}
