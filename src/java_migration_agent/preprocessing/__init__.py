"""Preprocessing utilities for repository setup."""

from java_migration_agent.preprocessing.seed_changes import (
    update_jdk_related,
    update_dependency_version,
)

__all__ = ["update_jdk_related", "update_dependency_version"]
