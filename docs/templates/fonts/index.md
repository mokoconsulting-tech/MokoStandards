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
 DEFGROUP: MokoStandards.Templates.Fonts
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/templates/fonts/index.md
 VERSION: 04.00.05
 BRIEF: Catalogue of locally bundled font assets in templates/fonts/ and Google Fonts usage guidance
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.05-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Templates: Font Assets

## Overview

The `templates/fonts/` directory holds locally bundled typeface files that may be distributed
as part of governed repository templates. For runtime web use, **Google Fonts is the approved
delivery mechanism** — see the [Google Fonts Policy](../../policy/google-fonts.md) for full
requirements.

## Directory Structure

```
templates/fonts/
└── osaka-re.ttf    # Osaka Re — stylized logo font (TrueType)
```

## Asset Reference

### Bundled Fonts

| File | Format | Family | Style | Weight | Classification |
|---|---|---|---|---|---|
| `osaka-re.ttf` | TrueType (TTF) | Osaka Re | Regular | 400 | **Stylized Logo Font** |

#### osaka-re.ttf

**Osaka Re** is the **official stylized logo font** for Moko Consulting. It is used exclusively
for the brand wordmark, logo lockups, and stylized display contexts (e.g., splash screens,
printed brand collateral). It is **not** used for body text or UI labels — use
**Open Sans** (via Google Fonts) for those purposes.

**Usage:**

```css
@font-face {
    font-family: 'Osaka Re';
    src: url('/fonts/osaka-re.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}
```

**License note:** Confirm the license for `osaka-re.ttf` before distributing in client
deliverables. Bundled font files are only for internal tooling unless the licence permits
redistribution.

## Web Font Strategy

For all **web-facing** projects, fonts must be loaded via Google Fonts rather than
self-hosted files. The official body text font is **Open Sans** (400, 600, 700).
See the [Google Fonts Policy](../../policy/google-fonts.md) for:

- Approved font families and approved weights
- Required `<link>` preconnect and stylesheet tags
- `font-display: swap` requirement
- Privacy and GDPR considerations

## Governance

- Locally bundled fonts in `templates/fonts/` are supplemental for **offline / print / native**
  use cases only.
- Web projects must use the Google Fonts CDN unless a documented exception has been approved.
- New font files must be reviewed for licence compatibility before being added to this directory.
- Font updates must be submitted via PR to this repository.

## Related

- [Google Fonts Policy](../../policy/google-fonts.md)
- [Templates Catalog](../index.md)
- [Image Assets](../images/index.md)
- [Network Egress Policy](../../policy/network-egress.md) (approves `fonts.googleapis.com` + `fonts.gstatic.com`)

## Revision History

| Date       | Author         | Change                    | Notes                               |
| ---------- | -------------- | ------------------------- | ----------------------------------- |
| 2026-03-10 | GitHub Copilot | Initial catalogue created | Scanned templates/fonts/ assets     |
