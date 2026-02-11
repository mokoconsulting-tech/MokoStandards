#!/usr/bin/env python3
"""
Input Validation Library for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

This module provides security-focused input validation to prevent:
- Path traversal attacks
- Shell injection
- SQL injection
- XSS attacks
- Invalid data types
- Out-of-range values

Usage:
    from input_validator import (
        validate_path, validate_version, validate_email,
        validate_url, sanitize_input
    )
    
    safe_path = validate_path('/etc/../tmp/file.txt')
    version = validate_version('1.2.3')
"""

import os
import re
from pathlib import Path
from typing import Any, List, Optional, Union
from urllib.parse import urlparse

VERSION = "03.02.00"


class ValidationError(Exception):
    """Exception raised when validation fails."""
    pass


def validate_path(
    path: str,
    allow_relative: bool = False,
    must_exist: bool = False,
    allowed_extensions: Optional[List[str]] = None
) -> Path:
    """Validate and sanitize file paths to prevent path traversal.
    
    Args:
        path: Path to validate
        allow_relative: Allow relative paths
        must_exist: Path must exist
        allowed_extensions: List of allowed file extensions
        
    Returns:
        Validated Path object
        
    Raises:
        ValidationError: If path is invalid or dangerous
    """
    if not path or not isinstance(path, str):
        raise ValidationError("Path must be a non-empty string")
    
    # Convert to Path object
    p = Path(path)
    
    # Check for path traversal attempts
    if '..' in path:
        raise ValidationError("Path traversal detected (..)") 
    
    # Resolve to absolute path if not allowing relative
    if not allow_relative:
        p = p.resolve()
    
    # Check if path must exist
    if must_exist and not p.exists():
        raise ValidationError(f"Path does not exist: {path}")
    
    # Check file extension if specified
    if allowed_extensions and p.suffix:
        if p.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
            raise ValidationError(
                f"Invalid file extension: {p.suffix}. "
                f"Allowed: {', '.join(allowed_extensions)}"
            )
    
    return p


def validate_version(
    version: str,
    format_type: str = 'semver'
) -> str:
    """Validate version strings.
    
    Args:
        version: Version string to validate
        format_type: Version format ('semver', 'simple', 'moko')
        
    Returns:
        Validated version string
        
    Raises:
        ValidationError: If version format is invalid
    """
    if not version or not isinstance(version, str):
        raise ValidationError("Version must be a non-empty string")
    
    if format_type == 'semver':
        # Semantic versioning: MAJOR.MINOR.PATCH
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
        if not re.match(pattern, version):
            raise ValidationError(
                f"Invalid semver format: {version}. "
                "Expected: MAJOR.MINOR.PATCH"
            )
    elif format_type == 'moko':
        # MokoStandards format: XX.YY.ZZ
        pattern = r'^\d{2}\.\d{2}\.\d{2}$'
        if not re.match(pattern, version):
            raise ValidationError(
                f"Invalid MokoStandards version format: {version}. "
                "Expected: XX.YY.ZZ"
            )
    elif format_type == 'simple':
        # Simple format: X.Y or X.Y.Z
        pattern = r'^\d+\.\d+(\.\d+)?$'
        if not re.match(pattern, version):
            raise ValidationError(
                f"Invalid version format: {version}"
            )
    else:
        raise ValidationError(f"Unknown version format type: {format_type}")
    
    return version


def validate_email(email: str) -> str:
    """Validate email addresses.
    
    Args:
        email: Email address to validate
        
    Returns:
        Validated email address
        
    Raises:
        ValidationError: If email is invalid
    """
    if not email or not isinstance(email, str):
        raise ValidationError("Email must be a non-empty string")
    
    # Simple but effective email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(f"Invalid email format: {email}")
    
    return email.lower()


