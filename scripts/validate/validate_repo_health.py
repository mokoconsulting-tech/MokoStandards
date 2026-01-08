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
# PATH: /scripts/validate/validate_repo_health.py
# VERSION: 01.00.00
# BRIEF: Validates repository health configuration XML against schema
# ============================================================================

"""
Repository Health XML Validator

Validates repo health configuration XML files against the schema definition.
Supports local files and remote URLs.
"""

import argparse
import sys
import urllib.request
from pathlib import Path
from typing import Optional, Tuple
from xml.etree import ElementTree as ET


# Namespace for repo health schema
REPO_HEALTH_NS = "http://mokoconsulting.com/schemas/repo-health"
NS_MAP = {"rh": REPO_HEALTH_NS}


class RepoHealthValidator:
    """Validates repository health XML configuration."""

    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize validator.

        Args:
            schema_path: Optional path to XSD schema file
        """
        self.schema_path = schema_path
        self.errors = []
        self.warnings = []

    def validate_xml(self, xml_source: str) -> Tuple[bool, list, list]:
        """
        Validate a repository health XML configuration.

        Args:
            xml_source: Path to XML file or URL

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        try:
            # Load XML from file or URL
            if xml_source.startswith("http://") or xml_source.startswith("https://"):
                xml_content = self._load_from_url(xml_source)
            else:
                xml_content = self._load_from_file(xml_source)

            # Parse XML
            root = ET.fromstring(xml_content)

            # Basic validation
            self._validate_structure(root)
            self._validate_metadata(root)
            self._validate_scoring(root)
            self._validate_checks(root)

        except ET.ParseError as e:
            self.errors.append(f"XML parsing error: {e}")
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Validation error: {e}")
            return False, self.errors, self.warnings

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

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

    def _validate_structure(self, root: ET.Element):
        """Validate basic XML structure."""
        # Check root element
        if not root.tag.endswith("repo-health"):
            self.errors.append(
                f"Invalid root element: expected 'repo-health', got '{root.tag}'"
            )

        # Check required attributes
        version = root.get("version")
        if not version:
            self.errors.append("Missing required attribute: version")

        schema_version = root.get("schema-version")
        if not schema_version:
            self.warnings.append("Missing schema-version attribute")
        elif schema_version != "1.0":
            self.warnings.append(
                f"Unexpected schema-version: {schema_version} (expected 1.0)"
            )

        # Check required sections
        required_sections = ["metadata", "scoring", "checks"]
        for section in required_sections:
            if root.find(f"{{{REPO_HEALTH_NS}}}{section}") is None:
                self.errors.append(f"Missing required section: {section}")

    def _validate_metadata(self, root: ET.Element):
        """Validate metadata section."""
        metadata = root.find(f"{{{REPO_HEALTH_NS}}}metadata")
        if metadata is None:
            return

        required_fields = ["name", "description", "effective-date", "maintainer"]
        for field in required_fields:
            element = metadata.find(f"{{{REPO_HEALTH_NS}}}{field}")
            if element is None:
                self.errors.append(f"Missing required metadata field: {field}")
            elif not element.text or not element.text.strip():
                self.errors.append(f"Empty metadata field: {field}")

    def _validate_scoring(self, root: ET.Element):
        """Validate scoring section."""
        scoring = root.find(f"{{{REPO_HEALTH_NS}}}scoring")
        if scoring is None:
            return

        # Validate total points
        total_points_elem = scoring.find(f"{{{REPO_HEALTH_NS}}}total-points")
        if total_points_elem is None:
            self.errors.append("Missing total-points in scoring section")
            return

        try:
            total_points = int(total_points_elem.text)
        except ValueError:
            self.errors.append(
                f"Invalid total-points value: {total_points_elem.text}"
            )
            return

        # Validate categories
        categories = scoring.find(f"{{{REPO_HEALTH_NS}}}categories")
        if categories is None:
            self.errors.append("Missing categories in scoring section")
            return

        category_sum = 0
        category_ids = set()

        for category in categories.findall(f"{{{REPO_HEALTH_NS}}}category"):
            cat_id = category.find(f"{{{REPO_HEALTH_NS}}}id")
            if cat_id is not None and cat_id.text:
                if cat_id.text in category_ids:
                    self.errors.append(f"Duplicate category ID: {cat_id.text}")
                category_ids.add(cat_id.text)

            max_points = category.find(f"{{{REPO_HEALTH_NS}}}max-points")
            if max_points is not None:
                try:
                    points = int(max_points.text)
                    category_sum += points
                except ValueError:
                    self.errors.append(
                        f"Invalid max-points in category: {max_points.text}"
                    )

        # Check if category points sum to total
        if category_sum != total_points:
            self.errors.append(
                f"Category points sum ({category_sum}) does not equal total-points ({total_points})"
            )

        # Validate thresholds
        thresholds = scoring.find(f"{{{REPO_HEALTH_NS}}}thresholds")
        if thresholds is None:
            self.errors.append("Missing thresholds in scoring section")
            return

        threshold_levels = set()
        for threshold in thresholds.findall(f"{{{REPO_HEALTH_NS}}}threshold"):
            level = threshold.find(f"{{{REPO_HEALTH_NS}}}level")
            if level is not None and level.text:
                if level.text in threshold_levels:
                    self.errors.append(f"Duplicate threshold level: {level.text}")
                threshold_levels.add(level.text)

            # Validate percentage ranges
            min_pct = threshold.find(f"{{{REPO_HEALTH_NS}}}min-percentage")
            max_pct = threshold.find(f"{{{REPO_HEALTH_NS}}}max-percentage")

            if min_pct is not None and max_pct is not None:
                try:
                    min_val = float(min_pct.text)
                    max_val = float(max_pct.text)

                    if min_val < 0 or min_val > 100:
                        self.errors.append(
                            f"Invalid min-percentage: {min_val} (must be 0-100)"
                        )
                    if max_val < 0 or max_val > 100:
                        self.errors.append(
                            f"Invalid max-percentage: {max_val} (must be 0-100)"
                        )
                    if min_val > max_val:
                        self.errors.append(
                            f"min-percentage ({min_val}) > max-percentage ({max_val})"
                        )
                except ValueError as e:
                    self.errors.append(f"Invalid percentage value: {e}")

    def _validate_checks(self, root: ET.Element):
        """Validate checks section."""
        checks = root.find(f"{{{REPO_HEALTH_NS}}}checks")
        if checks is None:
            return

        check_ids = set()
        category_refs = set()

        for check_group in checks.findall(f"{{{REPO_HEALTH_NS}}}check-group"):
            cat_ref = check_group.find(f"{{{REPO_HEALTH_NS}}}category-ref")
            if cat_ref is not None and cat_ref.text:
                category_refs.add(cat_ref.text)

            for check in check_group.findall(f"{{{REPO_HEALTH_NS}}}check"):
                # Validate check ID uniqueness
                check_id = check.find(f"{{{REPO_HEALTH_NS}}}id")
                if check_id is not None and check_id.text:
                    if check_id.text in check_ids:
                        self.errors.append(f"Duplicate check ID: {check_id.text}")
                    check_ids.add(check_id.text)

                # Validate check has required fields
                required_check_fields = [
                    "id",
                    "name",
                    "description",
                    "points",
                    "check-type",
                ]
                for field in required_check_fields:
                    elem = check.find(f"{{{REPO_HEALTH_NS}}}{field}")
                    if elem is None:
                        self.errors.append(
                            f"Missing required field '{field}' in check {check_id.text if check_id is not None else 'unknown'}"
                        )

                # Validate points value
                points = check.find(f"{{{REPO_HEALTH_NS}}}points")
                if points is not None:
                    try:
                        int(points.text)
                    except ValueError:
                        self.errors.append(f"Invalid points value: {points.text}")

        # Note: We can't validate category references without loading the full config
        if len(category_refs) == 0:
            self.warnings.append("No category references found in checks")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate repository health XML configuration"
    )
    parser.add_argument(
        "xml_source", help="Path to XML file or URL to validate"
    )
    parser.add_argument(
        "--schema",
        help="Path to XSD schema file (optional)",
        default=None,
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    args = parser.parse_args()

    # Create validator
    schema_path = Path(args.schema) if args.schema else None
    validator = RepoHealthValidator(schema_path=schema_path)

    # Validate XML
    print(f"Validating: {args.xml_source}")
    is_valid, errors, warnings = validator.validate_xml(args.xml_source)

    # Print results
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print("\n✅ Validation successful!")

    if args.verbose:
        print(f"\nSummary:")
        print(f"  Errors: {len(errors)}")
        print(f"  Warnings: {len(warnings)}")

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
