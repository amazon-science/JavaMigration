"""Main entry point for running migration experiments."""

import argparse
import logging
import sys

from java_migration_agent.agents import BaselineAgent, HybridAgent, RAGAgent
from java_migration_agent.config.settings import Config, ModelConfig, AgentConfig, ExperimentConfig
from java_migration_agent.orchestrator import MigrationOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


AGENT_TYPES = {
    "baseline": BaselineAgent,
    "pe": BaselineAgent,
    "hybrid": HybridAgent,
    "rag": RAGAgent,
}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run Java 8 to 17 migration experiments")

    parser.add_argument(
        "--agent-type",
        type=str,
        required=True,
        choices=list(AGENT_TYPES.keys()),
        help="Type of agent to use (baseline, pe, hybrid, or rag)",
    )

    parser.add_argument(
        "--exp-id",
        type=str,
        required=True,
        help="Experiment identifier for organizing results",
    )

    # Data source configuration
    parser.add_argument(
        "--hf-dataset",
        type=str,
        default="AmazonScience/migration-bench-java-selected",
        help="HuggingFace dataset name. "
        "Options: AmazonScience/migration-bench-java-selected or AmazonScience/migration-bench-java-full",
    )

    # Model configuration
    parser.add_argument(
        "--model-id",
        type=str,
        default="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        help="Bedrock model ID to use",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Model temperature",
    )

    # Agent configuration
    parser.add_argument(
        "--max-messages",
        type=int,
        default=80,
        help="Maximum number of messages per conversation",
    )

    parser.add_argument(
        "--max-workers",
        type=int,
        default=8,
        help="Maximum number of parallel workers",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./migration_results",
        help="Directory for storing results",
    )

    args = parser.parse_args()

    # Create configuration
    config = Config(
        model=ModelConfig(
            model_id=args.model_id,
            temperature=args.temperature,
        ),
        agent=AgentConfig(
            max_messages=args.max_messages,
        ),
        experiment=ExperimentConfig(
            exp_id=args.exp_id,
            hf_dataset=args.hf_dataset,
            output_dir=args.output_dir,
            max_workers=args.max_workers,
        ),
    )

    # Get agent class
    agent_class = AGENT_TYPES[args.agent_type]

    # Create orchestrator and run
    orchestrator = MigrationOrchestrator(agent_class=agent_class, config=config)

    logger.info(f"Starting {args.agent_type} agent with experiment ID: {args.exp_id}")
    logger.info(f"Model: {args.model_id}")
    logger.info(f"HuggingFace Dataset: {args.hf_dataset}")

    try:
        orchestrator.run_batch_migration()
        logger.info("Migration completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
