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
 PATH: /docs/policy/branding.md
 VERSION: 04.00.05
 BRIEF: Moko Consulting branding policy — logo, typography, colour palette, and background assets
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.05-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Moko Consulting Branding Policy

## Purpose

This policy establishes the authoritative brand standards for Moko Consulting across all governed
repositories, templates, and client-facing artefacts. It defines the approved logo files,
typography stack, colour palette (with hex and RGB references), background assets, and the rules
for using them correctly in templates and web projects.

All designers, developers, and AI coding tools working in governed repositories must follow this
policy. Where a requirement contradicts a third-party theme or framework default, this policy
takes precedence.

## Scope

This policy applies to:

- All MokoWaaS (Joomla) client site templates
- All MokoCRM (Dolibarr) front-end templates and module UIs
- The MokoStandards repository itself (README, documentation, web interface)
- Any template file under `templates/` that produces user-visible output

---

## 1 · Logo

### Canonical Logo Files

All logo and wordmark assets live in `templates/images/primary/`. The files below are the only
approved sources. Do **not** create alternate versions or modify these files without design-lead
approval.

| File | Format | Use Case |
|---|---|---|
| `templates/images/primary/logo.png` | PNG (raster) | **Default** — README headers, HTML `<img>`, documentation |
| `templates/images/primary/logo.svg` | SVG (vector) | Web pages, print, any scalable context |
| `templates/images/primary/logo_tiger.png` | PNG (raster) | Tiger-head brand variant (alternative contexts) |
| `templates/images/primary/tigerhead_3.svg` | SVG (vector) | Decorative tiger-head illustration |

### Using the Logo in a Repository README

Reference the asset with a repo-relative path so the image renders on GitHub, in local checkouts,
and in forks without depending on an external URL:

```markdown
![Moko Consulting](templates/images/primary/logo.png)
```

### Using the Logo in an HTML Template

```html
<img src="/img/logo.png" alt="Moko Consulting" width="180" loading="lazy">
```

Sync `templates/images/primary/logo.png` to the project's `img/` directory via the bulk sync
definition, or copy it manually during initial project setup.

### Logo Don'ts

- Do **not** stretch, skew, or alter the aspect ratio.
- Do **not** place the logo on a background colour that creates insufficient contrast (minimum
  4.5:1 contrast ratio per WCAG 2.1 AA).
- Do **not** re-render the wordmark using any font other than Osaka Re (see §2).
- Do **not** use a pixelated or low-resolution version — use the SVG where possible.

---

## 2 · Typography

### Font Assignments

| Role | Family | Source | Weights |
|---|---|---|---|
| **Logo / Wordmark** | **Osaka Re** | `templates/fonts/osaka-re.ttf` (local TrueType) | 400 |
| **Body text / UI labels** | **Open Sans** | Google Fonts CDN | 400, 600, 700 |
| **Code / monospace** | **Roboto Mono** | Google Fonts CDN | 400, 700 |
| **Fallback (no CDN)** | `system-ui, -apple-system, 'Segoe UI', Arial, sans-serif` | System | — |

### Logo Font — Osaka Re

**Osaka Re** is used exclusively for the brand wordmark and stylized brand headings. It is
distributed as a local TrueType file and is **not** available on Google Fonts.

```css
@font-face {
	font-family: 'Osaka Re';
	src: url('/fonts/osaka-re.ttf') format('truetype');
	font-weight: 400;
	font-style: normal;
	font-display: swap;
}

.brand-wordmark {
	font-family: 'Osaka Re', sans-serif;
}
```

Do **not** use Osaka Re for body copy, UI labels, or any text longer than a short headline.

### Body Font — Open Sans

