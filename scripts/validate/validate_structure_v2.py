#!/usr/bin/env python3
"""
Repository Structure Validator (XML/JSON Support)

Validates repository structure against XML or JSON schema definitions.
Checks for required files, directories, validates naming conventions, and enforces
requirement statuses (required, suggested, optional, not-allowed).

Supports both XML and JSON schema formats for maximum flexibility.

Usage:
    python3 validate_structure_v2.py [--schema SCHEMA_FILE] [--format xml|json|auto] [--repo-path PATH]

Examples:
    # Auto-detect format from file extension
    python3 validate_structure_v2.py --schema scripts/definitions/default-repository.xml
    python3 validate_structure_v2.py --schema scripts/definitions/default-repository.json
    
    # Explicit format specification
    python3 validate_structure_v2.py --schema my-schema.txt --format json --repo-path /path/to/repo

Exit codes:
    0: Success (all validations passed)
    1: Validation errors found (required items missing or not-allowed items present)
    2: Validation warnings (suggested items missing)
    3: Configuration error (invalid schema, missing files, etc.)
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class RequirementStatus(Enum):
    """Requirement status levels"""
    REQUIRED = "required"
    SUGGESTED = "suggested"
    OPTIONAL = "optional"
    NOT_ALLOWED = "not-allowed"


@dataclass
class ValidationResult:
    """Result of a validation check"""
    severity: Severity
    message: str
    path: str
    requirement_status: Optional[RequirementStatus] = None
    rule_type: Optional[str] = None


class RepositoryStructureValidator:
    """Validates repository structure against XML or JSON definition"""
    
    def __init__(self, schema_path: str, repo_path: str = ".", schema_format: str = "auto"):
        """
        Initialize validator
        
        Args:
            schema_path: Path to schema definition (XML or JSON)
            repo_path: Path to repository to validate (default: current directory)
            schema_format: Format of schema file ('xml', 'json', or 'auto' for auto-detection)
        """
        self.schema_path = schema_path
        self.repo_path = Path(repo_path).resolve()
        self.results: List[ValidationResult] = []
        self.schema_format = schema_format
        self.structure_data = None
        
        # Determine format
        if self.schema_format == "auto":
            self.schema_format = self._detect_format()
        
        # Load schema
        try:
            if self.schema_format == "xml":
                self._load_xml_schema()
            elif self.schema_format == "json":
                self._load_json_schema()
            else:
                raise ValueError(f"Unsupported schema format: {self.schema_format}")
        except Exception as e:
            print(f"Error loading schema: {e}", file=sys.stderr)
            sys.exit(3)
    
    def _detect_format(self) -> str:
        """Auto-detect schema format from file extension"""
        ext = Path(self.schema_path).suffix.lower()
        if ext == ".json":
            return "json"
        elif ext in [".xml", ""]:
            return "xml"
        else:
            # Try to detect from content
            try:
                with open(self.schema_path, 'r') as f:
                    content = f.read().strip()
                    if content.startswith('{') or content.startswith('['):
                        return "json"
                    elif content.startswith('<?xml') or content.startswith('<'):
                        return "xml"
            except Exception:
                pass
            
            # Unable to detect format
            raise ValueError(f"Unable to detect schema format for {self.schema_path}")
    
    def _load_xml_schema(self):
        """Load XML schema"""
        self.tree = ET.parse(self.schema_path)
        self.root = self.tree.getroot()
        self.namespace = {'rs': 'http://mokoconsulting.com/schemas/repository-structure'}
        self.structure_data = self._parse_xml_to_dict()
    
    def _load_json_schema(self):
        """Load JSON schema"""
        with open(self.schema_path, 'r') as f:
            self.structure_data = json.load(f)
    
    def _parse_xml_to_dict(self) -> Dict[str, Any]:
        """Convert XML structure to dictionary format for unified processing"""
        structure = {}
        
        # Parse metadata
        metadata_elem = self.root.find('rs:metadata', self.namespace)
        if metadata_elem is not None:
            structure['metadata'] = {
                'name': self._get_element_text(metadata_elem, 'name'),
                'description': self._get_element_text(metadata_elem, 'description'),
                'repositoryType': self._get_element_text(metadata_elem, 'repository-type'),
                'platform': self._get_element_text(metadata_elem, 'platform'),
            }
        
        # Parse structure
        structure_elem = self.root.find('rs:structure', self.namespace)
        if structure_elem is not None:
            structure['structure'] = {}
            
            # Parse root files
            root_files_elem = structure_elem.find('rs:root-files', self.namespace)
            if root_files_elem is not None:
                structure['structure']['rootFiles'] = []
                for file_elem in root_files_elem.findall('rs:file', self.namespace):
                    structure['structure']['rootFiles'].append(self._parse_xml_file(file_elem))
            
            # Parse directories
            directories_elem = structure_elem.find('rs:directories', self.namespace)
            if directories_elem is not None:
                structure['structure']['directories'] = []
                for dir_elem in directories_elem.findall('rs:directory', self.namespace):
                    structure['structure']['directories'].append(self._parse_xml_directory(dir_elem))
        
        return structure
    
    def _parse_xml_file(self, file_elem) -> Dict[str, Any]:
        """Parse XML file element to dictionary"""
        file_data = {
            'name': self._get_element_text(file_elem, 'name'),
            'description': self._get_element_text(file_elem, 'description'),
            'requirementStatus': self._get_element_text(file_elem, 'requirement-status', 'required'),
            'audience': self._get_element_text(file_elem, 'audience'),
            'template': self._get_element_text(file_elem, 'template'),
        }
        
        # Handle extension attribute
        if 'extension' in file_elem.attrib:
            file_data['extension'] = file_elem.attrib['extension']
        
        return {k: v for k, v in file_data.items() if v is not None}
    
    def _parse_xml_directory(self, dir_elem) -> Dict[str, Any]:
        """Parse XML directory element to dictionary"""
        dir_data = {
            'name': self._get_element_text(dir_elem, 'name'),
            'path': dir_elem.attrib.get('path'),
            'description': self._get_element_text(dir_elem, 'description'),
            'requirementStatus': self._get_element_text(dir_elem, 'requirement-status', 'required'),
            'purpose': self._get_element_text(dir_elem, 'purpose'),
        }
        
        # Parse files within directory
        files_elem = dir_elem.find('rs:files', self.namespace)
        if files_elem is not None:
            dir_data['files'] = []
            for file_elem in files_elem.findall('rs:file', self.namespace):
                dir_data['files'].append(self._parse_xml_file(file_elem))
        
        # Parse subdirectories
        subdirs_elem = dir_elem.find('rs:subdirectories', self.namespace)
        if subdirs_elem is not None:
            dir_data['subdirectories'] = []
            for subdir_elem in subdirs_elem.findall('rs:directory', self.namespace):
                dir_data['subdirectories'].append(self._parse_xml_directory(subdir_elem))
        
        return {k: v for k, v in dir_data.items() if v is not None}
    
    def _get_element_text(self, parent, tag_name, default=None):
        """Get text content of XML element"""
        if self.schema_format == "xml":
            elem = parent.find(f'rs:{tag_name}', self.namespace)
            return elem.text if elem is not None else default
        return default
    
    def validate(self) -> List[ValidationResult]:
        """
        Run all validation checks
        
        Returns:
            List of validation results
        """
        self.results = []
        
        print(f"Validating repository: {self.repo_path}")
        print(f"Against schema: {self.schema_path} (format: {self.schema_format})")
        print("-" * 80)
        
        # Validate root files
        if 'structure' in self.structure_data and 'rootFiles' in self.structure_data['structure']:
            for file_def in self.structure_data['structure']['rootFiles']:
                self._validate_file(file_def, self.repo_path)
        
        # Validate directories
        if 'structure' in self.structure_data and 'directories' in self.structure_data['structure']:
            for dir_def in self.structure_data['structure']['directories']:
                self._validate_directory(dir_def, self.repo_path)
        
        return self.results
    
    def _validate_file(self, file_def: Dict[str, Any], parent_path: Path):
        """Validate a file requirement"""
        file_name = file_def.get('name')
        requirement_status = RequirementStatus(file_def.get('requirementStatus', 'required'))
        file_path = parent_path / file_name
        exists = file_path.exists() and file_path.is_file()
        
        if requirement_status == RequirementStatus.REQUIRED and not exists:
            self.results.append(ValidationResult(
                severity=Severity.ERROR,
                message=f"Required file missing: {file_name}",
                path=str(file_path.relative_to(self.repo_path)),
                requirement_status=requirement_status
            ))
        elif requirement_status == RequirementStatus.SUGGESTED and not exists:
            self.results.append(ValidationResult(
                severity=Severity.WARNING,
                message=f"Suggested file missing: {file_name}",
                path=str(file_path.relative_to(self.repo_path)),
                requirement_status=requirement_status
            ))
        elif requirement_status == RequirementStatus.NOT_ALLOWED and exists:
            self.results.append(ValidationResult(
                severity=Severity.ERROR,
                message=f"Not-allowed file present: {file_name} (should not be committed)",
                path=str(file_path.relative_to(self.repo_path)),
                requirement_status=requirement_status
            ))
        elif exists:
            self.results.append(ValidationResult(
                severity=Severity.INFO,
                message=f"File present: {file_name}",
                path=str(file_path.relative_to(self.repo_path)),
                requirement_status=requirement_status
            ))
    
    def _validate_directory(self, dir_def: Dict[str, Any], parent_path: Path):
        """Validate a directory requirement"""
        dir_name = dir_def.get('name')
        dir_path_str = dir_def.get('path', dir_name)
        requirement_status = RequirementStatus(dir_def.get('requirementStatus', 'required'))
        dir_path = self.repo_path / dir_path_str
        exists = dir_path.exists() and dir_path.is_dir()
        
        if requirement_status == RequirementStatus.REQUIRED and not exists:
            self.results.append(ValidationResult(
                severity=Severity.ERROR,
                message=f"Required directory missing: {dir_name}",
                path=dir_path_str,
                requirement_status=requirement_status
            ))
            return  # Skip validating contents if directory doesn't exist
        elif requirement_status == RequirementStatus.SUGGESTED and not exists:
            self.results.append(ValidationResult(
                severity=Severity.WARNING,
                message=f"Suggested directory missing: {dir_name}",
                path=dir_path_str,
                requirement_status=requirement_status
            ))
            return
        elif requirement_status == RequirementStatus.NOT_ALLOWED and exists:
            self.results.append(ValidationResult(
                severity=Severity.ERROR,
                message=f"Not-allowed directory present: {dir_name} (should not be committed)",
                path=dir_path_str,
                requirement_status=requirement_status
            ))
            return
        elif exists:
            self.results.append(ValidationResult(
                severity=Severity.INFO,
                message=f"Directory present: {dir_name}",
                path=dir_path_str,
                requirement_status=requirement_status
            ))
        
        # Validate files within directory
        if exists and 'files' in dir_def:
            for file_def in dir_def['files']:
                self._validate_file(file_def, dir_path)
        
        # Validate subdirectories
        if exists and 'subdirectories' in dir_def:
            for subdir_def in dir_def['subdirectories']:
                self._validate_directory(subdir_def, dir_path)
    
    def print_results(self):
        """Print validation results"""
        errors = [r for r in self.results if r.severity == Severity.ERROR]
        warnings = [r for r in self.results if r.severity == Severity.WARNING]
        infos = [r for r in self.results if r.severity == Severity.INFO]
        
        print("\n" + "=" * 80)
        print("VALIDATION RESULTS")
        print("=" * 80)
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for result in errors:
                print(f"   {result.path}: {result.message}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for result in warnings:
                print(f"   {result.path}: {result.message}")
        
        if infos:
            print(f"\n✓ INFO ({len(infos)} items validated successfully)")
        
        print("\n" + "=" * 80)
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
        print("=" * 80)
        
        return len(errors), len(warnings)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Validate repository structure against XML or JSON schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--schema',
        default='scripts/definitions/default-repository.xml',
        help='Path to schema file (XML or JSON). Default: scripts/definitions/default-repository.xml'
    )
    parser.add_argument(
        '--format',
        choices=['xml', 'json', 'auto'],
        default='auto',
        help='Schema format (xml, json, or auto-detect). Default: auto'
    )
    parser.add_argument(
        '--repo-path',
        default='.',
        help='Path to repository to validate. Default: current directory'
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = RepositoryStructureValidator(
        schema_path=args.schema,
        repo_path=args.repo_path,
        schema_format=args.format
    )
    
    # Run validation
    validator.validate()
    
    # Print results
    errors, warnings = validator.print_results()
    
    # Exit with appropriate code
    if errors > 0:
        sys.exit(1)  # Errors found
    elif warnings > 0:
        sys.exit(2)  # Only warnings
    else:
        sys.exit(0)  # Success


if __name__ == '__main__':
    main()
