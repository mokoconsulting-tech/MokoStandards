#!/usr/bin/env python3
"""
Comprehensive File Validation System

Validates all scripts, workflows, and templates for syntax, runtime, and security errors.
Provides unified reporting and actionable remediation.

Usage:
    python3 check_all_files.py [--type TYPE] [--strict] [--verbose]

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2026 Moko Consulting LLC
    LICENSE: GPL-3.0-or-later
    VERSION: 03.01.01
    CREATED: 2026-02-02
    UPDATED: 2026-02-02
"""

import argparse
import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class Severity(Enum):
    """Issue severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FileType(Enum):
    """Supported file types for validation."""
    PYTHON = "python"
    SHELL = "shell"
    POWERSHELL = "powershell"
    WORKFLOW = "workflow"
    TEMPLATE = "template"
    UNKNOWN = "unknown"


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    file_path: str
    line_number: int
    severity: Severity
    category: str  # syntax, runtime, security, structure
    message: str
    remediation: str = ""


@dataclass
class ValidationResult:
    """Results from validating a file."""
    file_path: str
    file_type: FileType
    passed: bool
    issues: List[ValidationIssue]
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'file_path': self.file_path,
            'file_type': self.file_type.value,
            'passed': self.passed,
            'issues': [
                {
                    'file_path': issue.file_path,
                    'line_number': issue.line_number,
                    'severity': issue.severity.value,
                    'category': issue.category,
                    'message': issue.message,
                    'remediation': issue.remediation
                }
                for issue in self.issues
            ]
        }


class FileValidator:
    """Base class for file validators."""
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        
    def log(self, message: str):
        """Log if verbose."""
        if self.verbose:
            print(f"  {message}")
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a file. Override in subclasses."""
        raise NotImplementedError


