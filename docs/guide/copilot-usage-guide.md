<!--
SPDX-License-Identifier: GPL-3.0-or-later
Copyright (C) 2024-2026 Moko Consulting LLC

This file is part of MokoStandards.
For full license text, see LICENSE file in repository root.
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# GitHub Copilot Usage Guide

## Metadata

| Field | Value |
|-------|-------|
| **Document Type** | Guide |
| **Domain** | Development |
| **Applies To** | All Repositories |
| **Jurisdiction** | Organization-wide |
| **Owner** | Development Team |
| **Repo** | MokoStandards |
| **Path** | docs/guide/copilot-usage-guide.md |
| **VERSION** | 04.00.03 |
| **Status** | Active |
| **Last Reviewed** | 2026-01-28 |
| **Reviewed By** | Development Team |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 04.00.03 | 2026-01-28 | Development Team | Initial creation of Copilot usage guide |

---

## Introduction

This guide provides practical instructions, examples, and best practices for using GitHub Copilot effectively and safely within the organization. It complements the [Copilot Usage Policy](../policy/copilot-usage-policy.md) with hands-on guidance.

## Getting Started

### Prerequisites

- GitHub account with Copilot access
- Supported IDE installed (VS Code, JetBrains, Neovim, etc.)
- GitHub Copilot extension installed
- Familiarity with your programming language

### Initial Setup

1. **Install Copilot Extension**
	```bash
	# VS Code: Search for "GitHub Copilot" in extensions
	# Or install via command line
	code --install-extension GitHub.copilot
	```

2. **Sign In to GitHub**
	- Click GitHub icon in IDE
	- Authorize GitHub Copilot
	- Verify connection

3. **Configure Settings**
	```json
	// VS Code settings.json
	{
		"github.copilot.enable": {
			"*": true,
			"yaml": true,
			"markdown": true
		},
		"editor.inlineSuggest.enabled": true
	}
	```

4. **Verify Installation**
	- Open a code file
	- Start typing
	- Look for gray suggestion text
	- Press Tab to accept

## Core Features

### 1. Inline Code Completion

**How It Works**: As you type, Copilot suggests code completions in gray text.

**Usage**:
- **Accept**: Press `Tab`
- **Reject**: Keep typing or press `Esc`
- **Next Suggestion**: `Alt + ]` or `Option + ]`
- **Previous Suggestion**: `Alt + [` or `Option + [`

**Example**:
```python
# Type: def calculate_fibonacci(
# Copilot suggests complete function
def calculate_fibonacci(n: int) -> int:
	"""Calculate the nth Fibonacci number."""
	if n <= 1:
		return n
	return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
```

### 2. Copilot Chat

**Access**: Click chat icon in IDE or use command palette

**Usage Patterns**:

**Explain Code**:
```
Select code → Right-click → "Copilot: Explain This"
```

**Fix Issues**:
```
Select error → Right-click → "Copilot: Fix This"
```

**Generate Tests**:
```
Select function → Chat: "Write unit tests for this function"
```

**Refactor Code**:
```
Select code → Chat: "Refactor this to use async/await"
```

### 3. Copilot for CLI

**Setup**:
```bash
# Install
gh extension install github/gh-copilot

# Authenticate
gh auth login

# Test
gh copilot suggest "find all PDF files modified in last 7 days"
```

**Usage**:
```bash
# Get command suggestions
gh copilot suggest "compress all PNG files in current directory"

# Explain commands
gh copilot explain "tar -czf backup.tar.gz /home/user"
```

## Effective Prompt Engineering

### Principles

1. **Be Specific**: Provide clear requirements
2. **Add Context**: Include relevant information
3. **Specify Format**: Request particular style/structure
4. **Iterate**: Refine prompts based on results

### Comment-Driven Development

Use comments to guide Copilot:

```python
# Create a function that:
# - Validates email addresses using regex
# - Returns True if valid, False otherwise
# - Handles None and empty strings
# - Uses standard email regex pattern
def validate_email(email: str) -> bool:
	# Copilot will generate implementation
```

