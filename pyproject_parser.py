import re
import tomllib

#gets a pyproject.toml file path and returns a list of dependencies
def parse_pyproject_toml(file_path):
    dependencies = []

    with open(file_path, "rb") as file:
        data = tomllib.load(file)

    project = data.get("project", {})

    for dep in project.get("dependencies", []):
        # Match:
        # package_name [optional_operator] [optional_version]
        match = re.match(r"^([A-Za-z0-9_.-]+)\s*([<>=!~]+)?\s*(.*)?$",dep)

        if not match:
            continue

        dependencies.append({
            "name": match.group(1),
            "operator": match.group(2),
            "version": match.group(3),
            "ecosystem": "python",
            "dependency_type": "dependencies",
            "source_file": str(file_path)
        })

    return dependencies
