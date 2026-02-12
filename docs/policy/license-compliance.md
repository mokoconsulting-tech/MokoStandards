[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# License Compliance

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

MokoStandards enforces strict license compliance to ensure legal use of software, protect intellectual property, and maintain open-source commitments. This document defines approved licenses, compliance procedures, and SPDX header requirements.

## Approved Open-Source Licenses

### Strongly Preferred

These licenses are strongly preferred for MokoStandards projects:

| License | SPDX Identifier | Use Case | Notes |
|---------|----------------|----------|-------|
| GNU GPLv3 | GPL-3.0-or-later | Primary license for MokoStandards | Copyleft, ensures freedom |
| MIT License | MIT | Permissive projects | Simple, permissive |
| Apache License 2.0 | Apache-2.0 | Patent-sensitive projects | Patent grant included |

### Approved for Use

These licenses are approved but should be evaluated case-by-case:

| License | SPDX Identifier | Compatible With | Notes |
|---------|----------------|-----------------|-------|
| BSD 2-Clause | BSD-2-Clause | Most projects | Permissive, simple |
| BSD 3-Clause | BSD-3-Clause | Most projects | Permissive, no endorsement clause |
| ISC License | ISC | Most projects | Similar to MIT |
| LGPL 3.0 | LGPL-3.0-or-later | Libraries | Weaker copyleft |
| Mozilla Public License 2.0 | MPL-2.0 | File-level copyleft | Good for plugins |

### Restricted Licenses

These licenses require special approval:

| License | SPDX Identifier | Restriction Reason |
|---------|----------------|-------------------|
| AGPL 3.0 | AGPL-3.0-or-later | Network copyleft (very strict) |
| GPLv2 only | GPL-2.0-only | Incompatible with GPLv3 |
| Creative Commons Non-Commercial | CC-BY-NC-* | Non-commercial restriction |

## License Compatibility Matrix

### GPL-3.0 Compatibility

When your project uses GPL-3.0-or-later:

| Can Include | License | Notes |
|------------|---------|-------|
| ✅ Yes | MIT, BSD, Apache-2.0, LGPL | Compatible and can be included |
| ✅ Yes | GPL-3.0, GPL-2.0-or-later | Same or compatible copyleft |
| ⚠️ Caution | MPL-2.0 | Compatible but complex |
| ❌ No | GPL-2.0-only | Version incompatibility |
| ❌ No | Proprietary, unlicensed | No license or incompatible |

### MIT/Apache Compatibility

When your project uses MIT or Apache-2.0:

| Can Include | License | Notes |
|------------|---------|-------|
| ✅ Yes | MIT, BSD, Apache-2.0, ISC | All permissive licenses compatible |
| ❌ No | GPL, LGPL, AGPL | Would force your project to GPL |
| ⚠️ Caution | MPL-2.0 | File-level copyleft, possible but complex |

## SPDX Header Requirements

All source files MUST include an SPDX license header.

### Standard PHP Header

```php
<?php
/**
 * Copyright (C) 2026 Your Name <email@example.com>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */
```

### Standard JavaScript/TypeScript Header

```javascript
/**
 * Copyright (C) 2026 Your Name <email@example.com>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */
```

### Shell Script Header

```bash
#!/bin/bash
# Copyright (C) 2026 Your Name <email@example.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
```

### Makefile Header

```makefile
# Copyright (C) 2026 Your Name <email@example.com>
# SPDX-License-Identifier: GPL-3.0-or-later
```

### YAML/Workflow Header

```yaml
# Copyright (C) 2026 Your Name <email@example.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
```

## Adding License Headers to Files

### Using Tools

#### PHP Files (PHP-CS-Fixer)

```php
// .php-cs-fixer.php
$header = <<<'EOF'
Copyright (C) 2026 Your Name <email@example.com>

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software...
EOF;

return (new PhpCsFixer\Config())
    ->setRules([
        'header_comment' => ['header' => $header],
    ]);
```

#### JavaScript Files (ESLint)

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'header/header': [2, 'block', [
      ' * Copyright (C) 2026 Your Name',
      ' * SPDX-License-Identifier: GPL-3.0-or-later',
    ]],
  },
};
```

### Bulk Adding Headers

```bash
# Add headers to all PHP files
find src -name "*.php" -exec sed -i '1i<?php\n/**\n * Copyright...\n */' {} \;

