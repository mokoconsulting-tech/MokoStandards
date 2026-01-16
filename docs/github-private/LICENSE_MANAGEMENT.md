# License Management Guide

## Overview

This document outlines the process for managing software licenses for development tools used by Moko Consulting organization members.

**Key Principle:** Users may purchase their own licenses for Sublime Text and its SFTP plugin, or request organization-provided licenses through the issue template system.

## License Inventory

### Development Tools

| Tool | License Type | Cost | Organization Pool | Personal Purchase |
|------|--------------|------|-------------------|-------------------|
| **Sublime Text** | Individual | $99 USD | 20 licenses available | ✅ Yes, recommended |
| **Sublime SFTP** | Individual | $16 USD | Not provided | ✅ Yes, required for SFTP |
| **GitHub Copilot** | Organization | $19/user/month | Unlimited | N/A - Auto-provisioned |

### Infrastructure Licenses

| Service | Plan | Monthly Cost | Notes |
|---------|------|--------------|-------|
| **GitHub Enterprise Cloud** | Organization | Variable | Includes Advanced Security |
| **CodeQL** | Included | $0 | Part of GitHub Advanced Security |
| **GitHub Actions** | Pay-as-you-go | Variable | 50,000 minutes/month included |

---

## Sublime Text License Management

### Licensing Options

**Option 1: Personal Purchase** (Recommended)
- **Cost**: $99 USD one-time
- **Benefits**: 
  - Immediate access (no approval wait)
  - Keep license if you change jobs
  - Use for personal projects
  - No organizational restrictions
- **Purchase**: https://www.sublimetext.com/buy

**Option 2: Organization License Pool**
- **Cost**: Free to employee
- **Process**: Request via GitHub issue
- **Pool Size**: 20 licenses available
- **Timeline**: 1-2 business days approval
- **Restriction**: Return license upon leaving organization

### When to Use Each Option

**Choose Personal Purchase if:**
- You want immediate access
- You plan to use Sublime Text long-term
- You work on personal projects
- You prefer ownership

**Choose Organization License if:**
- Budget constraints
- Temporary/trial use
- Organization mandate for centralized management
- You only need it for work projects

### Requesting Organization License

**For Organization Members who choose organization license:**

1. **Open an Issue** in the MokoStandards repository:
   ```
   Title: [LICENSE REQUEST] Sublime Text - [Your Name]
   Template: .github/ISSUE_TEMPLATE/request-license.md
   ```

2. **Provide Required Information**:
   ```markdown
   - **Name**: Your full name
   - **GitHub Username**: @yourusername
   - **Team**: Your team/department
   - **Email**: work@mokoconsulting.tech
   - **Justification**: Brief reason for license need
   - **Platform**: Windows / macOS / Linux
   - **License Type**: Organization (or specify if you purchased personally)
   ```

3. **Approval Process**:
   - Manager approval (1 business day)
   - Admin verification (same day)
   - License key sent via encrypted email

4. **Expected Timeline**: 1-2 business days

### Personal License Registration (Optional)

If you purchased your own Sublime Text license, you may optionally register it with the organization for support purposes:

1. Open issue with title: `[LICENSE REGISTRATION] Sublime Text Personal - [Your Name]`
2. Indicate you have purchased your own license
3. Organization will note in records for support purposes
4. No license key needs to be shared

**Benefits of registration:**
- Organization aware you have access
- Eligible for organizational support/training
- Helps with team planning

---

## Sublime Text SFTP Plugin

### Personal Purchase Required

**Sublime SFTP is a separate purchase** ($16 USD) and is **NOT provided by the organization**.

All users must purchase their own SFTP plugin license if they need remote development capabilities.

### Why Personal Purchase Only?

- **Low cost**: $16 USD is minimal investment
- **Personal benefit**: Useful for personal projects and career development
- **Lifetime license**: One-time purchase, use forever
- **Portable**: Keep it if you change jobs

### SFTP Plugin Acquisition