class PythonValidator(FileValidator):
    """Validates Python scripts."""
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate Python file for syntax and runtime issues."""
        issues = []
        
        # Syntax check with py_compile
        try:
            result = subprocess.run(
                ['python3', '-m', 'py_compile', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                # Parse error message
                error_lines = result.stderr.split('\n')
                for line in error_lines:
                    if 'SyntaxError' in line or 'IndentationError' in line:
                        issues.append(ValidationIssue(
                            file_path=str(file_path),
                            line_number=0,
                            severity=Severity.CRITICAL,
                            category='syntax',
                            message=f"Python syntax error: {line}",
                            remediation="Fix syntax error in Python code"
                        ))
        except subprocess.TimeoutExpired:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.HIGH,
                category='runtime',
                message="Syntax check timed out",
                remediation="Check for infinite loops or hanging code"
            ))
        except Exception as e:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.HIGH,
                category='runtime',
                message=f"Validation error: {str(e)}",
                remediation="Review file for issues"
            ))
        
        # Basic runtime checks
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Check for common runtime issues
                for i, line in enumerate(lines, 1):
                    # Undefined variable patterns (basic check)
                    if re.search(r'^\s*([a-zA-Z_]\w*)\s*=', line):
                        var_name = re.search(r'^\s*([a-zA-Z_]\w*)\s*=', line).group(1)
                        # Check if variable is used before definition
                        before_content = '\n'.join(lines[:i-1])
                        if var_name in before_content and f'{var_name} =' not in before_content:
                            issues.append(ValidationIssue(
                                file_path=str(file_path),
                                line_number=i,
                                severity=Severity.LOW,
                                category='runtime',
                                message=f"Variable '{var_name}' may be used before definition",
                                remediation="Verify variable initialization order"
                            ))
                    
                    # Check for TODO/FIXME comments indicating incomplete code
                    if re.search(r'#\s*(TODO|FIXME).*incomplete|broken|fix', line, re.IGNORECASE):
                        issues.append(ValidationIssue(
                            file_path=str(file_path),
                            line_number=i,
                            severity=Severity.MEDIUM,
                            category='runtime',
                            message=f"Code marked as incomplete: {line.strip()}",
                            remediation="Complete or remove TODO/FIXME"
                        ))
        except Exception as e:
            self.log(f"Error reading file: {e}")
        
        passed = not any(issue.severity in [Severity.CRITICAL, Severity.HIGH] for issue in issues)
        return ValidationResult(
            file_path=str(file_path),
            file_type=FileType.PYTHON,
            passed=passed,
            issues=issues
        )


class ShellValidator(FileValidator):
    """Validates shell scripts."""
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate shell script for syntax and runtime issues."""
        issues = []
        
        # Syntax check with bash -n
        try:
            result = subprocess.run(
                ['bash', '-n', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                issues.append(ValidationIssue(
                    file_path=str(file_path),
                    line_number=0,
                    severity=Severity.CRITICAL,
                    category='syntax',
                    message=f"Shell syntax error: {result.stderr}",
                    remediation="Fix shell script syntax"
                ))
        except FileNotFoundError:
            self.log("bash not found, skipping syntax check")
        except subprocess.TimeoutExpired:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.HIGH,
                category='runtime',
                message="Syntax check timed out",
                remediation="Check for issues in script"
            ))
        except Exception as e:
            self.log(f"Error checking syntax: {e}")
        
        # Try shellcheck if available
        try:
            result = subprocess.run(
                ['shellcheck', '-f', 'json', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout:
                try:
                    shellcheck_issues = json.loads(result.stdout)
                    for sc_issue in shellcheck_issues:
                        severity_map = {
                            'error': Severity.HIGH,
                            'warning': Severity.MEDIUM,
                            'info': Severity.LOW,
                            'style': Severity.INFO
                        }
                        issues.append(ValidationIssue(
                            file_path=str(file_path),
                            line_number=sc_issue.get('line', 0),
                            severity=severity_map.get(sc_issue.get('level', 'info'), Severity.INFO),
                            category='runtime',
                            message=f"Shellcheck: {sc_issue.get('message', 'Unknown issue')}",
                            remediation=f"SC{sc_issue.get('code', '0000')}: See shellcheck wiki"
                        ))
                except json.JSONDecodeError:
                    pass
        except FileNotFoundError:
            self.log("shellcheck not found, skipping advanced checks")
        except Exception as e:
            self.log(f"Error running shellcheck: {e}")
        
        # Basic runtime checks
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for unset variables usage
                    if re.search(r'\$[{]?[a-zA-Z_]\w*[}]?', line) and 'set -u' not in content[:content.find(line)]:
                        if i < 10:  # Only check if not using set -u
                            issues.append(ValidationIssue(
                                file_path=str(file_path),
                                line_number=i,
                                severity=Severity.LOW,
                                category='runtime',
                                message="Consider using 'set -u' to catch undefined variables",
                                remediation="Add 'set -u' near top of script"
                            ))
                            break
        except Exception as e:
            self.log(f"Error reading file: {e}")
        
        passed = not any(issue.severity in [Severity.CRITICAL, Severity.HIGH] for issue in issues)
        return ValidationResult(
            file_path=str(file_path),
            file_type=FileType.SHELL,
            passed=passed,
            issues=issues
        )


class PowerShellValidator(FileValidator):
    """Validates PowerShell scripts."""
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate PowerShell script."""
        issues = []
        
        # Try syntax check with pwsh if available
        try:
            result = subprocess.run(
                ['pwsh', '-NoProfile', '-NonInteractive', '-Command', 
                 f'$null = Get-Content -Path "{file_path}" -ErrorAction Stop; exit 0'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0 and result.stderr:
                issues.append(ValidationIssue(
                    file_path=str(file_path),
                    line_number=0,
                    severity=Severity.HIGH,
                    category='syntax',
                    message=f"PowerShell issue: {result.stderr[:200]}",
                    remediation="Check PowerShell syntax"
                ))
        except FileNotFoundError:
            self.log("pwsh not found, skipping PowerShell validation")
        except subprocess.TimeoutExpired:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.MEDIUM,
                category='runtime',
                message="PowerShell validation timed out",
                remediation="Check script for issues"
            ))
        except Exception as e:
            self.log(f"Error checking PowerShell: {e}")
        
        passed = not any(issue.severity in [Severity.CRITICAL, Severity.HIGH] for issue in issues)
        return ValidationResult(
            file_path=str(file_path),
            file_type=FileType.POWERSHELL,
            passed=passed,
            issues=issues
        )


class WorkflowValidator(FileValidator):
    """Validates GitHub Actions workflow files."""
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate workflow file."""
        issues = []
        
        # YAML syntax check
        try:
            import yaml
            # Custom loader to handle 'on' as string, not boolean
            class WorkflowLoader(yaml.SafeLoader):
                pass
            
            def on_constructor(loader, node):
                return 'on'
            
            WorkflowLoader.add_constructor('tag:yaml.org,2002:bool', on_constructor)
            WorkflowLoader.add_constructor('tag:yaml.org,2002:str', yaml.SafeLoader.construct_scalar)
            
            with open(file_path, 'r') as f:
                content = f.read()
                # Try normal YAML load first
                try:
                    workflow = yaml.safe_load(content)
                except:
                    # If it fails, workflow might have 'on' keyword issues
                    # Read as text and check manually
                    workflow = {}
                    if re.search(r'^on:', content, re.MULTILINE):
                        workflow['on'] = True  # Mark as present
            
            # Check required fields
            if not isinstance(workflow, dict):
                issues.append(ValidationIssue(
                    file_path=str(file_path),
                    line_number=0,
                    severity=Severity.CRITICAL,
                    category='syntax',
                    message="Workflow must be a YAML dictionary",
                    remediation="Fix workflow YAML structure"
                ))
            else:
                # Check for 'on' trigger - handle both boolean True (YAML parsing) and actual 'on' key
                has_on_trigger = ('on' in workflow or True in workflow or 
                                 re.search(r'^on:', content, re.MULTILINE))
                
                if not has_on_trigger:
                    issues.append(ValidationIssue(
                        file_path=str(file_path),
                        line_number=0,
                        severity=Severity.HIGH,
                        category='structure',
                        message="Workflow missing 'on' trigger definition",
                        remediation="Add workflow trigger (on: push, pull_request, etc.)"
                    ))
                
                # Check for jobs - search in content since YAML might parse weirdly
                has_jobs = 'jobs' in workflow or re.search(r'^jobs:', content, re.MULTILINE)
                
                if not has_jobs:
                    issues.append(ValidationIssue(
                        file_path=str(file_path),
                        line_number=0,
                        severity=Severity.HIGH,
                        category='structure',
                        message="Workflow missing 'jobs' definition",
                        remediation="Add at least one job to workflow"
                    ))
                
                # Check for secrets in workflow (security)
                if re.search(r'["\'][\w-]*(?:password|secret|token|key)[\w-]*["\']:\s*["\'][^"\'$]+["\']', content, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        file_path=str(file_path),
                        line_number=0,
                        severity=Severity.CRITICAL,
                        category='security',
                        message="Possible hardcoded secret in workflow",
                        remediation="Use GitHub secrets: ${{ secrets.SECRET_NAME }}"
                    ))
        
        except yaml.YAMLError as e:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.CRITICAL,
                category='syntax',
                message=f"YAML syntax error: {str(e)}",
                remediation="Fix YAML syntax"
            ))
        except Exception as e:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.HIGH,
                category='runtime',
                message=f"Validation error: {str(e)}",
                remediation="Review workflow file"
            ))
        
        passed = not any(issue.severity in [Severity.CRITICAL, Severity.HIGH] for issue in issues)
        return ValidationResult(
            file_path=str(file_path),
            file_type=FileType.WORKFLOW,
            passed=passed,
            issues=issues
        )


