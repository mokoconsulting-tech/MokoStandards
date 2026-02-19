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
DEFGROUP: MokoStandards.Training
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/training/session-6-git-github-workflow.md
VERSION: 04.00.01
BRIEF: Session 6 - Git, GitHub, and GitHub Projects workflow training
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 6: Git, GitHub & GitHub Projects Workflow

**Duration**: 2.5 hours  
**Format**: Interactive Workshop with Hands-on Exercises  
**Prerequisites**: Basic command line knowledge  
**Level**: Beginner to Intermediate

---

## Session Objectives

By the end of this session, you will:
- ✅ Understand Git fundamentals and core concepts
- ✅ Master the standard Git workflow for MokoStandards projects
- ✅ Create and manage branches following naming conventions
- ✅ Write effective commit messages following standards
- ✅ Create and review pull requests professionally
- ✅ Use GitHub Projects to track and manage work
- ✅ Integrate Git workflow with GitHub Projects boards
- ✅ Follow MokoStandards Git and GitHub policies

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:45 | Git Fundamentals & Standard Workflow | Presentation + Demo |
| 0:45-1:30 | GitHub Workflow & Pull Requests | Interactive Workshop |
| 1:30-2:00 | GitHub Projects for Work Management | Hands-on Practice |
| 2:00-2:30 | Complete Workflow Exercise | Guided Practice |

---

## Part 1: Git Fundamentals (45 minutes)

### What is Git?

Git is a distributed version control system that tracks changes in your code:
- ✅ **Distributed**: Every developer has a complete copy of the repository
- ✅ **Version Control**: Track all changes with complete history
- ✅ **Branching**: Work on features in isolation
- ✅ **Collaboration**: Multiple developers can work simultaneously
- ✅ **Integrity**: Cryptographic hashing ensures data integrity

### Git Repository Structure

```
repository/
├── .git/                    # Git database (hidden)
│   ├── objects/             # All commits, trees, blobs
│   ├── refs/                # Branch and tag references
│   ├── HEAD                 # Current branch pointer
│   └── config               # Repository configuration
├── .gitignore               # Files to ignore
├── README.md                # Project documentation
└── <project files>          # Your actual code
```

### Essential Git Commands

#### 1. Repository Setup

```bash
# Clone existing repository
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards

# Check repository status
git status

# View current branch
git branch

# View commit history
git log --oneline --graph --all
```

#### 2. Basic Workflow Commands

```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name

# Check what changed
git status
git diff

# Stage files for commit
git add <file>              # Add specific file
git add .                   # Add all changed files
git add -p                  # Interactive staging

# Commit changes
git commit -m "feat: add feature description"

# Push to remote
git push origin feature/your-feature-name

# Pull latest changes
git pull origin main
```

#### 3. Branch Management

```bash
# List all branches
git branch -a

# Switch branches
git checkout main
git checkout feature/branch-name

# Create new branch
git checkout -b feature/new-feature

# Delete branch (local)
git branch -d feature/old-feature

# Delete branch (remote)
git push origin --delete feature/old-feature

# Rename current branch
git branch -m new-branch-name
```

#### 4. Viewing History

```bash
# View commit history
git log
git log --oneline
git log --graph --all --decorate

# View specific file history
git log -- path/to/file

# View changes in commit
git show <commit-hash>

# View who changed what
git blame path/to/file
```

### Understanding Commits

A commit is a snapshot of your repository at a point in time:

```
commit abc123def456...
Author: John Doe <john@example.com>
Date:   Thu Feb 14 10:30:00 2026 +0000

    feat: add user authentication

    - Implement JWT-based authentication
    - Add login and logout endpoints
    - Update security documentation
```

**Commit Components**:
- **Hash**: Unique identifier (SHA-1)
- **Author**: Who made the commit
- **Date**: When it was committed
- **Message**: What changed and why

### Branching Strategy

MokoStandards uses a feature branch workflow:

```
main (protected)
  ├── feature/user-authentication
  ├── fix/security-vulnerability
  ├── docs/update-readme
  └── refactor/improve-performance
```

**Branch Types**:
- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation changes
- `refactor/`: Code improvements
- `test/`: Test additions/fixes
- `chore/`: Maintenance tasks

