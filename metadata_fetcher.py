import requests

#gets a pypi package name and returns its metadata
def fetch_pypi_metadata(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()

    releases = data.get("releases", {})
    versions = list(releases.keys())
    release_dates = []

    for files in releases.values():
        for file in files:
            upload_time = file.get("upload_time_iso_8601")
            if upload_time:
                release_dates.append(upload_time)

    if release_dates:
        first_release_date = min(release_dates)
    else:
        first_release_date = None

    return {
        "name": package_name,
        "ecosystem": "python",
        "latest_version": data["info"].get("version"),
        "description": data["info"].get("summary"),
        "license": data["info"].get("license"),
        "homepage": data["info"].get("home_page"),
        "versions": versions,
        "version_count": len(versions),
        "first_release_date": first_release_date
    }

#gets a npm package name and returns its metadata
def fetch_npm_metadata(package_name):
    url = f"https://registry.npmjs.org/{package_name}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()

    time_data = data.get("time", {})
    versions = list(data.get("versions", {}).keys())

    return {
        "name": package_name,
        "ecosystem": "javascript",
        "latest_version": data.get("dist-tags", {}).get("latest"),
        "description": data.get("description"),
        "license": data.get("license"),
        "homepage": data.get("homepage"),
        "versions": versions,
        "version_count": len(versions),
        "first_release_date": time_data.get("created")
    }

#gets a dependency, checks whether its a python or a javascript one and calls the relevant function
def fetch_metadata(dependency):
    ecosystem = dependency["ecosystem"]
    name = dependency["name"]

    if ecosystem == "python":
        return fetch_pypi_metadata(name)

    if ecosystem == "javascript":
        return fetch_npm_metadata(name)

    return None