1. **Purchase directly**: https://codexns.io/products/sftp_for_sublime
2. **Cost**: $16 USD one-time purchase
3. **License**: Tied to your email, use on all your machines
4. **Activation**: Enter license in Sublime Text

**Registration with organization**: Optional, no need to notify organization of SFTP plugin purchase.

### Who Needs SFTP Plugin?

- ✅ Developers working on remote servers (Joomla/Dolibarr)
- ✅ DevOps engineers managing server configurations
- ✅ Anyone regularly editing files on staging/production servers
- ❌ Developers working entirely locally with git

### SFTP Plugin Alternatives (Free)

If you prefer not to purchase SFTP plugin:

| Tool | Cost | Pros | Cons |
|------|------|------|------|
| **VS Code Remote-SSH** | Free | Full IDE features remotely | Heavier than Sublime |
| **rsync + file watchers** | Free | Scriptable, flexible | Manual setup required |
| **Git-based workflows** | Free | Version controlled | Not immediate sync |
| **SSHFS mounts** | Free | Transparent file access | Performance overhead |

---

## GitHub Copilot

### Automatic Provisioning

All organization members automatically have access to GitHub Copilot.

**Activation**:
1. Install GitHub Copilot extension in your IDE
2. Sign in with your GitHub organization account
3. Copilot automatically enabled for organization members

**No manual request needed** - automatic via organization membership.

---

## Issue Template for License Requests

Location: `.github/ISSUE_TEMPLATE/request-license.md`

```markdown
---
name: License Request
about: Request an organization license for Sublime Text or JetBrains tools
title: '[LICENSE REQUEST] [Tool Name] - [Your Name]'
labels: ['license-request', 'admin']
assignees: ['@mokoconsulting-tech/admins']
---

## License Request

### Tool Information
**Tool Name**: Sublime Text

**License Type Requested**: Organization Pool

**Personal Purchase**: 
- [ ] I prefer to purchase my own license (Sublime Text only - $99)
- [ ] I prefer an organization license (if available)
- [ ] I have already purchased my own license (registration only)

### Requestor Information
**Name**: 
**GitHub Username**: @
**Email**: 
**Team/Department**: 
**Manager**: @

### Justification
**Why do you need this license?**


**Primary use case**:
- [ ] Remote development (SFTP)
- [ ] Local development
- [ ] Code review
- [ ] Documentation editing
- [ ] Other (specify):

**Alternative tools considered**:


### Platform
- [ ] Windows
- [ ] macOS  
- [ ] Linux (distribution: ________)

### Urgency
- [ ] Urgent (needed within 24 hours)
- [ ] Normal (1-2 business days)
- [ ] Low priority (when available)

### Acknowledgment
- [ ] I have read the License Management Policy
- [ ] I understand Sublime SFTP plugin ($16) is a separate personal purchase
- [ ] I understand organization licenses must be returned upon departure
- [ ] I understand personal purchases are an alternative option for Sublime Text
- [ ] I agree to the terms of use

---

**For Admin Use Only**
- [ ] Manager approval received
- [ ] License available in pool (or marked as personal purchase)
- [ ] License key sent (organization) OR user purchased personally
- [ ] Activation confirmed
- [ ] Added to license tracking sheet
```

---

## License Compliance

### Organization License Tracking

For organization-provided licenses only:

**Quarterly audits** to ensure compliance:

1. **Active license count** vs active developers
2. **License usage tracking** via audit logs
3. **Revoke unused licenses** (>90 days inactive)
4. **Renewal planning** for expiring subscriptions

### Personal License Policy

- **Personal purchases** are not tracked by organization
- **Optional registration** for support purposes
- **User responsibility** to maintain personal licenses
- **Organization** provides guidance but not management

### Compliance Requirements (Organization Licenses)

- **Track all licenses** in internal database
- **Maintain proof of purchase** for audits
- **Ensure user attribution** (name tied to license)
- **Document transfers** when users change roles
- **Retain records** for 7 years

---

## Cost Management

### Organization Budget Allocation