---

## Part 2: GitHub Workflow (45 minutes)

### Fork and Clone Workflow

#### Step 1: Fork the Repository

1. Navigate to GitHub repository
2. Click "Fork" button (top right)
3. Fork creates a copy in your account

#### Step 2: Clone Your Fork

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/MokoStandards.git
cd MokoStandards

# Add upstream remote (original repository)
git remote add upstream https://github.com/mokoconsulting-tech/MokoStandards.git

# Verify remotes
git remote -v
# origin    https://github.com/YOUR-USERNAME/MokoStandards.git (fetch)
# origin    https://github.com/YOUR-USERNAME/MokoStandards.git (push)
# upstream  https://github.com/mokoconsulting-tech/MokoStandards.git (fetch)
# upstream  https://github.com/mokoconsulting-tech/MokoStandards.git (push)
```

#### Step 3: Keep Your Fork Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push updates to your fork
git push origin main
```

### Creating a Pull Request

#### Step 1: Create Feature Branch

```bash
# Ensure main is up to date
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/add-new-library

# Make your changes
# ... edit files ...

# Stage and commit
git add .
git commit -m "feat: add new enterprise library

- Implement CacheManager library
- Add unit tests
- Update documentation"

# Push to your fork
git push origin feature/add-new-library
```

#### Step 2: Open Pull Request on GitHub

1. Navigate to your fork on GitHub
2. Click "Compare & pull request" button
3. Fill out PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [x] Added unit tests
- [x] All tests pass
- [x] Manual testing completed

## Checklist
- [x] Code follows style guidelines
- [x] Documentation updated
- [x] No breaking changes
- [x] Reviewed own code
```

4. Click "Create pull request"

### Code Review Process

#### As Pull Request Author:

1. **Respond to feedback promptly**
2. **Make requested changes**:
   ```bash
   # Make changes
   git add .
   git commit -m "fix: address review comments"
   git push origin feature/add-new-library
   ```
3. **Resolve conversations** when addressed
4. **Request re-review** when ready

#### As Reviewer:

1. **Review code thoroughly**
2. **Leave constructive comments**
3. **Approve or request changes**
4. **Use review features**:
   - Comment: General feedback
   - Approve: LGTM (Looks Good To Me)
   - Request Changes: Issues must be fixed

### Managing Issues

#### Creating Issues

```markdown
**Title**: Clear, descriptive title

**Description**:
- What is the problem?
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details

**Labels**:
- bug, enhancement, documentation, etc.

**Assignees**:
- Assign to person responsible

**Milestone**:
- Link to release/sprint
```

#### Issue Labels

Common labels in MokoStandards:
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority: high`: High priority
- `status: in progress`: Currently being worked on

---

## Part 3: GitHub Projects (30 minutes)

### What are GitHub Projects?

GitHub Projects provides Kanban-style boards for tracking work:
- ✅ **Visual workflow**: Track issues through stages
- ✅ **Automation**: Auto-update based on events
- ✅ **Integration**: Links with issues and PRs
- ✅ **Flexibility**: Customize columns and views
- ✅ **Reporting**: Track progress and metrics

### Creating a Project Board

#### Step 1: Create New Project

1. Go to repository → Projects tab
2. Click "New project"
3. Choose template:
   - **Basic kanban**: Simple workflow
   - **Automated kanban**: With automation
   - **Bug triage**: For bug management
4. Name your project (e.g., "Sprint 1", "Q1 2026 Development")

#### Step 2: Configure Columns

Default columns:
- **To Do**: Work not started
- **In Progress**: Currently working
- **Review**: Ready for review
- **Done**: Completed work

Custom columns can be added:
- **Blocked**: Issues with blockers
- **Testing**: In QA/testing phase
- **Backlog**: Future work

#### Step 3: Set Up Automation

Automation rules:
```yaml
To Do:
  - Newly added issues/PRs

In Progress:
  - Issue/PR reopened
  - Assignee added

Review:
  - Pull request opened
  - Review requested

Done:
  - Issue closed
  - PR merged
```

### Using Projects in Workflow

#### Step 1: Add Issues to Project

