<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Development
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/coding-style-guide.md
VERSION: 02.00.00
BRIEF: Universal coding style standards across all programming languages
-->

# Coding Style Guide

## Purpose

This document establishes universal coding style standards for all programming languages used across Moko Consulting projects. It defines formatting conventions, naming patterns, code organization, and documentation requirements to ensure consistent, readable, and maintainable code across the organization.

## Scope

This policy applies to:

- All application source code
- Custom modules and extensions
- Libraries and shared components
- API implementations
- Database queries and schema definitions
- Configuration code
- Test code

This policy does not apply to:

- Third-party libraries (follow their conventions)
- Generated code (unless we control the generator)
- Legacy code (unless actively refactoring)

## Responsibilities

### Developers

Responsible for:

- Following coding style standards
- Running linters and formatters
- Writing self-documenting code
- Requesting clarification when standards conflict
- Proposing improvements to standards

### Code Reviewers

Responsible for:

- Enforcing coding style in reviews
- Providing constructive feedback
- Ensuring consistency across codebase
- Approving style exceptions
- Documenting style decisions

### Technical Leads

Accountable for:

- Defining language-specific standards
- Resolving style conflicts
- Approving linter configurations
- Maintaining this guide
- Training teams on standards

## Universal Principles

### Readability First

**Code is read far more often than it is written.**

- Prioritize clarity over cleverness
- Use descriptive names
- Keep functions small and focused
- Avoid deep nesting
- Write code for humans, not just computers

### Consistency Over Perfection

- Follow project conventions even if you disagree
- Don't mix styles within a file
- Match existing code style when modifying files
- Propose changes through PRs, not inline

### Automated Formatting

- Use language-specific formatters when available
- Configure formatters in repository
- Run formatters before committing
- Integrate formatters in CI/CD
- Document formatter configuration

## Naming Conventions

### General Rules

**Be Descriptive**:
- Use full words, not abbreviations (except common acronyms)
- Names should reveal intent
- Avoid single-letter names except loop counters

**Be Consistent**:
- Follow language conventions (camelCase, snake_case, PascalCase)
- Use consistent patterns across codebase
- Match framework/library conventions

**Examples**:
```
✅ Good:
- getUserById()
- total_price
- MAX_RETRY_COUNT
- isAuthenticated

❌ Bad:
- get()
- tp
- max
- auth
```

### Language-Specific Naming

**PHP** (Dolibarr, WordPress):
- Classes: `PascalCase` - `UserManager`
- Functions/Methods: `camelCase` - `getUserData()`
- Variables: `$snake_case` - `$user_id`
- Constants: `UPPER_SNAKE_CASE` - `MAX_USERS`
- Database tables: `snake_case` with prefix - `llx_moko_users`

**JavaScript/TypeScript**:
- Classes: `PascalCase` - `UserService`
- Functions/Variables: `camelCase` - `getUserData()`
- Constants: `UPPER_SNAKE_CASE` - `API_URL`
- Files: `kebab-case` - `user-service.ts`
- Components: `PascalCase` - `UserProfile.tsx`

**Python**:
- Classes: `PascalCase` - `UserManager`
- Functions/Variables: `snake_case` - `get_user_data()`
- Constants: `UPPER_SNAKE_CASE` - `MAX_RETRIES`
- Modules: `snake_case` - `user_service.py`
- Private: prefix with `_` - `_internal_helper()`

**SQL**:
- Tables: `snake_case` - `user_accounts`
- Columns: `snake_case` - `created_at`
- Indexes: `idx_table_column` - `idx_users_email`
- Foreign keys: `fk_table_column` - `fk_user_id`

## Code Organization

### File Structure

**Single Responsibility**:
- One class per file (unless tightly coupled)
- Group related functions
- Separate concerns clearly

**Standard Order**:
1. File header/copyright
2. Imports/requires (grouped logically)
3. Constants
4. Type definitions/interfaces
5. Main code (classes, functions)
6. Exports

**Example (TypeScript)**:
```typescript
/**
 * Copyright (C) 2026 Moko Consulting
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

// External imports
import { Injectable } from '@nestjs/common';
import { Repository } from 'typeorm';

// Internal imports
import { User } from './entities/user.entity';
import { CreateUserDto } from './dto/create-user.dto';

// Constants
const MAX_USERNAME_LENGTH = 50;
const DEFAULT_ROLE = 'user';

// Types
interface UserSearchOptions {
  limit?: number;
  offset?: number;
}

// Main class
@Injectable()
export class UserService {
  // Implementation
}

// Exports
export { UserService, UserSearchOptions };
```

