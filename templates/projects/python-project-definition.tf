/**
 * Python Project Template
 * Standard project configuration for Python application and library development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Python Project"
      description = "Standard project template for Python application and library development"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "python"
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
        description = "List of criteria for task completion"
      },
      {
        name        = "Python Version"
        type        = "single_select"
        description = "Minimum Python version required"
        options     = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
      },
      {
        name        = "Framework"
        type        = "single_select"
        description = "Primary Python framework"
        options     = ["Django", "Flask", "FastAPI", "Pyramid", "Tornado", "Quart", "Sanic", "Streamlit", "None", "Other"]
      },
      {
        name        = "Package Manager"
        type        = "single_select"
        description = "Dependency management tool"
        options     = ["pip", "Poetry", "Pipenv", "conda", "PDM", "Rye"]
      },
      {
        name        = "Virtual Environment"
        type        = "single_select"
        description = "Virtual environment tool"
        options     = ["venv", "virtualenv", "conda", "Poetry", "pipenv", "None"]
      },
      {
        name        = "Test Framework"
        type        = "single_select"
        description = "Testing framework used"
        options     = ["pytest", "unittest", "nose2", "doctest", "tox", "Multiple", "None"]
      },
      {
        name        = "Type Checking"
        type        = "single_select"
        description = "Static type checking tool"
        options     = ["mypy", "pyright", "pyre", "pytype", "None"]
      },
      {
        name        = "Code Quality"
        type        = "single_select"
        description = "Linter and formatter"
        options     = ["black + ruff", "black + flake8", "pylint", "autopep8", "yapf", "Multiple", "None"]
      },
      {
        name        = "PyPI Status"
        type        = "single_select"
        description = "Python Package Index publication status"
        options     = ["Not Published", "Test PyPI", "PyPI Published", "Private Package", "Deprecated"]
      },
      {
        name        = "Package Name"
        type        = "text"
        description = "PyPI package name"
      },
      {
        name        = "Package Version"
        type        = "text"
        description = "Current package version (semantic versioning or PEP 440)"
      },
      {
        name        = "Has Type Hints"
        type        = "single_select"
        description = "PEP 484 type hints included?"
        options     = ["Complete", "Partial", "None"]
      },
      {
        name        = "Test Coverage"
        type        = "text"
        description = "Code coverage percentage"
      },
      {
        name        = "Documentation"
        type        = "single_select"
        description = "Documentation system"
        options     = ["Sphinx", "MkDocs", "pdoc", "pydoc", "Docusaurus", "None"]
      },
      {
        name        = "License Type"
        type        = "single_select"
        description = "Software license"
        options     = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "PSF", "Proprietary", "Other"]
      },
      {
        name        = "Async Support"
        type        = "single_select"
        description = "Asyncio/async-await usage"
        options     = ["Full Async", "Partial", "None"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Assignee", "Sprint", "Framework"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Sprint Board"
        type        = "board"
        description = "Current sprint work board"
        group_by    = "Status"
        filter = {
          field    = "Sprint"
          operator = "equals"
          value    = "current"
        }
        columns = ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done"]
      },
      {
        name        = "Release Roadmap"
        type        = "roadmap"
        description = "Timeline view of planned releases"
        group_by    = "Target Version"
        date_field  = "Target Date"
      },
      {
        name        = "Blocked Items"
        type        = "table"
        description = "Tasks currently blocked"
        filter = {
          field    = "Status"
          operator = "equals"
          value    = "Blocked"
        }
        columns = ["Title", "Priority", "Blocked Reason", "Assignee", "Days Blocked"]
      },
      {
        name        = "PyPI Pipeline"
        type        = "board"
        description = "Package publication workflow"
        group_by    = "PyPI Status"
        columns     = ["Not Published", "Test PyPI", "PyPI Published"]
      },
      {
        name        = "Testing Matrix"
        type        = "table"
        description = "Test coverage and quality metrics"
        columns     = ["Title", "Test Framework", "Test Coverage", "Type Checking", "Has Type Hints", "Status"]
      },
      {
        name        = "Framework Distribution"
        type        = "table"
        description = "Projects by framework"
        group_by    = "Framework"
        columns     = ["Title", "Framework", "Python Version", "Async Support", "Status"]
      },
      {
        name        = "Type Hints Adoption"
        type        = "table"
        description = "Type safety tracking"
        filter = {
          field    = "Has Type Hints"
          operator = "not_equals"
          value    = "None"
        }
        columns = ["Title", "Has Type Hints", "Type Checking", "Test Coverage", "Status"]
      },
    ]

    workflows = [
      {
        name    = "Auto-status on PR"
        trigger = "pull_request_opened"
        actions = [
          {
            set_field = "Status"
            value     = "In Review"
          }
        ]
      },
      {
        name    = "Auto-status on merge"
        trigger = "pull_request_merged"
        actions = [
          {
            set_field = "Status"
            value     = "Testing"
          }
        ]
      },
      {
        name    = "Auto-status on close"
        trigger = "pull_request_closed"
        actions = [
          {
            set_field = "Status"
            value     = "Cancelled"
          }
        ]
      },
      {
        name    = "Low coverage alert"
        trigger = "field_changed"
        field   = "Test Coverage"
        condition = {
          operator = "less_than"
          value    = "80"
        }
        actions = [
          {
            add_label = "needs-tests"
            notify    = "team"
          }
        ]
      },
      {
        name    = "PyPI publish notification"
        trigger = "field_changed"
        field   = "PyPI Status"
        condition = {
          operator = "equals"
          value    = "PyPI Published"
        }
        actions = [
          {
            notify  = "team"
            message = "Package published to PyPI"
          }
        ]
      },
    ]

    metadata = {
      version = "1.0.0"
      created = "2026-02-27"
      author  = "Moko Consulting"
      license = "GPL-3.0-or-later"
    }
  }
}

output "python_project_config" {
  description = "Python project template configuration"
  value       = local.project_config
}
