"""Factory for creating LLM models."""

from botocore.config import Config as BotocoreConfig
from strands.models import BedrockModel

from java_migration_agent.config.settings import ModelConfig


def create_bedrock_model(config: ModelConfig) -> BedrockModel:
    """
    Create a Bedrock model from configuration.

    Args:
        config: Model configuration

    Returns:
        Configured BedrockModel instance
    """
    return BedrockModel(
        model_id=config.model_id,
        region_name=config.region_name,
        temperature=config.temperature,
        boto_client_config=BotocoreConfig(
            retries={"max_attempts": config.max_retries, "mode": "standard"}
        ),
        additional_request_fields={
            "thinking": {"type": "enabled", "budget_tokens": config.thinking_budget_tokens}
        },
    )
