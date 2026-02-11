#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Validation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/validate/schema_aware_health_check.py
VERSION: 03.02.00
BRIEF: Schema-aware repository health checker that uses repository structure schema

DESCRIPTION:
    This script performs repository health checks guided by the repository
    structure schema. It validates that repositories meet both structural
    requirements (from repository-structure.schema.json) and health standards
    (from repo-health.xsd), providing a unified health assessment.

USAGE:
    # Run health check using schema
    python3 scripts/validate/schema_aware_health_check.py

    # Use custom schema
    python3 scripts/validate/schema_aware_health_check.py \
        --schema scripts/definitions/default-repository.xml

    # Output as JSON
    python3 scripts/validate/schema_aware_health_check.py --format json

    # Detailed report
    python3 scripts/validate/schema_aware_health_check.py --verbose

EXAMPLES:
    # Basic health check
    python3 scripts/validate/schema_aware_health_check.py

    # Check specific repository type
    python3 scripts/validate/schema_aware_health_check.py \
        --schema scripts/definitions/crm-module.xml

    # Generate report
    python3 scripts/validate/schema_aware_health_check.py \
        --format json --output health-report.json
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    check_id: str
    category: str
    name: str
    status: str  # 'pass', 'fail', 'warning', 'info'
    message: str
    points: int = 0
    max_points: int = 0
    details: Dict = field(default_factory=dict)


@dataclass
class CategoryScore:
    """Score for a category of health checks."""
    category_id: str
    category_name: str
    points: int
    max_points: int
    checks: List[HealthCheckResult] = field(default_factory=list)

    @property
    def percentage(self) -> float:
        """Calculate percentage score."""
        if self.max_points == 0:
            return 100.0
        return (self.points / self.max_points) * 100.0


@dataclass
class HealthReport:
    """Complete health report for a repository."""
    total_points: int
    max_points: int
    percentage: float
    health_level: str
    categories: List[CategoryScore]
    summary: Dict
    timestamp: str


