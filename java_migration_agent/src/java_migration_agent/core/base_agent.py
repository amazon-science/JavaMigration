"""Base class for all migration agents."""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Optional, List, Any

from strands import Agent
from strands.agent.conversation_manager import NullConversationManager

from java_migration_agent.config.settings import Config
from java_migration_agent.core.repository import Repository
from java_migration_agent.core.model_factory import create_bedrock_model
from java_migration_agent.evaluation.evaluator import Evaluator
from java_migration_agent.hooks.agent_hooks import MessageLimitHook, MaxMessageLimitException

logger = logging.getLogger(__name__)


class BaseMigrationAgent(ABC):
    """Abstract base class for Java migration agents."""

    def __init__(
        self,
        config: Config,
        agent_type: str = "baseline",
    ):
        """
        Initialize the migration agent.

        Args:
            config: Configuration object
            agent_type: Type of agent (baseline, hybrid, rag, etc.)
        """
        self.config = config
        self.agent_type = agent_type
        self.config.initialize()

        # Will be set when migrating a repo
        self.repository: Optional[Repository] = None
        self.agent: Optional[Agent] = None
        self.evaluator = Evaluator()

    @abstractmethod
    def get_tools(self) -> List[Any]:
        """
        Get the list of tools for this agent.

        Returns:
            List of Strands tools
        """
        pass

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.

        Returns:
            System prompt string
        """
        return self.config.agent.get_system_prompt(self.agent_type)

    def get_user_input(self, repo_path: str) -> str:
        """
        Generate the initial user input prompt.

        Args:
            repo_path: Path to the repository

        Returns:
            User input string
        """
        return f"The code repository located at {repo_path} is currently written in Java 8. Please migrate the entire codebase to Java 17."

    def prepare_repository(self, repo: Repository) -> None:
        """
        Prepare the repository before migration (optional hook for subclasses).

        Args:
            repo: Repository object
        """
        pass

    def create_agent(self) -> Agent:
        """
        Create a Strands agent with the appropriate configuration.

        Returns:
            Configured Strands Agent
        """
        model = create_bedrock_model(self.config.model)
        tools = self.get_tools()
        system_prompt = self.get_system_prompt()

        return Agent(
            model=model,
            tools=tools,
            system_prompt=system_prompt,
            conversation_manager=NullConversationManager(),
            hooks=[MessageLimitHook(max_messages=self.config.agent.max_messages)],
        )

    def migrate(self, repository: Repository) -> dict:
        """
        Execute migration on a repository.

        Args:
            repository: Repository object to migrate

        Returns:
            Dictionary with migration results
        """
        self.repository = repository
        self.agent = self.create_agent()

        # Prepare repository (subclasses can override)
        self.prepare_repository(repository)

        # Generate user input
        user_input = self.get_user_input(repository.path)
        logger.info(f"Starting migration for {repository.repo_id}")
        logger.info(f"User input: {user_input}")

        messages = []
        max_success = False
        min_success = False

        try:
            # Run the agent
            _ = self.agent(user_input)
            messages = self.agent.messages
        except MaxMessageLimitException as e:
            logger.warning(f"Message limit reached: {e}")
            messages = self.agent.messages
        except Exception as e:
            logger.error(f"Error during migration: {e}")
            messages = self.agent.messages if hasattr(self.agent, "messages") else []

        # Evaluate migration results
        try:
            max_success = self.evaluator.evaluate(
                repo_path=repository.path,
                github_url=repository.github_url,
                require_maximal_migration=True,
            )
            min_success = self.evaluator.evaluate(
                repo_path=repository.path,
                github_url=repository.github_url,
                require_maximal_migration=False,
            )
        except Exception as e:
            logger.error(f"Error during evaluation: {e}")

        return {
            "messages": messages,
            "max_success": max_success,
            "min_success": min_success,
        }

    def save_results(self, repo_id: str, results: dict) -> None:
        """
        Save migration results to disk.

        Args:
            repo_id: Repository identifier
            results: Migration results dictionary
        """
        if not self.config.experiment:
            logger.warning("No experiment config provided, skipping save")
            return

        output_dir = os.path.join(self.config.experiment.output_dir, self.config.experiment.exp_id)
        os.makedirs(output_dir, exist_ok=True)

        # Create output data with renamed keys
        output_data = {
            "max_migration_success": results["max_success"],
            "min_migration_success": results["min_success"],
            "trajectory": results["messages"],
        }

        # Save to single JSON file named after repo_id
        filename = repo_id.replace("/", "__") + ".json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(output_data, f, indent=2)

        logger.info(f"Results saved to {filepath}")
