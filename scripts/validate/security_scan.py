#!/usr/bin/env python3
"""
Comprehensive security scanning orchestration script.

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

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

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Validate
INGROUP: MokoStandards.Security
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/validate/security_scan.py
VERSION: 01.00.00
BRIEF: Orchestrates comprehensive security scanning for repositories
NOTE: Runs CodeQL validation, secret scanning, and dependency checks
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("Warning: Cannot import common lib, continuing without it", file=sys.stderr)


class SecurityScanner:
    """Orchestrates security scanning operations."""

    def __init__(self, repo_path: Path, verbose: bool = False, dry_run: bool = False):
        self.repo_path = repo_path
        self.verbose = verbose
        self.dry_run = dry_run
        self.findings = {
            'codeql': {'status': 'not_run', 'issues': []},
            'secrets': {'status': 'not_run', 'issues': []},
            'dependencies': {'status': 'not_run', 'issues': []},
            'config': {'status': 'not_run', 'issues': []}
        }

    def log(self, message: str, level: str = 'INFO'):
        """Log message with level."""
        prefix = {
            'INFO': '✓',
            'WARN': '⚠',
            'ERROR': '✗',
            'DEBUG': '→'
        }.get(level, '•')
        dry_run_prefix = '[DRY-RUN] ' if self.dry_run else ''
        print(f"{prefix} {dry_run_prefix}{message}")

    def run_command(self, cmd: List[str], check: bool = True) -> Tuple[int, str, str]:
        """Run shell command and return exit code, stdout, stderr."""
        if self.verbose:
            self.log(f"Running: {' '.join(cmd)}", 'DEBUG')

        if self.dry_run:
            self.log(f"Would run: {' '.join(cmd)}", 'DEBUG')
            return 0, '', ''

        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        return result.returncode, result.stdout, result.stderr

    def validate_codeql_config(self) -> bool:
        """Validate CodeQL workflow configuration."""
        self.log("Validating CodeQL configuration...", 'INFO')

        validate_script = self.repo_path / 'scripts/validate/validate_codeql_config.py'
        if not validate_script.exists():
            self.findings['config']['status'] = 'skipped'
            self.log("CodeQL validation script not found, skipping", 'WARN')
            return True

        try:
            returncode, stdout, stderr = self.run_command([
                sys.executable,
                str(validate_script),
                '--repo-path', str(self.repo_path)
            ])

            if returncode == 0:
                self.findings['config']['status'] = 'passed'
                self.log("CodeQL configuration is valid", 'INFO')
                return True
            else:
                self.findings['config']['status'] = 'failed'
                self.findings['config']['issues'].append({
                    'severity': 'high',
                    'message': 'CodeQL configuration validation failed',
                    'details': stderr or stdout
                })
                self.log(f"CodeQL configuration issues found: {stderr}", 'ERROR')
                return False
        except Exception as e:
            self.findings['config']['status'] = 'error'
            self.log(f"Error validating CodeQL config: {e}", 'ERROR')
            return False

    def scan_secrets(self) -> bool:
        """Scan for accidentally committed secrets."""
        self.log("Scanning for secrets...", 'INFO')

        secrets_script = self.repo_path / 'scripts/validate/no_secrets.py'
        if not secrets_script.exists():
            self.findings['secrets']['status'] = 'skipped'
            self.log("Secret scanning script not found, skipping", 'WARN')
            return True

        try:
            returncode, stdout, stderr = self.run_command([
                sys.executable,
                str(secrets_script),
                '-s', str(self.repo_path)
            ])

            if returncode == 0:
                self.findings['secrets']['status'] = 'passed'
                self.log("No secrets detected", 'INFO')
                return True
            else:
                self.findings['secrets']['status'] = 'failed'
                # Parse output for secret findings
                for line in stdout.split('\n'):
                    if 'FOUND' in line or 'SECRET' in line:
                        self.findings['secrets']['issues'].append({
                            'severity': 'critical',
                            'message': 'Potential secret detected',
                            'details': line
                        })
                self.log(f"Secrets detected! {stdout}", 'ERROR')
                return False
        except Exception as e:
            self.findings['secrets']['status'] = 'error'
            self.log(f"Error scanning for secrets: {e}", 'ERROR')
            return False

    def check_dependencies(self) -> bool:
        """Check for vulnerable dependencies."""
        self.log("Checking dependencies...", 'INFO')

        # Check for common dependency files
        dep_files = [
            'requirements.txt',
            'package.json',
            'composer.json',
            'Gemfile',
            'go.mod',
            'pom.xml'
        ]

        found_deps = [f for f in dep_files if (self.repo_path / f).exists()]

        if not found_deps:
            self.findings['dependencies']['status'] = 'skipped'
            self.log("No dependency files found, skipping", 'INFO')
            return True

        # Check if pip-audit is available for Python dependencies
        if 'requirements.txt' in found_deps or (self.repo_path / 'pyproject.toml').exists():
            try:
                # Check if pip-audit exists
                check_cmd = subprocess.run(
                    ['which', 'pip-audit'],
                    capture_output=True,
                    text=True
                )

                if check_cmd.returncode != 0:
                    self.findings['dependencies']['status'] = 'skipped'
                    self.log("pip-audit not installed, skipping dependency check", 'WARN')
                    return True

                returncode, stdout, stderr = self.run_command([
                    'pip-audit', '--desc', '--format', 'json'
                ], check=False)
                if returncode == 0:
                    self.findings['dependencies']['status'] = 'passed'
                    self.log("No vulnerable dependencies found", 'INFO')
                    return True
                else:
                    self.findings['dependencies']['status'] = 'failed'
                    try:
                        vulns = json.loads(stdout)
                        for vuln in vulns.get('dependencies', []):
                            self.findings['dependencies']['issues'].append({
                                'severity': 'high',
                                'message': f"Vulnerable dependency: {vuln.get('name')}",
                                'details': vuln
                            })
                    except json.JSONDecodeError:
                        self.findings['dependencies']['issues'].append({
                            'severity': 'high',
                            'message': 'Vulnerable dependencies detected',
                            'details': stdout
                        })
                    self.log("Vulnerable dependencies found!", 'ERROR')
                    return False
            except Exception as e:
                self.findings['dependencies']['status'] = 'error'
                self.log(f"Error checking dependencies: {e}", 'WARN')
                return True

        self.findings['dependencies']['status'] = 'skipped'
        self.log(f"Found dependency files but no scanner available: {found_deps}", 'WARN')
        return True

    def check_codeql_workflow(self) -> bool:
        """Check if CodeQL workflow exists."""
        self.log("Checking for CodeQL workflow...", 'INFO')

        codeql_workflow = self.repo_path / '.github/workflows/codeql-analysis.yml'

        if codeql_workflow.exists():
            self.findings['codeql']['status'] = 'configured'
            self.log("CodeQL workflow is configured", 'INFO')
            return True
        else:
            self.findings['codeql']['status'] = 'missing'
            self.findings['codeql']['issues'].append({
                'severity': 'high',
                'message': 'CodeQL workflow not configured',
                'details': 'Create .github/workflows/codeql-analysis.yml'
            })
            self.log("CodeQL workflow not found!", 'ERROR')
            return False

    def generate_report(self) -> Dict:
        """Generate comprehensive security report."""
        total_issues = sum(
            len(scan['issues'])
            for scan in self.findings.values()
        )

        critical_count = sum(
            1 for scan in self.findings.values()
            for issue in scan['issues']
            if issue.get('severity') == 'critical'
        )

        high_count = sum(
            1 for scan in self.findings.values()
            for issue in scan['issues']
            if issue.get('severity') == 'high'
        )

        all_passed = all(
            scan['status'] in ['passed', 'skipped', 'configured']
            for scan in self.findings.values()
        )

        report = {
            'summary': {
                'total_issues': total_issues,
                'critical': critical_count,
                'high': high_count,
                'status': 'PASS' if all_passed else 'FAIL'
            },
            'scans': self.findings,
            'recommendations': []
        }

        # Add recommendations
        if self.findings['codeql']['status'] == 'missing':
            report['recommendations'].append(
                'Install CodeQL workflow from templates/workflows/codeql-analysis.yml.template'
            )

        if self.findings['secrets']['status'] == 'failed':
            report['recommendations'].append(
                'Remove detected secrets and rotate credentials immediately'
            )

        if self.findings['dependencies']['status'] == 'failed':
            report['recommendations'].append(
                'Update vulnerable dependencies to patched versions'
            )

        return report

    def print_report(self, report: Dict):
        """Print formatted security report."""
        print("\n" + "="*70)
        print("🛡️  SECURITY SCAN REPORT")
        print("="*70)
        print(f"\nStatus: {report['summary']['status']}")
        print(f"Total Issues: {report['summary']['total_issues']}")
        print(f"  Critical: {report['summary']['critical']}")
        print(f"  High: {report['summary']['high']}")

        print("\n" + "-"*70)
        print("SCAN RESULTS")
        print("-"*70)

        for scan_name, scan_data in report['scans'].items():
            status_icon = {
                'passed': '✓',
                'failed': '✗',
                'skipped': '○',
                'configured': '✓',
                'missing': '✗',
                'not_run': '-',
                'error': '⚠'
            }.get(scan_data['status'], '?')

            print(f"\n{status_icon} {scan_name.upper()}: {scan_data['status']}")

            if scan_data['issues']:
                for issue in scan_data['issues']:
                    severity_icon = {
                        'critical': '🔴',
                        'high': '🟠',
                        'medium': '🟡',
                        'low': '🟢'
                    }.get(issue['severity'], '⚪')
                    print(f"  {severity_icon} [{issue['severity'].upper()}] {issue['message']}")

        if report['recommendations']:
            print("\n" + "-"*70)
            print("RECOMMENDATIONS")
            print("-"*70)
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec}")

        print("\n" + "="*70 + "\n")

    def run_all_scans(self) -> bool:
        """Run all security scans and return overall status."""
        print("🛡️  Starting comprehensive security scan...\n")

        results = []

        # Run all scans
        results.append(self.check_codeql_workflow())
        results.append(self.validate_codeql_config())
        results.append(self.scan_secrets())
        results.append(self.check_dependencies())

        # Generate and print report
        report = self.generate_report()
        self.print_report(report)

        # Return overall status
        return report['summary']['status'] == 'PASS'


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Comprehensive security scanning for repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  %(prog)s

  # Scan specific repository
  %(prog)s --repo-path /path/to/repo

  # Verbose output
  %(prog)s --verbose

  # Generate JSON report
  %(prog)s --json-output report.json
        """
    )

    parser.add_argument(
        '--repo-path',
        type=Path,
        default=Path.cwd(),
        help='Path to repository root (default: current directory)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--json-output',
        type=Path,
        help='Write JSON report to file'
    )

    parser.add_argument(
        '--no-fail-on-findings',
        dest='fail_on_findings',
        action='store_false',
        help='Do not exit with non-zero status if security issues found'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be checked without executing'
    )

    args = parser.parse_args()

    # Validate repository path
    if not args.repo_path.exists():
        print(f"Error: Repository path does not exist: {args.repo_path}", file=sys.stderr)
        return 1

    if not (args.repo_path / '.git').exists():
        print(f"Warning: Not a git repository: {args.repo_path}", file=sys.stderr)

    # Run security scans
    scanner = SecurityScanner(args.repo_path, verbose=args.verbose, dry_run=args.dry_run)
    success = scanner.run_all_scans()

    # Write JSON report if requested
    if args.json_output:
        report = scanner.generate_report()
        with open(args.json_output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"JSON report written to: {args.json_output}")

    # Exit with appropriate status code
    if args.fail_on_findings and not success:
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
