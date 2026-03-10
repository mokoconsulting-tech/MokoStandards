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
 INGROUP: MokoStandards.Design
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/google-fonts.md
 VERSION: 04.00.05
 BRIEF: Policy governing the use of Google Fonts across all Moko Consulting web projects
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.05-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Google Fonts Policy

## Purpose

This policy establishes standards for loading web fonts across all Moko Consulting governed web
projects. It designates Google Fonts as the approved web-font delivery mechanism, defines approved
typefaces and weights, mandates performance and privacy controls, and restricts self-hosted or
third-party font CDN alternatives.

## Scope

This policy applies to:

- All Moko WaaS (Joomla) client sites
- All MokoCRM (Dolibarr) front-end templates and custom modules with a browser UI
- Any other web-facing project under MokoStandards governance that renders text in a browser

Offline artefacts (PDF exports, native desktop/mobile apps, print workflows) are **exempt**; use
the locally bundled fonts in `templates/fonts/` for those contexts.

## Approved Delivery Mechanism

**Google Fonts (`fonts.googleapis.com`) is the only approved web-font CDN.**

The domains `fonts.googleapis.com` and `fonts.gstatic.com` are already on the MokoStandards
[approved network egress allow-list](./network-egress.md#google-services) and the
GitHub Copilot domain allow-list.

Self-hosted font files on project servers, other CDN providers (Typekit, Bunny Fonts, etc.), and
inline base64-encoded fonts are **prohibited** unless a documented exception is approved by the
engineering lead.

## Approved Font Families

The following Google Fonts families are approved for use in Moko Consulting web projects:

| Family | Weights | Intended Use |
|---|---|---|
| **Inter** | 400, 500, 600, 700 | Body text, UI labels, default sans-serif |
| **Roboto** | 400, 500, 700 | Alternative body text (legacy compatibility) |
| **Roboto Mono** | 400, 700 | Code blocks, monospace UI |
| **Merriweather** | 400, 700 | Long-form editorial / blog body copy |
| **Poppins** | 400, 600, 700 | Marketing headings, landing pages |
| **Open Sans** | 400, 600, 700 | General purpose sans-serif alternative |

Requesting additional font families requires a PR to this policy with a documented design
justification. The PR must be reviewed and approved before the font is used in any governed
project.

## Required Implementation

### HTML — Preconnect + Stylesheet

All pages loading Google Fonts **must** include preconnect hints immediately before the
stylesheet `<link>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">
```

The `display=swap` query parameter is **mandatory** (see Performance section below).

### CSS — font-display

When fonts are referenced via `@font-face` (e.g., in a custom CSS build), the `font-display`
descriptor **must** be set to `swap`:

```css
@font-face {
    font-family: 'Inter';
    src: url('https://fonts.gstatic.com/...');
    font-display: swap;
}
```

### Subsets and Variable Fonts

- Prefer the variable font API (`family=Inter:ital,opsz,wght@...`) when multiple weights
  are needed, as the Google Fonts API v2 automatically optimises served glyphs.
- Use the `text` parameter when only a fixed string is needed (e.g., a logo or heading)
  to receive a minimal character-subset response.
- Do **not** load the full Unicode range unless required by localisation.

## Performance Requirements

- Load no more than **two** font families per page.
- Load no more than **four** weights in total per page (across all families).
- Use `font-display: swap` at all times to prevent invisible-text flashes.
- Preconnect hints must be placed in `<head>` before the stylesheet link.

## Privacy and GDPR

Google Fonts serves font files from `fonts.gstatic.com` and logs request metadata (IP address,
user agent, referrer). For EU-resident users this constitutes a third-party data transfer.

Requirements:

1. Ensure your project's Privacy Policy discloses the use of Google Fonts.
2. For projects subject to strict GDPR consent requirements, load Google Fonts only after
   consent is granted, or switch to the locally bundled equivalent from `templates/fonts/`
   under a documented exception.
3. Do **not** pass user-identifying query parameters (e.g., session tokens) in font URLs.

## Locally Bundled Fonts (`templates/fonts/`)

The `templates/fonts/` directory provides TrueType files for **offline / print / native** use
cases where the Google Fonts CDN is unavailable. See the
[Font Assets catalogue](../templates/fonts/index.md) for the current inventory.

Bundled fonts must **not** be copied into a web project's public assets directory as a
self-hosting workaround for the CDN requirement. Raise a documented exception if CDN access
is genuinely unavailable in production.

## Enforcement

| Level | Enforcement |
|---|---|
| Web font CDN | **REQUIRED** — non-Google CDN or self-hosted web fonts trigger a standards compliance failure |
| `font-display: swap` | **REQUIRED** — missing descriptor triggers a standards compliance warning |
| Approved families | **REQUIRED** — unapproved families require policy amendment PR |
| Preconnect hints | **SUGGESTED** — recommended for performance; absence triggers a suggestion |
| Subset restriction | **SUGGESTED** — recommended for performance |

## Exceptions

Documented exceptions must be recorded in the repository's `.moko-standards` file under
`exceptions.google_fonts` with:

- Reason for exception
- Alternative approach used
- Approving engineer name and date
- Planned remediation date (if temporary)

## Related Policies

- [Network Egress Policy](./network-egress.md) — approves `fonts.googleapis.com` and `fonts.gstatic.com`
- [Font Assets (templates/fonts/)](../templates/fonts/index.md) — locally bundled fonts for offline use
- [Image Assets (templates/images/)](../templates/images/index.md) — brand images and favicon assets

## Metadata

| Field         | Value                                                  |
| ------------- | ------------------------------------------------------ |
| Document Type | Policy                                                 |
| Domain        | Design / Frontend                                      |
| Applies To    | All web-facing governed repositories                   |
| Jurisdiction  | Tennessee, USA                                         |
| Owner         | Moko Consulting                                        |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards   |
| Path          | /docs/policy/google-fonts.md                           |
| Version       | 04.00.05                                               |
| Status        | Active                                                 |
| Last Reviewed | 2026-03-10                                             |
| Reviewed By   | Engineering Team                                       |

## Revision History

| Date       | Author         | Change                   | Notes                                           |
| ---------- | -------------- | ------------------------ | ----------------------------------------------- |
| 2026-03-10 | GitHub Copilot | Initial policy created   | Google Fonts as approved web-font CDN           |