### Function Length

**Keep functions small**:
- Ideal: 10-20 lines
- Maximum: 50 lines
- If longer, extract helper functions
- One level of abstraction per function

**Example**:
```javascript
// ❌ Bad: Too long, multiple responsibilities
function processUserRegistration(data) {
  // 100 lines of validation, database, email, logging...
}

// ✅ Good: Extracted responsibilities
function processUserRegistration(data) {
  validateUserData(data);
  const user = createUser(data);
  sendWelcomeEmail(user);
  logRegistration(user);
  return user;
}
```

### Nesting Depth

**Maximum 3 levels of nesting**:
- Use early returns
- Extract conditions to functions
- Invert conditions when possible

**Example**:
```php
<?php
// ❌ Bad: Deep nesting
function processOrder($order) {
    if ($order) {
        if ($order->isValid()) {
            if ($order->hasStock()) {
                if ($order->paymentValid()) {
                    // Process order
                }
            }
        }
    }
}

// ✅ Good: Early returns
function processOrder($order) {
    if (!$order) return false;
    if (!$order->isValid()) return false;
    if (!$order->hasStock()) return false;
    if (!$order->paymentValid()) return false;
    
    // Process order
    return true;
}
```

## Formatting Standards

### Indentation

- **Use spaces, not tabs** (unless language convention dictates otherwise)
- **4 spaces** for PHP, Python
- **2 spaces** for JavaScript/TypeScript, JSON, YAML
- Configure editor to insert spaces
- Be consistent within each file

### Line Length

- **Soft limit**: 80 characters (aim for this)
- **Hard limit**: 120 characters (never exceed)
- Break long lines at logical points
- Indent continuation lines

### Whitespace

**Use blank lines to separate**:
- Logical sections
- Function definitions
- Class definitions
- Import groups

**No trailing whitespace**:
- Configure editor to strip on save
- Use linter to detect

**Space around operators**:
```javascript
// ✅ Good
const total = price + tax;
if (x === 5) {
  return true;
}

// ❌ Bad
const total=price+tax;
if(x===5){
  return true;
}
```

### Braces and Brackets

**PHP/JavaScript/TypeScript** (K&R style):
```javascript
// ✅ Opening brace on same line
function calculate() {
  if (condition) {
    return true;
  }
}

// ❌ Allman style not used
function calculate()
{
  if (condition)
  {
    return true;
  }
}
```

**Python** (use colons):
```python
# ✅ Follow PEP 8
def calculate():
    if condition:
        return True
```

## Comments and Documentation

### When to Comment

**Good reasons to comment**:
- Explain "why", not "what"
- Document complex algorithms
- Note non-obvious behavior
- Reference external documentation
- Mark TODOs with issue numbers
- Explain workarounds

**Bad reasons to comment**:
- Stating the obvious
- Replacing poor naming
- Leaving dead code
- Writing change logs (use git)

**Example**:
```php
<?php
// ✅ Good: Explains why
// Use bcrypt with cost 12 for PCI DSS compliance
$hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

// ❌ Bad: States the obvious
// Hash the password
$hash = password_hash($password, PASSWORD_BCRYPT);
```

### Function Documentation

**Document all public functions**:

**PHP (PHPDoc)**:
```php
<?php
/**
 * Calculate the total price including tax
 *
 * @param float $price Base price before tax
 * @param float $taxRate Tax rate as decimal (e.g., 0.20 for 20%)
 * @param bool $roundUp Whether to round up to nearest cent
 * @return float Total price including tax
 * @throws InvalidArgumentException If price or tax rate is negative
 */
function calculateTotal($price, $taxRate, $roundUp = false) {
  // Implementation
}
```

**JavaScript (JSDoc)**:
```javascript
/**
 * Fetch user data from the API
 * 
 * @param {number} userId - The ID of the user to fetch
 * @param {Object} options - Optional parameters
 * @param {boolean} options.includeProfile - Include profile data
 * @returns {Promise<User>} User object
 * @throws {ApiError} If user not found or API fails
 */
async function fetchUser(userId, options = {}) {
  // Implementation
}
```

