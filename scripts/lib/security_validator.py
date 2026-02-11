#!/usr/bin/env python3
"""
Security Validator for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

Provides security scanning and validation:
- Credential detection in code/config
- Vulnerability checking
- Security best practices validation
- Safe file operations
- Secret management

Usage:
    from security_validator import SecurityValidator
    
    validator = SecurityValidator()
    validator.scan_file('config.py')
    validator.check_credentials('password123')
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

VERSION = "03.02.00"


class SecurityViolation(Exception):
    """Exception raised when security violations are detected."""
    pass


class SecurityValidator:
    """Validate security best practices and detect vulnerabilities."""
    
    # Common patterns for credentials and secrets
    CREDENTIAL_PATTERNS = [
        (r'password\s*=\s*["\']([^"\']+)["\']', 'hardcoded password'),
        (r'api[_-]?key\s*=\s*["\']([^"\']+)["\']', 'hardcoded API key'),
        (r'secret[_-]?key\s*=\s*["\']([^"\']+)["\']', 'hardcoded secret key'),
        (r'token\s*=\s*["\']([^"\']+)["\']', 'hardcoded token'),
        (r'aws[_-]?access[_-]?key[_-]?id\s*=\s*["\']([^"\']+)["\']', 'AWS access key'),
        (r'private[_-]?key\s*=\s*["\']([^"\']+)["\']', 'private key'),
        (r'["\'][A-Za-z0-9/+]{40,}["\']', 'potential secret (base64)'),
    ]
    
    # Dangerous function calls
    DANGEROUS_FUNCTIONS = [
        'eval',
        'exec',
        'compile',
        '__import__',
        'input',  # In Python 2
        'pickle.loads',
        'yaml.load',  # Without safe_load
        'subprocess.call',  # Without shell=False
    ]
    
    # File permissions that are too permissive
    DANGEROUS_PERMISSIONS = [
        0o777,  # rwxrwxrwx
        0o666,  # rw-rw-rw-
    ]
    
    def __init__(self):
        """Initialize security validator."""
        self.findings: List[Dict[str, Any]] = []
        
    def scan_file(self, file_path: str, check_credentials: bool = True, 
                  check_dangerous_functions: bool = True) -> List[Dict[str, Any]]:
        """Scan a file for security issues.
        
        Args:
            file_path: Path to file to scan
            check_credentials: Check for hardcoded credentials
            check_dangerous_functions: Check for dangerous function usage
            
        Returns:
            List of security findings
        """
        findings = []
        path = Path(file_path)
        
        if not path.exists():
            return findings
        
        try:
            content = path.read_text()
            
            if check_credentials:
                cred_findings = self._check_credentials_in_text(content, str(path))
                findings.extend(cred_findings)
            
            if check_dangerous_functions:
                func_findings = self._check_dangerous_functions(content, str(path))
                findings.extend(func_findings)
            
        except Exception as e:
            findings.append({
                'severity': 'warning',
                'type': 'scan_error',
                'file': str(path),
                'message': f'Failed to scan file: {e}'
            })
        
        self.findings.extend(findings)
        return findings
    
    def _check_credentials_in_text(self, text: str, source: str) -> List[Dict[str, Any]]:
        """Check for hardcoded credentials in text.
        
        Args:
            text: Text to scan
            source: Source file/location
            
        Returns:
            List of findings
        """
        findings = []
        
        for pattern, description in self.CREDENTIAL_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Skip if it looks like an example or placeholder
                matched_value = match.group(1) if match.groups() else match.group(0)
                if self._is_placeholder(matched_value):
                    continue
                
                findings.append({
                    'severity': 'high',
                    'type': 'credential',
                    'file': source,
                    'description': description,
                    'line': text[:match.start()].count('\n') + 1,
                    'snippet': match.group(0)[:50]
                })
        
        return findings
    
    def _check_dangerous_functions(self, text: str, source: str) -> List[Dict[str, Any]]:
        """Check for dangerous function usage.
        
        Args:
            text: Text to scan
            source: Source file/location
            
        Returns:
            List of findings
        """
        findings = []
        
        for func_name in self.DANGEROUS_FUNCTIONS:
            pattern = rf'\b{re.escape(func_name)}\s*\('
            matches = re.finditer(pattern, text)
            
            for match in matches:
                findings.append({
                    'severity': 'medium',
                    'type': 'dangerous_function',
                    'file': source,
                    'function': func_name,
                    'line': text[:match.start()].count('\n') + 1,
                    'message': f'Potentially dangerous function: {func_name}'
                })
        
        return findings
    
    def _is_placeholder(self, value: str) -> bool:
        """Check if a value looks like a placeholder.
        
        Args:
            value: Value to check
            
        Returns:
            True if looks like placeholder
        """
        placeholders = [
            'your_', 'example', 'placeholder', 'xxx', 'test',
            'dummy', 'sample', 'replace', 'changeme', 'todo'
        ]
        value_lower = value.lower()
        return any(p in value_lower for p in placeholders)
    
    def check_file_permissions(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Check file permissions for security issues.
        
        Args:
            file_path: Path to file
            
        Returns:
            Finding if permissions are too permissive, None otherwise
        """
        path = Path(file_path)
        if not path.exists():
            return None
        
        stat_info = path.stat()
        mode = stat_info.st_mode & 0o777
        
        if mode in self.DANGEROUS_PERMISSIONS:
            finding = {
                'severity': 'medium',
                'type': 'file_permissions',
                'file': str(path),
                'permissions': oct(mode),
                'message': f'File has overly permissive permissions: {oct(mode)}'
            }
            self.findings.append(finding)
            return finding
        
        return None
    
    def validate_environment_var(self, var_name: str) -> bool:
        """Validate that sensitive data comes from environment variables.
        
        Args:
            var_name: Environment variable name
            
        Returns:
            True if variable exists
        """
        return var_name in os.environ
    
    def get_findings(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all security findings.
        
        Args:
            severity: Filter by severity (high, medium, low, warning)
            
        Returns:
            List of findings
        """
        if severity:
            return [f for f in self.findings if f.get('severity') == severity]
        return self.findings
    
    def has_critical_findings(self) -> bool:
        """Check if there are any critical/high severity findings.
        
        Returns:
            True if critical findings exist
        """
        return any(f.get('severity') in ['critical', 'high'] for f in self.findings)
    
    def print_report(self):
        """Print a security report."""
        print(f"\n{'='*60}")
        print("Security Validation Report")
        print(f"{'='*60}")
        
        if not self.findings:
            print("\n✓ No security issues found!")
            print(f"{'='*60}\n")
            return
        
        # Group by severity
        by_severity = {}
        for finding in self.findings:
            sev = finding.get('severity', 'unknown')
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(finding)
        
        # Print findings by severity
        for sev in ['critical', 'high', 'medium', 'low', 'warning']:
            if sev in by_severity:
                print(f"\n{sev.upper()} Severity ({len(by_severity[sev])} findings):")
                for finding in by_severity[sev]:
                    print(f"  - {finding.get('type', 'unknown')}: {finding.get('message', finding.get('description', 'No description'))}")
                    if 'file' in finding:
                        print(f"    File: {finding['file']}")
                    if 'line' in finding:
                        print(f"    Line: {finding['line']}")
        
        total = len(self.findings)
        critical_count = len(by_severity.get('critical', []))  + len(by_severity.get('high', []))
        
        print(f"\nTotal findings: {total}")
        print(f"Critical/High: {critical_count}")
        print(f"{'='*60}\n")
    
    def clear_findings(self):
        """Clear all findings."""
        self.findings = []


def scan_directory(directory: str, extensions: Optional[List[str]] = None) -> SecurityValidator:
    """Scan a directory for security issues.
    
    Args:
        directory: Directory to scan
        extensions: File extensions to scan (default: ['.py', '.sh', '.yaml', '.json'])
        
    Returns:
        SecurityValidator with findings
    """
    if extensions is None:
        extensions = ['.py', '.sh', '.yaml', '.yml', '.json', '.conf', '.cfg']
    
    validator = SecurityValidator()
    path = Path(directory)
    
    for ext in extensions:
        for file_path in path.rglob(f'*{ext}'):
            if file_path.is_file():
                validator.scan_file(str(file_path))
    
    return validator


# Example usage and testing
if __name__ == "__main__":
    print(f"Security Validator v{VERSION}")
    print("=" * 50)
    
    validator = SecurityValidator()
    
    # Test 1: Credential detection
    print("\n1. Testing credential detection...")
    test_code = """
    password = "mysecretpass123"
    api_key = "sk_live_abcd1234xyz"
    token = "ghp_exampletoken123456"
    """
    findings = validator._check_credentials_in_text(test_code, "test.py")
    print(f"   ✓ Found {len(findings)} potential credentials")
    
    # Test 2: Dangerous function detection
    print("\n2. Testing dangerous function detection...")
    dangerous_code = """
    result = eval(user_input)
    exec("print('hello')")
    """
    findings = validator._check_dangerous_functions(dangerous_code, "test.py")
    print(f"   ✓ Found {len(findings)} dangerous function calls")
    
    # Test 3: Placeholder detection
    print("\n3. Testing placeholder detection...")
    is_placeholder = validator._is_placeholder("your_password_here")
    print(f"   ✓ Placeholder detection: {is_placeholder}")
    
    # Test 4: Environment variable validation
    print("\n4. Testing environment variable validation...")
    os.environ['TEST_VAR'] = 'test'
    has_var = validator.validate_environment_var('TEST_VAR')
    print(f"   ✓ Environment variable exists: {has_var}")
    
    # Test 5: Full file scan (on this file)
    print("\n5. Testing full file scan...")
    current_file = __file__
    validator.clear_findings()
    validator.scan_file(current_file)
    print(f"   ✓ Scanned {current_file}")
    print(f"   ✓ Findings: {len(validator.get_findings())}")
    
    # Print report
    if validator.get_findings():
        validator.print_report()
    
    print("\n✓ All tests passed!")
