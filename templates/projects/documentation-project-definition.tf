/**
 * Documentation Governance Project Template
 * Control register for documentation artifacts, policies, and compliance tracking
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Documentation Governance Project"
      description = "Control register for documentation artifacts, policies, and compliance tracking"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "documentation"
    }

    custom_fields = [
      {
        name        = "Status"
        type        = "single_select"
        description = "Current lifecycle state of the document"
        options     = ["Draft", "In Review", "Approved", "Published", "Archived", "Deprecated"]
      },
      {
        name        = "Priority"
        type        = "single_select"
        description = "Urgency and importance of the document"
        options     = ["Critical", "High", "Medium", "Low"]
      },
      {
        name        = "Document Type"
        type        = "single_select"
        description = "Type of documentation artifact"
        options     = ["Policy", "Procedure", "Standard", "Guideline", "Template", "Report", "Manual", "API Docs", "Other"]
      },
      {
        name        = "Owner"
        type        = "text"
        description = "Document owner or responsible party"
      },
      {
        name        = "Version"
        type        = "text"
        description = "Document version (semantic versioning)"
      },
      {
        name        = "Review Date"
        type        = "date"
        description = "Next scheduled review date"
      },
      {
        name        = "Last Reviewed"
        type        = "date"
        description = "Date of last review"
      },
      {
        name        = "Compliance Framework"
        type        = "single_select"
        description = "Related compliance framework"
        options     = ["ISO 9001", "ISO 27001", "GDPR", "SOC 2", "HIPAA", "PCI DSS", "None", "Multiple"]
      },
      {
        name        = "Audience"
        type        = "single_select"
        description = "Target audience for this document"
        options     = ["Internal - All", "Internal - Technical", "Internal - Management", "External - Public", "External - Clients", "Mixed"]
      },
      {
        name        = "Confidentiality"
        type        = "single_select"
        description = "Document confidentiality level"
        options     = ["Public", "Internal", "Confidential", "Restricted"]
      },
      {
        name        = "Format"
        type        = "single_select"
        description = "Document format"
        options     = ["Markdown", "PDF", "Word", "HTML", "Wiki", "Confluence", "Other"]
      },
      {
        name        = "Location"
        type        = "text"
        description = "Document location or URL"
      },
      {
        name        = "Approval Required"
        type        = "single_select"
        description = "Does this document require formal approval?"
        options     = ["Yes", "No"]
      },
      {
        name        = "Approver"
        type        = "text"
        description = "Person or role responsible for approval"
      },
      {
        name        = "Translation Status"
        type        = "single_select"
        description = "Translation or localization status"
        options     = ["Not Required", "In Progress", "Complete", "Partial"]
      },
      {
        name        = "Languages"
        type        = "text"
        description = "Available language versions (comma-separated)"
      },
      {
        name        = "Related Standards"
        type        = "text"
        description = "Related standards or policies (references)"
      },
    ]

    views = [
      {
        name        = "All Documents"
        type        = "table"
        description = "Complete register of all documentation"
        columns     = ["Title", "Document Type", "Status", "Version", "Owner", "Last Reviewed", "Review Date"]
        sort = [
          {
            field     = "Status"
            direction = "asc"
          },
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Review Pipeline"
        type        = "board"
        description = "Document review workflow board"
        group_by    = "Status"
        columns     = ["Draft", "In Review", "Approved", "Published"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Review Calendar"
        type        = "roadmap"
        description = "Scheduled document reviews"
        group_by    = "Document Type"
        date_field  = "Review Date"
        filter = {
          field    = "Status"
          operator = "not_equals"
          value    = "Archived"
        }
      },
      {
        name        = "Overdue Reviews"
        type        = "table"
        description = "Documents past their review date"
        filter = {
          field    = "Review Date"
          operator = "less_than"
          value    = "today"
        }
        columns = ["Title", "Document Type", "Owner", "Review Date", "Last Reviewed", "Priority"]
        sort = [
          {
            field     = "Review Date"
            direction = "asc"
          }
        ]
      },
      {
        name        = "By Document Type"
        type        = "table"
        description = "Documents grouped by type"
        group_by    = "Document Type"
        columns     = ["Title", "Status", "Version", "Owner", "Last Reviewed"]
        sort = [
          {
            field     = "Document Type"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Compliance Dashboard"
        type        = "table"
        description = "Compliance framework documentation"
        group_by    = "Compliance Framework"
        filter = {
          field    = "Compliance Framework"
          operator = "not_equals"
          value    = "None"
        }
        columns = ["Title", "Document Type", "Status", "Owner", "Last Reviewed"]
      },
      {
        name        = "Publication Status"
        type        = "board"
        description = "Track publication workflow"
        group_by    = "Status"
        columns     = ["Title", "Document Type", "Version", "Owner", "Audience"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Translation Tracker"
        type        = "table"
        description = "Multi-language documentation status"
        filter = {
          field    = "Translation Status"
          operator = "not_equals"
          value    = "Not Required"
        }
        columns = ["Title", "Translation Status", "Languages", "Status", "Owner"]
      },
    ]

    workflows = [
      {
        name    = "New document workflow"
        trigger = "issue_created"
        actions = [
          {
            set_field = "Status"
            value     = "Draft"
          }
        ]
      },
      {
        name    = "Submit for review"
        trigger = "field_changed"
        field   = "Status"
        condition = {
          operator = "equals"
          value    = "In Review"
        }
        actions = [
          {
            notify  = "approver"
            message = "Document submitted for review"
          }
        ]
      },
      {
        name    = "Document approved"
        trigger = "field_changed"
        field   = "Status"
        condition = {
          operator = "equals"
          value    = "Approved"
        }
        actions = [
          {
            set_field = "Last Reviewed"
            value     = "today"
          },
          {
            notify  = "owner"
            message = "Document approved"
          }
        ]
      },
      {
        name    = "Review reminder"
        trigger = "schedule_weekly"
        actions = [
          {
            action = "find_items"
            query  = "Review Date < 30 days from now AND Status = Published"
          },
          {
            notify  = "owner"
            message = "Document review due soon"
          }
        ]
      },
      {
        name    = "Overdue review alert"
        trigger = "schedule_daily"
        actions = [
          {
            action = "find_items"
            query  = "Review Date < today AND Status != Archived"
          },
          {
            add_label = "overdue-review"
          },
          {
            notify  = "owner"
            message = "Document review is overdue"
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

output "documentation_project_config" {
  description = "Documentation Governance project template configuration"
  value       = local.project_config
}
