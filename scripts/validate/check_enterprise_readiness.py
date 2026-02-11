#!/usr/bin/env python3
"""
Enterprise Readiness Checker - Validates enterprise compliance for repositories.

This script checks whether a repository meets all enterprise readiness requirements:
- All 10 enterprise libraries present (scripts/lib/)
- All 5 enterprise workflows present (.github/workflows/)
- Terraform installation scripts present
- Version badges in key documentation
- MokoStandards.override.tf present and up-to-date
- Enterprise metadata in configs
- Monitoring setup (logs/, metrics/)
- Returns enterprise readiness score (0-100%)
- Provides actionable recommendations

File: scripts/validate/check_enterprise_readiness.py
Version: 03.02.00
Classification: ValidationScript
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
    2026-02-11: Initial implementation for enterprise readiness checking
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

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
class CheckResult:
    """Result of an individual enterprise readiness check."""
    name: str
    passed: bool
    score: int
    max_score: int
    message: str
    recommendations: List[str] = field(default_factory=list)
    details: Dict = field(default_factory=dict)

@dataclass
class EnterpriseReadinessReport:
    """Complete enterprise readiness assessment report."""
    total_score: int
    max_score: int
    percentage: float
    checks: List[CheckResult]
    summary: str
    recommendations: List[str]
    
    def is_enterprise_ready(self) -> bool:
        """Determine if repository meets minimum enterprise readiness threshold."""
        return self.percentage >= 80.0

class EnterpriseReadinessChecker:
    """Check enterprise readiness of a repository."""
    
    # Enterprise library files (10 required)
    REQUIRED_LIBRARIES = [
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
    
    # Enterprise workflows (5 required)
    REQUIRED_WORKFLOWS = [
        '.github/workflows/audit-log-archival.yml',
        '.github/workflows/metrics-collection.yml',
        '.github/workflows/health-check.yml',
        '.github/workflows/security-scan.yml',
        '.github/workflows/integration-tests.yml',
    ]
    
    # Terraform installation scripts (2 required)
    TERRAFORM_SCRIPTS = [
        'scripts/automation/install_terraform.sh',
        'scripts/automation/install_terraform.py',
    ]
    
    # Key documentation files that should have version badges
    KEY_DOCS = [
        'README.md',
        'CHANGELOG.md',
        'docs/README.md',
    ]
    
    # Required monitoring directories
    MONITORING_DIRS = [
        'logs/',
        'logs/audit/',
        'logs/metrics/',
    ]
    
    def __init__(self, repo_path: str = '.', verbose: bool = False, json_output: bool = False):
        """Initialize the enterprise readiness checker.
        
        Args:
            repo_path: Path to the repository root
            verbose: Enable verbose output
            json_output: Output results as JSON
        """
        self.repo_path = Path(repo_path).resolve()
        self.verbose = verbose
        self.json_output = json_output
        self.checks: List[CheckResult] = []
        
    def run_all_checks(self) -> EnterpriseReadinessReport:
        """Run all enterprise readiness checks.
        
        Returns:
            Complete enterprise readiness report
        """
        self.checks = []
        
        # Run individual checks
        self.check_enterprise_libraries()
        self.check_enterprise_workflows()
        self.check_terraform_scripts()
        self.check_version_badges()
        self.check_override_config()
        self.check_enterprise_metadata()
        self.check_monitoring_setup()
        
        # Calculate scores
        total_score = sum(c.score for c in self.checks)
        max_score = sum(c.max_score for c in self.checks)
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Generate summary and recommendations
        summary = self._generate_summary(percentage)
        recommendations = self._collect_recommendations()
        
        return EnterpriseReadinessReport(
            total_score=total_score,
            max_score=max_score,
            percentage=percentage,
            checks=self.checks,
            summary=summary,
            recommendations=recommendations
        )
    
    def check_enterprise_libraries(self) -> CheckResult:
        """Check for presence of all required enterprise libraries."""
        missing = []
        present = []
        
        for lib in self.REQUIRED_LIBRARIES:
            lib_path = self.repo_path / lib
            if lib_path.exists():
                present.append(lib)
            else:
                missing.append(lib)
        
        score = len(present)
        max_score = len(self.REQUIRED_LIBRARIES)
        passed = len(missing) == 0
        
        message = f"Enterprise libraries: {score}/{max_score} present"
        recommendations = []
        
        if missing:
            recommendations.append(
                f"Install missing enterprise libraries: {', '.join(missing)}"
            )
            recommendations.append(
                "Run: python scripts/automation/setup_enterprise_repo.py --install-libraries"
            )
        
        result = CheckResult(
            name="Enterprise Libraries",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details={'missing': missing, 'present': present}
        )
        
        self.checks.append(result)
        return result
    
    def check_enterprise_workflows(self) -> CheckResult:
        """Check for presence of all required enterprise workflows."""
        missing = []
        present = []
        
        for workflow in self.REQUIRED_WORKFLOWS:
            workflow_path = self.repo_path / workflow
            if workflow_path.exists():
                present.append(workflow)
            else:
                missing.append(workflow)
        
        score = len(present)
        max_score = len(self.REQUIRED_WORKFLOWS)
        passed = len(missing) == 0
        
        message = f"Enterprise workflows: {score}/{max_score} present"
        recommendations = []
        
        if missing:
            recommendations.append(
                f"Install missing enterprise workflows: {', '.join([Path(w).name for w in missing])}"
            )
            recommendations.append(
                "Run: python scripts/automation/setup_enterprise_repo.py --install-workflows"
            )
        
        result = CheckResult(
            name="Enterprise Workflows",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details={'missing': missing, 'present': present}
        )
        
        self.checks.append(result)
        return result
    
    def check_terraform_scripts(self) -> CheckResult:
        """Check for Terraform installation scripts."""
        missing = []
        present = []
        
        for script in self.TERRAFORM_SCRIPTS:
            script_path = self.repo_path / script
            if script_path.exists():
                present.append(script)
            else:
                missing.append(script)
        
        score = len(present)
        max_score = len(self.TERRAFORM_SCRIPTS)
        passed = len(missing) == 0
        
        message = f"Terraform scripts: {score}/{max_score} present"
        recommendations = []
        
        if missing:
            recommendations.append(
                "Install missing Terraform installation scripts from MokoStandards"
            )
        
        result = CheckResult(
            name="Terraform Scripts",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details={'missing': missing, 'present': present}
        )
        
        self.checks.append(result)
        return result
    
    def check_version_badges(self) -> CheckResult:
        """Check for version badges in key documentation."""
        version_badge_pattern = re.compile(
            r'!\[Version\].*?badge.*?version.*?03\.0[12]\.0[0-9]',
            re.IGNORECASE
        )
        
        with_badges = []
        without_badges = []
        
        for doc in self.KEY_DOCS:
            doc_path = self.repo_path / doc
            if doc_path.exists():
                content = doc_path.read_text(errors='ignore')
                if version_badge_pattern.search(content):
                    with_badges.append(doc)
                else:
                    without_badges.append(doc)
        
        score = len(with_badges)
        max_score = len([d for d in self.KEY_DOCS if (self.repo_path / d).exists()])
        passed = len(without_badges) == 0 and max_score > 0
        
        message = f"Version badges: {score}/{max_score} documents"
        recommendations = []
        
        if without_badges:
            recommendations.append(
                f"Add version badges to: {', '.join(without_badges)}"
            )
            recommendations.append(
                "Format: ![Version](https://img.shields.io/badge/version-03.02.00-blue)"
            )
        
        result = CheckResult(
            name="Version Badges",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details={'with_badges': with_badges, 'without_badges': without_badges}
        )
        
        self.checks.append(result)
        return result
    
    def check_override_config(self) -> CheckResult:
        """Check for MokoStandards.override.tf configuration."""
        override_path = self.repo_path / 'MokoStandards.override.tf'
        
        score = 0
        max_score = 10
        passed = False
        recommendations = []
        details = {}
        
        if not override_path.exists():
            message = "MokoStandards.override.tf: NOT FOUND"
            recommendations.append(
                "Create MokoStandards.override.tf with sync configuration"
            )
            recommendations.append(
                "Run: python scripts/automation/setup_enterprise_repo.py --create-override"
            )
        else:
            content = override_path.read_text()
            details['exists'] = True
            score += 5
            
            # Check for required sections
            has_metadata = 'override_metadata' in content
            has_sync_config = 'sync_config' in content
            has_version = '03.02.00' in content
            
            if has_metadata:
                score += 2
                details['has_metadata'] = True
            else:
                recommendations.append("Add override_metadata section to override config")
            
            if has_sync_config:
                score += 2
                details['has_sync_config'] = True
            else:
                recommendations.append("Add sync_config section to override config")
            
            if has_version:
                score += 1
                details['has_version'] = True
                passed = True
                message = "MokoStandards.override.tf: PRESENT and up-to-date"
            else:
                message = "MokoStandards.override.tf: PRESENT but outdated"
                recommendations.append("Update version to 03.02.00 in override config")
        
        result = CheckResult(
            name="Override Configuration",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details=details
        )
        
        self.checks.append(result)
        return result
    
    def check_enterprise_metadata(self) -> CheckResult:
        """Check for enterprise metadata in configuration files."""
        config_files = [
            'pyproject.toml',
            'package.json',
            'composer.json',
        ]
        
        with_metadata = []
        without_metadata = []
        
        metadata_patterns = [
            re.compile(r'enterprise[_-]ready\s*=\s*true', re.IGNORECASE),
            re.compile(r'"enterprise[_-]ready"\s*:\s*true', re.IGNORECASE),
            re.compile(r'monitoring[_-]enabled\s*=\s*true', re.IGNORECASE),
            re.compile(r'"monitoring[_-]enabled"\s*:\s*true', re.IGNORECASE),
        ]
        
        for config in config_files:
            config_path = self.repo_path / config
            if config_path.exists():
                content = config_path.read_text(errors='ignore')
                has_metadata = any(pattern.search(content) for pattern in metadata_patterns)
                
                if has_metadata:
                    with_metadata.append(config)
                else:
                    without_metadata.append(config)
        
        score = len(with_metadata) * 2
        max_score = 10
        passed = score >= 6
        
        message = f"Enterprise metadata: {len(with_metadata)} configs with metadata"
        recommendations = []
        
        if without_metadata:
            recommendations.append(
                f"Add enterprise metadata to: {', '.join(without_metadata)}"
            )
            recommendations.append(
                'Add fields: enterprise_ready=true, monitoring_enabled=true'
            )
        
        result = CheckResult(
            name="Enterprise Metadata",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details={'with_metadata': with_metadata, 'without_metadata': without_metadata}
        )
        
        self.checks.append(result)
        return result
    
    def check_monitoring_setup(self) -> CheckResult:
        """Check for monitoring directory structure."""
        present = []
        missing = []
        
        for dir_path in self.MONITORING_DIRS:
            full_path = self.repo_path / dir_path
            if full_path.exists() and full_path.is_dir():
                present.append(dir_path)
            else:
                missing.append(dir_path)
        
        score = len(present) * 3
        max_score = len(self.MONITORING_DIRS) * 3
        passed = len(missing) == 0
        
        message = f"Monitoring directories: {len(present)}/{len(self.MONITORING_DIRS)} present"
        recommendations = []
        
        if missing:
            recommendations.append(
                f"Create missing monitoring directories: {', '.join(missing)}"
            )
            recommendations.append(
                "Run: python scripts/automation/setup_enterprise_repo.py --create-dirs"
            )
        
        result = CheckResult(
            name="Monitoring Setup",
            passed=passed,
            score=score,
            max_score=max_score,
            message=message,
            recommendations=recommendations,
            details={'present': present, 'missing': missing}
        )
        
        self.checks.append(result)
        return result
    
    def _generate_summary(self, percentage: float) -> str:
        """Generate a summary message based on readiness percentage."""
        if percentage >= 90:
            return "✓ Repository is FULLY enterprise-ready with excellent compliance"
        elif percentage >= 80:
            return "✓ Repository is enterprise-ready with minor improvements recommended"
        elif percentage >= 60:
            return "⚠ Repository is PARTIALLY enterprise-ready - several improvements needed"
        elif percentage >= 40:
            return "⚠ Repository has BASIC enterprise features - significant work required"
        else:
            return "✗ Repository is NOT enterprise-ready - major setup required"
    
    def _collect_recommendations(self) -> List[str]:
        """Collect all recommendations from failed checks."""
        recommendations = []
        for check in self.checks:
            if not check.passed:
                recommendations.extend(check.recommendations)
        
        # Deduplicate while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def print_report(self, report: EnterpriseReadinessReport):
        """Print formatted enterprise readiness report to console.
        
        Args:
            report: The readiness report to print
        """
        if self.json_output:
            self._print_json_report(report)
            return
        
        # Header
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'ENTERPRISE READINESS REPORT':^70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")
        
        # Repository path
        print(f"{Colors.BOLD}Repository:{Colors.RESET} {self.repo_path}")
        print()
        
        # Score
        score_color = Colors.GREEN if report.percentage >= 80 else Colors.YELLOW if report.percentage >= 60 else Colors.RED
        print(f"{Colors.BOLD}Overall Score:{Colors.RESET} {score_color}{report.total_score}/{report.max_score} ({report.percentage:.1f}%){Colors.RESET}")
        print()
        
        # Summary
        print(f"{Colors.BOLD}Summary:{Colors.RESET} {report.summary}")
        print()
        
        # Individual checks
        print(f"{Colors.BOLD}{Colors.BLUE}Detailed Checks:{Colors.RESET}\n")
        
        for check in report.checks:
            status_symbol = "✓" if check.passed else "✗"
            status_color = Colors.GREEN if check.passed else Colors.RED
            
            print(f"  {status_color}{status_symbol}{Colors.RESET} {Colors.BOLD}{check.name}{Colors.RESET}")
            print(f"    Score: {check.score}/{check.max_score}")
            print(f"    {check.message}")
            
            if self.verbose and check.details:
                print(f"    {Colors.DIM}Details: {json.dumps(check.details, indent=6)}{Colors.RESET}")
            
            if check.recommendations:
                print(f"    {Colors.YELLOW}Recommendations:{Colors.RESET}")
                for rec in check.recommendations:
                    print(f"      • {rec}")
            print()
        
        # Recommendations
        if report.recommendations:
            print(f"{Colors.BOLD}{Colors.YELLOW}Action Items:{Colors.RESET}\n")
            for i, rec in enumerate(report.recommendations, 1):
                print(f"  {i}. {rec}")
            print()
        
        # Footer
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")
    
    def _print_json_report(self, report: EnterpriseReadinessReport):
        """Print report as JSON."""
        output = {
            'repository': str(self.repo_path),
            'score': {
                'total': report.total_score,
                'max': report.max_score,
                'percentage': round(report.percentage, 2)
            },
            'enterprise_ready': report.is_enterprise_ready(),
            'summary': report.summary,
            'checks': [
                {
                    'name': check.name,
                    'passed': check.passed,
                    'score': check.score,
                    'max_score': check.max_score,
                    'message': check.message,
                    'recommendations': check.recommendations,
                    'details': check.details
                }
                for check in report.checks
            ],
            'recommendations': report.recommendations
        }
        
        print(json.dumps(output, indent=2))

def main():
    """Main entry point for the enterprise readiness checker."""
    parser = argparse.ArgumentParser(
        description='Check enterprise readiness of a repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check current repository
  python check_enterprise_readiness.py
  
  # Check specific repository with verbose output
  python check_enterprise_readiness.py --path /path/to/repo --verbose
  
  # Output as JSON for programmatic use
  python check_enterprise_readiness.py --json
  
Exit codes:
  0 - Repository is enterprise-ready (>=80% score)
  1 - Repository is not enterprise-ready (<80% score)
  2 - Error during checking
        """
    )
    
    parser.add_argument(
        '--path',
        default='.',
        help='Path to repository root (default: current directory)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed information'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 03.02.00'
    )
    
    args = parser.parse_args()
    
    try:
        checker = EnterpriseReadinessChecker(
            repo_path=args.path,
            verbose=args.verbose,
            json_output=args.json
        )
        
        report = checker.run_all_checks()
        checker.print_report(report)
        
        # Exit with appropriate code
        sys.exit(0 if report.is_enterprise_ready() else 1)
        
    except Exception as e:
        if args.json:
            print(json.dumps({'error': str(e)}), file=sys.stderr)
        else:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()