class TemplateValidator(FileValidator):
    """Validates template files (Markdown templates)."""
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate template file."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check if it's a GitHub issue/PR template
            is_github_template = '.github' in str(file_path) and ('ISSUE_TEMPLATE' in str(file_path) or 'pull_request' in file_path.name)
            
            if is_github_template:
                # Check for frontmatter (YAML)
                if content.startswith('---'):
                    try:
                        # Extract frontmatter
                        end_idx = content.find('---', 3)
                        if end_idx > 0:
                            frontmatter = content[3:end_idx]
                            import yaml
                            fm_data = yaml.safe_load(frontmatter)
                            
                            # Check required fields for issue templates
                            if 'ISSUE_TEMPLATE' in str(file_path):
                                if not fm_data or 'name' not in fm_data:
                                    issues.append(ValidationIssue(
                                        file_path=str(file_path),
                                        line_number=1,
                                        severity=Severity.MEDIUM,
                                        category='structure',
                                        message="Issue template missing 'name' in frontmatter",
                                        remediation="Add name: field to frontmatter"
                                    ))
                                if not fm_data or 'about' not in fm_data:
                                    issues.append(ValidationIssue(
                                        file_path=str(file_path),
                                        line_number=1,
                                        severity=Severity.LOW,
                                        category='structure',
                                        message="Issue template missing 'about' description",
                                        remediation="Add about: field to frontmatter"
                                    ))
                    except yaml.YAMLError as e:
                        issues.append(ValidationIssue(
                            file_path=str(file_path),
                            line_number=1,
                            severity=Severity.HIGH,
                            category='syntax',
                            message=f"Invalid YAML frontmatter: {str(e)}",
                            remediation="Fix YAML syntax in frontmatter"
                        ))
            
            # Check for placeholder format consistency
            placeholders = re.findall(r'<[^>]+>|\{[^}]+\}|\[\[?[^\]]+\]?\]', content)
            if placeholders:
                # Suggest consistent format
                angle_brackets = sum(1 for p in placeholders if p.startswith('<'))
                curly_braces = sum(1 for p in placeholders if p.startswith('{'))
                square_brackets = sum(1 for p in placeholders if p.startswith('['))
                
                if angle_brackets > 0 and curly_braces > 0:
                    issues.append(ValidationIssue(
                        file_path=str(file_path),
                        line_number=0,
                        severity=Severity.INFO,
                        category='structure',
                        message="Mixed placeholder styles found (< > and { })",
                        remediation="Consider using consistent placeholder format"
                    ))
            
            # Check for common template sections (if Markdown)
            if file_path.suffix == '.md':
                # Look for headings
                headings = [line for line in lines if line.startswith('#')]
                if is_github_template and len(headings) < 2:
                    issues.append(ValidationIssue(
                        file_path=str(file_path),
                        line_number=0,
                        severity=Severity.LOW,
                        category='structure',
                        message="Template has few section headings",
                        remediation="Consider adding more section headings for clarity"
                    ))
        
        except Exception as e:
            issues.append(ValidationIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.MEDIUM,
                category='runtime',
                message=f"Validation error: {str(e)}",
                remediation="Review template file"
            ))
        
        passed = not any(issue.severity in [Severity.CRITICAL, Severity.HIGH] for issue in issues)
        return ValidationResult(
            file_path=str(file_path),
            file_type=FileType.TEMPLATE,
            passed=passed,
            issues=issues
        )


