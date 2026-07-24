"""Orchestrator for running migration experiments."""

import concurrent.futures
import logging
from typing import Optional, Type

from java_migration_agent.config.settings import Config
from java_migration_agent.core.base_agent import BaseMigrationAgent
from java_migration_agent.core.repository import Repository
from java_migration_agent.utils.hf_utils import get_repo_ids_from_dataset

logger = logging.getLogger(__name__)


class MigrationOrchestrator:
    """Orchestrates batch migration experiments."""

    def __init__(
        self,
        agent_class: Type[BaseMigrationAgent],
        config: Config,
    ):
        """
        Initialize the orchestrator.

        Args:
            agent_class: The agent class to use (BaselineAgent, HybridAgent, etc.)
            config: Configuration object
        """
        self.agent_class = agent_class
        self.config = config

        if not self.config.experiment:
            raise ValueError("Experiment configuration is required")

    def migrate_single_repo(self, repo_id: str) -> None:
        """
        Migrate a single repository from HuggingFace dataset.

        Args:
            repo_id: Repository identifier
        """
        try:
            # Load repository from HuggingFace
            repository = Repository.from_huggingface(
                dataset_name=self.config.experiment.hf_dataset,
                repo_id=repo_id,
                exp_id=self.config.experiment.exp_id,
            )
            logger.info(f"Loaded repository: {repo_id} at {repository.path}")

            # Create and run agent
            agent = self.agent_class(self.config)
            results = agent.migrate(repository)

            # Save results
            agent.save_results(repo_id, results)

            logger.info(
                f"Completed {repo_id}: max_success={results['max_success']}, "
                f"min_success={results['min_success']}"
            )

        except Exception as e:
            logger.error(f"Error migrating repository {repo_id}: {e}", exc_info=True)

    def run_batch_migration(self, max_workers: Optional[int] = None) -> None:
        """
        Run migration on all repositories from HuggingFace dataset.

        Args:
            max_workers: Maximum number of parallel workers (defaults to config value)
        """
        if max_workers is None:
            max_workers = self.config.experiment.max_workers

        # Get repository IDs from HuggingFace dataset
        repo_ids = get_repo_ids_from_dataset(self.config.experiment.hf_dataset)
        logger.info(
            f"Starting batch migration for {len(repo_ids)} repositories "
            f"from HuggingFace dataset: {self.config.experiment.hf_dataset}"
        )

        # Process in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.migrate_single_repo, repo_id): repo_id
                for repo_id in repo_ids
            }

            for future in concurrent.futures.as_completed(futures):
                repo_id = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error processing repository {repo_id}: {e}")

        logger.info("Batch migration completed")
