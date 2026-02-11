#!/usr/bin/env python3
"""
Enterprise Setup Script - Automated enterprise repository setup and configuration.

This script automates the setup of enterprise features for repositories:
- Checks for missing enterprise components
- Installs missing enterprise libraries
- Creates required directory structure
- Sets up monitoring directories (logs/audit/, logs/metrics/)
- Initializes configuration files
- Adds version badges to README.md
- Creates MokoStandards.override.tf if missing
- Interactive mode with confirmations
- Dry-run mode for testing

File: scripts/automation/setup_enterprise_repo.py
Version: 03.02.00
Classification: AutomationScript
Author: MokoStandards Team

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Revision History:
    2026-02-11: Initial implementation for enterprise setup automation
"""

import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# ANSI color codes for output
class Colors:
    """Terminal color codes for formatted output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    DIM = '\033[2m'

@dataclass
class SetupResult:
    """Result of a setup operation."""
    success: bool
    message: str
    details: List[str]

class EnterpriseRepoSetup:
    """Setup enterprise features for a repository."""
    
    # MokoStandards repository (source for templates)
    MOKOSTANDARDS_REPO = 'https://github.com/mokoconsulting-tech/MokoStandards.git'
    
    # Enterprise libraries to install
    ENTERPRISE_LIBRARIES = [
        'scripts/lib/enterprise_audit.py',
        'scripts/lib/audit_logger.py',
        'scripts/lib/validation_framework.py',
        'scripts/lib/unified_validation.py',
        'scripts/lib/config_manager.py',
        'scripts/lib/security_validator.py',
        'scripts/lib/error_recovery.py',
        'scripts/lib/transaction_manager.py',
        'scripts/lib/cli_framework.py',
        'scripts/lib/common.py',
    ]
    
    # Enterprise workflows to install
    ENTERPRISE_WORKFLOWS = [
        '.github/workflows/audit-log-archival.yml',
        '.github/workflows/metrics-collection.yml',
        '.github/workflows/health-check.yml',
        '.github/workflows/security-scan.yml',
        '.github/workflows/integration-tests.yml',
    ]
    
    # Terraform scripts
    TERRAFORM_SCRIPTS = [
        'scripts/automation/install_terraform.sh',
        'scripts/automation/install_terraform.py',
    ]
    
    # Required directories
    REQUIRED_DIRECTORIES = [
        'scripts/lib',
        'scripts/automation',
        'scripts/validate',
        '.github/workflows',
        'logs',
        'logs/audit',
        'logs/metrics',
        'logs/validation',
        'docs',
        'docs/guide',
    ]
    
    def __init__(self, repo_path: str = '.', dry_run: bool = False, 
                 interactive: bool = True, verbose: bool = False,
                 source_path: Optional[str] = None):
        """Initialize the enterprise setup manager.
        
        Args:
            repo_path: Path to the target repository
            dry_run: If True, only show what would be done
            interactive: If True, ask for confirmation before actions
            verbose: Enable verbose output
            source_path: Path to MokoStandards source (if local copy exists)
        """
        self.repo_path = Path(repo_path).resolve()
        self.dry_run = dry_run
        self.interactive = interactive
        self.verbose = verbose
        self.source_path = Path(source_path).resolve() if source_path else None
        
        # Detect source path if not provided
        if not self.source_path:
            self.source_path = self._find_mokostandards_source()
    
    def _find_mokostandards_source(self) -> Optional[Path]:
        """Try to find MokoStandards source repository."""
        # Check if current repo IS MokoStandards
        if (self.repo_path / 'MokoStandards.override.tf').exists():
            return self.repo_path
        
        # Check parent directory
        parent_mokostandards = self.repo_path.parent / 'MokoStandards'
        if parent_mokostandards.exists() and (parent_mokostandards / 'MokoStandards.override.tf').exists():
            return parent_mokostandards
        
        # Check sibling directory
        sibling_mokostandards = self.repo_path.parent / 'MokoStandards'
        if sibling_mokostandards.exists():
            return sibling_mokostandards
        
        return None
    
    def _log(self, message: str, color: str = Colors.RESET):
        """Print a log message."""
        prefix = "[DRY RUN] " if self.dry_run else ""
        print(f"{color}{prefix}{message}{Colors.RESET}")
    
    def _confirm(self, prompt: str) -> bool:
        """Ask for user confirmation in interactive mode."""
        if not self.interactive or self.dry_run:
            return True
        
        response = input(f"{Colors.YELLOW}{prompt} (y/N): {Colors.RESET}").strip().lower()
        return response in ['y', 'yes']
    
    def setup_all(self) -> bool:
        """Run complete enterprise setup.
        
        Returns:
            True if all setup steps succeeded
        """
        self._log(f"\n{Colors.BOLD}{Colors.CYAN}Starting Enterprise Repository Setup{Colors.RESET}\n", Colors.CYAN)
        self._log(f"Target repository: {self.repo_path}", Colors.BLUE)
        
        if self.source_path:
            self._log(f"Source: {self.source_path}", Colors.BLUE)
        else:
            self._log("Source: Will copy from local files if available", Colors.YELLOW)
        
        print()
        
        results = []
        
        # Create directory structure
        result = self.create_directories()
        results.append(result)
        self._print_result(result)
        
        # Install enterprise libraries
        result = self.install_libraries()
        results.append(result)
        self._print_result(result)
        
        # Install enterprise workflows
        result = self.install_workflows()
        results.append(result)
        self._print_result(result)
        
        # Install Terraform scripts
        result = self.install_terraform_scripts()
        results.append(result)
        self._print_result(result)
        
        # Create override configuration
        result = self.create_override_config()
        results.append(result)
        self._print_result(result)
        
        # Add version badges
        result = self.add_version_badges()
        results.append(result)
        self._print_result(result)
        
        # Create monitoring setup
        result = self.setup_monitoring()
        results.append(result)
        self._print_result(result)
        
        # Summary
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
        if success_count == total_count:
            self._log(f"✓ Enterprise setup completed successfully! ({success_count}/{total_count})", Colors.GREEN)
        else:
            self._log(f"⚠ Enterprise setup completed with warnings ({success_count}/{total_count})", Colors.YELLOW)
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")
        
        return success_count == total_count
    
    def create_directories(self) -> SetupResult:
        """Create required directory structure."""
        if not self._confirm("Create required directory structure?"):
            return SetupResult(success=True, message="Skipped by user", details=[])
        
        created = []
        exists = []
        
        for dir_path in self.REQUIRED_DIRECTORIES:
            full_path = self.repo_path / dir_path
            
            if full_path.exists():
                exists.append(str(dir_path))
            else:
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                    # Create .gitkeep for empty directories
                    gitkeep = full_path / '.gitkeep'
                    if not gitkeep.exists():
                        gitkeep.touch()
                created.append(str(dir_path))
        
        details = []
        if created:
            details.append(f"Created {len(created)} directories")
            if self.verbose:
                details.extend(created)
        if exists:
            details.append(f"{len(exists)} directories already exist")
        
        return SetupResult(
            success=True,
            message="Directory structure created",
            details=details
        )
    
    def install_libraries(self) -> SetupResult:
        """Install enterprise library files."""
        if not self.source_path:
            return SetupResult(
                success=False,
                message="Cannot install libraries - MokoStandards source not found",
                details=["Specify source with --source-path or ensure MokoStandards is accessible"]
            )
        
        if not self._confirm(f"Install {len(self.ENTERPRISE_LIBRARIES)} enterprise libraries?"):
            return SetupResult(success=True, message="Skipped by user", details=[])
        
        installed = []
        skipped = []
        failed = []
        
        for lib_path in self.ENTERPRISE_LIBRARIES:
            source_file = self.source_path / lib_path
            target_file = self.repo_path / lib_path
            
            if target_file.exists():
                skipped.append(lib_path)
                continue
            
            if not source_file.exists():
                failed.append(f"{lib_path} (source not found)")
                continue
            
            if not self.dry_run:
                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
                    target_file.chmod(0o755)
                    installed.append(lib_path)
                except Exception as e:
                    failed.append(f"{lib_path} ({e})")
            else:
                installed.append(lib_path)
        
        details = []
        if installed:
            details.append(f"Installed {len(installed)} libraries")
            if self.verbose:
                details.extend(installed)
        if skipped:
            details.append(f"Skipped {len(skipped)} existing libraries")
        if failed:
            details.append(f"Failed {len(failed)} libraries")
            details.extend(failed)
        
        return SetupResult(
            success=len(failed) == 0,
            message="Enterprise libraries installed" if len(failed) == 0 else "Some libraries failed",
            details=details
        )
    
    def install_workflows(self) -> SetupResult:
        """Install enterprise workflow files."""
        if not self.source_path:
            return SetupResult(
                success=False,
                message="Cannot install workflows - MokoStandards source not found",
                details=[]
            )
        
        if not self._confirm(f"Install {len(self.ENTERPRISE_WORKFLOWS)} enterprise workflows?"):
            return SetupResult(success=True, message="Skipped by user", details=[])
        
        installed = []
        skipped = []
        failed = []
        
        for workflow_path in self.ENTERPRISE_WORKFLOWS:
            source_file = self.source_path / workflow_path
            target_file = self.repo_path / workflow_path
            
            if target_file.exists():
                skipped.append(workflow_path)
                continue
            
            if not source_file.exists():
                failed.append(f"{workflow_path} (source not found)")
                continue
            
            if not self.dry_run:
                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
                    installed.append(workflow_path)
                except Exception as e:
                    failed.append(f"{workflow_path} ({e})")
            else:
                installed.append(workflow_path)
        
        details = []
        if installed:
            details.append(f"Installed {len(installed)} workflows")
            if self.verbose:
                details.extend(installed)
        if skipped:
            details.append(f"Skipped {len(skipped)} existing workflows")
        if failed:
            details.append(f"Failed {len(failed)} workflows")
            details.extend(failed)
        
        return SetupResult(
            success=len(failed) == 0,
            message="Enterprise workflows installed" if len(failed) == 0 else "Some workflows failed",
            details=details
        )
    
    def install_terraform_scripts(self) -> SetupResult:
        """Install Terraform installation scripts."""
        if not self.source_path:
            return SetupResult(
                success=False,
                message="Cannot install Terraform scripts - MokoStandards source not found",
                details=[]
            )
        
        if not self._confirm("Install Terraform installation scripts?"):
            return SetupResult(success=True, message="Skipped by user", details=[])
        
        installed = []
        skipped = []
        failed = []
        
        for script_path in self.TERRAFORM_SCRIPTS:
            source_file = self.source_path / script_path
            target_file = self.repo_path / script_path
            
            if target_file.exists():
                skipped.append(script_path)
                continue
            
            if not source_file.exists():
                failed.append(f"{script_path} (source not found)")
                continue
            
            if not self.dry_run:
                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
                    target_file.chmod(0o755)
                    installed.append(script_path)
                except Exception as e:
                    failed.append(f"{script_path} ({e})")
            else:
                installed.append(script_path)
        
        details = []
        if installed:
            details.append(f"Installed {len(installed)} Terraform scripts")
        if skipped:
            details.append(f"Skipped {len(skipped)} existing scripts")
        if failed:
            details.extend(failed)
        
        return SetupResult(
            success=len(failed) == 0,
            message="Terraform scripts installed" if len(failed) == 0 else "Some scripts failed",
            details=details
        )
    
    def create_override_config(self) -> SetupResult:
        """Create MokoStandards.override.tf configuration file."""
        override_file = self.repo_path / 'MokoStandards.override.tf'
        
        if override_file.exists():
            return SetupResult(
                success=True,
                message="MokoStandards.override.tf already exists",
                details=["Skipped - file exists"]
            )
        
        if not self._confirm("Create MokoStandards.override.tf configuration?"):
            return SetupResult(success=True, message="Skipped by user", details=[])
        
        # Generate override configuration
        repo_name = self.repo_path.name
        
        override_content = f'''# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Override
# INGROUP: MokoStandards.Configuration
# REPO: https://github.com/mokoconsulting-tech/{repo_name}
# PATH: /MokoStandards.override.tf
# VERSION: 03.02.00
# BRIEF: MokoStandards Sync Override Configuration for {repo_name}

# MokoStandards Repository Override Configuration
# This file configures sync behavior for the bulk_update_repos.py script

locals {{
  # Metadata about this override configuration
  override_metadata = {{
    name           = "{repo_name} Override Configuration"
    description    = "Override configuration for {repo_name} repository"
    version        = "03.02.00"
    last_updated   = "{self._get_timestamp()}"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/{repo_name}"
    repository_type = "generic"
    compliance_level = "standard"
    format = "terraform"
    enterprise_ready = true
    monitoring_enabled = true
    audit_logging = true
  }}

  # Sync configuration
  sync_config = {{
    enabled = true
    
    # Cleanup configuration for obsolete files
    cleanup_mode = "conservative"  # Options: none, conservative, aggressive
  }}

  # Files to exclude from sync
  exclude_files = [
    # Add any repository-specific files that should not be synced
    # Example:
    # {{
    #   path   = ".github/workflows/custom-workflow.yml"
    #   reason = "Repository-specific custom workflow"
    # }},
  ]

  # Files that should never be overwritten
  protected_files = [
    {{
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns"
    }},
    {{
      path   = "MokoStandards.override.tf"
      reason = "This override file itself"
    }},
    # Add more protected files as needed
  ]
}}
'''
        
        if not self.dry_run:
            try:
                override_file.write_text(override_content)
            except Exception as e:
                return SetupResult(
                    success=False,
                    message=f"Failed to create override config: {e}",
                    details=[]
                )
        
        return SetupResult(
            success=True,
            message="MokoStandards.override.tf created",
            details=["Created override configuration with default settings"]
        )
    
    def add_version_badges(self) -> SetupResult:
        """Add version badges to README.md."""
        readme_file = self.repo_path / 'README.md'
        
        if not readme_file.exists():
            return SetupResult(
                success=False,
                message="README.md not found",
                details=["Create README.md first"]
            )
        
        content = readme_file.read_text()
        
        # Check if version badge already exists
        if re.search(r'!\[Version\].*badge.*version', content, re.IGNORECASE):
            return SetupResult(
                success=True,
                message="Version badge already present in README.md",
                details=[]
            )
        
        if not self._confirm("Add version badge to README.md?"):
            return SetupResult(success=True, message="Skipped by user", details=[])
        
        # Add badge after first heading
        badge = "![Version](https://img.shields.io/badge/version-03.02.00-blue) ![Enterprise Ready](https://img.shields.io/badge/enterprise-ready-green)\n\n"
        
        lines = content.split('\n')
        new_lines = []
        badge_added = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            # Add badge after first markdown heading
            if not badge_added and line.startswith('#'):
                new_lines.append('')
                new_lines.append(badge.rstrip())
                badge_added = True
        
        if not badge_added:
            # If no heading found, add at the beginning
            new_lines.insert(0, badge.rstrip())
            new_lines.insert(1, '')
        
        new_content = '\n'.join(new_lines)
        
        if not self.dry_run:
            try:
                readme_file.write_text(new_content)
            except Exception as e:
                return SetupResult(
                    success=False,
                    message=f"Failed to update README.md: {e}",
                    details=[]
                )
        
        return SetupResult(
            success=True,
            message="Version badge added to README.md",
            details=["Added version 03.02.00 and enterprise-ready badges"]
        )
    
    def setup_monitoring(self) -> SetupResult:
        """Set up monitoring configuration files."""
        details = []
        
        # Create README in logs directory
        logs_readme = self.repo_path / 'logs' / 'README.md'
        if not logs_readme.exists() and not self.dry_run:
            logs_readme.write_text('''# Logs Directory

This directory contains various log files generated by enterprise monitoring:

- `audit/` - Audit logs for compliance and security tracking
- `metrics/` - Performance and operational metrics
- `validation/` - Validation and health check results

Logs are automatically rotated and archived by enterprise workflows.
''')
            details.append("Created logs/README.md")
        
        return SetupResult(
            success=True,
            message="Monitoring setup completed",
            details=details
        )
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def _print_result(self, result: SetupResult):
        """Print a setup result."""
        status_symbol = "✓" if result.success else "✗"
        status_color = Colors.GREEN if result.success else Colors.RED
        
        print(f"{status_color}{status_symbol}{Colors.RESET} {Colors.BOLD}{result.message}{Colors.RESET}")
        
        if result.details:
            for detail in result.details:
                print(f"  {Colors.DIM}• {detail}{Colors.RESET}")
        print()

def main():
    """Main entry point for the enterprise setup script."""
    parser = argparse.ArgumentParser(
        description='Setup enterprise features for a repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full interactive setup
  python setup_enterprise_repo.py
  
  # Non-interactive with dry-run
  python setup_enterprise_repo.py --no-interactive --dry-run
  
  # Install only libraries
  python setup_enterprise_repo.py --install-libraries
  
  # Setup with custom source
  python setup_enterprise_repo.py --source-path /path/to/MokoStandards
        """
    )
    
    parser.add_argument(
        '--path',
        default='.',
        help='Path to target repository (default: current directory)'
    )
    parser.add_argument(
        '--source-path',
        help='Path to MokoStandards source repository'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Run without interactive confirmations'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--install-libraries',
        action='store_true',
        help='Install only enterprise libraries'
    )
    parser.add_argument(
        '--install-workflows',
        action='store_true',
        help='Install only enterprise workflows'
    )
    parser.add_argument(
        '--create-dirs',
        action='store_true',
        help='Create only required directories'
    )
    parser.add_argument(
        '--create-override',
        action='store_true',
        help='Create only override configuration'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 03.02.00'
    )
    
    args = parser.parse_args()
    
    try:
        setup = EnterpriseRepoSetup(
            repo_path=args.path,
            dry_run=args.dry_run,
            interactive=not args.no_interactive,
            verbose=args.verbose,
            source_path=args.source_path
        )
        
        # Run specific action if requested
        if args.install_libraries:
            result = setup.install_libraries()
            setup._print_result(result)
            sys.exit(0 if result.success else 1)
        
        if args.install_workflows:
            result = setup.install_workflows()
            setup._print_result(result)
            sys.exit(0 if result.success else 1)
        
        if args.create_dirs:
            result = setup.create_directories()
            setup._print_result(result)
            sys.exit(0 if result.success else 1)
        
        if args.create_override:
            result = setup.create_override_config()
            setup._print_result(result)
            sys.exit(0 if result.success else 1)
        
        # Run full setup
        success = setup.setup_all()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