class SchemaAwareHealthChecker:
    """Schema-aware repository health checker."""

    def __init__(
        self,
        repo_path: str = ".",
        schema_path: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize the health checker.

        Args:
            repo_path: Path to repository to check
            schema_path: Path to structure schema XML file
            verbose: Enable verbose output
        """
        self.repo_path = Path(repo_path).resolve()
        self.schema_path = schema_path
        self.verbose = verbose
        self.results: List[HealthCheckResult] = []

    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            prefix = {"INFO": "ℹ", "WARNING": "⚠", "ERROR": "✗", "SUCCESS": "✓"}.get(level, "•")
            print(f"{prefix} {message}")

    def load_structure_schema(self) -> Optional[ET.Element]:
        """
        Load repository structure schema from XML file.

        Returns:
            XML root element or None if not found
        """
        if not self.schema_path:
            # Try to find default schema
            possible_paths = [
                "scripts/definitions/default-repository.xml",
                "../scripts/definitions/default-repository.xml",
            ]
            for path in possible_paths:
                schema_file = self.repo_path / path
                if schema_file.exists():
                    self.schema_path = str(schema_file)
                    break

        if not self.schema_path:
            self.log("No structure schema found, using basic checks only", "WARNING")
            return None

        try:
            # Disable external entity processing to prevent XXE attacks
            parser = ET.XMLParser()
            parser.entity = {}  # Disable entity expansion
            tree = ET.parse(self.schema_path, parser=parser)
            self.log(f"Loaded structure schema: {self.schema_path}", "SUCCESS")
            return tree.getroot()
        except Exception as e:
            self.log(f"Failed to load schema: {e}", "ERROR")
            return None

    def check_required_files(self, schema_root: Optional[ET.Element]) -> List[HealthCheckResult]:
        """
        Check for required files from schema.

        Args:
            schema_root: XML schema root element

        Returns:
            List of health check results
        """
        results = []

        if schema_root is None:
            # Fallback to basic required files
            required_files = [
                ("README.md", "Project documentation"),
                ("LICENSE", "License file"),
                ("CHANGELOG.md", "Change log"),
                ("CONTRIBUTING.md", "Contribution guidelines"),
            ]
        else:
            # Extract required files from schema
            required_files = self._extract_required_files_from_schema(schema_root)

        for file_name, description in required_files:
            file_path = self.repo_path / file_name

            if file_path.exists():
                results.append(HealthCheckResult(
                    check_id=f"file_{file_name.replace('.', '_').replace('/', '_')}",
                    category="documentation",
                    name=f"Required file: {file_name}",
                    status="pass",
                    message=f"✓ {file_name} exists",
                    points=10,
                    max_points=10,
                    details={"file": file_name, "description": description}
                ))
            else:
                results.append(HealthCheckResult(
                    check_id=f"file_{file_name.replace('.', '_').replace('/', '_')}",
                    category="documentation",
                    name=f"Required file: {file_name}",
                    status="fail",
                    message=f"✗ {file_name} missing",
                    points=0,
                    max_points=10,
                    details={"file": file_name, "description": description}
                ))

        return results

    def check_required_directories(self, schema_root: Optional[ET.Element]) -> List[HealthCheckResult]:
        """
        Check for required directories from schema.

        Args:
            schema_root: XML schema root element

        Returns:
            List of health check results
        """
        results = []

        if schema_root is None:
            # Fallback to basic required directories
            required_dirs = [
                ("docs", "Documentation directory"),
                ("scripts", "Scripts directory"),
            ]
        else:
            # Extract required directories from schema
            required_dirs = self._extract_required_directories_from_schema(schema_root)

        for dir_name, description in required_dirs:
            dir_path = self.repo_path / dir_name

            if dir_path.exists() and dir_path.is_dir():
                results.append(HealthCheckResult(
                    check_id=f"dir_{dir_name.replace('/', '_')}",
                    category="structure",
                    name=f"Required directory: {dir_name}",
                    status="pass",
                    message=f"✓ {dir_name}/ exists",
                    points=5,
                    max_points=5,
                    details={"directory": dir_name, "description": description}
                ))
            else:
                results.append(HealthCheckResult(
                    check_id=f"dir_{dir_name.replace('/', '_')}",
                    category="structure",
                    name=f"Required directory: {dir_name}",
                    status="fail",
                    message=f"✗ {dir_name}/ missing",
                    points=0,
                    max_points=5,
                    details={"directory": dir_name, "description": description}
                ))

        return results

    def check_installation_doc(self) -> HealthCheckResult:
        """Check for INSTALLATION.md in docs."""
        install_path = self.repo_path / "docs" / "INSTALLATION.md"

        if install_path.exists():
            # Check file size (should be substantial)
            size = install_path.stat().st_size
            if size > 500:  # At least 500 bytes
                return HealthCheckResult(
                    check_id="installation_doc",
                    category="documentation",
                    name="Installation documentation",
                    status="pass",
                    message="✓ docs/INSTALLATION.md exists and is substantial",
                    points=15,
                    max_points=15,
                    details={"file": "docs/INSTALLATION.md", "size": size}
                )
            else:
                return HealthCheckResult(
                    check_id="installation_doc",
                    category="documentation",
                    name="Installation documentation",
                    status="warning",
                    message="⚠ docs/INSTALLATION.md exists but is too short",
                    points=5,
                    max_points=15,
                    details={"file": "docs/INSTALLATION.md", "size": size}
                )
        else:
            return HealthCheckResult(
                check_id="installation_doc",
                category="documentation",
                name="Installation documentation",
                status="fail",
                message="✗ docs/INSTALLATION.md missing (required)",
                points=0,
                max_points=15,
                details={"file": "docs/INSTALLATION.md"}
            )

    def check_core_structure_compliance(self) -> List[HealthCheckResult]:
        """Check compliance with CORE_STRUCTURE.md requirements."""
        results = []

        # Check docs structure
        docs_dir = self.repo_path / "docs"
        if docs_dir.exists():
            required_docs_files = [
                ("index.md", "Documentation catalog", 5),
                ("INSTALLATION.md", "Installation guide", 15),
                ("README.md", "Documentation overview", 5),
            ]

            for file_name, desc, points in required_docs_files:
                file_path = docs_dir / file_name
                if file_path.exists():
                    results.append(HealthCheckResult(
                        check_id=f"core_structure_docs_{file_name.replace('.', '_')}",
                        category="structure",
                        name=f"Core structure: docs/{file_name}",
                        status="pass",
                        message=f"✓ docs/{file_name} present",
                        points=points,
                        max_points=points
                    ))
                else:
                    results.append(HealthCheckResult(
                        check_id=f"core_structure_docs_{file_name.replace('.', '_')}",
                        category="structure",
                        name=f"Core structure: docs/{file_name}",
                        status="fail",
                        message=f"✗ docs/{file_name} missing",
                        points=0,
                        max_points=points
                    ))

        # Check scripts structure (if scripts exist)
        scripts_dir = self.repo_path / "scripts"
        if scripts_dir.exists():
            required_scripts_files = [
                ("README.md", "Scripts overview", 5),
                ("index.md", "Scripts catalog", 5),
            ]

            for file_name, desc, points in required_scripts_files:
                file_path = scripts_dir / file_name
                if file_path.exists():
                    results.append(HealthCheckResult(
                        check_id=f"core_structure_scripts_{file_name.replace('.', '_')}",
                        category="structure",
                        name=f"Core structure: scripts/{file_name}",
                        status="pass",
                        message=f"✓ scripts/{file_name} present",
                        points=points,
                        max_points=points
                    ))
                else:
                    results.append(HealthCheckResult(
                        check_id=f"core_structure_scripts_{file_name.replace('.', '_')}",
                        category="structure",
                        name=f"Core structure: scripts/{file_name}",
                        status="fail",
                        message=f"✗ scripts/{file_name} missing",
                        points=0,
                        max_points=points
                    ))

        return results

    def _extract_required_files_from_schema(self, schema_root: ET.Element) -> List[Tuple[str, str]]:
        """Extract required files from XML schema."""
        required_files = []
        ns = {'ns': 'http://mokoconsulting.com/schemas/repository-structure'}

        # Extract from root-files
        for file_elem in schema_root.findall('.//ns:root-files/ns:file', ns):
            req_status = file_elem.find('ns:requirement-status', ns)
            if req_status is not None and req_status.text == 'required':
                name_elem = file_elem.find('ns:name', ns)
                desc_elem = file_elem.find('ns:description', ns)
                if name_elem is not None:
                    name = name_elem.text
                    desc = desc_elem.text if desc_elem is not None else ""
                    required_files.append((name, desc))

        return required_files

    def _extract_required_directories_from_schema(self, schema_root: ET.Element) -> List[Tuple[str, str]]:
        """Extract required directories from XML schema."""
        required_dirs = []
        ns = {'ns': 'http://mokoconsulting.com/schemas/repository-structure'}

        # Extract from directories
        for dir_elem in schema_root.findall('.//ns:directories/ns:directory', ns):
            req_status = dir_elem.find('ns:requirement-status', ns)
            if req_status is not None and req_status.text == 'required':
                name_elem = dir_elem.find('ns:name', ns)
                desc_elem = dir_elem.find('ns:description', ns)
                if name_elem is not None:
                    name = name_elem.text
                    desc = desc_elem.text if desc_elem is not None else ""
                    required_dirs.append((name, desc))

        return required_dirs

    def run_all_checks(self) -> HealthReport:
        """
        Run all health checks.

        Returns:
            Complete health report
        """
        self.log("Starting schema-aware health checks...", "INFO")

        # Load structure schema
        schema_root = self.load_structure_schema()

        # Run checks
        all_results = []

        # Schema-based checks
        all_results.extend(self.check_required_files(schema_root))
        all_results.extend(self.check_required_directories(schema_root))

        # Core structure checks
        all_results.append(self.check_installation_doc())
        all_results.extend(self.check_core_structure_compliance())

        # Calculate scores by category
        categories = {}
        for result in all_results:
            if result.category not in categories:
                categories[result.category] = CategoryScore(
                    category_id=result.category,
                    category_name=result.category.title(),
                    points=0,
                    max_points=0
                )

            cat = categories[result.category]
            cat.points += result.points
            cat.max_points += result.max_points
            cat.checks.append(result)

        # Calculate totals
        total_points = sum(cat.points for cat in categories.values())
        max_points = sum(cat.max_points for cat in categories.values())
        percentage = (total_points / max_points * 100) if max_points > 0 else 0

        # Determine health level
        if percentage >= 90:
            health_level = "excellent"
        elif percentage >= 70:
            health_level = "good"
        elif percentage >= 50:
            health_level = "fair"
        else:
            health_level = "poor"

        # Generate summary
        summary = {
            "passed": sum(1 for r in all_results if r.status == "pass"),
            "failed": sum(1 for r in all_results if r.status == "fail"),
            "warnings": sum(1 for r in all_results if r.status == "warning"),
            "total_checks": len(all_results),
        }

        import datetime
        return HealthReport(
            total_points=total_points,
            max_points=max_points,
            percentage=percentage,
            health_level=health_level,
            categories=list(categories.values()),
            summary=summary,
            timestamp=datetime.datetime.now().isoformat()
        )

    def format_report(self, report: HealthReport, format: str = "text") -> str:
        """
        Format health report for output.

        Args:
            report: Health report to format
            format: Output format ('text' or 'json')

        Returns:
            Formatted report string
        """
        if format == "json":
            return json.dumps({
                "total_points": report.total_points,
                "max_points": report.max_points,
                "percentage": round(report.percentage, 2),
                "health_level": report.health_level,
                "summary": report.summary,
                "categories": [
                    {
                        "id": cat.category_id,
                        "name": cat.category_name,
                        "points": cat.points,
                        "max_points": cat.max_points,
                        "percentage": round(cat.percentage, 2),
                        "checks": [
                            {
                                "id": check.check_id,
                                "name": check.name,
                                "status": check.status,
                                "message": check.message,
                                "points": check.points,
                                "max_points": check.max_points,
                            }
                            for check in cat.checks
                        ]
                    }
                    for cat in report.categories
                ],
                "timestamp": report.timestamp
            }, indent=2)

        # Text format
        lines = []
        lines.append("=" * 70)
        lines.append("Repository Health Report (Schema-Aware)")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Score: {report.total_points}/{report.max_points} ({report.percentage:.1f}%)")
        lines.append(f"Health Level: {report.health_level.upper()}")
        lines.append("")
        lines.append(f"Summary:")
        lines.append(f"  ✓ Passed: {report.summary['passed']}")
        lines.append(f"  ✗ Failed: {report.summary['failed']}")
        lines.append(f"  ⚠ Warnings: {report.summary['warnings']}")
        lines.append(f"  Total Checks: {report.summary['total_checks']}")
        lines.append("")
        lines.append("-" * 70)

        for category in report.categories:
            lines.append(f"\n{category.category_name} ({category.points}/{category.max_points} - {category.percentage:.1f}%)")
            lines.append("-" * 70)
            for check in category.checks:
                status_icon = {"pass": "✓", "fail": "✗", "warning": "⚠", "info": "ℹ"}.get(check.status, "•")
                lines.append(f"  {status_icon} {check.message}")

        lines.append("")
        lines.append("=" * 70)
        lines.append(f"Timestamp: {report.timestamp}")
        lines.append("=" * 70)

        return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Schema-aware repository health checker",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--repo",
        default=".",
        help="Repository path (default: current directory)"
    )

    parser.add_argument(
        "--schema",
        help="Path to structure schema XML file"
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--output",
        help="Output file (default: stdout)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    try:
        checker = SchemaAwareHealthChecker(
            repo_path=args.repo,
            schema_path=args.schema,
            verbose=args.verbose
        )

        report = checker.run_all_checks()
        output = checker.format_report(report, format=args.format)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"✓ Report written to {args.output}")
        else:
            print(output)

        # Exit with error if health is poor
        if report.health_level == "poor":
            return 1

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
