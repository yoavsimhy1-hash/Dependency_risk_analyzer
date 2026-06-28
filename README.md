Dependency Risk Analyzer

🚧 Status: Under active development

Overview

Dependency Risk Analyzer is a Python-based software supply chain security tool that analyzes a project's third-party dependencies and evaluates their potential risk.

Unlike traditional Software Composition Analysis (SCA) tools that primarily focus on known vulnerabilities (CVEs), this project aims to assess broader supply chain risk indicators, such as package metadata, maintainer activity, repository health, release history, and other trust signals.

The goal is to provide a more complete picture of the security posture of a project's dependencies.

Current Features
✅ Stage 1 – Dependency Discovery

The current implementation supports:

Recursively scanning a project directory for supported dependency manifests.
Parsing Python and Node.js dependency files.
Extracting dependency names and version information into a normalized internal format.

Currently supported manifest files:

requirements.txt
pyproject.toml
package.json
