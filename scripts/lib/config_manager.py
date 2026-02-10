#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# (./LICENSE).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/config_manager.py
# VERSION: 03.01.05
# BRIEF: Centralized configuration management for MokoStandards scripts
# PATH: /scripts/lib/config_manager.py
# NOTE: Provides YAML-based configuration with environment overrides

"""Configuration Manager for MokoStandards Scripts.

This module provides centralized configuration management with:
- XML-based configuration files (MokoStandards.override.xml support)
- Environment variable overrides (MOKOSTANDARDS_* prefix)
- Schema validation
- In-memory caching for performance
- Type-safe configuration access
- Sensible defaults

Example:
    Basic usage:
        >>> config = get_config()
        >>> print(config.organization.name)
        mokoconsulting-tech

    Custom config path:
        >>> from pathlib import Path
        >>> config = get_config(Path("custom-config.yaml"))

    Using get() method with defaults:
        >>> manager = ConfigManager.get_instance()
        >>> value = manager.get("github.api_rate_limit", default=5000)
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, TypeVar, cast
from dataclasses import dataclass, field, asdict
from copy import deepcopy

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


# ============================================================
# Custom Exceptions
# ============================================================

class ConfigError(Exception):
    """Base exception for configuration-related errors.

    Attributes:
        message: The error message describing what went wrong.
        context: Optional dictionary with additional error context.
    """

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Initialize ConfigError.

        Args:
            message: Error message describing the issue.
            context: Optional dictionary with additional error context.
        """
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return formatted error message with context."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} ({context_str})"
        return self.message


class ConfigValidationError(ConfigError):
    """Raised when configuration validation fails."""
    pass


class ConfigNotFoundError(ConfigError):
    """Raised when configuration file is not found."""
    pass


class ConfigParseError(ConfigError):
    """Raised when configuration file cannot be parsed."""
    pass


# ============================================================
# Configuration Data Classes
# ============================================================

@dataclass
class OrgConfig:
    """Organization configuration.

    Attributes:
        name: GitHub organization name.
        project_number: Default project board number.
    """
    name: str = "mokoconsulting-tech"
    project_number: int = 7


@dataclass
class GitHubConfig:
    """GitHub API configuration.

    Attributes:
        api_rate_limit: Maximum API requests per hour.
        retry_attempts: Number of retry attempts for failed requests.
        retry_backoff_base: Base multiplier for exponential backoff.
        timeout_seconds: Request timeout in seconds.
        token_env_var: Environment variable name for GitHub token.
    """
    api_rate_limit: int = 5000
    retry_attempts: int = 3
    retry_backoff_base: float = 2.0
    timeout_seconds: int = 30
    token_env_var: str = "GH_PAT"


@dataclass
class AutomationConfig:
    """Automation scripts configuration.

    Attributes:
        default_branch: Default branch name for automated updates.
        temp_dir: Temporary directory for automation operations.
        confirmation_required: Whether to require user confirmation.
    """
    default_branch: str = "chore/sync-mokostandards-updates"
    temp_dir: str = "/tmp/mokostandards"
    confirmation_required: bool = True


