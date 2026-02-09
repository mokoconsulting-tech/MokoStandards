#!/usr/bin/env python3
"""
Terraform Drift Validator

Validates that Terraform configuration stays in sync with Python implementations.
Checks for drift between repo health check types defined in Terraform and
implemented in Python code.

Usage:
    python3 validate_terraform_drift.py [--strict]

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2026 Moko Consulting LLC
    LICENSE: GPL-3.0-or-later
    VERSION: 03.01.02
    CREATED: 2026-02-02
    UPDATED: 2026-02-02
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class TerraformDriftValidator:
    """Validates Terraform configuration against Python implementation."""
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        
    def log(self, message: str, level: str = 'INFO'):
        """Log message with level."""
        if level == 'ERROR':
            self.errors.append(message)
            print(f"❌ {message}")
        elif level == 'WARNING':
            self.warnings.append(message)
            print(f"⚠️  {message}")
        elif self.verbose:
            print(f"ℹ️  {message}")
    
    def extract_check_types_from_terraform(self) -> Dict[str, List[Dict]]:
        """Extract check types from Terraform configuration."""
        tf_file = self.repo_root / 'terraform' / 'repository-types' / 'repo-health-defaults.tf'
        
        if not tf_file.exists():
            self.log(f"Terraform file not found: {tf_file}", 'ERROR')
            return {}
        
        with open(tf_file, 'r') as f:
            content = f.read()
        
        # Extract check types
        check_types = {}
        pattern = r'check_type\s*=\s*"([^"]+)"'
        matches = re.findall(pattern, content)
        
        for check_type in matches:
            if check_type not in check_types:
                check_types[check_type] = []
        
        # Extract detailed check information
        check_pattern = r'(\w+)\s*=\s*{\s*id\s*=\s*"([^"]+)".*?check_type\s*=\s*"([^"]+)".*?points\s*=\s*(\d+).*?category\s*=\s*"([^"]+)"'
        detailed_matches = re.findall(check_pattern, content, re.DOTALL)
        
        for name, check_id, check_type, points, category in detailed_matches:
            check_types.setdefault(check_type, []).append({
                'name': name,
                'id': check_id,
                'points': int(points),
                'category': category
            })
        
        return check_types
    
    def extract_check_types_from_python(self) -> Set[str]:
        """Extract implemented check types from Python code."""
        py_file = self.repo_root / 'scripts' / 'validate' / 'check_repo_health.py'
        
        if not py_file.exists():
            self.log(f"Python file not found: {py_file}", 'ERROR')
            return set()
        
        with open(py_file, 'r') as f:
            content = f.read()
        
        # Find all check type handlers
        check_types = set()
        pattern = r'elif check_type == "([^"]+)":'
        matches = re.findall(pattern, content)
        check_types.update(matches)
        
        # Also check if statements
        pattern = r'if check_type == "([^"]+)":'
        matches = re.findall(pattern, content)
        check_types.update(matches)
        
        return check_types
    
    def validate_check_types(self) -> bool:
        """Validate that all Terraform check types are implemented in Python."""
        tf_checks = self.extract_check_types_from_terraform()
        py_checks = self.extract_check_types_from_python()
        
        self.log(f"Terraform defines {len(tf_checks)} check types")
        self.log(f"Python implements {len(py_checks)} check types")
        
        all_valid = True
        
        # Check for missing implementations
        for check_type in tf_checks.keys():
            if check_type not in py_checks:
                self.log(f"Check type '{check_type}' defined in Terraform but not implemented in Python", 'ERROR')
                all_valid = False
            else:
                self.log(f"Check type '{check_type}' verified ({len(tf_checks[check_type])} instances)")
        
        # Check for unused implementations
        for check_type in py_checks:
            if check_type not in tf_checks:
                self.log(f"Check type '{check_type}' implemented in Python but not used in Terraform", 'WARNING')
        
        return all_valid
    
    def validate_category_points(self) -> bool:
        """Validate that category points match sum of check points."""
        tf_file = self.repo_root / 'terraform' / 'repository-types' / 'repo-health-defaults.tf'
        
        with open(tf_file, 'r') as f:
            content = f.read()
        
        # Extract categories with max_points
        categories = {}
        cat_pattern = r'(\w+)\s*=\s*{[^}]*id\s*=\s*"([^"]+)"[^}]*max_points\s*=\s*(\d+)'
        for match in re.finditer(cat_pattern, content, re.DOTALL):
            cat_name, cat_id, max_points = match.groups()
            categories[cat_id] = {
                'name': cat_name,
                'max_points': int(max_points),
                'actual_points': 0
            }
        
        # Sum up points by category
        check_pattern = r'check_type\s*=\s*"([^"]+)".*?points\s*=\s*(\d+).*?category\s*=\s*"([^"]+)"'
        for match in re.finditer(check_pattern, content, re.DOTALL):
            check_type, points, category = match.groups()
            if category in categories:
                categories[category]['actual_points'] += int(points)
        
        # Validate
        all_valid = True
        for cat_id, cat_info in categories.items():
            max_pts = cat_info['max_points']
            actual_pts = cat_info['actual_points']
            
            if actual_pts > max_pts:
                self.log(f"Category '{cat_id}': sum of check points ({actual_pts}) exceeds max_points ({max_pts})", 'ERROR')
                all_valid = False
            elif actual_pts < max_pts:
                self.log(f"Category '{cat_id}': sum of check points ({actual_pts}) is less than max_points ({max_pts}) - {max_pts - actual_pts} points remaining", 'WARNING')
            else:
                self.log(f"Category '{cat_id}': points match perfectly ({actual_pts}/{max_pts})")
        
        return all_valid
    
    def validate_total_points(self) -> bool:
        """Validate total_points calculation."""
        tf_file = self.repo_root / 'terraform' / 'repository-types' / 'repo-health-defaults.tf'
        
        with open(tf_file, 'r') as f:
            content = f.read()
        
        # Get declared total_points
        total_match = re.search(r'total_points\s*=\s*(\d+)', content)
        if not total_match:
            self.log("Could not find total_points in Terraform", 'ERROR')
            return False
        
        declared_total = int(total_match.group(1))
        
        # Calculate actual total from categories
        cat_pattern = r'max_points\s*=\s*(\d+)'
        category_points = [int(m) for m in re.findall(cat_pattern, content)]
        calculated_total = sum(category_points)
        
        self.log(f"Declared total_points: {declared_total}")
        self.log(f"Calculated from categories: {calculated_total}")
        
        if declared_total != calculated_total:
            self.log(f"Total points mismatch: declared {declared_total} vs calculated {calculated_total}", 'ERROR')
            return False
        
        self.log(f"Total points validated: {declared_total}")
        return True
    
    def validate_parameters(self) -> bool:
        """Validate that check parameters match between Terraform and Python."""
        tf_file = self.repo_root / 'terraform' / 'repository-types' / 'repo-health-defaults.tf'
        py_file = self.repo_root / 'scripts' / 'validate' / 'check_repo_health.py'
        
        with open(tf_file, 'r') as f:
            tf_content = f.read()
        
        with open(py_file, 'r') as f:
            py_content = f.read()
        
        # Check security-scan parameters
        if 'security-scan' in tf_content:
            if 'max_severity' in tf_content and 'max_severity' in py_content:
                self.log("security-scan: max_severity parameter validated")
            else:
                self.log("security-scan: max_severity parameter mismatch", 'ERROR')
                return False
        
        # Check script-integrity parameters
        if 'script-integrity' in tf_content:
            if 'priority' in tf_content and 'priority' in py_content:
                self.log("script-integrity: priority parameter validated")
            else:
                self.log("script-integrity: priority parameter mismatch", 'ERROR')
                return False
        
        return True
    
    def validate_all(self) -> bool:
        """Run all validations."""
        print("=" * 70)
        print("🔍 Terraform Drift Validation")
        print("=" * 70)
        print()
        
        results = []
        
        print("1️⃣  Validating check type implementations...")
        results.append(self.validate_check_types())
        print()
        
        print("2️⃣  Validating category points...")
        results.append(self.validate_category_points())
        print()
        
        print("3️⃣  Validating total points...")
        results.append(self.validate_total_points())
        print()
        
        print("4️⃣  Validating parameters...")
        results.append(self.validate_parameters())
        print()
        
        # Summary
        print("=" * 70)
        print("📊 Validation Summary")
        print("=" * 70)
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()
        
        all_passed = all(results)
        
        if all_passed and not self.errors:
            print("✅ All validations passed - Terraform is in sync!")
            return True
        else:
            print("❌ Validation failed - Terraform drift detected!")
            return False


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Validate Terraform configuration against Python implementation'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on warnings as well as errors'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent.parent
    validator = TerraformDriftValidator(repo_root, verbose=args.verbose)
    
    success = validator.validate_all()
    
    if not success:
        return 1
    
    if args.strict and validator.warnings:
        print("\n⚠️  Strict mode: failing due to warnings")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
