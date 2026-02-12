#!/usr/bin/env python3
"""
Configuration Manager - Centralized, environment-aware configuration.

File: scripts/lib/config_manager.py
Version: 03.02.00
Classification: EnterpriseLibrary
Author: MokoStandards Team
Copyright: (C) 2026 Moko Consulting LLC. All rights reserved.
License: GPL-3.0-or-later

Revision History:
    2026-02-10: Rewritten for Phase 2 enterprise libraries
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

VERSION = "03.02.00"


class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    pass


class Config:
    """Enterprise configuration manager with environment support."""
    
    DEFAULT_CONFIG = {
        'version': VERSION,
        'environment': 'development',
        'github': {
            'organization': 'mokoconsulting-tech',
            'rate_limit': 5000,
            'max_retries': 3,
            'timeout': 30
        },
        'logging': {
            'level': 'INFO',
            'format': 'json',
            'directory': 'logs',
            'retention_days': 90
        },
        'audit': {
            'enabled': True,
            'directory': 'logs/audit',
            'max_file_size_mb': 10,
            'retention_days': 90
        },
        'cache': {
            'enabled': True,
            'ttl_seconds': 300
        },
        'circuit_breaker': {
            'enabled': True,
            'threshold': 5,
            'timeout_seconds': 60
        }
    }
    
    def __init__(self, config_data: Optional[Dict[str, Any]] = None, environment: str = 'development'):
        """Initialize configuration.
        
        Args:
            config_data: Configuration dictionary (uses DEFAULT_CONFIG if None)
            environment: Environment name (development, staging, production)
        """
        if config_data is None:
            config_data = self.DEFAULT_CONFIG.copy()
            environment = os.environ.get('MOKO_ENV', environment)
        self._config_data = config_data
        self._environment = environment
        self._override_data: Dict[str, Any] = {}
    
    @classmethod
    def load(cls, env: Optional[str] = None) -> 'Config':
        """Load configuration."""
        if env is None:
            env = os.environ.get('MOKO_ENV', 'development')
        config_data = cls.DEFAULT_CONFIG.copy()
        config_data['environment'] = env
        return cls(config_data, env)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation."""
        if key in self._override_data:
            return self._override_data[key]
        value = self._config_data
        for part in key.split('.'):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value (runtime override)."""
        self._override_data[key] = value
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer value."""
        return int(self.get(key, default))
    
    def get_str(self, key: str, default: str = '') -> str:
        """Get string value."""
        return str(self.get(key, default))
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean value."""
        return bool(self.get(key, default))
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section."""
        return self.get(section, {})
    
    def get_environment(self) -> str:
        """Get current environment."""
        return self._environment
    
    def is_production(self) -> bool:
        """Check if production environment."""
        return self._environment in ('production', 'prod')
    
    def is_development(self) -> bool:
        """Check if development environment."""
        return self._environment in ('development', 'dev')
    
    def __repr__(self) -> str:
        return f"Config(environment='{self._environment}')"


# Backward compatibility alias
ConfigManager = Config


if __name__ == '__main__':
    print(f"Configuration Manager v{VERSION}")
    print("=" * 60)
    config = Config.load()
    print(f"Environment: {config.get_environment()}")
    print(f"Organization: {config.get('github.organization')}")
    print(f"Rate Limit: {config.get_int('github.rate_limit')}")
    print("✅ Configuration Manager initialized")