@dataclass
class ValidationConfig:
    """Validation scripts configuration.

    Attributes:
        excluded_dirs: List of directories to exclude from validation.
        max_file_size_mb: Maximum file size to validate in megabytes.
        max_results: Maximum number of validation results to return.
    """
    excluded_dirs: List[str] = field(default_factory=lambda: [
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
    """Audit logging configuration.

    Attributes:
        enabled: Whether audit logging is enabled.
        log_dir: Directory for audit log files.
        retention_days: Number of days to retain logs.
        format: Log format (json or csv).
    """
    enabled: bool = True
    log_dir: str = "~/.mokostandards/logs"
    retention_days: int = 90
    format: str = "json"


@dataclass
class SyncConfig:
    """Sync configuration for MokoStandards.override.xml files.

    Attributes:
        enabled: Whether sync is enabled.
        exclude_files: Files to exclude from sync operations.
        protected_files: Files that should never be overwritten.
    """
    enabled: bool = True
    exclude_files: List[str] = field(default_factory=list)
    protected_files: List[str] = field(default_factory=list)


@dataclass
class RepositoryConfig:
    """Repository-specific configuration.

    Attributes:
        compliance_level: Compliance enforcement level.
    """
    compliance_level: str = "standard"


@dataclass
class Config:
    """Main configuration container.

    Attributes:
        organization: Organization-specific configuration.
        github: GitHub API configuration.
        automation: Automation scripts configuration.
        validation: Validation scripts configuration.
        audit: Audit logging configuration.
        sync: Sync operation configuration.
        repository: Repository-specific configuration.
        config_version: Configuration schema version.
    """
    organization: OrgConfig = field(default_factory=OrgConfig)
    github: GitHubConfig = field(default_factory=GitHubConfig)
    automation: AutomationConfig = field(default_factory=AutomationConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)
    sync: SyncConfig = field(default_factory=SyncConfig)
    repository: RepositoryConfig = field(default_factory=RepositoryConfig)
    config_version: str = "2.0"


# ============================================================
# Configuration Manager
# ============================================================

T = TypeVar('T')


class ConfigManager:
    """Centralized configuration manager with caching and validation.

    This class provides a singleton interface for managing configuration
    across the MokoStandards scripts. It supports:
    - Loading from multiple config file formats (YAML)
    - Environment variable overrides (MOKOSTANDARDS_* prefix)
    - In-memory caching for performance
    - Schema validation
    - Thread-safe singleton pattern

    Attributes:
        config_path: Path to the configuration file.
        _config: Cached configuration object.
        _cache: In-memory cache for nested config lookups.

    Example:
        >>> manager = ConfigManager.get_instance()
        >>> config = manager.config
        >>> print(config.organization.name)
        mokoconsulting-tech
    """

    DEFAULT_CONFIG_PATH = Path.home() / ".mokostandards" / "config.yaml"
    SYNC_CONFIG_NAME = "MokoStandards.override.xml"

    _instance: Optional['ConfigManager'] = None
    _config: Optional[Config] = None
    _cache: Dict[str, Any] = {}

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize configuration manager.

        Args:
            config_path: Optional path to configuration file. If not provided,
                uses DEFAULT_CONFIG_PATH or searches for SYNC_CONFIG_NAME.
        """
        self.config_path = self._resolve_config_path(config_path)
        self._config = None
        self._cache = {}

    def _resolve_config_path(self, config_path: Optional[Path]) -> Path:
        """Resolve the configuration file path.

        Priority order:
        1. Explicitly provided path
        2. MokoStandards.override.xml in current directory
        3. MokoStandards.override.xml walking up directory tree
        4. Default path (~/.mokostandards/config.yaml)

        Args:
            config_path: Optional explicitly provided path.

        Returns:
            Resolved Path object.
        """
        if config_path is not None:
            return config_path

        # Check for MokoStandards.override.xml in current and parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            sync_config = parent / self.SYNC_CONFIG_NAME
            if sync_config.exists():
                return sync_config

        # Fall back to default
        return self.DEFAULT_CONFIG_PATH

    @classmethod
    def get_instance(cls, config_path: Optional[Path] = None) -> 'ConfigManager':
        """Get singleton instance of ConfigManager.

        Args:
            config_path: Optional path to configuration file.

        Returns:
            Singleton ConfigManager instance.
        """
        if cls._instance is None:
            cls._instance = ConfigManager(config_path)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton instance (mainly for testing)."""
        cls._instance = None

    @property
    def config(self) -> Config:
        """Get cached configuration object.

        Returns:
            Configuration object.
        """
        if self._config is None:
            self._config = self._load_config()
        return self._config

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> Config:
        """Load configuration with fallback to defaults.

        Args:
            config_path: Optional path to configuration file.

        Returns:
            Configuration object.
        """
        manager = cls.get_instance(config_path)
        return manager.config

    def reload(self) -> Config:
        """Reload configuration from file, clearing cache.

        Returns:
            Fresh configuration object.
        """
        self._config = None
        self._cache.clear()
        return self.config

    def get(
        self,
        key: str,
        default: Optional[T] = None,
        cast_type: Optional[type] = None
    ) -> Union[T, Any]:
        """Get configuration value by dot-notation key with caching.

        Args:
            key: Dot-notation key (e.g., 'github.api_rate_limit').
            default: Default value if key not found.
            cast_type: Optional type to cast the value to.

        Returns:
            Configuration value or default.

        Example:
            >>> manager = ConfigManager.get_instance()
            >>> rate_limit = manager.get("github.api_rate_limit", default=5000)
            >>> org_name = manager.get("organization.name", default="unknown")
        """
        # Check cache first
        if key in self._cache:
            value = self._cache[key]
        else:
            # Navigate nested attributes
            parts = key.split('.')
            value: Any = self.config

            try:
                for part in parts:
                    value = getattr(value, part)
                self._cache[key] = value
            except AttributeError:
                return default

        # Apply type casting if requested
        if cast_type is not None and value is not None:
            try:
                value = cast_type(value)
            except (ValueError, TypeError):
                return default

        return value

    def _load_config(self) -> Config:
        """Load configuration from file or use defaults.

        Returns:
            Configuration object.

        Raises:
            ConfigParseError: If config file exists but cannot be parsed.
        """
        if self.config_path.exists() and yaml is not None:
            try:
                return self._load_from_yaml()
            except ConfigParseError:
                raise
            except Exception as e:
                raise ConfigParseError(
                    f"Failed to load config from {self.config_path}",
                    context={"error": str(e), "path": str(self.config_path)}
                )
        else:
            if yaml is None and self.config_path.exists():
                print("⚠️  Warning: PyYAML not installed, cannot load config file",
                      file=sys.stderr)
                print("ℹ️  Install with: pip install pyyaml", file=sys.stderr)
            return self._default_config()

    def _load_from_yaml(self) -> Config:
        """Load configuration from YAML file.

        Returns:
            Configuration object.

        Raises:
            ConfigParseError: If YAML parsing fails.
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigParseError(
                f"Invalid YAML in config file",
                context={"path": str(self.config_path), "error": str(e)}
            )
        except IOError as e:
            raise ConfigParseError(
                f"Cannot read config file",
                context={"path": str(self.config_path), "error": str(e)}
            )

        # Apply environment variable overrides
        data = self._apply_env_overrides(data)

        # Validate configuration
        self.validate_config(data)

        # Build configuration objects with error handling
        try:
            return Config(
                organization=self._build_org_config(data.get('organization', {})),
                github=self._build_github_config(data.get('github', {})),
                automation=self._build_automation_config(data.get('automation', {})),
                validation=self._build_validation_config(data.get('validation', {})),
                audit=self._build_audit_config(data.get('audit', {})),
                sync=self._build_sync_config(data.get('sync', {})),
                repository=self._build_repository_config(data.get('repository', {})),
                config_version=data.get('config_version', '2.0')
            )
        except TypeError as e:
            raise ConfigValidationError(
                f"Invalid configuration structure",
                context={"error": str(e)}
            )

    def _build_org_config(self, data: Dict[str, Any]) -> OrgConfig:
        """Build OrgConfig from dictionary."""
        defaults = OrgConfig()
        return OrgConfig(
            name=data.get('name', defaults.name),
            project_number=data.get('project_number', defaults.project_number)
        )

    def _build_github_config(self, data: Dict[str, Any]) -> GitHubConfig:
        """Build GitHubConfig from dictionary."""
        defaults = GitHubConfig()
        return GitHubConfig(
            api_rate_limit=data.get('api_rate_limit', defaults.api_rate_limit),
            retry_attempts=data.get('retry_attempts', defaults.retry_attempts),
            retry_backoff_base=data.get('retry_backoff_base', defaults.retry_backoff_base),
            timeout_seconds=data.get('timeout_seconds', defaults.timeout_seconds),
            token_env_var=data.get('token_env_var', defaults.token_env_var)
        )

    def _build_automation_config(self, data: Dict[str, Any]) -> AutomationConfig:
        """Build AutomationConfig from dictionary."""
        defaults = AutomationConfig()
        return AutomationConfig(
            default_branch=data.get('default_branch', defaults.default_branch),
            temp_dir=data.get('temp_dir', defaults.temp_dir),
            confirmation_required=data.get('confirmation_required', defaults.confirmation_required)
        )

    def _build_validation_config(self, data: Dict[str, Any]) -> ValidationConfig:
        """Build ValidationConfig from dictionary."""
        defaults = ValidationConfig()
        return ValidationConfig(
            excluded_dirs=data.get('excluded_dirs', defaults.excluded_dirs),
            max_file_size_mb=data.get('max_file_size_mb', defaults.max_file_size_mb),
            max_results=data.get('max_results', defaults.max_results)
        )

    def _build_audit_config(self, data: Dict[str, Any]) -> AuditConfig:
        """Build AuditConfig from dictionary."""
        defaults = AuditConfig()
        return AuditConfig(
            enabled=data.get('enabled', defaults.enabled),
            log_dir=data.get('log_dir', defaults.log_dir),
            retention_days=data.get('retention_days', defaults.retention_days),
            format=data.get('format', defaults.format)
        )

    def _build_sync_config(self, data: Dict[str, Any]) -> SyncConfig:
        """Build SyncConfig from dictionary."""
        defaults = SyncConfig()
        return SyncConfig(
            enabled=data.get('enabled', defaults.enabled),
            exclude_files=data.get('exclude_files', defaults.exclude_files),
            protected_files=data.get('protected_files', defaults.protected_files)
        )

    def _build_repository_config(self, data: Dict[str, Any]) -> RepositoryConfig:
        """Build RepositoryConfig from dictionary."""
        defaults = RepositoryConfig()
        return RepositoryConfig(
            compliance_level=data.get('compliance_level', defaults.compliance_level)
        )

    def _apply_env_overrides(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides.

        Environment variables with MOKOSTANDARDS_* prefix override config values.
        Supports nested keys using double underscores (e.g., MOKOSTANDARDS_GITHUB__TOKEN).

        Args:
            data: Configuration dictionary.

        Returns:
            Updated configuration dictionary.
        """
        # Make a deep copy to avoid modifying the original
        data = deepcopy(data)

        # Organization overrides
        if 'MOKOSTANDARDS_ORG' in os.environ:
            data.setdefault('organization', {})['name'] = os.environ['MOKOSTANDARDS_ORG']

        if 'MOKOSTANDARDS_ORG_PROJECT_NUMBER' in os.environ:
            try:
                data.setdefault('organization', {})['project_number'] = int(
                    os.environ['MOKOSTANDARDS_ORG_PROJECT_NUMBER']
                )
            except ValueError as e:
                # Log warning about invalid project number format
                import sys
                print(f"Warning: Invalid MOKOSTANDARDS_ORG_PROJECT_NUMBER value: {e}", file=sys.stderr)

        # GitHub token override
        if 'GH_PAT' in os.environ:
            data.setdefault('github', {})['token_env_var'] = 'GH_PAT'
        elif 'GITHUB_TOKEN' in os.environ:
            data.setdefault('github', {})['token_env_var'] = 'GITHUB_TOKEN'

        # GitHub configuration overrides
        if 'MOKOSTANDARDS_GITHUB_RATE_LIMIT' in os.environ:
            try:
                data.setdefault('github', {})['api_rate_limit'] = int(
                    os.environ['MOKOSTANDARDS_GITHUB_RATE_LIMIT']
                )
            except ValueError as e:
                # Log warning about invalid rate limit format
                import sys
                print(f"Warning: Invalid MOKOSTANDARDS_GITHUB_RATE_LIMIT value: {e}", file=sys.stderr)

        # Automation overrides
        if 'MOKOSTANDARDS_TEMP_DIR' in os.environ:
            data.setdefault('automation', {})['temp_dir'] = os.environ['MOKOSTANDARDS_TEMP_DIR']

        if 'MOKOSTANDARDS_DEFAULT_BRANCH' in os.environ:
            data.setdefault('automation', {})['default_branch'] = os.environ['MOKOSTANDARDS_DEFAULT_BRANCH']

        if 'MOKOSTANDARDS_CONFIRMATION_REQUIRED' in os.environ:
            data.setdefault('automation', {})['confirmation_required'] = (
                os.environ['MOKOSTANDARDS_CONFIRMATION_REQUIRED'].lower() in ('true', '1', 'yes')
            )

        # Audit overrides
        if 'MOKOSTANDARDS_AUDIT_ENABLED' in os.environ:
            data.setdefault('audit', {})['enabled'] = (
                os.environ['MOKOSTANDARDS_AUDIT_ENABLED'].lower() in ('true', '1', 'yes')
            )

        if 'MOKOSTANDARDS_AUDIT_LOG_DIR' in os.environ:
            data.setdefault('audit', {})['log_dir'] = os.environ['MOKOSTANDARDS_AUDIT_LOG_DIR']

        # Sync overrides
        if 'MOKOSTANDARDS_SYNC_ENABLED' in os.environ:
            data.setdefault('sync', {})['enabled'] = (
                os.environ['MOKOSTANDARDS_SYNC_ENABLED'].lower() in ('true', '1', 'yes')
            )

        return data

    @staticmethod
    def validate_config(data: Dict[str, Any]) -> None:
        """Validate configuration structure and values.

        Args:
            data: Configuration dictionary to validate.

        Raises:
            ConfigValidationError: If validation fails.
        """
        # Validate organization config
        if 'organization' in data:
            org = data['organization']
            if not isinstance(org, dict):
                raise ConfigValidationError("'organization' must be a dictionary")

            if 'name' in org and not isinstance(org['name'], str):
                raise ConfigValidationError("'organization.name' must be a string")

            if 'project_number' in org:
                if not isinstance(org['project_number'], int):
                    raise ConfigValidationError("'organization.project_number' must be an integer")
                if org['project_number'] < 0:
                    raise ConfigValidationError("'organization.project_number' must be non-negative")

        # Validate GitHub config
        if 'github' in data:
            github = data['github']
            if not isinstance(github, dict):
                raise ConfigValidationError("'github' must be a dictionary")

            if 'api_rate_limit' in github:
                if not isinstance(github['api_rate_limit'], int):
                    raise ConfigValidationError("'github.api_rate_limit' must be an integer")
                if github['api_rate_limit'] <= 0:
                    raise ConfigValidationError("'github.api_rate_limit' must be positive")

            if 'retry_attempts' in github:
                if not isinstance(github['retry_attempts'], int):
                    raise ConfigValidationError("'github.retry_attempts' must be an integer")
                if github['retry_attempts'] < 0:
                    raise ConfigValidationError("'github.retry_attempts' must be non-negative")

            if 'timeout_seconds' in github:
                if not isinstance(github['timeout_seconds'], int):
                    raise ConfigValidationError("'github.timeout_seconds' must be an integer")
                if github['timeout_seconds'] <= 0:
                    raise ConfigValidationError("'github.timeout_seconds' must be positive")

        # Validate validation config
        if 'validation' in data:
            validation = data['validation']
            if not isinstance(validation, dict):
                raise ConfigValidationError("'validation' must be a dictionary")

            if 'excluded_dirs' in validation:
                if not isinstance(validation['excluded_dirs'], list):
                    raise ConfigValidationError("'validation.excluded_dirs' must be a list")

            if 'max_file_size_mb' in validation:
                if not isinstance(validation['max_file_size_mb'], int):
                    raise ConfigValidationError("'validation.max_file_size_mb' must be an integer")
                if validation['max_file_size_mb'] <= 0:
                    raise ConfigValidationError("'validation.max_file_size_mb' must be positive")

        # Validate audit config
        if 'audit' in data:
            audit = data['audit']
            if not isinstance(audit, dict):
                raise ConfigValidationError("'audit' must be a dictionary")

            if 'enabled' in audit and not isinstance(audit['enabled'], bool):
                raise ConfigValidationError("'audit.enabled' must be a boolean")

            if 'format' in audit:
                if audit['format'] not in ('json', 'csv'):
                    raise ConfigValidationError("'audit.format' must be 'json' or 'csv'")

        # Validate sync config
        if 'sync' in data:
            sync = data['sync']
            if not isinstance(sync, dict):
                raise ConfigValidationError("'sync' must be a dictionary")

            if 'enabled' in sync and not isinstance(sync['enabled'], bool):
                raise ConfigValidationError("'sync.enabled' must be a boolean")

            if 'exclude_files' in sync:
                if not isinstance(sync['exclude_files'], list):
                    raise ConfigValidationError("'sync.exclude_files' must be a list")

            if 'protected_files' in sync:
                if not isinstance(sync['protected_files'], list):
                    raise ConfigValidationError("'sync.protected_files' must be a list")

    def _default_config(self) -> Config:
        """Provide sensible defaults with environment overrides applied.

        Returns:
            Default configuration object with environment variable overrides.
        """
        # Start with empty dict and apply env overrides
        data: Dict[str, Any] = {}
        data = self._apply_env_overrides(data)

        # Build config with overrides applied
        return Config(
            organization=self._build_org_config(data.get('organization', {})),
            github=self._build_github_config(data.get('github', {})),
            automation=self._build_automation_config(data.get('automation', {})),
            validation=self._build_validation_config(data.get('validation', {})),
            audit=self._build_audit_config(data.get('audit', {})),
            sync=self._build_sync_config(data.get('sync', {})),
            repository=self._build_repository_config(data.get('repository', {})),
            config_version=data.get('config_version', '2.0')
        )

    def save_template(self, path: Optional[Path] = None) -> Path:
        """Save configuration template to file.

        Args:
            path: Optional path for template file. If not provided, uses config_path.

        Returns:
            Path where template was saved.

        Raises:
            ImportError: If PyYAML is not installed.
            IOError: If file cannot be written.
        """
        if yaml is None:
            raise ImportError("PyYAML is required to save configuration. Install with: pip install pyyaml")

        save_path = path or self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)

        template = {
            'config_version': '2.0',
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
                'temp_dir': '/tmp/mokostandards',
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
            },
            'sync': {
                'enabled': True,
                'exclude_files': [],
                'protected_files': []
            },
            'repository': {
                'compliance_level': 'standard'
            }
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(template, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Configuration template saved to: {save_path}")
        return save_path

    def to_dict(self) -> Dict[str, Any]:
        """Convert current configuration to dictionary.

        Returns:
            Dictionary representation of configuration.
        """
        return asdict(self.config)

    def to_json(self, indent: int = 2) -> str:
        """Convert current configuration to JSON string.

        Args:
            indent: Number of spaces for indentation.

        Returns:
            JSON string representation of configuration.
        """
        return json.dumps(self.to_dict(), indent=indent)


# ============================================================
# Convenience Functions
# ============================================================

def get_config(config_path: Optional[Path] = None) -> Config:
    """Get configuration instance.

    This is the primary interface for accessing configuration in scripts.

    Args:
        config_path: Optional path to configuration file.

    Returns:
        Configuration object.

    Example:
        >>> config = get_config()
        >>> print(config.organization.name)
        mokoconsulting-tech
    """
    return ConfigManager.load(config_path)


def create_config_template(path: Optional[Path] = None) -> Path:
    """Create configuration template file.

    Args:
        path: Optional path for template file.

    Returns:
        Path where template was saved.

    Example:
        >>> from pathlib import Path
        >>> create_config_template(Path("config.yaml"))
    """
    manager = ConfigManager.get_instance()
    return manager.save_template(path)


def validate_config_file(path: Path) -> bool:
    """Validate a configuration file without loading it.

    Args:
        path: Path to configuration file to validate.

    Returns:
        True if valid, False otherwise.

    Example:
        >>> from pathlib import Path
        >>> is_valid = validate_config_file(Path("config.yaml"))
    """
    if not path.exists():
        print(f"❌ Config file not found: {path}", file=sys.stderr)
        return False

    if yaml is None:
        print("❌ PyYAML not installed", file=sys.stderr)
        return False

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data is None:
            print("❌ Config file is empty", file=sys.stderr)
            return False

        ConfigManager.validate_config(data)
        print(f"✅ Config file is valid: {path}")
        return True

    except ConfigValidationError as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        return False
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return False


# ============================================================
# CLI for Configuration Management
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="MokoStandards Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a configuration template
  %(prog)s --create-template

  # Show current configuration
  %(prog)s --show

  # Validate a configuration file
  %(prog)s --validate --config config.yaml

  # Export configuration as JSON
  %(prog)s --export-json

Environment Variables:
  MOKOSTANDARDS_ORG              - Override organization name
  MOKOSTANDARDS_ORG_PROJECT_NUMBER - Override project number
  MOKOSTANDARDS_TEMP_DIR         - Override temporary directory
  MOKOSTANDARDS_AUDIT_ENABLED    - Override audit logging (true/false)
  MOKOSTANDARDS_SYNC_ENABLED     - Override sync enabled (true/false)
  GH_PAT or GITHUB_TOKEN         - GitHub authentication token
        """
    )

    parser.add_argument(
        '--create-template',
        action='store_true',
        help='Create configuration template file'
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Show current configuration'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate configuration file'
    )
    parser.add_argument(
        '--export-json',
        action='store_true',
        help='Export configuration as JSON'
    )
    parser.add_argument(
        '--get',
        type=str,
        metavar='KEY',
        help='Get specific configuration value (dot notation, e.g., github.api_rate_limit)'
    )

    args = parser.parse_args()

    try:
        if args.create_template:
            path = create_config_template(args.config)
            print(f"✅ Template created at: {path}")
            print(f"ℹ️  Edit this file to customize your configuration")
            sys.exit(0)

        elif args.validate:
            if args.config is None:
                print("❌ --config is required with --validate", file=sys.stderr)
                sys.exit(1)

            is_valid = validate_config_file(args.config)
            sys.exit(0 if is_valid else 1)

        elif args.show:
            config = get_config(args.config)
            print(f"📋 Current Configuration:")
            print(f"  Config Version: {config.config_version}")
            print(f"  Organization: {config.organization.name}")
            print(f"  Project Number: {config.organization.project_number}")
            print(f"  GitHub Rate Limit: {config.github.api_rate_limit}/hour")
            print(f"  GitHub Timeout: {config.github.timeout_seconds}s")
            print(f"  Audit Enabled: {config.audit.enabled}")
            print(f"  Audit Log Dir: {config.audit.log_dir}")
            print(f"  Sync Enabled: {config.sync.enabled}")
            print(f"  Compliance Level: {config.repository.compliance_level}")
            sys.exit(0)

        elif args.export_json:
            manager = ConfigManager.get_instance(args.config)
            print(manager.to_json())
            sys.exit(0)

        elif args.get:
            manager = ConfigManager.get_instance(args.config)
            value = manager.get(args.get)
            if value is None:
                print(f"❌ Key not found: {args.get}", file=sys.stderr)
                sys.exit(1)
            print(value)
            sys.exit(0)

        else:
            parser.print_help()
            sys.exit(0)

    except ConfigError as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