```bash
# Create issue
# On GitHub: New Issue → Fill form

# Link to project
# Sidebar: Projects → Select project
# Card appears in "To Do" column
```

#### Step 2: Move Cards as Work Progresses

```
To Do → In Progress:
  - Assign yourself to issue
  - Move card manually or auto-moves

In Progress → Review:
  - Create PR linking issue
  - Card auto-moves to Review

Review → Done:
  - PR approved and merged
  - Card auto-moves to Done
```

#### Step 3: Track Progress

Project views:
- **Board view**: Kanban columns
- **Table view**: Spreadsheet format
- **Roadmap view**: Timeline view

Metrics to track:
- Cards per column
- Cycle time (To Do → Done)
- WIP (Work In Progress) limits
- Burndown charts

### Best Practices for Projects

1. **Keep it current**: Update card status regularly
2. **Use templates**: Standard issue templates
3. **Set milestones**: Group related work
4. **Review regularly**: Team standup or weekly review
5. **Archive completed**: Clean up old projects

### Integrating Projects with Git Workflow

#### Complete Workflow Example

```bash
# 1. Pick issue from project board
#    - Find card in "To Do" column
#    - Assign to yourself
#    - Card moves to "In Progress"

# 2. Create branch
git checkout main
git pull upstream main
git checkout -b fix/issue-123-bug-description

# 3. Make changes and commit
git add .
git commit -m "fix: resolve issue #123

Fixes #123"

# 4. Push and create PR
git push origin fix/issue-123-bug-description
# Create PR on GitHub
# Reference issue in PR description: "Fixes #123"
# Card auto-moves to "Review"

# 5. After review and merge
# Card auto-moves to "Done"
# Branch can be deleted
```

#### Linking Issues and PRs

**In Commit Messages**:
```bash
git commit -m "fix: resolve authentication bug

Fixes #123
Related to #124, #125"
```

**In PR Description**:
```markdown
## Related Issues
Fixes #123
Closes #124
Addresses #125
```

**Keywords that close issues**:
- `Fixes #123`
- `Closes #123`
- `Resolves #123`

---

## Part 4: MokoStandards Git Standards (30 minutes)

### Branch Naming Conventions

Follow this pattern: `<type>/<short-description>`

**Types**:
- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation
- `refactor/`: Code refactoring
- `test/`: Tests
- `chore/`: Maintenance

**Examples**:
```bash
feature/user-authentication
fix/security-vulnerability-cve-2024-1234
docs/update-installation-guide
refactor/improve-error-handling
test/add-unit-tests-api-client
chore/update-dependencies
```

**Rules**:
- Lowercase only
- Use hyphens, not underscores
- Be descriptive but concise
- Include issue number if applicable: `fix/123-memory-leak`

### Commit Message Standards

Follow Conventional Commits specification:

#### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance
- `perf`: Performance improvement
- `ci`: CI/CD changes
- `build`: Build system changes

#### Examples

**Simple commit**:
```bash
git commit -m "feat: add cache manager library"
```

**Detailed commit**:
```bash
git commit -m "feat(cache): add cache manager with Redis support

- Implement CacheManager class with PSR-16 interface
- Add Redis adapter for distributed caching
- Include connection pooling and retry logic
- Add comprehensive unit tests

Fixes #456
BREAKING CHANGE: Requires Redis 6.0+ for advanced features"
```

**Bug fix**:
```bash
git commit -m "fix(auth): resolve JWT token expiration issue

The JWT tokens were expiring immediately due to incorrect
timestamp calculation. This fixes the calculation to use
proper Unix timestamps.

Fixes #789"
```

### Pull Request Guidelines

#### PR Title Format

Same as commit messages:
```
feat: add new enterprise library
fix: resolve memory leak in API client
docs: update integration workshop guide
```

#### PR Description Template

```markdown
## Description
<!-- Describe your changes in detail -->

## Motivation and Context
<!-- Why is this change required? What problem does it solve? -->
<!-- If it fixes an open issue, please link to the issue here -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## How Has This Been Tested?
<!-- Describe the tests you ran to verify your changes -->
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the code style of this project
- [ ] My change requires a change to the documentation
- [ ] I have updated the documentation accordingly
- [ ] I have added tests to cover my changes
- [ ] All new and existing tests passed
- [ ] I have checked my code and corrected any misspellings
```

