<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation; either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP:  MokoStandards
 INGROUP:  Documentation
	REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE:  template-api-endpoint.md
 VERSION:  2.0
 BRIEF:  API Endpoint Template
 PATH:  ./docs/templates/template-api-endpoint.md
 NOTE:
-->

# API Endpoint Template

**.GitHub:** Documentation Change issue template → [./.github/ISSUE_TEMPLATE/docs_update.md](/mnt/data/template-api-endpoint.md)

## Endpoint Summary

Describe the purpose and high-level function of this endpoint.

## Request

Detail method, path, headers, parameters, and payload requirements.

## Response

Specify success responses, structure, and field definitions.

## Errors

Document error codes, conditions, and remediation guidance.

## Security Considerations

Outline authentication, authorization, rate limits, and data protection.

## Observability

Define logging, metrics, tracing, and monitoring expectations.

## Review and Approval

Include reviewers, approval date, and versioning notes.

## Example

````text
### Endpoint Summary
Retrieve a list of active users.

### Request
- Method: GET
- Path: /api/v1/users
- Headers:
  - Authorization: Bearer <token>
- Query Parameters:
  - status=active

### Response
200 OK
```
{
  "users": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ]
}
```

### Errors
- 401 Unauthorized: Missing or invalid token.
- 500 Internal Server Error: Unexpected server failure.

### Security Considerations
- Requires valid JWT.
- Logged under audit scope "user_list_access".

### Observability
- Metrics: api.users.list.count
- Trace: includes db query span

### Review and Approval
API Lead, Security Lead
````

## Metadata

```
Owner: Documentation Lead
Reviewers: Governance, Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 0.0.1   | TBD    | Initial stub |
