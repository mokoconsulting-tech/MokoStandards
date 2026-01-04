<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Technical Terms Glossary

## Purpose

Defines technical terminology related to software development, platforms, infrastructure, and tooling used in MokoStandards.

---

## A

**Artifact**
: A tangible output of development process, such as compiled code, documentation, or test results

**Autobuild**
: Automated process of compiling source code into executable format without manual intervention

**Authentication**
: Process of verifying the identity of a user, system, or application

**Authorization**
: Process of determining what actions an authenticated entity is permitted to perform

---

## B

**Baseline**
: A known, approved configuration or state used as reference point for changes

**Branch**
: Independent line of development in version control system

**Branch Protection**
: Rules preventing direct changes to specific branches without review

**Build**
: Process of converting source code into executable or deployable format

---

## C

**Cache**
: Temporary storage for frequently accessed data to improve performance

**CI/CD Pipeline**
: Automated workflow for building, testing, and deploying software

**CodeQL**
: Static analysis tool by GitHub for finding security vulnerabilities in code

**Commit**
: Saved change to version control repository with descriptive message

**Component** (Joomla)
: Primary extension type in Joomla providing major application functionality

**Configuration Management**
: Practice of maintaining and tracking system configurations consistently

**CRUD Operations**
: Basic database operations: Create, Read, Update, Delete

---

## D

**Database Migration**
: Scripted changes to database schema tracked in version control

**Dependency**
: External library or package required for software to function

**Dependabot**
: GitHub tool for automated dependency updates and security alerts

**Deployment**
: Process of releasing software to production or target environment

**Descriptor** (Dolibarr)
: Module definition class containing metadata and configuration

**Docker**
: Containerization platform for packaging applications with dependencies

**Dolibarr**
: Open-source ERP/CRM platform, basis for MokoCRM

---

## E

**Endpoint**
: URL path in API that accepts requests and returns responses

**Entity**
: Database record or object representing real-world concept

**Environment Variable**
: Configuration value stored outside code, often for credentials

**Extrafield** (Dolibarr)
: Custom field added to standard Dolibarr objects without core modification

---

## F

**Feature Branch**
: Git branch containing development for single feature or fix

**Foreign Key**
: Database field referencing primary key in another table

---

## G

**Git**
: Distributed version control system for tracking code changes

**GitHub Actions**
: CI/CD automation platform integrated with GitHub

**GitHub CLI**
: Command-line tool for interacting with GitHub

**GitHub Project**
: Project management tool integrated with GitHub repositories

**Grandfathered**
: Existing code exempt from new standards for backward compatibility

---

## H

**Hook** (Dolibarr)
: Extension point allowing custom code execution at specific events

**Hotfix**
: Urgent fix deployed directly to production to resolve critical issue

---

## I

**Idempotent**
: Operation producing same result whether executed once or multiple times

**Index** (Database)
: Data structure improving database query performance

**Integration Test**
: Test validating multiple components work together correctly

---

## J

**Joomla**
: Open-source CMS platform, basis for MokoWaaS

**JSON**
: JavaScript Object Notation, text-based data interchange format

---

## L

**Linter**
: Tool analyzing code for style violations and potential errors

**Lock File**
: File recording exact versions of dependencies for reproducibility

---

## M

**Manifest** (Joomla)
: XML file describing extension metadata and installation requirements

**Merge Conflict**
: Situation where version control cannot automatically combine changes

**Migration** (Database)
: Script modifying database schema in versioned, repeatable manner

**Module** (Dolibarr)
: Self-contained extension adding functionality to Dolibarr

**Module** (Joomla)
: Extension displaying content in designated positions on pages

---

## N

**Namespace**
: Organizational scope preventing name collisions between code elements

---

## O

**ORM**
: Object-Relational Mapping, technique for database interaction using objects

---

## P

**Package Manager**
: Tool automating installation and management of software dependencies

**Patch**
: Small code change fixing bug or adding minor improvement

**PHP**
: Server-side programming language used by Dolibarr and Joomla

**Plugin** (Joomla)
: Extension responding to system events to modify behavior

**Pull Request (PR)**
: Proposed code changes submitted for review before merging

**Push Protection**
: Feature preventing commits containing secrets or credentials

---

## Q

**Query**
: Request for data from database using SQL or API

---

## R

**RBAC** (Role-Based Access Control)
: Security model assigning permissions based on user roles

**Refactoring**
: Restructuring code without changing external behavior to improve quality

**Repository (Repo)**
: Storage location for version-controlled code and documentation

**REST API**
: Web service architecture using HTTP methods for resource operations

**Rollback**
: Reverting system or database to previous state after failed change

---

## S

**SARIF**
: Static Analysis Results Interchange Format for security scan results

**SAST**
: Static Application Security Testing, analyzing code without execution

**Schema** (Database)
: Structure defining tables, fields, relationships, and constraints

**SDK**
: Software Development Kit, tools and libraries for platform development

**Secret Scanning**
: Tool detecting committed credentials or sensitive data in code

**Semantic Versioning**
: Version numbering scheme: MAJOR.MINOR.PATCH

**Shebang**
: First line of script specifying interpreter: `#!/usr/bin/env python3`

**SQL Injection**
: Security vulnerability allowing attackers to execute malicious SQL

**Squash Merge**
: Combining multiple commits into single commit when merging

**Staging Environment**
: Pre-production environment for testing before release

---

## T

**Table Prefix**
: Characters prepended to database table names (e.g., `llx_` in Dolibarr)

**Template** (Joomla)
: Extension controlling site appearance and layout

**Transitive Dependency**
: Indirect dependency required by direct dependency

**Trigger** (Database)
: Automated action executed when database event occurs

**Trigger** (Dolibarr)
: Event handler executing custom code on specific Dolibarr events

**Type Hint**
: Explicit declaration of expected data type for function parameters

---

## U

**Unit Test**
: Test validating single function or component in isolation

**Upstream**
: Original repository from which fork was created

---

## V

**Validation**
: Process verifying data meets required format and constraints

**Version Control**
: System tracking changes to files over time (e.g., Git)

**Virtual Environment**
: Isolated Python environment with independent dependencies

**Vulnerability**
: Security weakness that could be exploited to compromise system

---

## W

**Webhook**
: HTTP callback triggered by specific event to send data to URL

**Workflow**
: Automated process defined in CI/CD system

**Working Directory**
: Current directory where commands execute

---

## X

**XSS** (Cross-Site Scripting)
: Security vulnerability injecting malicious scripts into web pages

**XML**
: Extensible Markup Language for structured data

---

## Y

**YAML**
: Human-readable data serialization format used for configuration

---

## Z

**Zero-Day**
: Vulnerability exploited before patch is available

---

## See Also

- [Process Terms](process-terms.md)
- [Security Terms](security-terms.md)
- [Business Terms](business-terms.md)
- [Glossary Index](index.md)

## Metadata

- **Document Type**: glossary
- **Document Subtype**: technical
- **Owner Role**: Documentation Owner
- **Status**: Published

## Revision History

| Date       | Version  | Author          | Notes                             |
| ---------- | -------- | --------------- | --------------------------------- |
| 2026-01-04 | 01.00.00 | Moko Consulting | Initial technical terms glossary |
