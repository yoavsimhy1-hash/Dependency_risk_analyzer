from pathlib import Path
from requirements_parser import parse_requirements_txt
from pyproject_parser import parse_pyproject_toml
from package_json_parser import parse_package_json
from metadata_fetcher import fetch_metadata

SUPPORTED_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json"
}

#gets a project path and returns a list of its dependency files, only if they are in SUPPORTED_FILES
def find_dependency_files(project_path):
    dependency_files = []

    for file_path in Path(project_path).rglob("*"):
        if file_path.name in SUPPORTED_FILES:
            dependency_files.append(file_path)

    return dependency_files

#gets a file path and returns a list of its dependencies
def parse_dependency_file(file_path):
    if file_path.name == "requirements.txt":
        return parse_requirements_txt(file_path)

    if file_path.name == "pyproject.toml":
        return parse_pyproject_toml(file_path)

    if file_path.name == "package.json":
        return parse_package_json(file_path)

    return []

#gets a project path and returns a list of its dependencies
def analyze_project(project_path):
    all_dependencies = []

    dependency_files = find_dependency_files(project_path)

    if not dependency_files:
        print("No supported dependency files found.")
        return []

    for file_path in dependency_files:
        dependencies = parse_dependency_file(file_path)
        all_dependencies.extend(dependencies)

    return all_dependencies

dependencies = analyze_project(r"") #project path here
for dependency in dependencies:
    metadata = fetch_metadata(dependency)
    print(metadata)
