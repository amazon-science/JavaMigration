"""Baseline agent that migrates with minimal guidance."""

from typing import List, Any

from strands_tools import editor

from java_migration_agent.config.settings import Config
from java_migration_agent.core.base_agent import BaseMigrationAgent
from java_migration_agent.tools.shell_tools import create_restricted_shell


class BaselineAgent(BaseMigrationAgent):
    """
    Baseline migration agent with minimal tools.

    This agent only has access to:
    - A restricted shell for running commands
    - An editor for modifying files

    It must discover and implement all migration steps on its own.
    """

    def __init__(self, config: Config):
        """
        Initialize the baseline agent.

        Args:
            config: Configuration object
        """
        super().__init__(config, agent_type="baseline")

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