### Function Signatures

Start with clear signatures:

```typescript
interface User {
	id: string;
	name: string;
	email: string;
}

// Copilot understands context from interface
async function fetchUserById(id: string): Promise<User> {
	// Implementation suggested based on signature
}
```

### Test-Driven Prompting

Write tests first, let Copilot implement:

```javascript
describe('calculateDiscount', () => {
	it('should apply 10% discount for orders over $100', () => {
		expect(calculateDiscount(100)).toBe(90);
	});

	it('should apply 20% discount for orders over $500', () => {
		expect(calculateDiscount(500)).toBe(400);
	});
});

// Now implement function - Copilot knows requirements from tests
function calculateDiscount(amount) {
	// Implementation suggested based on tests
}
```

## Common Use Cases

### 1. Writing Boilerplate Code

**REST API Endpoint**:
```python
# FastAPI endpoint to create a new user with validation
@app.post("/users")
async def create_user(user: UserCreate):
	# Copilot generates:
	# - Validation logic
	# - Database insertion
	# - Error handling
	# - Response formatting
```

**Database Model**:
```python
# SQLAlchemy model for Product with timestamps, soft deletes
class Product(Base):
	# Copilot generates:
	# - Table name
	# - Columns with proper types
	# - Relationships
	# - Timestamps
	# - Soft delete flag
```

### 2. Writing Tests

**Unit Test Template**:
```python
# Write comprehensive unit tests for the User class
# Include tests for:
# - User creation
# - Email validation
# - Password hashing
# - User authentication
# - Edge cases and error handling

import pytest
from models import User

# Copilot generates complete test suite
```

**Test Data Generation**:
```python
# Generate realistic test data for user testing
# Include various edge cases (empty strings, special characters, etc.)
def create_test_users():
	# Copilot generates diverse test data
```

### 3. Documentation

**Docstrings**:
```python
def process_payment(amount, currency, payment_method):
	"""
	# Just type opening quotes, Copilot suggests complete docstring:
	# - Description
	# - Args
	# - Returns
	# - Raises
	# - Examples
	"""
```

**README Generation**:
```markdown
<!-- Write a comprehensive README for this Python package
Include:
- Project description
- Installation instructions
- Usage examples
- API documentation
- Contributing guidelines
- License information
-->

# Copilot generates structured README
```

### 4. Code Refactoring

**Modernize Code**:
```python
# Chat: "Convert this callback-based code to use async/await"
# Select old code, Copilot refactors
```

**Improve Error Handling**:
```python
# Chat: "Add comprehensive error handling with specific exception types"
# Copilot adds try/except blocks with proper error messages
```

**Optimize Performance**:
```python
# Chat: "Optimize this function for better performance"
# Copilot suggests improvements
```

### 5. Learning New APIs

**Exploring Libraries**:
```python
# I want to use requests library to:
# - Make GET request with authentication header
# - Handle timeouts and retries
# - Parse JSON response
# - Handle errors gracefully

import requests

# Copilot shows proper library usage
```

**Framework Patterns**:
```javascript
// Create a React component using hooks for:
// - Fetching data from API on mount
// - Loading and error states
// - Displaying data in a table
// - Pagination support

import React, { useState, useEffect } from 'react';

// Copilot generates proper React patterns
```

### 6. Converting Between Languages

**Language Translation**:
```
Chat: "Convert this Python function to TypeScript with proper type annotations"
```

```python
# Python version
def calculate_total(items):
	return sum(item['price'] * item['quantity'] for item in items)
```

```typescript
// TypeScript version (Copilot generates)
interface Item {
	price: number;
	quantity: number;
}

function calculateTotal(items: Item[]): number {
	return items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}
```

## Advanced Techniques

### 1. Multi-Step Prompts

Break complex tasks into steps:

