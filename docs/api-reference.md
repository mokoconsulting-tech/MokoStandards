<!--	Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

	This file is part of a Moko Consulting project.

	SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

	This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License (./LICENSE.md).

	# FILE INFORMATION
	DEFGROUP:  MokoStandards
	INGROUP:  Documentation
	REPO:  https://github.com/mokoconsulting-tech/MokoStandards
	FILE:  api-reference.md
	VERSION:  2.0
	BRIEF:  API Reference Guide
	PATH:  ./docs/api-reference.md
	-->

# API Reference

## Navigation

**You are here:** Documentation -> API Reference

Related documents:

* [Documentation Index](./index.md)
* [Architecture Guide](./architecture.md)
* [Data Model Guide](./data-model.md)
* [Integrations Guide](./integrations.md)
* [Security Guide](./security.md)
* [Testing Guide](./testing.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The API Reference defines all public and internal API endpoints, request/response contracts, authentication requirements, and error structures.

This serves as the authoritative source for all client and service integrations.

## 2. Authentication

All API access requires one of the following:

* OAuth2 access token
* API key (service-to-service only)
* Signed webhook token (incoming integrations)

Requests without proper authentication must return:

```
401 Unauthorized
```

## 3. Conventions

### 3.1 URL Structure

* Base URL: `/api/v1/`
* Resources use plural nouns

### 3.2 Request Format

* JSON only
* Include `Content-Type: application/json`

### 3.3 Response Structure

All responses must include:

```
{
  "success": boolean,
  "data": {},
  "error": {}
}
```

## 4. Error Handling

Errors must follow a consistent structure:

```
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

Common codes:

* `INVALID_INPUT`
* `NOT_FOUND`
* `UNAUTHORIZED`
* `FORBIDDEN`
* `CONFLICT`
* `INTERNAL_ERROR`

## 5. Endpoint Structure

Each endpoint section must include:

* Method
* Path
* Authentication
* Description
* Request Body
* Response Body
* Status Codes

Templates stored under:

```
docs/templates/api/
```

## Metadata

```
Owner: API Lead (role not created yet)
Reviewers: Architecture, Integrations, QA
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes |
| ---------- | ------- | ------ | ----- |
| 2025-11-23 |         |        |       |
