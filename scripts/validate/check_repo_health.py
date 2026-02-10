#!/usr/bin/env python3
# ============================================================================
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts.Validate
# INGROUP: MokoStandards
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /scripts/validate/check_repo_health.py
# VERSION: 03.01.05
# BRIEF: Performs repository health checks based on Terraform configuration
# ============================================================================

"""
Repository Health Checker

Performs repository health checks based on Terraform configuration.
Migrated from XML-based schema to Terraform infrastructure-as-code approach.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Import Terraform schema reader
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from terraform_schema_reader import TerraformSchemaReader


# Default health threshold for pass/fail (percentage)
DEFAULT_HEALTH_THRESHOLD = 70.0


class RepoHealthChecker:
    """Performs repository health checks based on Terraform configuration."""

    def __init__(self, repo_path: str = ".", dry_run: bool = False):
        """
        Initialize health checker.

        Args:
            repo_path: Path to repository to check (default: current directory)
            dry_run: Show what would be checked without executing
        """
        self.repo_path = Path(repo_path).resolve()
        self.dry_run = dry_run
        self.schema_reader = TerraformSchemaReader()
        self.config = None
        self.results = {
            "categories": {},
            "checks": [],
            "score": 0,
            "max_score": 0,
            "percentage": 0.0,
            "level": "unknown",
        }

    def load_config(self) -> bool:
        """Load configuration from Terraform."""
        try:
            self.config = self.schema_reader.get_health_config()
            return True
        except Exception as e:
            print(f"Error loading Terraform configuration: {e}", file=sys.stderr)
            print("Note: Terraform configuration must be initialized. Run 'terraform init' in terraform/ directory.", file=sys.stderr)
            return False

    def run_checks(self) -> Dict:
        """Run all health checks and calculate score."""
        if self.config is None:
            if not self.load_config():
                raise RuntimeError("Configuration not loaded. Ensure Terraform is initialized.")

        # Get configuration components
        scoring = self.config.get('scoring', {})
        categories = self.config.get('categories', {})
        thresholds = self.config.get('thresholds', {})
        checks = self.config.get('checks', {})

        total_points = scoring.get('total_points', 100)

        # Initialize category scores
        for cat_id, cat_info in categories.items():
            self.results["categories"][cat_id] = {
                "name": cat_info["name"],
                "max_points": cat_info["max_points"],
                "earned_points": 0,
                "checks_passed": 0,
                "checks_failed": 0,
            }

        # Run checks
        for check_id, check in checks.items():
            result = self._run_single_check(check)
            self.results["checks"].append(result)

            # Update category scores
            cat_ref = check.get('category')
            if cat_ref in self.results["categories"]:
                if result["passed"]:
                    self.results["categories"][cat_ref]["earned_points"] += result["points"]
                    self.results["categories"][cat_ref]["checks_passed"] += 1
                else:
                    self.results["categories"][cat_ref]["checks_failed"] += 1

        # Calculate total score
        total_earned = sum(cat["earned_points"] for cat in self.results["categories"].values())
        self.results["score"] = total_earned
        self.results["max_score"] = total_points
        self.results["percentage"] = (total_earned / total_points * 100) if total_points > 0 else 0

        # Determine health level
        self.results["level"] = self._determine_health_level(self.results["percentage"], thresholds)

        return self.results

    def _run_single_check(self, check: Dict) -> Dict:
        """Run a single health check."""
        check_id = check.get("id", "unknown")
        name = check.get("name", "Unknown Check")
        description = check.get("description", "")
        points = check.get("points", 0)
        check_type = check.get("check_type", "unknown")
        required = check.get("required", True)
        remediation = check.get("remediation", "")
        category_ref = check.get("category", "unknown")

        # Get parameters
        parameters = check.get("parameters", {})

        if self.dry_run:
            message = f"[DRY-RUN] Would check: {name}"
            return {
                "check_id": check_id,
                "name": name,
                "description": description,
                "passed": True,
                "message": message,
                "points": points,
                "required": required,
                "remediation": remediation,
                "category": category_ref,
            }

        # Run check based on type
        passed = False
        message = ""

        try:
            if check_type == "file-exists":
                passed, message = self._check_file_exists(parameters)
            elif check_type == "directory-exists":
                passed, message = self._check_directory_exists(parameters)
            elif check_type == "directory-exists-any":
                passed, message = self._check_directory_exists_any(parameters)
            elif check_type == "content-pattern":
                passed, message = self._check_file_content(parameters)
            elif check_type == "file-size":
                passed, message = self._check_file_size(parameters)
            elif check_type == "workflow-exists":
                passed, message = self._check_workflow_exists(parameters)
            elif check_type == "branch-exists":
                passed, message = self._check_branch_exists(parameters)
            elif check_type == "security-scan":
                passed, message = self._check_security_scan(parameters)
            elif check_type == "script-integrity":
                passed, message = self._check_script_integrity(parameters)
            else:
                passed = False
                message = (
                    f"Check type '{check_type}' not implemented. "
                    "This version supports: file-exists, directory-exists, content-pattern, "
                    "file-size, workflow-exists, branch-exists, security-scan, script-integrity. "
                    "Check types workflow-passing, github-setting, secret-configured, and "
                    "custom-script require GitHub API access or custom handlers."
                )
        except Exception as e:
            passed = False
            message = f"Check failed with error: {str(e)}"

        return {
            "id": check_id,
            "name": name,
            "description": description,
            "category": category_ref,
            "points": points,
            "passed": passed,
            "required": required,
            "message": message,
            "remediation": remediation if not passed else "",
        }

    def _check_file_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a file exists."""
        file_path = params.get("file_path", "")
        full_path = self.repo_path / file_path

        if not full_path.exists():
            return False, f"File not found: {file_path}"

        # Check minimum size if specified
        min_size = params.get("min_size")
        if min_size:
            size = full_path.stat().st_size
            if size < int(min_size):
                return False, f"File size ({size} bytes) below minimum ({min_size} bytes)"

        return True, f"File exists: {file_path}"

    def _check_directory_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a directory exists."""
        dir_path = params.get("directory_path", "")
        full_path = self.repo_path / dir_path

        if not full_path.exists():
            return False, f"Directory not found: {dir_path}"

        if not full_path.is_dir():
            return False, f"Path exists but is not a directory: {dir_path}"

        return True, f"Directory exists: {dir_path}"

    def _check_directory_exists_any(self, params: Dict) -> Tuple[bool, str]:
        """Check if any of the specified directories exist."""
        dir_paths = params.get("directory_paths", [])

        for dir_path in dir_paths:
            full_path = self.repo_path / dir_path
            if full_path.exists() and full_path.is_dir():
                return True, f"Directory found: {dir_path}"

        return False, f"None of the directories found: {', '.join(dir_paths)}"

    def _check_file_content(self, params: Dict) -> Tuple[bool, str]:
        """Check if a file contains expected content."""
        file_path = params.get("file_path", "")
        pattern = params.get("pattern", "")

        full_path = self.repo_path / file_path

        if not full_path.exists():
            return False, f"File not found: {file_path}"

        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                return True, f"Pattern found in {file_path}"
            else:
                return False, f"Pattern not found in {file_path}"
        except re.error as e:
            return False, f"Invalid regex pattern: {str(e)}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    def _check_file_size(self, params: Dict) -> Tuple[bool, str]:
        """Check file size constraints."""
        file_path = params.get("file-path", "")
        min_size = params.get("min-size")
        max_size = params.get("max-size")

        full_path = self.repo_path / file_path

        if not full_path.exists():
            return False, f"File not found: {file_path}"

        size = full_path.stat().st_size

        if min_size and size < int(min_size):
            return False, f"File size ({size} bytes) below minimum ({min_size} bytes)"

        if max_size and size > int(max_size):
            return False, f"File size ({size} bytes) exceeds maximum ({max_size} bytes)"

        return True, f"File size OK: {size} bytes"

    def _check_workflow_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a workflow file exists."""
        workflow_path = params.get("workflow_path", "")
        full_path = self.repo_path / workflow_path

        if not full_path.exists():
            return False, f"Workflow not found: {workflow_path}"

        return True, f"Workflow exists: {workflow_path}"

    def _check_branch_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a branch exists (requires git)."""
        # This check requires git commands which are not yet fully implemented.
        # Returning False to indicate the check cannot be performed rather than
        # incorrectly passing all branch-exists checks.
        return False, "Branch existence check not fully implemented (requires git integration)"

    def _check_security_scan(self, params: Dict) -> Tuple[bool, str]:
        """Run security scan on scripts."""
        try:
            # Import and run security scanner
            script_path = Path(__file__).parent / "check_script_security.py"
            if not script_path.exists():
                return False, "Security scanner not found"
            
            # Run security scan
            import subprocess
            result = subprocess.run(
                ['python3', str(script_path), '--path', 'scripts'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Check severity threshold
            max_severity = params.get('max_severity', 'medium')
            severity_levels = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
            max_level = severity_levels.get(max_severity, 1)
            
            # Parse output for severity counts
            output = result.stdout
            critical_count = 0
            high_count = 0
            
            for line in output.split('\n'):
                if 'Critical:' in line:
                    critical_count = int(line.split(':')[-1].strip())
                elif 'High:' in line:
                    high_count = int(line.split(':')[-1].strip())
            
            # Determine pass/fail based on severity threshold
            if max_level < 3 and critical_count > 0:
                return False, f"Security scan failed: {critical_count} critical issues found"
            elif max_level < 2 and high_count > 0:
                return False, f"Security scan failed: {high_count} high severity issues found"
            
            return True, "Security scan passed - no critical/high issues"
            
        except subprocess.TimeoutExpired:
            return False, "Security scan timed out"
        except Exception as e:
            return False, f"Security scan error: {str(e)}"

    def _check_script_integrity(self, params: Dict) -> Tuple[bool, str]:
        """Validate script integrity against registry."""
        try:
            # Import and run integrity validator
            script_path = Path(__file__).parent.parent / "maintenance" / "validate_script_registry.py"
            if not script_path.exists():
                return False, "Script integrity validator not found"
            
            # Get priority level
            priority = params.get('priority', 'critical')
            
            # Run validation
            import subprocess
            result = subprocess.run(
                ['python3', str(script_path), '--priority', priority],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if validation passed
            if result.returncode == 0:
                return True, f"Script integrity validated ({priority} priority)"
            else:
                # Parse output for details
                output = result.stdout
                modified_count = 0
                for line in output.split('\n'):
                    if 'Modified:' in line:
                        try:
                            modified_count = int(line.split('/')[0].split(':')[-1].strip())
                        except:
                            pass
                
                if modified_count > 0:
                    return False, f"Script integrity check failed: {modified_count} scripts modified"
                return False, "Script integrity validation failed"
                
        except subprocess.TimeoutExpired:
            return False, "Script integrity check timed out"
        except Exception as e:
            return False, f"Script integrity check error: {str(e)}"

    def _determine_health_level(self, percentage: float, thresholds: Dict) -> str:
        """Determine health level based on percentage and thresholds."""
        for threshold_name, threshold in thresholds.items():
            min_pct = threshold.get("min_percentage", 0)
            max_pct = threshold.get("max_percentage", 100)
            if min_pct <= percentage <= max_pct:
                return threshold.get("level", threshold_name)
        return "unknown"


def write_github_summary(results: Dict, repo_path: str):
    """Write detailed results to GitHub Actions summary."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return

    try:
        with open(summary_file, "a") as f:
            f.write("\n## 🏥 Repository Health Check Results\n\n")

            # Overall score
            percentage = results["percentage"]
            level = results["level"].upper()
            score = results["score"]
            max_score = results["max_score"]

            # Determine emoji based on level
            if level == "EXCELLENT":
                emoji = "✅"
            elif level == "GOOD":
                emoji = "⚠️"
            elif level == "FAIR":
                emoji = "🟠"
            else:
                emoji = "❌"

            f.write(f"**Repository:** `{repo_path}`\n\n")
            f.write(f"### {emoji} Overall Health: {level}\n\n")
            f.write(f"**Score:** {score}/{max_score} ({percentage:.1f}%)\n\n")

            # Progress bar
            bar_length = 20
            filled = int(bar_length * percentage / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            f.write(f"```\n{bar} {percentage:.1f}%\n```\n\n")

            # Category breakdown
            f.write("### 📊 Category Breakdown\n\n")
            f.write("| Category | Points | Passed | Failed | Status |\n")
            f.write("|----------|--------|--------|--------|--------|\n")

            for cat_id, cat_info in results["categories"].items():
                earned = cat_info["earned_points"]
                max_pts = cat_info["max_points"]
                passed = cat_info["checks_passed"]
                failed = cat_info["checks_failed"]
                pct = (earned / max_pts * 100) if max_pts > 0 else 0

                if failed == 0:
                    status = "✅"
                elif passed == 0:
                    status = "❌"
                else:
                    status = "⚠️"

                f.write(f"| {cat_info['name']} | {earned}/{max_pts} ({pct:.0f}%) | {passed} | {failed} | {status} |\n")

            f.write("\n")

            # Failed checks details
            failed_checks = [c for c in results["checks"] if not c["passed"]]
            if failed_checks:
                f.write("### ❌ Failed Checks\n\n")
                f.write("<details>\n")
                f.write("<summary>Click to expand failed checks details</summary>\n\n")

                for check in failed_checks:
                    required_badge = "🔴 REQUIRED" if check["required"] else "🟡 OPTIONAL"
                    f.write(f"#### {required_badge} {check['name']}\n\n")
                    f.write(f"**Category:** {check['category']}\n\n")
                    f.write(f"**Points Lost:** {check['points']}\n\n")
                    f.write(f"**Issue:** {check['message']}\n\n")

                    if check["remediation"]:
                        f.write(f"**Remediation:**\n```\n{check['remediation']}\n```\n\n")

                    f.write("---\n\n")

                f.write("</details>\n\n")

            # Passed checks summary
            passed_checks = [c for c in results["checks"] if c["passed"]]
            if passed_checks:
                f.write(f"### ✅ Passed Checks ({len(passed_checks)})\n\n")
                f.write("<details>\n")
                f.write("<summary>Click to see all passing checks</summary>\n\n")

                for check in passed_checks:
                    f.write(f"- ✅ **{check['name']}** ({check['points']} pts): {check['message']}\n")

                f.write("\n</details>\n\n")

            # Health thresholds reference
            f.write("### 📏 Health Level Thresholds\n\n")
            f.write("| Level | Score Range | Indicator |\n")
            f.write("|-------|-------------|----------|\n")
            f.write("| Excellent | 90-100% | ✅ Production-ready |\n")
            f.write("| Good | 70-89% | ⚠️ Minor improvements needed |\n")
            f.write("| Fair | 50-69% | 🟡 Significant improvements required |\n")
            f.write("| Poor | 0-49% | ❌ Critical issues |\n")
            f.write("\n")

    except Exception as e:
        print(f"Warning: Could not write to GitHub summary: {e}", file=sys.stderr)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check repository health based on Terraform configuration"
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to repository to check (default: current directory)",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be checked without executing"
    )

    args = parser.parse_args()

    # Create checker (config argument is ignored now)
    checker = RepoHealthChecker(args.repo_path, args.dry_run)

    # Load configuration
    if args.verbose:
        print("Loading configuration from Terraform...")

    if not checker.load_config():
        print("ERROR: Could not load Terraform configuration.", file=sys.stderr)
        print("Please ensure Terraform is initialized in the terraform/ directory.", file=sys.stderr)
        sys.exit(1)

    # Run checks
    if args.verbose:
        print(f"Checking repository: {args.repo_path}")

    results = checker.run_checks()

    # Output results
    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "=" * 60)
        print("REPOSITORY HEALTH CHECK RESULTS")
        print("=" * 60)
        print(f"\nRepository: {args.repo_path}")
        print(f"Score: {results['score']}/{results['max_score']} ({results['percentage']:.1f}%)")
        print(f"Health Level: {results['level'].upper()}")

        print("\n" + "-" * 60)
        print("CATEGORY BREAKDOWN")
        print("-" * 60)

        for cat_id, cat_info in results["categories"].items():
            print(f"\n{cat_info['name']}:")
            print(f"  Points: {cat_info['earned_points']}/{cat_info['max_points']}")
            print(f"  Passed: {cat_info['checks_passed']}, Failed: {cat_info['checks_failed']}")

        # Show failed checks
        failed_checks = [c for c in results["checks"] if not c["passed"] and c["required"]]
        if failed_checks:
            print("\n" + "-" * 60)
            print("REQUIRED CHECKS FAILED")
            print("-" * 60)
            for check in failed_checks:
                print(f"\n❌ {check['name']}")
                print(f"   {check['message']}")
                if check["remediation"]:
                    print(f"   Remediation: {check['remediation']}")

        if args.verbose:
            print("\n" + "-" * 60)
            print("ALL CHECKS")
            print("-" * 60)
            for check in results["checks"]:
                status = "✅" if check["passed"] else "❌"
                print(f"\n{status} {check['name']} ({check['points']} pts)")
                print(f"   {check['message']}")

    # Write to GitHub Actions Summary if running in CI
    if os.environ.get("GITHUB_ACTIONS") == "true":
        write_github_summary(results, args.repo_path)

    # Exit with appropriate code
    sys.exit(0 if results["percentage"] >= DEFAULT_HEALTH_THRESHOLD else 1)


if __name__ == "__main__":
    main()
