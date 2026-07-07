import requests
from metadata_fetcher import fetch_metadata


# gets two package names and checks how many edits are needed to turn one package name into another
def levenshtein_distance(package_name, candidate_name):
    package_name = package_name.lower()
    candidate_name = candidate_name.lower()

    rows = len(package_name) + 1
    cols = len(candidate_name) + 1

    distances = []

    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(0)
        distances.append(row)

    for i in range(rows):
        distances[i][0] = i

    for j in range(cols):
        distances[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if package_name[i - 1] == candidate_name[j - 1]:
                cost = 0
            else:
                cost = 1

            distances[i][j] = min(
                distances[i - 1][j] + 1,
                distances[i][j - 1] + 1,
                distances[i - 1][j - 1] + cost
            )

    return distances[-1][-1]


# gets a package name and a candidate name, and checks if both names are suspiciously similar
def are_names_similar(package_name, candidate_name):
    distance = levenshtein_distance(package_name, candidate_name)

    if distance == 1:
        return True

    if distance == 2 and len(package_name) >= 6:
        return True

    return False


# gets a npm package names and looks for similar package names in the npm registry
def search_similar_npm_packages(package_name):
    url = f"https://registry.npmjs.org/-/v1/search?text={package_name}&size=20"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return []

    if response.status_code != 200:
        return []

    data = response.json()
    results = data.get("objects", [])
    package_names = []

    for result in results:
        package = result.get("package", {})
        name = package.get("name")

        if name and name != package_name:
            package_names.append(name)

    return package_names


POSSIBLE_TYPOSQUATTING_RISK = 10
LIKELY_TYPOSQUATTING_RISK = 25
# gets a package metadata and returns whether the package is a suspicious typosquatting
def check_typosquatting(metadata):
    package_name = metadata.get("name")
    ecosystem = metadata.get("ecosystem")

    if not package_name or not ecosystem:
        return None

    if ecosystem != "javascript":
        return None

    similar_candidates = search_similar_npm_packages(package_name)
    possible_match = None

    for candidate_name in similar_candidates:
        if not are_names_similar(package_name, candidate_name):
            continue

        candidate_metadata = fetch_metadata({
            "name": candidate_name,
            "ecosystem": ecosystem
        })

        if not candidate_metadata:
            continue

        current_version_count = metadata.get("version_count") or 0
        candidate_version_count = candidate_metadata.get("version_count") or 0

        if candidate_version_count >= 20 and current_version_count <= 5:
            return {
                "risk": LIKELY_TYPOSQUATTING_RISK,
                "similar_package": candidate_name,
                "reason": f"Package name is very similar to '{candidate_name}', which has a much larger version history"
            }

        possible_match = {
            "risk": POSSIBLE_TYPOSQUATTING_RISK,
            "similar_package": candidate_name,
            "reason": f"Package name is very similar to '{candidate_name}'"
        }

    return possible_match