```python
# Step 1: Define data structure for a shopping cart
class ShoppingCart:
	# Copilot generates structure

# Step 2: Implement add_item method with quantity validation
	def add_item(self, product, quantity):
		# Copilot generates implementation

# Step 3: Implement calculate_total with tax and discounts
	def calculate_total(self, tax_rate, discount_code=None):
		# Copilot generates calculation logic
```

### 2. Context Building

Provide context through code structure:

```python
# config.py - Define constants Copilot can reference
MAX_ITEMS_PER_ORDER = 50
SHIPPING_COST_THRESHOLD = 100

# cart.py - Copilot uses constants from config
from config import MAX_ITEMS_PER_ORDER, SHIPPING_COST_THRESHOLD

class ShoppingCart:
	def validate_item_count(self):
		# Copilot knows to check against MAX_ITEMS_PER_ORDER
```

### 3. Pattern Replication

Show Copilot the pattern once, it replicates:

```python
# First function - you write
def get_user(user_id: str) -> User:
	"""Fetch user by ID."""
	result = db.query(User).filter(User.id == user_id).first()
	if not result:
		raise NotFoundException(f"User {user_id} not found")
	return result

# Second function - Copilot follows pattern
def get_product(product_id: str) -> Product:
	# Copilot replicates the same pattern
```

### 4. Contextual Comments

Use inline comments to guide specific sections:

```python
def process_order(order_data):
	# Validate order data structure
	# (Copilot generates validation)

	# Calculate total with tax
	# (Copilot generates calculation)

	# Check inventory availability
	# (Copilot generates inventory check)

	# Process payment
	# (Copilot generates payment processing)

	# Send confirmation email
	# (Copilot generates email logic)
```

## Language-Specific Tips

### Python

**Best Practices**:
```python
# Always specify type hints for better suggestions
def calculate_discount(price: float, discount_percent: float) -> float:

# Request specific testing framework
# Write unit tests using pytest for this function

# Specify docstring style
def process_data(data: list) -> dict:
	"""Process data and return summary statistics.

	Google-style docstring with:
	- Clear description
	- Args and Returns sections
	- Examples
	"""
```

### JavaScript/TypeScript

**Best Practices**:
```typescript
// Specify TypeScript for better type inference
interface ApiResponse<T> {
	data: T;
	error?: string;
	status: number;
}

// Request specific framework
// Create React component with TypeScript and hooks

// Specify async pattern preference
// Use async/await instead of Promises
```

### Go

**Best Practices**:
```go
// Specify error handling approach
// Implement with idiomatic Go error handling

// Request interface usage
// Define interface for dependency injection

// Specify testing style
// Write table-driven tests for this function
```

### Shell Scripts

**Best Practices**:
```bash
#!/bin/bash
# Create a bash script that:
# - Includes proper error handling (set -euo pipefail)
# - Has usage documentation
# - Validates all inputs
# - Uses quoted variables
# - Includes logging

# Copilot generates safe shell script
```

## Troubleshooting

### Issue: Copilot Not Suggesting

**Solutions**:
1. Check extension is enabled
2. Verify GitHub authentication
3. Restart IDE
4. Check network connection
5. Review Copilot status in IDE

### Issue: Poor Quality Suggestions

**Solutions**:
1. Provide more context in comments
2. Write clearer function signatures
3. Show Copilot examples of desired pattern
4. Break complex tasks into smaller steps
5. Use Copilot Chat for clarification

### Issue: Irrelevant Suggestions

**Solutions**:
1. Be more specific in comments
2. Establish context with existing code
3. Use Chat to explain requirements
4. Cycle through suggestions (Alt + ] / [)
5. Write more descriptive variable names

### Issue: Security Concerns in Suggestions

**Solutions**:
1. Always review suggestions for security issues
2. Run security scanners (CodeQL)
3. Never accept suggestions with hardcoded secrets
4. Validate input handling
5. Check for injection vulnerabilities

## Integration with Development Workflow

### Pre-Coding

1. **Review Requirements**: Understand what needs to be built
2. **Plan Architecture**: Sketch high-level design
3. **Write Tests First**: TDD approach guides Copilot
4. **Define Interfaces**: Clear contracts help suggestions