#### Code Review Standards

**For Authors**:
1. Self-review before requesting review
2. Ensure all CI checks pass
3. Keep PRs focused and reasonably sized
4. Respond to feedback within 24 hours
5. Update PR description if scope changes

**For Reviewers**:
1. Review within 24-48 hours
2. Be constructive and respectful
3. Focus on code quality, not style (use linters)
4. Approve or request changes with clear reasoning
5. Test locally if needed

### GitHub Actions Integration

MokoStandards uses GitHub Actions for CI/CD:

```yaml
# .github/workflows/pr-validation.yml
name: PR Validation

on:
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      - name: Install Dependencies
        run: composer install
      - name: Run Tests
        run: composer test
      - name: Check Code Style
        run: composer cs-check
```

**What Gets Checked**:
- ✅ Unit tests pass
- ✅ Code style compliance
- ✅ Security scanning
- ✅ Documentation builds
- ✅ No broken links

---

## Hands-On Exercises

### Exercise 1: Complete Git Workflow (20 minutes)

**Objective**: Practice the standard Git workflow

**Steps**:
1. Fork the MokoStandards repository
2. Clone your fork locally
3. Create a feature branch: `feature/update-readme`
4. Make a change to README.md (add your name to contributors)
5. Commit with proper message format
6. Push to your fork
7. Create a pull request

**Solution**:
```bash
# Fork on GitHub first

# Clone your fork
git clone https://github.com/YOUR-USERNAME/MokoStandards.git
cd MokoStandards

# Add upstream remote
git remote add upstream https://github.com/mokoconsulting-tech/MokoStandards.git

# Create branch
git checkout -b feature/update-readme

# Make changes
echo "\n- Your Name" >> CONTRIBUTORS.md

# Commit
git add CONTRIBUTORS.md
git commit -m "docs: add contributor name to CONTRIBUTORS.md"

# Push
git push origin feature/update-readme

# Create PR on GitHub
```

### Exercise 2: Branch Management (15 minutes)

**Objective**: Practice branch operations

**Tasks**:
1. Create multiple feature branches
2. Switch between branches
3. Merge changes
4. Delete old branches

**Commands**:
```bash
# Create multiple branches
git checkout -b feature/task-1
git checkout -b feature/task-2
git checkout -b fix/bug-1

# List all branches
git branch

# Switch branches
git checkout feature/task-1
git checkout main

# Merge feature to main (after PR)
git checkout main
git merge feature/task-1

# Delete merged branch
git branch -d feature/task-1
git push origin --delete feature/task-1
```

### Exercise 3: GitHub Projects Setup (25 minutes)

**Objective**: Create and configure a project board

**Steps**:
1. Create new GitHub Project
2. Set up columns: To Do, In Progress, Review, Done
3. Configure automation rules
4. Create 3 sample issues
5. Add issues to project
6. Move issues through workflow

**Practice Workflow**:
```
1. Create Issue: "Add documentation for CacheManager"
   - Add to project
   - Appears in "To Do"

2. Assign to yourself
   - Move to "In Progress"

3. Create PR
   - Reference issue: "Fixes #123"
   - Card moves to "Review"

4. Merge PR
   - Card moves to "Done"
   - Issue automatically closes
```

### Exercise 4: Resolving Merge Conflicts (20 minutes)

**Objective**: Handle merge conflicts properly

**Scenario**:
```bash
# Simulate conflict
git checkout main
git checkout -b feature/conflict-test-1
echo "Change 1" >> test.txt
git add test.txt
git commit -m "feat: add change 1"

git checkout main
git checkout -b feature/conflict-test-2
echo "Change 2" >> test.txt
git add test.txt
git commit -m "feat: add change 2"

# Try to merge (will conflict)
git checkout main
git merge feature/conflict-test-1  # Success
git merge feature/conflict-test-2  # Conflict!
```

**Resolution**:
```bash
# View conflict
git status
cat test.txt

# Edit file to resolve
# Choose which changes to keep or combine

# Mark as resolved
git add test.txt
git commit -m "merge: resolve conflict between test-1 and test-2"
```

