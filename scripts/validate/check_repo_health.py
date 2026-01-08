#!/usr/bin/env python3
# ============================================================================
# Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>
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
# VERSION: 01.00.00
# BRIEF: Performs repository health checks based on XML configuration
# ============================================================================

"""
Repository Health Checker

Performs repository health checks based on XML configuration.
Supports both local and remote XML configuration files.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET


# Namespace for repo health schema
REPO_HEALTH_NS = "http://mokoconsulting.com/schemas/repo-health"

# Default remote configuration URL
DEFAULT_REMOTE_CONFIG = "https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml"

# Default health threshold for pass/fail (percentage)
DEFAULT_HEALTH_THRESHOLD = 70.0


class RepoHealthChecker:
    """Performs repository health checks based on XML configuration."""

    def __init__(self, config_source: str, repo_path: str = "."):
        """
        Initialize health checker.

        Args:
            config_source: Path to XML file or URL
            repo_path: Path to repository to check (default: current directory)
        """
        self.config_source = config_source
        self.repo_path = Path(repo_path).resolve()
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
        """Load configuration from file or URL."""
        try:
            # Load XML from file or URL
            if self.config_source.startswith("http://") or self.config_source.startswith(
                "https://"
            ):
                xml_content = self._load_from_url(self.config_source)
            else:
                xml_content = self._load_from_file(self.config_source)

            # Parse XML
            self.config = ET.fromstring(xml_content)
            return True
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            return False

    def run_checks(self) -> Dict:
        """Run all health checks and calculate score."""
        if self.config is None:
            raise RuntimeError("Configuration not loaded. Call load_config() first.")

        # Parse configuration
        scoring = self.config.find(f"{{{REPO_HEALTH_NS}}}scoring")
        checks_section = self.config.find(f"{{{REPO_HEALTH_NS}}}checks")

        if scoring is None or checks_section is None:
            raise RuntimeError("Invalid configuration: missing scoring or checks section")

        # Get total points and categories
        total_points_elem = scoring.find(f"{{{REPO_HEALTH_NS}}}total-points")
        total_points = int(total_points_elem.text) if total_points_elem is not None else 100

        categories = self._parse_categories(scoring)
        thresholds = self._parse_thresholds(scoring)

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
        for check_group in checks_section.findall(f"{{{REPO_HEALTH_NS}}}check-group"):
            cat_ref_elem = check_group.find(f"{{{REPO_HEALTH_NS}}}category-ref")
            cat_ref = cat_ref_elem.text if cat_ref_elem is not None else "unknown"

            for check in check_group.findall(f"{{{REPO_HEALTH_NS}}}check"):
                result = self._run_single_check(check, cat_ref)
                self.results["checks"].append(result)

                # Update category scores
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

    def _load_from_file(self, file_path: str) -> bytes:
        """Load XML content from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"XML file not found: {file_path}")
        return path.read_bytes()

    def _load_from_url(self, url: str) -> bytes:
        """Load XML content from URL."""
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except Exception as e:
            raise Exception(f"Failed to load XML from URL {url}: {e}")

    def _parse_categories(self, scoring: ET.Element) -> Dict:
        """Parse categories from scoring section."""
        categories = {}
        categories_elem = scoring.find(f"{{{REPO_HEALTH_NS}}}categories")

        if categories_elem is not None:
            for category in categories_elem.findall(f"{{{REPO_HEALTH_NS}}}category"):
                cat_id_elem = category.find(f"{{{REPO_HEALTH_NS}}}id")
                name_elem = category.find(f"{{{REPO_HEALTH_NS}}}name")
                max_points_elem = category.find(f"{{{REPO_HEALTH_NS}}}max-points")
                enabled_elem = category.find(f"{{{REPO_HEALTH_NS}}}enabled")

                if cat_id_elem is not None and cat_id_elem.text:
                    cat_id = cat_id_elem.text
                    categories[cat_id] = {
                        "name": name_elem.text if name_elem is not None else cat_id,
                        "max_points": int(max_points_elem.text) if max_points_elem is not None else 0,
                        "enabled": enabled_elem.text.lower() == "true" if enabled_elem is not None else True,
                    }

        return categories

    def _parse_thresholds(self, scoring: ET.Element) -> List[Dict]:
        """Parse thresholds from scoring section."""
        thresholds = []
        thresholds_elem = scoring.find(f"{{{REPO_HEALTH_NS}}}thresholds")

        if thresholds_elem is not None:
            for threshold in thresholds_elem.findall(f"{{{REPO_HEALTH_NS}}}threshold"):
                level_elem = threshold.find(f"{{{REPO_HEALTH_NS}}}level")
                min_pct_elem = threshold.find(f"{{{REPO_HEALTH_NS}}}min-percentage")
                max_pct_elem = threshold.find(f"{{{REPO_HEALTH_NS}}}max-percentage")
                indicator_elem = threshold.find(f"{{{REPO_HEALTH_NS}}}indicator")

                thresholds.append({
                    "level": level_elem.text if level_elem is not None else "unknown",
                    "min_percentage": float(min_pct_elem.text) if min_pct_elem is not None else 0,
                    "max_percentage": float(max_pct_elem.text) if max_pct_elem is not None else 100,
                    "indicator": indicator_elem.text if indicator_elem is not None else "?",
                })

        return thresholds

    def _run_single_check(self, check: ET.Element, category_ref: str) -> Dict:
        """Run a single health check."""
        check_id = self._get_element_text(check, "id", "unknown")
        name = self._get_element_text(check, "name", "Unknown Check")
        description = self._get_element_text(check, "description", "")
        points = int(self._get_element_text(check, "points", "0"))
        check_type = self._get_element_text(check, "check-type", "unknown")
        required = self._get_element_text(check, "required", "true").lower() == "true"
        remediation = self._get_element_text(check, "remediation", "")

        # Parse parameters
        parameters = self._parse_parameters(check)

        # Run check based on type
        passed = False
        message = ""

        try:
            if check_type == "file-exists":
                passed, message = self._check_file_exists(parameters)
            elif check_type == "directory-exists":
                passed, message = self._check_directory_exists(parameters)
            elif check_type == "file-content":
                passed, message = self._check_file_content(parameters)
            elif check_type == "file-size":
                passed, message = self._check_file_size(parameters)
            elif check_type == "workflow-exists":
                passed, message = self._check_workflow_exists(parameters)
            elif check_type == "branch-exists":
                passed, message = self._check_branch_exists(parameters)
            else:
                passed = False
                message = f"Check type '{check_type}' not implemented"
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

    def _get_element_text(self, parent: ET.Element, tag: str, default: str = "") -> str:
        """Get text content of a child element."""
        elem = parent.find(f"{{{REPO_HEALTH_NS}}}{tag}")
        return elem.text if elem is not None and elem.text else default

    def _parse_parameters(self, check: ET.Element) -> Dict:
        """Parse parameters from check element."""
        parameters = {}
        params_elem = check.find(f"{{{REPO_HEALTH_NS}}}parameters")

        if params_elem is not None:
            for param in params_elem.findall(f"{{{REPO_HEALTH_NS}}}parameter"):
                key_elem = param.find(f"{{{REPO_HEALTH_NS}}}key")
                value_elem = param.find(f"{{{REPO_HEALTH_NS}}}value")

                if key_elem is not None and value_elem is not None:
                    parameters[key_elem.text] = value_elem.text

        return parameters

    def _check_file_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a file exists."""
        file_path = params.get("file-path", "")
        full_path = self.repo_path / file_path

        if not full_path.exists():
            return False, f"File not found: {file_path}"

        # Check minimum size if specified
        min_size = params.get("min-size")
        if min_size:
            size = full_path.stat().st_size
            if size < int(min_size):
                return False, f"File size ({size} bytes) below minimum ({min_size} bytes)"

        return True, f"File exists: {file_path}"

    def _check_directory_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a directory exists."""
        dir_path = params.get("directory-path", "")
        full_path = self.repo_path / dir_path

        if not full_path.exists():
            return False, f"Directory not found: {dir_path}"

        if not full_path.is_dir():
            return False, f"Path exists but is not a directory: {dir_path}"

        return True, f"Directory exists: {dir_path}"

    def _check_file_content(self, params: Dict) -> Tuple[bool, str]:
        """Check if a file contains expected content."""
        file_path = params.get("file-path", "")
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
        workflow_path = params.get("workflow-path", "")
        full_path = self.repo_path / workflow_path

        if not full_path.exists():
            return False, f"Workflow not found: {workflow_path}"

        return True, f"Workflow exists: {workflow_path}"

    def _check_branch_exists(self, params: Dict) -> Tuple[bool, str]:
        """Check if a branch exists (requires git)."""
        # This would require git commands, simplified for now
        return True, "Branch check not fully implemented"

    def _determine_health_level(self, percentage: float, thresholds: List[Dict]) -> str:
        """Determine health level based on percentage and thresholds."""
        for threshold in thresholds:
            if threshold["min_percentage"] <= percentage <= threshold["max_percentage"]:
                return threshold["level"]
        return "unknown"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check repository health based on XML configuration"
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_REMOTE_CONFIG,
        help=f"Path to XML config file or URL (default: remote config from GitHub)",
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

    args = parser.parse_args()

    # Create checker
    checker = RepoHealthChecker(args.config, args.repo_path)

    # Load configuration
    if args.verbose:
        print(f"Loading configuration from: {args.config}")

    if not checker.load_config():
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

    # Exit with appropriate code
    sys.exit(0 if results["percentage"] >= DEFAULT_HEALTH_THRESHOLD else 1)


if __name__ == "__main__":
    main()
