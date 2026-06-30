Dependency Risk Analyzer

A Python-based tool that analyzes Python and JavaScript project dependencies and evaluates their potential security risk.

The project is being developed incrementally, with each stage adding new analysis capabilities. The goal is to build a practical dependency risk analyzer similar to those used in software supply chain security.

Project Status: 🚧 Under active development

Current Features

Stage 1 – Dependency Parsing ✅
Extracts dependencies from common project files:

* requirements.txt
* pyproject.toml
* package.json

For each dependency, the parser collects:
* Package name
* Version
* Ecosystem (Python / JavaScript)
* Source file

Stage 2 – Package Metadata Collection ✅
Retrieves package metadata from the official package registries.

Python packages
* PyPI JSON API
JavaScript packages
* npm Registry API

Collected metadata currently includes:
* Latest version
* Package description
* Homepage
* License


Example Workflow
1. Parse dependency files.
2. Identify all project dependencies.
3. Retrieve metadata from PyPI or npm.
4. (Upcoming) Calculate a security risk score for each package.
5. (Upcoming) Generate a detailed risk report.


Motivation
Modern applications depend on hundreds of third-party packages. This project is an opportunity to explore software supply chain security while building a practical security tool from scratch.
The long-term goal is to identify potentially risky dependencies using package metadata, security heuristics, and other indicators that may suggest malicious or suspicious packages.

Disclaimer
This project is intended for educational and research purposes. It is currently under active development and should not yet be considered a production-ready security scanner.