# Add headers to all JavaScript files
find src -name "*.js" -exec sed -i '1i/**\n * Copyright...\n */' {} \;
```

## Dependency License Scanning

### Automated Scanning

Use these tools to scan dependency licenses:

**For Composer (PHP)**:
```bash
composer licenses
```

**For npm (Node.js)**:
```bash
npm install -g license-checker
license-checker --summary
```

**For Python**:
```bash
pip install pip-licenses
pip-licenses --summary
```

### GitHub Actions Integration

```yaml
# .github/workflows/license-check.yml
- name: Check Dependency Licenses
  run: |
    # Composer
    composer licenses --no-dev | grep -v "MIT\|BSD\|Apache-2.0\|GPL\|LGPL" && exit 1 || true

    # npm
    npx license-checker --production --onlyAllow "MIT;BSD;Apache-2.0;GPL;LGPL;ISC"
```

## License Compliance Checklist

### For New Projects

- [ ] LICENSE file present in repository root
- [ ] LICENSE contains full text of chosen license
- [ ] All source files have SPDX headers
- [ ] README.md mentions license
- [ ] package.json/composer.json specifies license
- [ ] Third-party code properly attributed
- [ ] NOTICE file created (if using Apache-2.0)

### For Existing Projects

- [ ] Audit all source files for license headers
- [ ] Add missing headers
- [ ] Verify dependency licenses
- [ ] Document any license changes
- [ ] Update copyright years
- [ ] Remove or relicense incompatible code

### For Dependencies

- [ ] All dependencies have compatible licenses
- [ ] License files included for bundled dependencies
- [ ] Attribution provided in NOTICE file
- [ ] No GPL dependencies in MIT/Apache projects
- [ ] No unlicensed or proprietary dependencies

## Third-Party Code Attribution

### When Including Third-Party Code

1. **Check License Compatibility**
   - Verify license is compatible with your project
   - Check if modifications are allowed

2. **Preserve Original License**
   - Keep original license header
   - Don't remove author attribution
   - Include copy of original license

3. **Document Attribution**
   - Add entry to NOTICE file
   - Document in README if significant
   - Keep link to original source

4. **Modify Appropriately**
   - Mark modifications clearly
   - Follow original license requirements
   - Don't misrepresent authorship

### Example NOTICE File

```
MokoStandards
Copyright (C) 2026 Moko Consulting

This product includes software developed by third parties:

1. Some Library (https://github.com/example/library)
   Copyright (C) 2026 Original Author
   Licensed under MIT License

2. Another Component (https://example.com/component)
   Copyright (C) 2024 Another Author
   Licensed under Apache License 2.0

Full license texts can be found in the licenses/ directory.
```

## License Violations

### Identifying Violations

Common license violations:
- Using GPL code in proprietary software
- Removing license headers
- Not providing source code (GPL requirement)
- Using code without permission
- Violating attribution requirements

### Resolving Violations

If a violation is discovered:

1. **Stop Distribution** - Immediately cease distribution
2. **Assess Impact** - Determine scope of violation
3. **Contact Legal** - Consult with legal counsel
4. **Remediate**:
   - Replace incompatible code
   - Obtain proper licensing
   - Relicense if possible
   - Remove violating code
5. **Document Resolution** - Keep records of how violation was resolved
6. **Prevent Recurrence** - Update processes to prevent future violations

## Best Practices

1. **Choose License Early** - Select license at project start
2. **Be Consistent** - Use same license across related projects
3. **Document Everything** - Keep records of license decisions
4. **Scan Regularly** - Check dependencies frequently
5. **Educate Team** - Ensure team understands license requirements
6. **Use SPDX Identifiers** - Standard, machine-readable format
7. **Keep Current** - Update copyright years annually
8. **Seek Guidance** - Consult legal for complex situations

## Resources

- **SPDX License List**: https://spdx.org/licenses/
- **Choose a License**: https://choosealicense.com/
- **GPL Compatibility**: https://www.gnu.org/licenses/license-compatibility.html
- **OSI Approved Licenses**: https://opensource.org/licenses

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/license-compliance.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial license compliance documentation with SPDX headers and compatibility matrix |

## See Also

- [LICENSE](../LICENSE)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Code Review Guidelines](code-review-guidelines.md)
- [Dependency Review Workflow](../../templates/workflows/generic/dependency-review.yml.template)

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
