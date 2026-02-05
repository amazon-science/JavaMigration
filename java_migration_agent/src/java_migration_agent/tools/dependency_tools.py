"""Tools for dependency version management."""

import json
import os
from pathlib import Path
from strands import tool


# Path to dependency version mapping file
_DATA_DIR = Path(__file__).parent.parent / "data"
_DEPENDENCY_VERSION_FILE = _DATA_DIR / "dependency_version.json"

# Load dependency versions at module import
_DEPENDENCY_VERSIONS = {}
if _DEPENDENCY_VERSION_FILE.exists():
    with open(_DEPENDENCY_VERSION_FILE, "r") as f:
        _DEPENDENCY_VERSIONS = json.load(f)


@tool
def search_dependency_version(dependency_coordinate: str) -> str:
    """
    Search for the recommended Java 17 compatible version of a Maven dependency.

    Args:
        dependency_coordinate: The Maven dependency coordinate in the format 'groupId:artifactId'
                               (e.g., 'org.springframework.boot:spring-boot-starter-parent')

    Returns:
        The recommended version string if found, or a message indicating the dependency was not found.
    """
    dependency_coordinate = dependency_coordinate.strip()

    if dependency_coordinate in _DEPENDENCY_VERSIONS:
        version = _DEPENDENCY_VERSIONS[dependency_coordinate]
        return f"Recommended version for '{dependency_coordinate}': {version}"

    return (
        f"No version information found for '{dependency_coordinate}'. "
        "Please select an appropriate version based on your knowledge."
    )


def get_dependency_versions() -> dict:
    """
    Get the complete dependency version mapping.

    Returns:
        Dictionary of dependency coordinates to versions
    """
    return _DEPENDENCY_VERSIONS.copy()


def load_dependency_versions(file_path: str) -> dict:
    """
    Load dependency versions from a custom file.

    Args:
        file_path: Path to JSON file containing dependency versions

    Returns:
        Dictionary of dependency coordinates to versions
    """
    with open(file_path, "r") as f:
        return json.load(f)
