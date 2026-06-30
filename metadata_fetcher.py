import requests

def fetch_pypi_metadata(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "name": package_name,
        "ecosystem": "python",
        "latest_version": data["info"].get("version"),
        "description": data["info"].get("summary"),
        "license": data["info"].get("license"),
        "homepage": data["info"].get("home_page"),
        "versions": list(data.get("releases", {}).keys())
    }

def fetch_npm_metadata(package_name):
    url = f"https://registry.npmjs.org/{package_name}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "name": package_name,
        "ecosystem": "javascript",
        "latest_version": data.get("dist-tags", {}).get("latest"),
        "description": data.get("description"),
        "license": data.get("license"),
        "homepage": data.get("homepage"),
        "versions": list(data.get("versions", {}).keys())
    }

def fetch_metadata(dependency):
    ecosystem = dependency["ecosystem"]
    name = dependency["name"]

    if ecosystem == "python":
        return fetch_pypi_metadata(name)

    if ecosystem == "javascript":
        return fetch_npm_metadata(name)

    return None