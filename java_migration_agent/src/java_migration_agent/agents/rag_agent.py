"""RAG-enhanced agent with dependency version lookup."""

from typing import List, Any

from strands_tools import editor

from java_migration_agent.config.settings import Config
from java_migration_agent.core.base_agent import BaseMigrationAgent
from java_migration_agent.tools.dependency_tools import search_dependency_version
from java_migration_agent.tools.shell_tools import create_restricted_shell


class RAGAgent(BaseMigrationAgent):
    """
    RAG-enhanced migration agent with dependency version lookup.

    This agent has access to:
    - A restricted shell for running commands
    - An editor for modifying files
    - A dependency version search tool that provides Java 17 compatible versions

    The search tool allows the agent to look up recommended versions for dependencies
    rather than guessing or using outdated versions.
    """

    def __init__(self, config: Config):
        """
        Initialize the RAG agent.

        Args:
            config: Configuration object
        """
        super().__init__(config, agent_type="rag")

    def get_tools(self) -> List[Any]:
        """
        Get the list of tools for this agent.

        Returns:
            List containing restricted shell, editor, and dependency search
        """
        if not self.repository:
            raise ValueError("Repository must be set before getting tools")

        restricted_shell = create_restricted_shell(self.repository.path)
        return [restricted_shell, editor, search_dependency_version]