**Open Sans** is the official body-text font for all web-facing projects. Load it from Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap">
```

```css
body {
	font-family: 'Open Sans', system-ui, -apple-system, 'Segoe UI', Arial, sans-serif;
}
```

See the [Google Fonts Policy](./google-fonts.md) for CDN, `font-display`, performance, and
GDPR requirements.

---

## 3 · Colour Palette

The colour system is based on **Material Design 3** and is defined in
`templates/web/assets/css/app.css` as CSS custom properties. The tables below are the
authoritative reference; always use the named CSS variable in code rather than hard-coding
the hex value.

### 3.1 Brand Colours

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#6750A4](https://placehold.co/16x16/6750A4/6750A4.png) Primary | Main brand colour | `--md-sys-color-primary` | `#6750A4` | `rgb(103, 80, 164)` |
| ![#FFFFFF](https://placehold.co/16x16/FFFFFF/FFFFFF.png) On Primary | Text / icons on primary | `--md-sys-color-on-primary` | `#FFFFFF` | `rgb(255, 255, 255)` |
| ![#EADDFF](https://placehold.co/16x16/EADDFF/EADDFF.png) Primary Container | Low-emphasis primary surface | `--md-sys-color-primary-container` | `#EADDFF` | `rgb(234, 221, 255)` |
| ![#21005D](https://placehold.co/16x16/21005D/21005D.png) On Primary Container | Text on primary container | `--md-sys-color-on-primary-container` | `#21005D` | `rgb(33, 0, 93)` |

### 3.2 Secondary Colours

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#625B71](https://placehold.co/16x16/625B71/625B71.png) Secondary | Supporting brand colour | `--md-sys-color-secondary` | `#625B71` | `rgb(98, 91, 113)` |
| ![#FFFFFF](https://placehold.co/16x16/FFFFFF/FFFFFF.png) On Secondary | Text / icons on secondary | `--md-sys-color-on-secondary` | `#FFFFFF` | `rgb(255, 255, 255)` |
| ![#E8DEF8](https://placehold.co/16x16/E8DEF8/E8DEF8.png) Secondary Container | Low-emphasis secondary surface | `--md-sys-color-secondary-container` | `#E8DEF8` | `rgb(232, 222, 248)` |
| ![#1D192B](https://placehold.co/16x16/1D192B/1D192B.png) On Secondary Container | Text on secondary container | `--md-sys-color-on-secondary-container` | `#1D192B` | `rgb(29, 25, 43)` |

### 3.3 Tertiary Colours

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#7D5260](https://placehold.co/16x16/7D5260/7D5260.png) Tertiary | Accent / complementary colour | `--md-sys-color-tertiary` | `#7D5260` | `rgb(125, 82, 96)` |
| ![#FFFFFF](https://placehold.co/16x16/FFFFFF/FFFFFF.png) On Tertiary | Text / icons on tertiary | `--md-sys-color-on-tertiary` | `#FFFFFF` | `rgb(255, 255, 255)` |

### 3.4 Background and Surface

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#FFFBFE](https://placehold.co/16x16/FFFBFE/FFFBFE.png) Background | Page / canvas background | `--md-sys-color-background` | `#FFFBFE` | `rgb(255, 251, 254)` |
| ![#1C1B1F](https://placehold.co/16x16/1C1B1F/1C1B1F.png) On Background | Default text on background | `--md-sys-color-on-background` | `#1C1B1F` | `rgb(28, 27, 31)` |
| ![#FFFBFE](https://placehold.co/16x16/FFFBFE/FFFBFE.png) Surface | Card / sheet surface | `--md-sys-color-surface` | `#FFFBFE` | `rgb(255, 251, 254)` |
| ![#1C1B1F](https://placehold.co/16x16/1C1B1F/1C1B1F.png) On Surface | Text on surface | `--md-sys-color-on-surface` | `#1C1B1F` | `rgb(28, 27, 31)` |
| ![#E7E0EC](https://placehold.co/16x16/E7E0EC/E7E0EC.png) Surface Variant | Elevated surface / chip | `--md-sys-color-surface-variant` | `#E7E0EC` | `rgb(231, 224, 236)` |
| ![#49454F](https://placehold.co/16x16/49454F/49454F.png) On Surface Variant | Secondary text on surface | `--md-sys-color-on-surface-variant` | `#49454F` | `rgb(73, 69, 79)` |

### 3.5 Outline

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#79747E](https://placehold.co/16x16/79747E/79747E.png) Outline | Borders, dividers, input outlines | `--md-sys-color-outline` | `#79747E` | `rgb(121, 116, 126)` |
| ![#CAC4D0](https://placehold.co/16x16/CAC4D0/CAC4D0.png) Outline Variant | Subtle borders, table separators | `--md-sys-color-outline-variant` | `#CAC4D0` | `rgb(202, 196, 208)` |

### 3.6 Semantic Colours

#### Error

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#B3261E](https://placehold.co/16x16/B3261E/B3261E.png) Error | Destructive actions, validation failures | `--md-sys-color-error` | `#B3261E` | `rgb(179, 38, 30)` |
| ![#FFFFFF](https://placehold.co/16x16/FFFFFF/FFFFFF.png) On Error | Text / icons on error | `--md-sys-color-on-error` | `#FFFFFF` | `rgb(255, 255, 255)` |
| ![#F9DEDC](https://placehold.co/16x16/F9DEDC/F9DEDC.png) Error Container | Low-emphasis error surface | `--md-sys-color-error-container` | `#F9DEDC` | `rgb(249, 222, 220)` |
| ![#410E0B](https://placehold.co/16x16/410E0B/410E0B.png) On Error Container | Text on error container | `--md-sys-color-on-error-container` | `#410E0B` | `rgb(65, 14, 11)` |

#### Success

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#2E7D32](https://placehold.co/16x16/2E7D32/2E7D32.png) Success | Positive outcomes, confirmations | `--md-sys-color-success` | `#2E7D32` | `rgb(46, 125, 50)` |
| ![#C8E6C9](https://placehold.co/16x16/C8E6C9/C8E6C9.png) Success Container | Low-emphasis success surface | `--md-sys-color-success-container` | `#C8E6C9` | `rgb(200, 230, 201)` |
| ![#1B5E20](https://placehold.co/16x16/1B5E20/1B5E20.png) On Success Container | Text on success container | `--md-sys-color-on-success-container` | `#1B5E20` | `rgb(27, 94, 32)` |

#### Warning

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#F57C00](https://placehold.co/16x16/F57C00/F57C00.png) Warning | Cautions, partial failures | `--md-sys-color-warning` | `#F57C00` | `rgb(245, 124, 0)` |
| ![#FFE0B2](https://placehold.co/16x16/FFE0B2/FFE0B2.png) Warning Container | Low-emphasis warning surface | `--md-sys-color-warning-container` | `#FFE0B2` | `rgb(255, 224, 178)` |
| ![#E65100](https://placehold.co/16x16/E65100/E65100.png) On Warning Container | Text on warning container | `--md-sys-color-on-warning-container` | `#E65100` | `rgb(230, 81, 0)` |

#### Info

| Swatch | Role | CSS Variable | Hex | RGB |
|---|---|---|---|---|
| ![#0288D1](https://placehold.co/16x16/0288D1/0288D1.png) Info | Informational messages | `--md-sys-color-info` | `#0288D1` | `rgb(2, 136, 209)` |
| ![#B3E5FC](https://placehold.co/16x16/B3E5FC/B3E5FC.png) Info Container | Low-emphasis info surface | `--md-sys-color-info-container` | `#B3E5FC` | `rgb(179, 229, 252)` |

### 3.7 Terminal / Code-Output Colours

Used in the dark-theme log output panels (`templates/web/assets/css/app.css`).

| Swatch | Role | CSS Variable / Class | Hex | RGB |
|---|---|---|---|---|
| ![#1E1E1E](https://placehold.co/16x16/1E1E1E/1E1E1E.png) Terminal Background | Log panel background | `.md-log-container` | `#1E1E1E` | `rgb(30, 30, 30)` |
| ![#D4D4D4](https://placehold.co/16x16/D4D4D4/D4D4D4.png) Terminal Text | Default log text | `.md-log-container` | `#D4D4D4` | `rgb(212, 212, 212)` |
| ![#4FC3F7](https://placehold.co/16x16/4FC3F7/4FC3F7.png) Log Info | Info-level log lines | `.md-log-info` | `#4FC3F7` | `rgb(79, 195, 247)` |
| ![#81C784](https://placehold.co/16x16/81C784/81C784.png) Log Success | Success-level log lines | `.md-log-success` | `#81C784` | `rgb(129, 199, 132)` |
| ![#FFB74D](https://placehold.co/16x16/FFB74D/FFB74D.png) Log Warning | Warning-level log lines | `.md-log-warning` | `#FFB74D` | `rgb(255, 183, 77)` |
| ![#E57373](https://placehold.co/16x16/E57373/E57373.png) Log Error | Error-level log lines | `.md-log-error` | `#E57373` | `rgb(229, 115, 115)` |

### Colour Usage Rules

1. Always reference the CSS custom property (`var(--md-sys-color-primary)`) in templates and stylesheets — never hard-code the hex value.
2. Maintain a minimum **4.5:1 contrast ratio** (WCAG 2.1 AA) between foreground and background colours in all user-facing text.
3. Never use brand colours to convey meaning on their own — always pair colour with a label, icon, or pattern (colour-blind accessibility).
4. The semantic colours (Error, Success, Warning, Info) are reserved for their named semantic role; do not repurpose them for decoration.

---

## 4 · Background Assets

The canonical background images are stored in `templates/images/primary/` alongside the logo files.

| File | Format | Dimensions | Use Case |
|---|---|---|---|
| `templates/images/primary/background.png` | PNG (raster) | Full-width | Hero sections, slide decks, PDF covers |
| `templates/images/primary/background.svg` | SVG (vector) | Scalable | Web hero sections where vector scaling is required |

### Using the Background in CSS

```css
.hero {
	background-image: url('/img/background.svg');
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
}
```

Prefer the SVG version for web pages; use the PNG version for raster contexts such as email
clients, PDF generators, and native apps.

When the background image is placed behind text, ensure the text meets the **4.5:1 contrast
ratio** requirement. Apply a semi-transparent overlay if the raw image does not provide
sufficient contrast:

```css
.hero-overlay {
	background-color: rgba(33, 0, 93, 0.6); /* On Primary Container at 60 % opacity */
}
```

---

## 5 · Favicon and App Icons

| File | Size | Use Case |
|---|---|---|
| `templates/images/primary/favicon_256.png` | 256 × 256 px | **Sync template** — Dolibarr module `img/` directory |
| `templates/images/primary/favicon_120.png` | 120 × 120 px | General favicon |
| `templates/images/primary/favicon-96x96.png` | 96 × 96 px | General favicon |
| `templates/images/primary/favicon.svg` | Vector | Modern browsers (preferred) |
| `templates/images/primary/favicon.ico` | Multi-size ICO | Legacy browsers |
| `templates/images/primary/favicon.gif` | Animated GIF | Animated favicon (legacy only) |
| `templates/images/primary/apple-touch-icon.png` | 180 × 180 px | iOS home-screen shortcut |
| `templates/images/primary/web-app-manifest-192x192.png` | 192 × 192 px | PWA `manifest.json` |
| `templates/images/primary/web-app-manifest-512x512.png` | 512 × 512 px | PWA splash screen |

See [Image Assets](../templates/images/index.md) for full usage guidance.

---

## 6 · Template Integration Checklist

When creating or updating a template that uses brand assets, confirm:

- [ ] Logo sourced from `templates/images/primary/` (not an external URL)
- [ ] Wordmark uses Osaka Re via `@font-face` local file (`templates/fonts/osaka-re.ttf`)
- [ ] Body text uses Open Sans loaded from Google Fonts CDN (`display=swap`)
- [ ] `font-family` fallback includes `system-ui, -apple-system, Arial, sans-serif`
- [ ] All colours reference CSS custom properties (`var(--md-sys-color-*)`)
- [ ] Text contrast ≥ 4.5:1 against background (verified with a colour-contrast tool)
- [ ] Background image uses the SVG version for web; PNG for raster contexts
- [ ] No brand assets hard-coded with absolute external URLs

---

## 7 · Enforcement

| Rule | Enforcement Level |
|---|---|
| Logo sourced from `templates/images/primary/` | **REQUIRED** |
| Osaka Re for logo wordmark only | **REQUIRED** |
| Open Sans as body text font | **REQUIRED** |
| System-font fallback in `font-family` stack | **REQUIRED** |
| CSS colour variables (no hard-coded hex in templates) | **REQUIRED** |
| WCAG 2.1 AA contrast ratio (4.5:1) | **REQUIRED** |
| `display=swap` on Google Fonts stylesheet | **REQUIRED** — see [Google Fonts Policy](./google-fonts.md) |
| Background asset from `templates/images/primary/` | **REQUIRED** |
| Logo alt text on all `<img>` elements | **REQUIRED** |
| SVG logo preferred over raster for web | **SUGGESTED** |

---

## Related Policies

- [Google Fonts Policy](./google-fonts.md) — CDN, `font-display`, performance and GDPR rules
- [Network Egress Policy](./network-egress.md) — approves `fonts.googleapis.com` and `fonts.gstatic.com`
- [Image Assets catalogue](../templates/images/index.md) — full inventory of `templates/images/primary/`
- [Font Assets catalogue](../templates/fonts/index.md) — `templates/fonts/osaka-re.ttf` details
- [File Header Standards](./file-header-standards.md) — copyright header required in all templates

---

## Metadata

| Field         | Value                                                  |
| ------------- | ------------------------------------------------------ |
| Document Type | Policy                                                 |
| Domain        | Design / Branding                                      |
| Applies To    | All web-facing and template-producing governed repos   |
| Jurisdiction  | Tennessee, USA                                         |
| Owner         | Moko Consulting                                        |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards   |
| Path          | /docs/policy/branding.md                               |
| Version       | 04.00.05                                               |
| Status        | Active                                                 |
| Last Reviewed | 2026-03-10                                             |
| Reviewed By   | Engineering Team                                       |

## Revision History

| Date       | Author         | Change                | Notes                                                        |
| ---------- | -------------- | --------------------- | ------------------------------------------------------------ |
| 2026-03-10 | GitHub Copilot | Initial policy created | Colour palette tables, logo, typography, background assets  |