**Python (Google style)**:
```python
def calculate_total(price: float, tax_rate: float, round_up: bool = False) -> float:
    """Calculate the total price including tax.
    
    Args:
        price: Base price before tax
        tax_rate: Tax rate as decimal (e.g., 0.20 for 20%)
        round_up: Whether to round up to nearest cent
    
    Returns:
        Total price including tax
    
    Raises:
        ValueError: If price or tax_rate is negative
    """
    # Implementation
```

## Error Handling

### Use Appropriate Error Handling

**PHP**:
```php
<?php
// Use exceptions for exceptional cases
try {
    $user = $userManager->getUser($id);
} catch (UserNotFoundException $e) {
    return null;
}

// Return error codes for expected failures
$result = $validator->validate($data);
if ($result->hasErrors()) {
    return $result->getErrors();
}
```

**JavaScript**:
```javascript
// Use try/catch for async operations
try {
  const data = await fetchData();
} catch (error) {
  console.error('Failed to fetch data:', error);
  throw new ApiError('Data fetch failed', error);
}

// Return null/undefined for optional values
function findUser(id) {
  return users.find(u => u.id === id) || null;
}
```

**Python**:
```python
# Use exceptions for error conditions
try:
    user = get_user(user_id)
except UserNotFoundError:
    return None

# Return None for optional values
def find_user(user_id: int) -> Optional[User]:
    return users.get(user_id)
```

### Error Messages

- Be specific and actionable
- Include context (what failed, why)
- Don't expose sensitive data
- Use consistent format

```javascript
// ✅ Good
throw new Error('Failed to create user: email "user@example.com" already exists');

// ❌ Bad
throw new Error('Error');
```

## Security Considerations

### Input Validation

- Validate all user input
- Use allow-lists, not deny-lists
- Sanitize before output
- Use parameterized queries

### Sensitive Data

- Never log passwords or tokens
- Never commit secrets
- Use environment variables
- Mask sensitive data in logs

### SQL Injection

```php
<?php
// ✅ Good: Prepared statement
$stmt = $db->prepare("SELECT * FROM users WHERE email = ?");
$stmt->execute([$email]);

// ❌ Bad: String concatenation
$sql = "SELECT * FROM users WHERE email = '$email'";
```

### XSS Prevention

```javascript
// ✅ Good: Escape output
<div>{escapeHtml(userInput)}</div>

// ❌ Bad: Direct output
<div dangerouslySetInnerHTML={{__html: userInput}} />
```

## Testing Standards

### Test Naming

```javascript
// ✅ Good: Descriptive
test('should return 404 when user not found', () => {});
test('should calculate total with 20% tax rate', () => {});

// ❌ Bad: Vague
test('test1', () => {});
test('works', () => {});
```

### Test Structure

- Arrange, Act, Assert pattern
- One assertion per test (when possible)
- Test edge cases
- Test error conditions

## Language-Specific Guides

For detailed language-specific standards, see:

- [Scripting Standards](scripting-standards.md) - Python automation scripts
- [CRM Development Standards](crm/development-standards.md) - PHP/Dolibarr
- [WaaS Development Standards](waas/development-standards.md) - PHP/Joomla

## Tools and Automation

### Recommended Linters

- **PHP**: PHP_CodeSniffer, PHPStan
- **JavaScript/TypeScript**: ESLint, Prettier
- **Python**: pylint, black, mypy
- **SQL**: sqlfluff

### Recommended Formatters

- **PHP**: PHP CS Fixer
- **JavaScript/TypeScript**: Prettier
- **Python**: black
- **SQL**: sqlformat

### Editor Configuration

**.editorconfig** (use in all projects):
```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{php,py}]
indent_style = space
indent_size = 4

[*.{js,ts,json,yml,yaml}]
indent_style = space
indent_size = 2
```

## Compliance and Enforcement

### Code Review Checklist

- [ ] Follows naming conventions
- [ ] Functions are appropriately sized
- [ ] Nesting depth is reasonable
- [ ] Code is well-documented
- [ ] No obvious security issues
- [ ] Tests are included
- [ ] Linter passes
- [ ] Formatter applied

### Automated Checks

- Run linters in CI/CD
- Block merge on style violations
- Use pre-commit hooks
- Generate style reports

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/coding-style-guide.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