| Team | Annual Budget | Primary Tools | Notes |
|------|---------------|---------------|-------|
| Development | $15,000 | Sublime Text pool, GitHub Copilot | ~$6k savings from personal purchases |
| DevOps | $10,000 | GitHub, Sublime Text | Reduced costs via personal licenses |
| QA | $8,000 | GitHub, minimal tooling | Primarily GitHub tools |

**Savings:** Encouraging personal Sublime Text purchases saves ~$6,000/year in organizational licensing costs.

### Cost Optimization Strategies

**Organization:**
- **License pooling** - Share licenses across teams
- **Usage monitoring** - Reclaim inactive licenses
- **Negotiated pricing** - Bulk discounts with GitHub
- **Personal purchase encouragement** - For Sublime Text (saves org budget)

**Personal:**
- **One-time purchases** - Sublime Text + SFTP = $115 total, lifetime use
- **Career investment** - Tools you keep regardless of employer
- **Tax deduction** - May be deductible as professional development (consult tax advisor)

---

## Alternative Tools (Free)

For team members not requiring licensed tools:

### Free IDEs

| Tool | Purpose | Recommendation |
|------|---------|----------------|
| **VS Code** | General development | Excellent free alternative to Sublime |
| **Vim/Neovim** | Terminal-based editing | For experienced users |
| **Eclipse PDT** | PHP development | Free alternative for PHP |

### When to Use Free Alternatives

- **Learning/Training**: Students or new hires evaluating options
- **Light usage**: Occasional editing
- **Personal projects**: Non-organizational work
- **Budget constraints**: Personal budget limitations

---

## Support & Questions

### License Request Issues

**Problem**: Request not processed within 2 business days  
**Solution**: Ping `@mokoconsulting-tech/admins` in issue

**Problem**: License key not working  
**Solution**: 
1. Verify copy-pasted correctly (no extra spaces/line breaks)
2. Contact admin for key verification
3. May need to request new key

**Problem**: Want to switch from organization to personal license  
**Solution**: 
1. Purchase personal license
2. Update issue with registration info
3. Return organization license to pool

### Personal Purchase Questions

**Question**: Can I expense a personal Sublime Text purchase?  
**Answer**: No, personal purchases are not reimbursable. Organization provides pool licenses as alternative.

**Question**: Can I use my personal license for work?  
**Answer**: Yes, personal licenses can be used for work and personal projects.

**Question**: What if I leave the organization?  
**Answer**: Personal licenses are yours to keep. Organization licenses must be returned.

### Contacts

- **License administration**: license-admin@mokoconsulting.tech
- **Budget/procurement**: finance@mokoconsulting.tech
- **Technical support**: dev@mokoconsulting.tech

---

## Summary: Sublime Text Decision Matrix

| Factor | Personal Purchase | Organization License |
|--------|-------------------|---------------------|
| **Cost to you** | $99 + $16 SFTP = $115 | $0 + $16 SFTP = $16 |
| **Approval wait** | None (immediate) | 1-2 business days |
| **Keep if leave job** | ✅ Yes | ❌ No, must return |
| **Personal use** | ✅ Yes | ❌ No |
| **Lifetime access** | ✅ Yes | ❌ Only while employed |
| **Support** | Sublime HQ + optional org registration | Organization provided |
| **Recommendation** | **Best for long-term users** | **Best for trial/temporary** |

**Bottom Line:** For most developers planning long-term careers, personal purchase ($115 one-time) provides better value than organization license (temporary access only).

---

**Document Status**: Active Policy  
**Owner**: Engineering Management  
**Reviewers**: Finance, Legal, IT Security  
**Last Review**: 2026-01-16  
**Next Review**: 2027-01-16

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-16 | Added personal purchase option for Sublime Text and SFTP | GitHub Copilot |
| 2026-01-16 | Clarified SFTP plugin is personal purchase only | GitHub Copilot |
| 2026-01-16 | Updated cost savings from personal purchase policy | GitHub Copilot |
