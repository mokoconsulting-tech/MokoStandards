#!/usr/bin/env python3
"""
Repository Structure Validator (Terraform-based)

Validates a repository against Terraform-based structure definitions.
This replaces the deprecated XML-based validator.

Usage:
    python validate_structure_terraform.py [<repo_path>] [--repo-type <type>]
    
Examples:
    # Validate current directory against default structure
    python validate_structure_terraform.py
    
    # Validate specific directory
    python validate_structure_terraform.py /path/to/repo
    
    # Validate with specific repository type
    python validate_structure_terraform.py . --repo-type library
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Import Terraform schema reader
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from terraform_schema_reader import TerraformSchemaReader


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
    requirement_status: str = None


class TerraformRepositoryStructureValidator:
    """Validates repository structure against Terraform definition"""
    
    def __init__(self, repo_path: str = ".", repo_type: str = "default"):
        """
        Initialize validator
        
        Args:
            repo_path: Path to repository to validate (default: current directory)
            repo_type: Repository type to validate against (default: "default")
        """
        self.repo_path = Path(repo_path).resolve()
        self.repo_type = repo_type
        self.results: List[ValidationResult] = []
        self.reader = TerraformSchemaReader()
        
        # Load structure from Terraform
        try:
            self.structure = self.reader.get_repository_structure(repo_type)
        except Exception as e:
            print(f"Error loading Terraform structure: {e}", file=sys.stderr)
            print("Make sure Terraform is initialized in terraform/ directory", file=sys.stderr)
            sys.exit(1)
    
    def validate(self) -> List[ValidationResult]:
        """
        Run all validation checks
        
        Returns:
            List of validation results
        """
        self.results = []
        
        print(f"Validating repository: {self.repo_path}")
        print(f"Against structure type: {self.repo_type}")
        print("-" * 80)
        
        # Print metadata
        self._print_metadata()
        
        # Validate root files
        root_files = self.structure.get('root_files', {})
        if root_files:
            self._validate_root_files(root_files)
        
        # Validate directories
        directories = self.structure.get('directories', {})
        if directories:
            self._validate_directories(directories)
        
        return self.results
    
    def _print_metadata(self):
        """Print structure metadata"""
        metadata = self.structure.get('metadata', {})
        if metadata:
            print(f"\nRepository Type: {metadata.get('name', 'Unknown')}")
            print(f"Platform: {metadata.get('platform', 'Unknown')}")
            print(f"Description: {metadata.get('description', 'N/A')}")
            print()
    
    def _validate_root_files(self, root_files: Dict):
        """Validate root-level files"""
        print("Validating root files...")
        
        for file_key, file_info in root_files.items():
            file_name = file_info.get('name')
            requirement_status = file_info.get('requirement_status', 'optional')
            description = file_info.get('description', '')
            
            file_path = self.repo_path / file_name
            
            if requirement_status == 'required':
                if not file_path.exists():
                    self.results.append(ValidationResult(
                        severity=Severity.ERROR,
                        message=f"Required file missing: {file_name} - {description}",
                        path=file_name,
                        requirement_status=requirement_status
                    ))
                    print(f"  ❌ {file_name} - MISSING (required)")
                else:
                    print(f"  ✅ {file_name} - OK")
            
            elif requirement_status == 'suggested':
                if not file_path.exists():
                    self.results.append(ValidationResult(
                        severity=Severity.WARNING,
                        message=f"Suggested file missing: {file_name} - {description}",
                        path=file_name,
                        requirement_status=requirement_status
                    ))
                    print(f"  ⚠️  {file_name} - MISSING (suggested)")
                else:
                    print(f"  ✅ {file_name} - OK")
            
            elif requirement_status == 'optional':
                if file_path.exists():
                    print(f"  ✅ {file_name} - OK (optional)")
                else:
                    print(f"  ℹ️  {file_name} - Not present (optional)")
        
        print()
    
    def _validate_directories(self, directories: Dict):
        """Validate directory structure"""
        print("Validating directories...")
        
        for dir_key, dir_info in directories.items():
            dir_name = dir_info.get('name')
            dir_path_str = dir_info.get('path', dir_name)
            requirement_status = dir_info.get('requirement_status', 'optional')
            description = dir_info.get('description', '')
            
            dir_path = self.repo_path / dir_path_str
            
            if requirement_status == 'required':
                if not dir_path.exists():
                    self.results.append(ValidationResult(
                        severity=Severity.ERROR,
                        message=f"Required directory missing: {dir_path_str} - {description}",
                        path=dir_path_str,
                        requirement_status=requirement_status
                    ))
                    print(f"  ❌ {dir_path_str}/ - MISSING (required)")
                elif not dir_path.is_dir():
                    self.results.append(ValidationResult(
                        severity=Severity.ERROR,
                        message=f"Path exists but is not a directory: {dir_path_str}",
                        path=dir_path_str,
                        requirement_status=requirement_status
                    ))
                    print(f"  ❌ {dir_path_str}/ - NOT A DIRECTORY")
                else:
                    print(f"  ✅ {dir_path_str}/ - OK")
                    # Validate subdirectories if present
                    subdirs = dir_info.get('subdirectories', {})
                    if subdirs:
                        self._validate_subdirectories(dir_path, subdirs, indent=2)
            
            elif requirement_status == 'suggested':
                if not dir_path.exists():
                    self.results.append(ValidationResult(
                        severity=Severity.WARNING,
                        message=f"Suggested directory missing: {dir_path_str} - {description}",
                        path=dir_path_str,
                        requirement_status=requirement_status
                    ))
                    print(f"  ⚠️  {dir_path_str}/ - MISSING (suggested)")
                elif not dir_path.is_dir():
                    self.results.append(ValidationResult(
                        severity=Severity.WARNING,
                        message=f"Path exists but is not a directory: {dir_path_str}",
                        path=dir_path_str,
                        requirement_status=requirement_status
                    ))
                    print(f"  ⚠️  {dir_path_str}/ - NOT A DIRECTORY")
                else:
                    print(f"  ✅ {dir_path_str}/ - OK")
                    subdirs = dir_info.get('subdirectories', {})
                    if subdirs:
                        self._validate_subdirectories(dir_path, subdirs, indent=2)
            
            elif requirement_status == 'optional':
                if dir_path.exists():
                    if dir_path.is_dir():
                        print(f"  ✅ {dir_path_str}/ - OK (optional)")
                        subdirs = dir_info.get('subdirectories', {})
                        if subdirs:
                            self._validate_subdirectories(dir_path, subdirs, indent=2)
                    else:
                        print(f"  ⚠️  {dir_path_str}/ - NOT A DIRECTORY (optional)")
                else:
                    print(f"  ℹ️  {dir_path_str}/ - Not present (optional)")
        
        print()
    
    def _validate_subdirectories(self, parent_path: Path, subdirs: Dict, indent: int = 0):
        """Validate subdirectories recursively"""
        indent_str = "  " * indent
        
        for subdir_key, subdir_info in subdirs.items():
            subdir_name = subdir_info.get('name')
            subdir_path_str = subdir_info.get('path', subdir_name)
            requirement_status = subdir_info.get('requirement_status', 'optional')
            
            # Get relative path from parent
            if '/' in subdir_path_str:
                # Full path provided
                subdir_path = self.repo_path / subdir_path_str
                display_path = subdir_path_str
            else:
                # Relative to parent
                subdir_path = parent_path / subdir_name
                display_path = f"{parent_path.relative_to(self.repo_path)}/{subdir_name}"
            
            if requirement_status == 'required':
                if not subdir_path.exists():
                    self.results.append(ValidationResult(
                        severity=Severity.ERROR,
                        message=f"Required subdirectory missing: {display_path}",
                        path=str(display_path),
                        requirement_status=requirement_status
                    ))
                    print(f"{indent_str}❌ {subdir_name}/ - MISSING (required)")
                else:
                    print(f"{indent_str}✅ {subdir_name}/ - OK")
            
            elif requirement_status == 'suggested':
                if not subdir_path.exists():
                    self.results.append(ValidationResult(
                        severity=Severity.WARNING,
                        message=f"Suggested subdirectory missing: {display_path}",
                        path=str(display_path),
                        requirement_status=requirement_status
                    ))
                    print(f"{indent_str}⚠️  {subdir_name}/ - MISSING (suggested)")
                else:
                    print(f"{indent_str}✅ {subdir_name}/ - OK")
    
    def print_summary(self):
        """Print validation summary"""
        errors = [r for r in self.results if r.severity == Severity.ERROR]
        warnings = [r for r in self.results if r.severity == Severity.WARNING]
        
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Total issues: {len(self.results)}")
        print(f"  Errors: {len(errors)}")
        print(f"  Warnings: {len(warnings)}")
        print()
        
        if errors:
            print("ERRORS:")
            for result in errors:
                print(f"  ❌ {result.path}: {result.message}")
            print()
        
        if warnings:
            print("WARNINGS:")
            for result in warnings:
                print(f"  ⚠️  {result.path}: {result.message}")
            print()
        
        if not errors and not warnings:
            print("✅ Repository structure is valid!")
        elif errors:
            print("❌ Repository structure validation FAILED")
        else:
            print("⚠️  Repository structure has warnings")
        
        return len(errors) == 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Validate repository structure using Terraform definitions"
    )
    parser.add_argument(
        "repo_path",
        nargs="?",
        default=".",
        help="Path to repository to validate (default: current directory)"
    )
    parser.add_argument(
        "--repo-type",
        default="default",
        help="Repository type to validate against (default: default)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = TerraformRepositoryStructureValidator(args.repo_path, args.repo_type)
    
    # Run validation
    validator.validate()
    
    # Print summary
    success = validator.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
