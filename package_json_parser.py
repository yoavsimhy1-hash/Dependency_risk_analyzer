import json

def parse_package_json(file_path):
    dependencies = []

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for section in ["dependencies", "devDependencies"]:
        packages = data.get(section, {})

        for name, version in packages.items():
            dependencies.append({
                "name": name,
                "version": version,
                "operator": None,
                "ecosystem": "javascript",
                "dependency_type": section,
                "source_file": str(file_path)
            })

    return dependencies