---

## Best Practices Summary

### Git Best Practices

1. **Commit Often**: Small, focused commits
2. **Write Clear Messages**: Follow conventional commits
3. **Pull Before Push**: Always sync with remote
4. **Use Branches**: Never commit directly to main
5. **Review Your Changes**: Use `git diff` before committing

### GitHub Best Practices

1. **Use Templates**: Issue and PR templates
2. **Link Issues**: Reference in PRs and commits
3. **Review Thoroughly**: Don't rubber-stamp approvals
4. **Keep PRs Small**: Easier to review
5. **Update Documentation**: Keep docs in sync with code

### GitHub Projects Best Practices

1. **Regular Updates**: Keep board current
2. **Clear Descriptions**: Detailed issue descriptions
3. **Use Labels**: Categorize work
4. **Set Priorities**: Use priority labels
5. **Track Progress**: Review metrics regularly

---

## Common Git Commands Reference

### Basic Operations
```bash
git status                  # Check repository status
git add <file>             # Stage file
git commit -m "message"    # Commit changes
git push                   # Push to remote
git pull                   # Pull from remote
```

### Branching
```bash
git branch                 # List branches
git checkout -b <branch>   # Create and switch to branch
git checkout <branch>      # Switch branch
git branch -d <branch>     # Delete branch
git push -u origin <branch> # Push new branch
```

### Remote Operations
```bash
git remote -v              # View remotes
git remote add <name> <url> # Add remote
git fetch <remote>         # Fetch from remote
git pull <remote> <branch> # Pull and merge
```

### History and Inspection
```bash
git log                    # View commit history
git log --oneline         # Compact history
git diff                   # View changes
git show <commit>         # Show commit details
git blame <file>          # See who changed what
```

### Undoing Changes
```bash
git checkout -- <file>    # Discard local changes
git reset HEAD <file>     # Unstage file
git revert <commit>       # Revert commit
git reset --hard <commit> # Reset to commit (DANGEROUS)
```

---

## Additional Resources

### Documentation
- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [GitHub Projects Guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Conventional Commits](https://www.conventionalcommits.org/)

### MokoStandards Policies
- `docs/policy/git-workflow-standards.md` - Git workflow policy
- `docs/policy/code-review-standards.md` - Code review guidelines
- `docs/policy/branch-protection.md` - Branch protection rules

### Tools
- [GitHub CLI](https://cli.github.com/) - Command-line GitHub
- [GitKraken](https://www.gitkraken.com/) - Visual Git client
- [GitHub Desktop](https://desktop.github.com/) - GUI for GitHub

---

## Knowledge Check

Test your understanding:

1. What is the proper branch naming format for a new feature?
2. What are the required components of a commit message?
3. How do you link a PR to an issue?
4. What are the default columns in a GitHub Projects board?
5. How do you keep your fork updated with upstream changes?

**Answers**:
1. `feature/<short-description>` (e.g., `feature/user-authentication`)
2. Type, scope (optional), subject, body (optional), footer (optional)
3. Use keywords like "Fixes #123" in PR description or commit message
4. To Do, In Progress, Review, Done
5. `git fetch upstream`, `git merge upstream/main`, `git push origin main`

---

## Next Steps

After completing this session:
1. ✅ Practice the workflow with real tasks
2. ✅ Set up a GitHub Project for your team
3. ✅ Review MokoStandards Git policies in detail
4. ✅ Contribute to an open issue in MokoStandards
5. ✅ Continue to Session 7 or review previous sessions

---

## Session Summary

You've learned:
- ✅ Git fundamentals and core commands
- ✅ Standard Git workflow for MokoStandards
- ✅ GitHub pull request and code review process
- ✅ GitHub Projects for work management
- ✅ Integration of Git, GitHub, and Projects
- ✅ MokoStandards Git and GitHub standards
- ✅ Best practices for version control and collaboration

**Time to Practice!** The best way to learn Git is by using it regularly. Start contributing to MokoStandards projects today!

---

**Questions or Need Help?**
- Slack: #git-help channel
- Email: devops@mokoconsulting.tech
- GitHub Discussions: MokoStandards repository