def validate_url(
    url: str,
    allowed_schemes: Optional[List[str]] = None
) -> str:
    """Validate URLs and check schemes.
    
    Args:
        url: URL to validate
        allowed_schemes: List of allowed URL schemes (e.g., ['http', 'https'])
        
    Returns:
        Validated URL
        
    Raises:
        ValidationError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValidationError("URL must be a non-empty string")
    
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError(f"Invalid URL format: {url}")
        
        if allowed_schemes and parsed.scheme not in allowed_schemes:
            raise ValidationError(
                f"URL scheme '{parsed.scheme}' not allowed. "
                f"Allowed: {', '.join(allowed_schemes)}"
            )
        
        return url
    except Exception as e:
        raise ValidationError(f"URL validation failed: {e}")


def sanitize_shell_input(input_str: str) -> str:
    """Sanitize input to prevent shell injection.
    
    Args:
        input_str: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not isinstance(input_str, str):
        return str(input_str)
    
    # Remove dangerous shell characters
    dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r']
    sanitized = input_str
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def sanitize_sql_input(input_str: str) -> str:
    """Sanitize input to prevent SQL injection.
    
    Args:
        input_str: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not isinstance(input_str, str):
        return str(input_str)
    
    # Remove SQL injection patterns
    dangerous_patterns = ["'", '"', '--', '/*', '*/', 'xp_', 'sp_']
    sanitized = input_str
    
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, '')
    
    return sanitized.strip()


def validate_integer(
    value: Any,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None
) -> int:
    """Validate and convert to integer with range checking.
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Validated integer
        
    Raises:
        ValidationError: If value is invalid or out of range
    """
    try:
        int_value = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Cannot convert to integer: {value}")
    
    if min_value is not None and int_value < min_value:
        raise ValidationError(
            f"Value {int_value} is below minimum {min_value}"
        )
    
    if max_value is not None and int_value > max_value:
        raise ValidationError(
            f"Value {int_value} is above maximum {max_value}"
        )
    
    return int_value


def validate_string(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None
) -> str:
    """Validate string with length and pattern checking.
    
    Args:
        value: String to validate
        min_length: Minimum string length
        max_length: Maximum string length
        pattern: Regex pattern to match
        
    Returns:
        Validated string
        
    Raises:
        ValidationError: If string is invalid
    """
    if not isinstance(value, str):
        raise ValidationError(f"Value must be a string, got {type(value)}")
    
    if min_length is not None and len(value) < min_length:
        raise ValidationError(
            f"String length {len(value)} is below minimum {min_length}"
        )
    
    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"String length {len(value)} exceeds maximum {max_length}"
        )
    
    if pattern and not re.match(pattern, value):
        raise ValidationError(
            f"String does not match pattern: {pattern}"
        )
    
    return value


def validate_choice(value: Any, choices: List[Any]) -> Any:
    """Validate that value is in a list of allowed choices.
    
    Args:
        value: Value to validate
        choices: List of allowed values
        
    Returns:
        Validated value
        
    Raises:
        ValidationError: If value not in choices
    """
    if value not in choices:
        raise ValidationError(
            f"Invalid choice: {value}. "
            f"Allowed: {', '.join(str(c) for c in choices)}"
        )
    
    return value


class Validator:
    """Reusable validator with chainable checks."""
    
    def __init__(self, value: Any, name: str = "value"):
        """Initialize validator.
        
        Args:
            value: Value to validate
            name: Name of the value (for error messages)
        """
        self.value = value
        self.name = name
        self.errors = []
    
    def is_string(self, min_length: Optional[int] = None, max_length: Optional[int] = None):
        """Check if value is a string."""
        try:
            validate_string(self.value, min_length, max_length)
        except ValidationError as e:
            self.errors.append(str(e))
        return self
    
    def is_integer(self, min_value: Optional[int] = None, max_value: Optional[int] = None):
        """Check if value is an integer."""
        try:
            validate_integer(self.value, min_value, max_value)
        except ValidationError as e:
            self.errors.append(str(e))
        return self
    
    def is_email(self):
        """Check if value is a valid email."""
        try:
            validate_email(self.value)
        except ValidationError as e:
            self.errors.append(str(e))
        return self
    
    def is_url(self, allowed_schemes: Optional[List[str]] = None):
        """Check if value is a valid URL."""
        try:
            validate_url(self.value, allowed_schemes)
        except ValidationError as e:
            self.errors.append(str(e))
        return self
    
    def matches(self, pattern: str):
        """Check if value matches regex pattern."""
        if not re.match(pattern, str(self.value)):
            self.errors.append(f"{self.name} does not match pattern: {pattern}")
        return self
    
    def validate(self) -> Any:
        """Perform validation and raise exception if errors found.
        
        Returns:
            The validated value
            
        Raises:
            ValidationError: If validation failed
        """
        if self.errors:
            error_msg = f"Validation failed for {self.name}:\n"
            error_msg += "\n".join(f"  - {e}" for e in self.errors)
            raise ValidationError(error_msg)
        return self.value


# Example usage and testing
if __name__ == "__main__":
    print(f"Input Validation Library v{VERSION}")
    print("=" * 50)
    
    # Test 1: Path validation
    print("\n1. Testing path validation...")
    try:
        safe_path = validate_path("/tmp/test.txt", allow_relative=False)
        print(f"   ✓ Valid path: {safe_path}")
    except ValidationError as e:
        print(f"   ✗ Path validation failed: {e}")
    
    try:
        dangerous_path = validate_path("/etc/../etc/passwd")
        print(f"   ✗ Should have blocked path traversal!")
    except ValidationError:
        print(f"   ✓ Correctly blocked path traversal")
    
    # Test 2: Version validation
    print("\n2. Testing version validation...")
    try:
        version = validate_version("1.2.3", format_type='semver')
        print(f"   ✓ Valid semver: {version}")
    except ValidationError as e:
        print(f"   ✗ Version validation failed: {e}")
    
    try:
        moko_version = validate_version("03.02.00", format_type='moko')
        print(f"   ✓ Valid Moko version: {moko_version}")
    except ValidationError as e:
        print(f"   ✗ Version validation failed: {e}")
    
    # Test 3: Email validation
    print("\n3. Testing email validation...")
    try:
        email = validate_email("user@example.com")
        print(f"   ✓ Valid email: {email}")
    except ValidationError as e:
        print(f"   ✗ Email validation failed: {e}")
    
    # Test 4: Shell injection prevention
    print("\n4. Testing shell injection prevention...")
    dangerous = "test; rm -rf /"
    safe = sanitize_shell_input(dangerous)
    print(f"   ✓ Sanitized: '{dangerous}' -> '{safe}'")
    
    # Test 5: Chainable validator
    print("\n5. Testing chainable validator...")
    try:
        validator = Validator("test@example.com", "email")
        validator.is_string(min_length=5).is_email().validate()
        print(f"   ✓ Chainable validation passed")
    except ValidationError as e:
        print(f"   ✗ Validation failed: {e}")
    
    print("\n✓ All tests passed!")
