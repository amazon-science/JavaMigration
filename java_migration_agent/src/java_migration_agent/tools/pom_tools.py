"""POM utilities for Maven project manipulation."""

import glob
import logging
import os
import re
from pathlib import Path
from typing import Dict, Optional
from xml.etree import ElementTree

from packaging import version

logger = logging.getLogger(__name__)

# Maven POM namespaces
NAMESPACES = {"xmlns": "http://maven.apache.org/POM/4.0.0"}


class PomUtils:
    """Utilities for working with Maven POM files."""

    @staticmethod
    def get_property(root: ElementTree.Element, properties: dict, ref: str) -> Optional[str]:
        """
        Obtain the actual version number referred by ${var} by searching the properties section.

        Args:
            root: Root of the POM XML tree
            properties: The entire properties section of the POM
            ref: The property name to be searched

        Returns:
            Actual version number referred by ref, or None if not found
        """
        # Remove ${ } from the reference
        name = ref[2:-1]
        if name in properties:
            property_version = properties[name]
            if property_version is not None:
                value = property_version
                if value.startswith("${"):
                    # Recursive call (rarely happens)
                    return PomUtils.get_property(root, properties, value)
                else:
                    return property_version
        return None

    @staticmethod
    def should_upgrade(old_version: Optional[str], new_version: str) -> bool:
        """
        Determine if a dependency should be upgraded.

        Args:
            old_version: Current version (can be None)
            new_version: Proposed new version

        Returns:
            True if should upgrade, False otherwise
        """
        if old_version is None:
            return True

        try:
            return version.parse(new_version) > version.parse(old_version)
        except Exception:
            # If version parsing fails, default to upgrading
            return True

    @staticmethod
    def update_jdk_related(input_pom: str, output_pom: str) -> None:
        """
        Update JDK-related settings in a POM file to Java 17.

        Args:
            input_pom: Path to input POM file
            output_pom: Path to output POM file
        """
        tree = ElementTree.parse(input_pom)
        root = tree.getroot()

        # Update properties for Java 17
        properties_to_update = {
            "maven.compiler.source": "17",
            "maven.compiler.target": "17",
            "java.version": "17",
        }

        properties = root.find("xmlns:properties", NAMESPACES)
        if properties is not None:
            for prop_name, prop_value in properties_to_update.items():
                prop_element = properties.find(f"xmlns:{prop_name}", NAMESPACES)
                if prop_element is not None:
                    prop_element.text = prop_value
                    logger.info(f"Updated {prop_name} to {prop_value} in {input_pom}")

        tree.write(output_pom, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def apply_selected_notes(
        pom_file: str,
        dependency_versions: Dict[str, str],
    ) -> None:
        """
        Update dependency versions in a POM file.

        Args:
            pom_file: Path to POM file
            dependency_versions: Dictionary of dependency coordinates to versions
        """
        tree = ElementTree.parse(pom_file)
        root = tree.getroot()

        # Update dependencies
        dependencies = root.findall(".//xmlns:dependency", NAMESPACES)
        for dep in dependencies:
            group_id_elem = dep.find("xmlns:groupId", NAMESPACES)
            artifact_id_elem = dep.find("xmlns:artifactId", NAMESPACES)
            version_elem = dep.find("xmlns:version", NAMESPACES)

            if group_id_elem is not None and artifact_id_elem is not None:
                coordinate = f"{group_id_elem.text}:{artifact_id_elem.text}"
                if coordinate in dependency_versions:
                    new_version = dependency_versions[coordinate]
                    old_version = version_elem.text if version_elem is not None else None

                    if PomUtils.should_upgrade(old_version, new_version):
                        if version_elem is not None:
                            version_elem.text = new_version
                            logger.info(
                                f"Updated {coordinate} from {old_version} to {new_version}"
                            )

        tree.write(pom_file, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def find_all_pom_files(root_dir: str) -> list[str]:
        """
        Find all POM files in a directory recursively.

        Args:
            root_dir: Root directory to search

        Returns:
            List of POM file paths
        """
        return sorted(glob.glob(os.path.join(root_dir, "**", "pom.xml"), recursive=True))

    @staticmethod
    def update_all_jdk_settings(root_dir: str) -> None:
        """
        Update JDK settings in all POM files within a directory.

        Args:
            root_dir: Root directory containing POM files
        """
        if not Path(os.path.join(root_dir, "pom.xml")).exists():
            raise ValueError(f"No `pom.xml` file found in repository root dir {root_dir}.")

        pom_files = PomUtils.find_all_pom_files(root_dir)
        logger.info(f"Updating JDK settings in {len(pom_files)} POM files")

        for pom_file in pom_files:
            PomUtils.update_jdk_related(pom_file, pom_file)

    @staticmethod
    def update_all_dependencies(root_dir: str, dependency_versions: Dict[str, str]) -> None:
        """
        Update dependency versions in all POM files within a directory.

        Args:
            root_dir: Root directory containing POM files
            dependency_versions: Dictionary of dependency coordinates to versions
        """
        if not Path(os.path.join(root_dir, "pom.xml")).exists():
            raise ValueError(f"No `pom.xml` file found in repository root dir {root_dir}.")

        pom_files = PomUtils.find_all_pom_files(root_dir)
        logger.info(f"Updating dependencies in {len(pom_files)} POM files")

        for pom_file in pom_files:
            PomUtils.apply_selected_notes(pom_file, dependency_versions)
