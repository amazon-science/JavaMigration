"""Hybrid agent with preprocessing and migration."""

from typing import List, Any

from strands_tools import editor

from java_migration_agent.config.settings import Config
from java_migration_agent.core.base_agent import BaseMigrationAgent
from java_migration_agent.core.repository import Repository
from java_migration_agent.preprocessing import update_jdk_related, update_dependency_version
from java_migration_agent.tools.shell_tools import create_restricted_shell


class HybridAgent(BaseMigrationAgent):
    """
    Hybrid migration agent with preprocessing.

    This agent:
    1. Preprocesses the repository by updating JDK settings and dependencies
    2. Then uses shell and editor to fix any remaining issues

    The preprocessing gives the agent a head start on common migration tasks.
    """

    def __init__(self, config: Config):
        """
        Initialize the hybrid agent.

        Args:
            config: Configuration object
        """
        super().__init__(config, agent_type="hybrid")

    def prepare_repository(self, repo: Repository) -> None:
        """
        Prepare the repository by applying seed changes.

        Args:
            repo: Repository object
        """
        update_jdk_related(repo.path)
        update_dependency_version(repo.path)

    def get_tools(self) -> List[Any]:
        """
        Get the list of tools for this agent.

        Returns:
            List containing restricted shell and editor
        """
        if not self.repository:
            raise ValueError("Repository must be set before getting tools")

        restricted_shell = create_restricted_shell(self.repository.path)
        return [restricted_shell, editor]
