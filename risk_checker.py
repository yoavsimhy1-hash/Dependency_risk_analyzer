from datetime import datetime, timezone

LOW_VERSION_THRESHOLD = 5
ONE_VERSION_RISK = 20
LOW_VERSION_COUNT_RISK = 10
MISSING_DESCRIPTION_RISK = 5
MISSING_LICENSE_RISK = 5
MISSING_HOMEPAGE_RISK = 5
SEVEN_DAYS_PACKAGE_RISK = 25
THIRTY_DAYS_PACKAGE_RISK = 15
NINETY_DAYS_PACKAGE_RISK = 5
MISSING_LATEST_VERSION_RISK = 20


def calculate_risk(metadata):

    homepage = metadata.get("homepage")
    version_count = metadata.get("version_count")
    latest_version = metadata.get("latest_version")
    description = metadata.get("description")
    first_release_date = metadata.get("first_release_date")
    license = metadata.get("license")


    score = 0
    checks = []

    # is there a homepage?
    if not homepage:
        score += MISSING_HOMEPAGE_RISK
        checks.append({
            "check": "Homepage",
            "reason": "Package is missing a homepage",
        })

    # is there a description?
    if not description:
        score += MISSING_DESCRIPTION_RISK
        checks.append({
            "check": "Description",
            "reason": "Package is missing a description",
        })

    # is there a licence?
    if not license:
        score += MISSING_LICENSE_RISK
        checks.append({
            "check": "licence",
            "reason": "Package is missing a licence"
        })

    # is there's only one version?
    if version_count == 1:
        score += ONE_VERSION_RISK
        checks.append({
            "check": "Version History",
            "reason": "Package has only one version",
        })
    # are there less than 5 versions?
    elif version_count is not None and version_count < 5:
        score += LOW_VERSION_COUNT_RISK
        checks.append({
            "check": "Version History",
            "reason": f"Package has fewer than {LOW_VERSION_THRESHOLD} published versions",
        })

    # how recently was the package released
    if first_release_date:
        first_release_date = first_release_date.replace("Z", "+00:00")

        # converts the string into a datetime object
        first_release_date = datetime.fromisoformat(first_release_date)

        today = datetime.now(timezone.utc)
        package_age = today - first_release_date
        package_age_days = package_age.days

        if package_age_days < 7:
            score += SEVEN_DAYS_PACKAGE_RISK
            checks.append({
                "check": "Package Age",
                "reason": f"Package is only {package_age_days} days old"
            })

        elif package_age_days < 30:
            score += THIRTY_DAYS_PACKAGE_RISK
            checks.append({
                "check": "Package Age",
                "reason": f"Package is only {package_age_days} days old"
            })

        elif package_age_days < 90:
            score += NINETY_DAYS_PACKAGE_RISK
            checks.append({
                "check": "Package Age",
                "reason": f"Package is only {package_age_days} days old"
            })

    # is the latest version missing?
    if not latest_version:
        score += MISSING_LATEST_VERSION_RISK
        checks.append({
            "check": "Latest Version",
            "reason": "Package is missing a latest version"
        })
    
    typosquatting_result = check_typosquatting(metadata)
    # is there typosquatting?
    if typosquatting_result is not None:
        score += typosquatting_result["risk"]
        checks.append({
            "check": "Typosquatting",
            "reason": typosquatting_result["reason"]
        })
     
      
    if score > 100:
        score = 100

    return {
        "score": score,
        "checks": checks,
    }