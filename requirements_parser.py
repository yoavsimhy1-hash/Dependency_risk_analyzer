import re

#gets a requirements.txt file path and returns a list of dependencies
def parse_requirements_txt(file_path):
    dependencies = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            # Match:
            # package_name [optional_operator] [optional_version]
            match = re.match(r"^([A-Za-z0-9_.-]+)\s*([<>=!~]+)?\s*(.*)?$", line)

            if match:
                dependencies.append({
                    "name": match.group(1),
                    "operator": match.group(2),
                    "version": match.group(3) if match.group(3) else None,
                    "ecosystem": "python",
                    "source_file": str(file_path)
                })

    return dependencies
