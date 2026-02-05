"""Example: Migrate a single repository."""

import logging

from java_migration_agent.agents import RAGAgent
from java_migration_agent.config.settings import Config, ModelConfig, AgentConfig, ExperimentConfig
from java_migration_agent.core.repository import Repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Migrate a single repository using the RAG agent."""

    # Create configuration
    config = Config(
        model=ModelConfig(
            model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
            temperature=1.0,
        ),
        agent=AgentConfig(
            max_messages=80,
        ),
        experiment=ExperimentConfig(
            exp_id="single_repo_test",
            hf_dataset="AmazonScience/migration-bench-java-selected",
            output_dir="./results",
        ),
    )

    # Load repository from HuggingFace dataset (will clone from GitHub)
    repo_id = "15093015999/EJServer"  # Format: "owner/repo"
    logger.info(f"Loading repository {repo_id} from HuggingFace dataset")

    try:
        repository = Repository.from_huggingface(
            dataset_name="AmazonScience/migration-bench-java-selected",
            repo_id=repo_id,
            exp_id="single_repo_test"
        )
    except Exception as e:
        logger.error(f"Failed to load repository: {e}")
        return

    logger.info(f"Repository loaded at: {repository.path}")
    logger.info(f"GitHub URL: {repository.github_url}")
    logger.info(f"Base commit: {repository.base_commit}")

    # Create RAG agent
    agent = RAGAgent(config)
    logger.info("RAG agent created")

    # Run migration
    logger.info("Starting migration...")
    results = agent.migrate(repository)

    # Print results
    logger.info("Migration completed!")
    logger.info(f"Max success: {results['max_success']}")
    logger.info(f"Min success: {results['min_success']}")
    logger.info(f"Messages exchanged: {len(results['messages'])}")

    # Save results
    agent.save_results(repository.repo_id, results)
    logger.info("Results saved")


if __name__ == "__main__":
    main()
