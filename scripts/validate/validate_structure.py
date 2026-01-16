#!/usr/bin/env python3
"""
Repository Structure Validator

Validates a repository against an XML structure definition.
Checks for required files, directories, and validates naming conventions.

Usage:
    python validate_structure.py <structure_xml> [<repo_path>]
    
Examples:
    # Validate current directory against CRM module structure
    python validate_structure.py scripts/definitions/crm-module.xml
    
    # Validate specific directory
    python validate_structure.py scripts/definitions/crm-module.xml /path/to/repo
"""

import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple
import re
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Result of a validation check"""
    severity: Severity
    message: str
    path: str
    rule_type: str = None


class RepositoryStructureValidator:
    """Validates repository structure against XML definition"""
    
    def __init__(self, structure_xml_path: str, repo_path: str = "."):
        """
        Initialize validator
        
        Args:
            structure_xml_path: Path to XML structure definition
            repo_path: Path to repository to validate (default: current directory)
        """
        self.structure_xml_path = structure_xml_path
        self.repo_path = Path(repo_path).resolve()
        self.results: List[ValidationResult] = []
        self.namespace = {'rs': 'http://mokoconsulting.com/schemas/repository-structure'}
        
        # Parse XML structure
        try:
            self.tree = ET.parse(structure_xml_path)
            self.root = self.tree.getroot()
        except Exception as e:
            print(f"Error parsing XML structure: {e}", file=sys.stderr)
            sys.exit(1)
    
    def validate(self) -> List[ValidationResult]:
        """
        Run all validation checks
        
        Returns:
            List of validation results
        """
        self.results = []
        
        print(f"Validating repository: {self.repo_path}")
        print(f"Against structure: {self.structure_xml_path}")
        print("-" * 80)
        
        # Validate metadata
        self._print_metadata()
        
        # Validate root files
        root_files = self.root.find('.//rs:root-files', self.namespace)
        if root_files is not None:
            self._validate_files(root_files, self.repo_path)
        
        # Validate directories
        directories = self.root.find('.//rs:directories', self.namespace)
        if directories is not None:
            self._validate_directories(directories, self.repo_path)
        
        return self.results
    
    def _print_metadata(self):
        """Print structure metadata"""
        metadata = self.root.find('.//rs:metadata', self.namespace)
        if metadata is not None:
            name = metadata.find('rs:name', self.namespace)
            desc = metadata.find('rs:description', self.namespace)
            repo_type = metadata.find('rs:repository-type', self.namespace)
            platform = metadata.find('rs:platform', self.namespace)
            
            if name is not None:
                print(f"Structure: {name.text}")
            if desc is not None:
                print(f"Description: {desc.text}")
            if repo_type is not None:
                print(f"Type: {repo_type.text}")
            if platform is not None:
                print(f"Platform: {platform.text}")
            print("-" * 80)
    
    def _validate_files(self, files_element: ET.Element, base_path: Path):
        """Validate files in a given location"""
        for file_elem in files_element.findall('rs:file', self.namespace):
            name = file_elem.find('rs:name', self.namespace)
            required = file_elem.find('rs:required', self.namespace)
            description = file_elem.find('rs:description', self.namespace)
            
            if name is None:
                continue
            
            file_name = name.text
            is_required = required is not None and required.text.lower() == 'true'
            file_path = base_path / file_name
            
            # Check if file exists
            if not file_path.exists():
                if is_required:
                    self.results.append(ValidationResult(
                        severity=Severity.ERROR,
                        message=f"Required file missing: {file_name}",
                        path=str(file_path.relative_to(self.repo_path)),
                        rule_type="file-exists"
                    ))
                else:
                    self.results.append(ValidationResult(
                        severity=Severity.INFO,
                        message=f"Optional file missing: {file_name}",
                        path=str(file_path.relative_to(self.repo_path)),
                        rule_type="file-exists"
                    ))
            else:
                # File exists - validate rules if any
                validation_rules = file_elem.find('rs:validation-rules', self.namespace)
                if validation_rules is not None:
                    self._validate_rules(validation_rules, file_path)
    
    def _validate_directories(self, directories_element: ET.Element, base_path: Path):
        """Validate directories in a given location"""
        for dir_elem in directories_element.findall('rs:directory', self.namespace):
            name = dir_elem.find('rs:name', self.namespace)
            required = dir_elem.find('rs:required', self.namespace)
            path_attr = dir_elem.get('path')
            
            if name is None:
                continue
            
            dir_name = name.text
            is_required = required is not None and required.text.lower() == 'true'
            
            # Use path attribute if specified, otherwise use name
            dir_path = base_path / (path_attr if path_attr else dir_name)
            
            # Check if directory exists
            if not dir_path.exists():
                if is_required:
                    self.results.append(ValidationResult(
                        severity=Severity.ERROR,
                        message=f"Required directory missing: {dir_name}",
                        path=str(dir_path.relative_to(self.repo_path)),
                        rule_type="directory-exists"
                    ))
                else:
                    self.results.append(ValidationResult(
                        severity=Severity.INFO,
                        message=f"Optional directory missing: {dir_name}",
                        path=str(dir_path.relative_to(self.repo_path)),
                        rule_type="directory-exists"
                    ))
            elif not dir_path.is_dir():
                self.results.append(ValidationResult(
                    severity=Severity.ERROR,
                    message=f"Path exists but is not a directory: {dir_name}",
                    path=str(dir_path.relative_to(self.repo_path)),
                    rule_type="directory-exists"
                ))
            else:
                # Directory exists - validate its contents
                files = dir_elem.find('rs:files', self.namespace)
                if files is not None:
                    self._validate_files(files, dir_path)
                
                # Validate subdirectories
                subdirs = dir_elem.find('rs:subdirectories', self.namespace)
                if subdirs is not None:
                    self._validate_directories(subdirs, dir_path)
                
                # Validate directory rules
                validation_rules = dir_elem.find('rs:validation-rules', self.namespace)
                if validation_rules is not None:
                    self._validate_rules(validation_rules, dir_path)
    
    def _validate_rules(self, rules_element: ET.Element, path: Path):
        """Validate specific rules for a file or directory"""
        for rule_elem in rules_element.findall('rs:rule', self.namespace):
            rule_type = rule_elem.find('rs:type', self.namespace)
            description = rule_elem.find('rs:description', self.namespace)
            pattern = rule_elem.find('rs:pattern', self.namespace)
            severity = rule_elem.find('rs:severity', self.namespace)
            
            if rule_type is None:
                continue
            
            severity_level = Severity(severity.text) if severity is not None else Severity.WARNING
            rule_type_text = rule_type.text
            
            # Implement different rule types
            if rule_type_text == 'naming-convention' and pattern is not None:
                if not re.match(pattern.text, path.name):
                    self.results.append(ValidationResult(
                        severity=severity_level,
                        message=f"Naming convention violation: {description.text if description is not None else 'Pattern: ' + pattern.text}",
                        path=str(path.relative_to(self.repo_path)),
                        rule_type=rule_type_text
                    ))
            
            elif rule_type_text == 'content-pattern' and pattern is not None:
                if path.is_file():
                    try:
                        content = path.read_text()
                        if not re.search(pattern.text, content):
                            self.results.append(ValidationResult(
                                severity=severity_level,
                                message=f"Content pattern not found: {description.text if description is not None else 'Pattern: ' + pattern.text}",
                                path=str(path.relative_to(self.repo_path)),
                                rule_type=rule_type_text
                            ))
                    except Exception as e:
                        self.results.append(ValidationResult(
                            severity=Severity.WARNING,
                            message=f"Could not read file for content validation: {e}",
                            path=str(path.relative_to(self.repo_path)),
                            rule_type=rule_type_text
                        ))
            
            elif rule_type_text == 'min-size' and pattern is not None:
                if path.is_file():
                    file_size = path.stat().st_size
                    min_size = int(pattern.text)
                    if file_size < min_size:
                        self.results.append(ValidationResult(
                            severity=severity_level,
                            message=f"File too small: {file_size} bytes < {min_size} bytes minimum",
                            path=str(path.relative_to(self.repo_path)),
                            rule_type=rule_type_text
                        ))
    
    def print_results(self):
        """Print validation results"""
        # Count by severity
        errors = [r for r in self.results if r.severity == Severity.ERROR]
        warnings = [r for r in self.results if r.severity == Severity.WARNING]
        info = [r for r in self.results if r.severity == Severity.INFO]
        
        print("\n" + "=" * 80)
        print("VALIDATION RESULTS")
        print("=" * 80)
        
        # Print errors
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            print("-" * 80)
            for result in errors:
                print(f"  {result.path}")
                print(f"    {result.message}")
                if result.rule_type:
                    print(f"    Rule: {result.rule_type}")
                print()
        
        # Print warnings
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            print("-" * 80)
            for result in warnings:
                print(f"  {result.path}")
                print(f"    {result.message}")
                if result.rule_type:
                    print(f"    Rule: {result.rule_type}")
                print()
        
        # Print info
        if info:
            print(f"\nℹ️  INFO ({len(info)}):")
            print("-" * 80)
            for result in info:
                print(f"  {result.path}")
                print(f"    {result.message}")
                print()
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total issues: {len(self.results)}")
        print(f"  Errors:   {len(errors)}")
        print(f"  Warnings: {len(warnings)}")
        print(f"  Info:     {len(info)}")
        
        if errors:
            print("\n❌ Validation FAILED - please fix errors")
            return 1
        elif warnings:
            print("\n⚠️  Validation PASSED with warnings")
            return 0
        else:
            print("\n✅ Validation PASSED")
            return 0


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate_structure.py <structure_xml> [<repo_path>]", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python validate_structure.py scripts/definitions/crm-module.xml", file=sys.stderr)
        print("  python validate_structure.py scripts/definitions/crm-module.xml /path/to/repo", file=sys.stderr)
        sys.exit(1)
    
    structure_xml = sys.argv[1]
    repo_path = sys.argv[2] if len(sys.argv) > 2 else "."
    
    if not os.path.exists(structure_xml):
        print(f"Error: Structure XML not found: {structure_xml}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path not found: {repo_path}", file=sys.stderr)
        sys.exit(1)
    
    # Run validation
    validator = RepositoryStructureValidator(structure_xml, repo_path)
    validator.validate()
    exit_code = validator.print_results()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
