"""Example: Migrate repositories from HuggingFace dataset."""

import logging

from java_migration_agent.agents import BaselineAgent
from java_migration_agent.config.settings import Config, ModelConfig, AgentConfig, ExperimentConfig
from java_migration_agent.orchestrator import MigrationOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Migrate repositories from HuggingFace dataset."""

    # Create configuration for HuggingFace dataset
    config = Config(
        model=ModelConfig(
            model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
            temperature=1.0,
        ),
        agent=AgentConfig(
            max_messages=80,
        ),
        experiment=ExperimentConfig(
            exp_id="hf_baseline_20260205",
            hf_dataset="AmazonScience/migration-bench-java-selected",  # or migration-bench-java-full
            output_dir="./results",
            max_workers=8,
        ),
    )

    # Create orchestrator with baseline agent
    orchestrator = MigrationOrchestrator(agent_class=BaselineAgent, config=config)

    logger.info("Starting batch migration from HuggingFace dataset")
    logger.info(f"Dataset: {config.experiment.hf_dataset}")

    try:
        orchestrator.run_batch_migration()
        logger.info("Migration completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()