### During Coding

1. **Comment-Driven**: Write comments describing intent
2. **Accept/Modify**: Review and adapt suggestions
3. **Iterate**: Refine prompts if suggestions miss mark
4. **Test Continuously**: Validate generated code works

### Post-Coding

1. **Review All Code**: Even Copilot-generated code
2. **Run Tests**: Ensure everything passes
3. **Security Scan**: Check for vulnerabilities
4. **Peer Review**: Get human review
5. **Document**: Update docs for changes

### Before Merge

Follow [Pre-Merge Checklist](../policy/copilot-pre-merge-checklist.md):
1. Update version numbers
2. Update CHANGELOG
3. Address review comments
4. Run security scans
5. Fix quality issues
6. Update documentation
7. Check for drift
8. Verify standards compliance

## Productivity Tips

### Keyboard Shortcuts

**VS Code**:
- `Tab` - Accept suggestion
- `Esc` - Reject suggestion
- `Alt + ]` - Next suggestion
- `Alt + [` - Previous suggestion
- `Ctrl + Enter` - Show all suggestions
- `Ctrl + Shift + P` - Copilot commands

**JetBrains**:
- `Tab` - Accept suggestion
- `Esc` - Reject suggestion
- `Alt + ]` - Next suggestion
- `Alt + [` - Previous suggestion

### Time-Saving Patterns

1. **Duplicate with Variation**: Copy-paste similar code, Copilot adapts
2. **Template Expansion**: Start with minimal template, let Copilot fill
3. **Batch Operations**: Write first operation, Copilot repeats for others
4. **Documentation Generation**: Write code first, generate docs after

### Quality Checklist

Before accepting Copilot suggestion:
- [ ] Does it match requirements?
- [ ] Is it secure?
- [ ] Does it follow coding standards?
- [ ] Is it efficient?
- [ ] Is it maintainable?
- [ ] Does it have proper error handling?
- [ ] Is it testable?

## Best Practices Summary

### DO ✅

- Review all suggestions before accepting
- Provide clear, specific prompts
- Use comments to guide generation
- Test generated code thoroughly
- Keep security and quality standards
- Iterate and refine prompts
- Learn from suggestions
- Combine with human expertise

### DON'T ❌

- Blindly accept without review
- Include sensitive data in prompts
- Skip testing generated code
- Ignore security warnings
- Accept code you don't understand
- Bypass code review
- Violate coding standards
- Treat as replacement for learning

## Resources

### Official Documentation
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Copilot Chat Guide](https://docs.github.com/en/copilot/github-copilot-chat)
- [Copilot CLI Guide](https://docs.github.com/en/copilot/github-copilot-in-the-cli)

### Internal Resources
- [Copilot Usage Policy](../policy/copilot-usage-policy.md)
- [Pre-Merge Checklist](../policy/copilot-pre-merge-checklist.md)
- [Code Review Guidelines](../policy/code-review-guidelines.md)
- [Security Scanning](../policy/security-scanning.md)

### Training
- Internal Copilot training sessions
- Team best practices sharing
- Monthly tips and tricks sessions
- Advanced techniques workshops

## Getting Help

### Support Channels

- **Technical Issues**: #copilot-support Slack channel
- **Best Practices**: #copilot-tips Slack channel
- **Policy Questions**: development-team@organization.com
- **Security Concerns**: security-team@organization.com

### Feedback

Share your experience:
- Success stories
- Challenges encountered
- Suggested improvements
- Training needs
- Policy feedback

## Conclusion

GitHub Copilot is a powerful tool that, when used correctly, can significantly enhance developer productivity while maintaining code quality and security. Remember:

- **You are responsible** for all code, Copilot-generated or not
- **Review everything** before accepting
- **Follow policies** and best practices
- **Keep learning** and improving your prompting skills
- **Share knowledge** with your team

For questions or suggestions, reach out to the Development Team.

---

**Guide Owner**: Development Team
**Last Updated**: 2026-01-28
**Next Review**: 2026-04-28