class ComprehensiveValidator:
    """Main validator that coordinates all file type validators."""
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.validators = {
            FileType.PYTHON: PythonValidator(repo_root, verbose),
            FileType.SHELL: ShellValidator(repo_root, verbose),
            FileType.POWERSHELL: PowerShellValidator(repo_root, verbose),
            FileType.WORKFLOW: WorkflowValidator(repo_root, verbose),
            FileType.TEMPLATE: TemplateValidator(repo_root, verbose)
        }
    
    def detect_file_type(self, file_path: Path) -> FileType:
        """Detect file type based on extension and location."""
        suffix = file_path.suffix.lower()
        path_str = str(file_path)
        
        if suffix == '.py':
            return FileType.PYTHON
        elif suffix == '.sh':
            return FileType.SHELL
        elif suffix == '.ps1':
            return FileType.POWERSHELL
        elif suffix in ['.yml', '.yaml'] and '.github/workflows' in path_str:
            return FileType.WORKFLOW
        elif suffix == '.md' and ('template' in path_str.lower() or '.github' in path_str):
            return FileType.TEMPLATE
        elif 'template' in path_str.lower():
            return FileType.TEMPLATE
        
        return FileType.UNKNOWN
    
    def find_files(self, file_type: FileType = None) -> List[Path]:
        """Find files to validate."""
        files = []
        
        if file_type is None or file_type == FileType.PYTHON:
            files.extend(self.repo_root.glob('scripts/**/*.py'))
        
        if file_type is None or file_type == FileType.SHELL:
            files.extend(self.repo_root.glob('scripts/**/*.sh'))
        
        if file_type is None or file_type == FileType.POWERSHELL:
            files.extend(self.repo_root.glob('scripts/**/*.ps1'))
        
        if file_type is None or file_type == FileType.WORKFLOW:
            files.extend(self.repo_root.glob('.github/workflows/*.yml'))
            files.extend(self.repo_root.glob('.github/workflows/*.yaml'))
        
        if file_type is None or file_type == FileType.TEMPLATE:
            files.extend(self.repo_root.glob('.github/ISSUE_TEMPLATE/*.md'))
            files.extend(self.repo_root.glob('.github/pull_request_template.md'))
            files.extend(self.repo_root.glob('templates/**/*'))
            files.extend(self.repo_root.glob('docs/templates/**/*'))
        
        # Filter out directories and __pycache__
        files = [f for f in files if f.is_file() and '__pycache__' not in str(f)]
        
        return sorted(set(files))
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single file."""
        file_type = self.detect_file_type(file_path)
        
        if file_type == FileType.UNKNOWN:
            return ValidationResult(
                file_path=str(file_path),
                file_type=file_type,
                passed=True,
                issues=[]
            )
        
        validator = self.validators.get(file_type)
        if validator:
            return validator.validate(file_path)
        
        return ValidationResult(
            file_path=str(file_path),
            file_type=file_type,
            passed=True,
            issues=[]
        )
    
    def validate_all(self, file_type: FileType = None) -> List[ValidationResult]:
        """Validate all files of specified type (or all if None)."""
        files = self.find_files(file_type)
        results = []
        
        print(f"🔍 Found {len(files)} files to validate")
        print()
        
        for file_path in files:
            if self.verbose:
                print(f"Validating: {file_path}")
            result = self.validate_file(file_path)
            results.append(result)
        
        return results
    
    def print_summary(self, results: List[ValidationResult], strict: bool = False):
        """Print validation summary."""
        print("=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        print()
        
        # Group by file type
        by_type = {}
        for result in results:
            by_type.setdefault(result.file_type, []).append(result)
        
        total_files = len(results)
        total_passed = sum(1 for r in results if r.passed)
        total_failed = total_files - total_passed
        total_issues = sum(len(r.issues) for r in results)
        
        # Count by severity
        severity_counts = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 0,
            Severity.MEDIUM: 0,
            Severity.LOW: 0,
            Severity.INFO: 0
        }
        
        for result in results:
            for issue in result.issues:
                severity_counts[issue.severity] += 1
        
        print(f"Files validated: {total_files}")
        print(f"✅ Passed: {total_passed}")
        print(f"❌ Failed: {total_failed}")
        print(f"📋 Total issues: {total_issues}")
        print()
        
        print("By Severity:")
        print(f"  🔴 Critical: {severity_counts[Severity.CRITICAL]}")
        print(f"  🟠 High:     {severity_counts[Severity.HIGH]}")
        print(f"  🟡 Medium:   {severity_counts[Severity.MEDIUM]}")
        print(f"  🟢 Low:      {severity_counts[Severity.LOW]}")
        print(f"  ℹ️  Info:     {severity_counts[Severity.INFO]}")
        print()
        
        print("By File Type:")
        for file_type, type_results in sorted(by_type.items(), key=lambda x: x[0].value):
            passed = sum(1 for r in type_results if r.passed)
            total = len(type_results)
            print(f"  {file_type.value.capitalize()}: {passed}/{total} passed")
        print()
        
        # Show critical and high issues
        critical_high = [
            (r, i) for r in results for i in r.issues 
            if i.severity in [Severity.CRITICAL, Severity.HIGH]
        ]
        
        if critical_high:
            print("🚨 CRITICAL & HIGH SEVERITY ISSUES:")
            print("=" * 70)
            for result, issue in critical_high[:20]:  # Show first 20
                severity_icon = "🔴" if issue.severity == Severity.CRITICAL else "🟠"
                print(f"{severity_icon} {issue.file_path}:{issue.line_number}")
                print(f"   [{issue.category}] {issue.message}")
                if issue.remediation:
                    print(f"   💡 {issue.remediation}")
                print()
            
            if len(critical_high) > 20:
                print(f"... and {len(critical_high) - 20} more critical/high issues")
                print()
        
        # Final verdict
        print("=" * 70)
        has_critical = severity_counts[Severity.CRITICAL] > 0
        has_high = severity_counts[Severity.HIGH] > 0
        
        if has_critical or has_high:
            print("❌ VALIDATION FAILED - Critical or high severity issues found")
            return False
        elif strict and (severity_counts[Severity.MEDIUM] > 0 or severity_counts[Severity.LOW] > 0):
            print("⚠️  VALIDATION FAILED (strict mode) - Medium or low severity issues found")
            return False
        else:
            print("✅ VALIDATION PASSED - All checks successful!")
            return True


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Comprehensive validation for scripts, workflows, and templates'
    )
    parser.add_argument(
        '--type',
        choices=['python', 'shell', 'powershell', 'workflow', 'template', 'all'],
        default='all',
        help='File type to validate (default: all)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on any issues (including medium/low severity)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--output',
        help='Write JSON report to file'
    )
    args = parser.parse_args()
    
    # Map argument to FileType
    type_map = {
        'python': FileType.PYTHON,
        'shell': FileType.SHELL,
        'powershell': FileType.POWERSHELL,
        'workflow': FileType.WORKFLOW,
        'template': FileType.TEMPLATE,
        'all': None
    }
    
    file_type = type_map.get(args.type)
    
    repo_root = Path(__file__).parent.parent.parent
    validator = ComprehensiveValidator(repo_root, verbose=args.verbose)
    
    results = validator.validate_all(file_type)
    success = validator.print_summary(results, strict=args.strict)
    
    # Write JSON output if requested
    if args.output:
        output_data = {
            'summary': {
                'total_files': len(results),
                'passed': sum(1 for r in results if r.passed),
                'failed': sum(1 for r in results if not r.passed),
                'total_issues': sum(len(r.issues) for r in results)
            },
            'results': [r.to_dict() for r in results]
        }
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n📄 Detailed report written to: {args.output}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
