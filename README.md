Dependency Risk Analyzer

🚧 Status: Under active development

Overview

a Python-based software supply chain security tool that analyzes a project's third-party dependencies and evaluates their potential risk.

The goal is to provide a more complete picture of the security posture of a project's dependencies.

Current Features 

Stage 1 – Dependency Discovery

The current implementation supports:

Recursively scanning a project directory for supported dependency manifests.
Parsing Python and Node.js dependency files.
Extracting dependency names and version information into a normalized internal format.

Currently supported manifest files:

requirements.txt,
pyproject.toml,
package.json

Stage 2 - Package Metadata Fetching

The analyzer now enriches each discovered dependency with metadata retrieved directly from the official package registries.
* Fetches package metadata from PyPI for Python packages.
* Fetches package metadata from the npm Registry for JavaScript packages.
* Automatically selects the correct registry based on the package ecosystem.
* Handles network errors and missing packages gracefully.
* Retrieves key package information, including:
    * Latest available version
    * Package description
    * License
    * Homepage
    * Available published versions
