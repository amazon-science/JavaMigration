"""Seed changes for repository preprocessing."""

import logging
from pathlib import Path

from java_migration_agent.tools.dependency_tools import get_dependency_versions
from java_migration_agent.tools.pom_tools import PomUtils

logger = logging.getLogger(__name__)


def update_jdk_related(root_dir: str) -> None:
    """
    Update JDK-related settings in all POM files to Java 17.

    Args:
        root_dir: Root directory of the repository
    """
    logger.info(f"Updating JDK settings in {root_dir}")
    PomUtils.update_all_jdk_settings(root_dir)


def update_dependency_version(root_dir: str) -> None:
    """
    Update dependency versions in all POM files to Java 17 compatible versions.

    Args:
        root_dir: Root directory of the repository
    """
    logger.info(f"Updating dependency versions in {root_dir}")
    dependency_versions = get_dependency_versions()
    PomUtils.update_all_dependencies(root_dir, dependency_versions)
