#!/usr/bin/env python3
"""
Terraform Schema Reader

Helper module to read repository schema configuration from Terraform.
This replaces the legacy XML/JSON schema parsing functionality.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List


class TerraformSchemaReader:
    """Read repository schema configuration from Terraform."""

    def __init__(self, terraform_dir: str = None):
        """
        Initialize Terraform schema reader.

        Args:
            terraform_dir: Path to terraform directory (default: auto-detect)
        """
        if terraform_dir is None:
            # Auto-detect terraform directory
            terraform_dir = self._find_terraform_dir()

        self.terraform_dir = Path(terraform_dir).resolve()
        self._cache = {}

        if not self.terraform_dir.exists():
            raise FileNotFoundError(f"Terraform directory not found: {self.terraform_dir}")

    def _find_terraform_dir(self) -> Path:
        """Find terraform directory relative to script location."""
        # Try common locations
        script_path = Path(__file__).resolve()

        # Walk up the directory tree to find .git directory (project root)
        current = script_path.parent
        while current != current.parent:
            if (current / '.git').exists():
                # Found project root
                terraform_path = current / 'terraform'
                if terraform_path.exists():
                    return terraform_path
            current = current.parent

        # Fallback: Check if terraform directory exists relative to current directory
        cwd_terraform = Path.cwd() / 'terraform'
        if cwd_terraform.exists():
            return cwd_terraform

        # Last resort: return relative path
        return Path('terraform')

    def _run_terraform_output(self, output_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Run terraform output command and return parsed JSON.

        Args:
            output_name: Specific output to retrieve (None for all)

        Returns:
            Parsed Terraform output as dictionary
        """
        cache_key = output_name or '__all__'
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            cmd = ['terraform', 'output', '-json']
            if output_name:
                cmd.append(output_name)

            result = subprocess.run(
                cmd,
                cwd=self.terraform_dir,
                capture_output=True,
                text=True,
                check=True
            )

            output = json.loads(result.stdout)

            # Extract value from Terraform output format
            if output_name and isinstance(output, dict) and 'value' in output:
                output = output['value']

            self._cache[cache_key] = output
            return output

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Terraform output failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse Terraform output: {e}")

    def get_health_config(self) -> Dict[str, Any]:
        """
        Get repository health configuration.

        Returns:
            Dictionary containing health scoring configuration, categories, and checks
        """
        try:
            # Get all outputs
            output = self._run_terraform_output()

            # Extract values from Terraform output format
            # Terraform outputs are wrapped with metadata: {"value": ..., "sensitive": false, "type": ...}
            if 'repository_schemas' in output:
                schemas = output['repository_schemas']
                if 'value' in schemas:
                    schemas_value = schemas['value']
                    if 'repo_health_config' in schemas_value:
                        return schemas_value['repo_health_config']

        except Exception as e:
            # Log error but continue to fallback
            import sys
            print(f"Warning: Could not load Terraform configuration: {e}", file=sys.stderr)

        # If Terraform is not available, return minimal config
        return self._get_fallback_health_config()

    def get_repository_structure(self, repo_type: str = 'default') -> Dict[str, Any]:
        """
        Get repository structure definition for given type.

        Args:
            repo_type: Repository type (default, waas-component, crm-module, etc.)

        Returns:
            Dictionary containing repository structure definition
        """
        try:
            output = self._run_terraform_output()

            # Extract values from Terraform output format
            if 'repository_schemas' in output:
                schemas = output['repository_schemas']
                if 'value' in schemas:
                    schemas_value = schemas['value']
                    if 'default_repository_structure' in schemas_value:
                        return schemas_value['default_repository_structure']

        except Exception as e:
            # Log error but continue to fallback
            import sys
            print(f"Warning: Could not load Terraform configuration: {e}", file=sys.stderr)

        # If Terraform is not available, return minimal structure
        return self._get_fallback_structure()

    def get_checks_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all health checks for a specific category.

        Args:
            category: Category ID (e.g., 'ci-cd-status', 'required-documentation')

        Returns:
            List of check definitions
        """
        config = self.get_health_config()
        checks = config.get('checks', {})

        return [
            check for check in checks.values()
            if check.get('category') == category
        ]

    def get_all_categories(self) -> Dict[str, Any]:
        """
        Get all health check categories.

        Returns:
            Dictionary of categories
        """
        config = self.get_health_config()
        return config.get('categories', {})

    def get_thresholds(self) -> Dict[str, Any]:
        """
        Get health score thresholds.

        Returns:
            Dictionary of threshold levels
        """
        config = self.get_health_config()
        return config.get('thresholds', {})

    def _get_fallback_health_config(self) -> Dict[str, Any]:
        """
        Return minimal health configuration when Terraform is not available.
        This allows scripts to function even without Terraform initialized.
        """
        return {
            'metadata': {
                'name': 'Repository Health Configuration',
                'version': '2.0'
            },
            'scoring': {
                'total_points': 100
            },
            'categories': {},
            'thresholds': {
                'excellent': {'min_percentage': 90, 'max_percentage': 100},
                'good': {'min_percentage': 70, 'max_percentage': 89},
                'fair': {'min_percentage': 50, 'max_percentage': 69},
                'poor': {'min_percentage': 0, 'max_percentage': 49}
            },
            'checks': {}
        }

    def _get_fallback_structure(self) -> Dict[str, Any]:
        """
        Return minimal repository structure when Terraform is not available.
        """
        return {
            'metadata': {
                'name': 'Default Repository Structure',
                'repository_type': 'library',
                'platform': 'multi-platform'
            },
            'root_files': {},
            'directories': {}
        }


if __name__ == '__main__':
    # Example usage
    try:
        reader = TerraformSchemaReader()

        print("Repository Health Configuration:")
        health_config = reader.get_health_config()
        print(f"  Total points: {health_config['scoring']['total_points']}")
        print(f"  Categories: {len(health_config['categories'])}")
        print(f"  Checks: {len(health_config['checks'])}")

        print("\nRepository Structure:")
        structure = reader.get_repository_structure()
        print(f"  Type: {structure['metadata']['repository_type']}")
        print(f"  Root files: {len(structure['root_files'])}")
        print(f"  Directories: {len(structure['directories'])}")

    except Exception as e:
        print(f"Error: {e}")
