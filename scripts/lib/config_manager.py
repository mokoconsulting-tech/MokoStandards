#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/config_manager.py
# VERSION: 01.00.00
# BRIEF: Centralized configuration management for MokoStandards scripts
# PATH: /scripts/lib/config_manager.py
# NOTE: Provides YAML-based configuration with environment overrides

"""
Configuration Manager for MokoStandards Scripts

Provides centralized configuration management with:
- YAML-based configuration files
- Environment variable overrides
- Sensible defaults
- Environment-specific configs (dev/staging/prod)
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

try:
    import yaml
except ImportError:
    # Fallback if PyYAML not available
    yaml = None


# ============================================================
# Configuration Data Classes
# ============================================================

@dataclass
class OrgConfig:
    """Organization configuration"""
    name: str = "mokoconsulting-tech"
    project_number: int = 7


@dataclass
class GitHubConfig:
    """GitHub API configuration"""
    api_rate_limit: int = 5000  # requests per hour
    retry_attempts: int = 3
    retry_backoff_base: float = 2.0
    timeout_seconds: int = 30
    token_env_var: str = "GH_PAT"


@dataclass
class AutomationConfig:
    """Automation scripts configuration"""
    default_branch: str = "chore/sync-mokostandards-updates"
    temp_dir: str = ""  # Empty means use secure tempfile.mkdtemp()
    confirmation_required: bool = True


@dataclass
class ValidationConfig:
    """Validation scripts configuration"""
    excluded_dirs: list = field(default_factory=lambda: [
        "vendor",
        "node_modules",
        "dist",
        "build",
        ".git",
        "__pycache__"
    ])
    max_file_size_mb: int = 10
    max_results: int = 50


@dataclass
class AuditConfig:
    """Audit logging configuration"""
    enabled: bool = True
    log_dir: str = "~/.mokostandards/logs"
    retention_days: int = 90
    format: str = "json"  # json or csv


@dataclass
class Config:
    """Main configuration container"""
    organization: OrgConfig = field(default_factory=OrgConfig)
    github: GitHubConfig = field(default_factory=GitHubConfig)
    automation: AutomationConfig = field(default_factory=AutomationConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)


# ============================================================
# Configuration Manager
# ============================================================

class ConfigManager:
    """Centralized configuration manager"""

    DEFAULT_CONFIG_PATH = Path.home() / ".mokostandards" / "config.yaml"

    _instance: Optional['ConfigManager'] = None
    _config: Optional[Config] = None

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager"""
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config = self._load_config()

    @classmethod
    def get_instance(cls, config_path: Optional[Path] = None) -> 'ConfigManager':
        """Get singleton instance of ConfigManager"""
        if cls._instance is None:
            cls._instance = ConfigManager(config_path)
        return cls._instance

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> Config:
        """Load configuration with fallback to defaults"""
        manager = cls.get_instance(config_path)
        return manager._config

    def _load_config(self) -> Config:
        """Load configuration from file or use defaults"""
        if self.config_path.exists() and yaml is not None:
            try:
                return self._load_from_yaml()
            except Exception as e:
                print(f"⚠️  Warning: Failed to load config from {self.config_path}: {e}",
                      file=sys.stderr)
                print("ℹ️  Using default configuration", file=sys.stderr)
                return self._default_config()
        else:
            if yaml is None and self.config_path.exists():
                print("⚠️  Warning: PyYAML not installed, cannot load config file",
                      file=sys.stderr)
                print("ℹ️  Install with: pip install pyyaml", file=sys.stderr)
            return self._default_config()

    def _load_from_yaml(self) -> Config:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            data = yaml.safe_load(f) or {}

        # Apply environment variable overrides
        data = self._apply_env_overrides(data)

        # Build configuration objects
        return Config(
            organization=OrgConfig(**data.get('organization', {})),
            github=GitHubConfig(**data.get('github', {})),
            automation=AutomationConfig(**data.get('automation', {})),
            validation=ValidationConfig(**data.get('validation', {})),
            audit=AuditConfig(**data.get('audit', {}))
        )

    def _apply_env_overrides(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides"""
        # Organization overrides
        if 'MOKOSTANDARDS_ORG' in os.environ:
            data.setdefault('organization', {})['name'] = os.environ['MOKOSTANDARDS_ORG']

        # GitHub token override
        if 'GH_PAT' in os.environ:
            data.setdefault('github', {})['token_env_var'] = 'GH_PAT'
        elif 'GITHUB_TOKEN' in os.environ:
            data.setdefault('github', {})['token_env_var'] = 'GITHUB_TOKEN'

        # Automation overrides
        if 'MOKOSTANDARDS_TEMP_DIR' in os.environ:
            data.setdefault('automation', {})['temp_dir'] = os.environ['MOKOSTANDARDS_TEMP_DIR']

        # Audit overrides
        if 'MOKOSTANDARDS_AUDIT_ENABLED' in os.environ:
            data.setdefault('audit', {})['enabled'] = os.environ['MOKOSTANDARDS_AUDIT_ENABLED'].lower() in ('true', '1', 'yes')

        return data

    @staticmethod
    def _default_config() -> Config:
        """Provide sensible defaults"""
        return Config()

    def save_template(self, path: Optional[Path] = None) -> Path:
        """Save configuration template to file"""
        if yaml is None:
            raise ImportError("PyYAML is required to save configuration. Install with: pip install pyyaml")

        save_path = path or self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)

        template = {
            'organization': {
                'name': 'mokoconsulting-tech',
                'project_number': 7
            },
            'github': {
                'api_rate_limit': 5000,
                'retry_attempts': 3,
                'retry_backoff_base': 2.0,
                'timeout_seconds': 30,
                'token_env_var': 'GH_PAT'
            },
            'automation': {
                'default_branch': 'chore/sync-mokostandards-updates',
                'temp_dir': '',  # Empty means use secure tempfile.mkdtemp()
                'confirmation_required': True
            },
            'validation': {
                'excluded_dirs': [
                    'vendor',
                    'node_modules',
                    'dist',
                    'build',
                    '.git',
                    '__pycache__'
                ],
                'max_file_size_mb': 10,
                'max_results': 50
            },
            'audit': {
                'enabled': True,
                'log_dir': '~/.mokostandards/logs',
                'retention_days': 90,
                'format': 'json'
            }
        }

        with open(save_path, 'w') as f:
            yaml.safe_dump(template, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Configuration template saved to: {save_path}")
        return save_path


# ============================================================
# Convenience Functions
# ============================================================

def get_config(config_path: Optional[Path] = None) -> Config:
    """Get configuration instance"""
    return ConfigManager.load(config_path)


def create_config_template(path: Optional[Path] = None) -> Path:
    """Create configuration template file"""
    manager = ConfigManager.get_instance()
    return manager.save_template(path)


# ============================================================
# CLI for Configuration Management
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MokoStandards Configuration Manager")
    parser.add_argument('--create-template', action='store_true',
                        help='Create configuration template file')
    parser.add_argument('--config', type=Path,
                        help='Path to configuration file')
    parser.add_argument('--show', action='store_true',
                        help='Show current configuration')

    args = parser.parse_args()

    if args.create_template:
        path = create_config_template(args.config)
        print(f"✅ Template created at: {path}")
        print(f"ℹ️  Edit this file to customize your configuration")
    elif args.show:
        config = get_config(args.config)
        print(f"📋 Current Configuration:")
        print(f"  Organization: {config.organization.name}")
        print(f"  Project Number: {config.organization.project_number}")
        print(f"  GitHub Rate Limit: {config.github.api_rate_limit}/hour")
        print(f"  Audit Enabled: {config.audit.enabled}")
        print(f"  Audit Log Dir: {config.audit.log_dir}")
    else:
        parser.print_help()
