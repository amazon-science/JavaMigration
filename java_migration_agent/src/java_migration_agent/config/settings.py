"""Centralized configuration for Java Migration Agent."""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelConfig:
    """Configuration for the LLM model."""

    model_id: str = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    temperature: float = 1.0
    region_name: str = "us-west-2"
    max_retries: int = 3
    thinking_budget_tokens: int = 2048

    @classmethod
    def from_dict(cls, config: dict) -> "ModelConfig":
        """Create ModelConfig from dictionary."""
        return cls(**{k: v for k, v in config.items() if k in cls.__annotations__})


@dataclass
class AgentConfig:
    """Configuration for agent behavior."""

    max_messages: int = 160
    shell_timeout: int = 300
    bypass_tool_consent: bool = True

    # System prompts for different agent types
    baseline_system_prompt: str = (
        "You are an expert Java developer assistant who can migrate Java projects "
        "from JDK 8 to JDK 17. Make sure `mvn clean verify` pass with JDK 17 after "
        "migration. When `mvn clean verify` succeeds, you can conclude the task. "
        "You don't have to provide any summary."
    )

    baseline_pe_system_prompt: str = (
        "You are an expert Java developer assistant who can migrate Java projects "
        "from JDK 8 to JDK 17. Make sure `mvn clean verify` pass with JDK 17 after "
        "migration. You should update all dependencies in the `pom.xml` file to their "
        "latest versions that support Java 17. When `mvn clean verify` succeeds, you "
        "can conclude the task. You don't have to provide any summary."
    )

    hybrid_system_prompt: str = (
        "You are an expert Java developer assistant who can migrate Java projects "
        "from JDK 8 to JDK 17. Make sure `mvn clean verify` pass with JDK 17 after "
        "migration. Dependencies in the `pom.xml` file have been updated to their "
        "latest versions that support Java 17, but these changes might introduce "
        "compatibility issues in the codebase. Please fix any such issues in your "
        "migration. Do not downgrade the dependency versions back to their JDK 8 "
        "compatible versions."
    )

    rag_system_prompt: str = (
        "You are an expert Java developer assistant who can migrate Java projects "
        "from JDK 8 to JDK 17. Make sure `mvn clean verify` pass with JDK 17 after "
        "migration.\n\n"
        "You have access to a dependency version lookup tool. When updating dependencies "
        "in pom.xml:\n"
        "1. Use the search_dependency_version tool to look up the recommended Java 17 "
        "compatible version for each dependency\n"
        "2. If a dependency is not found in the database, use your knowledge to select "
        "an appropriate version\n"
        "3. Update all dependencies to their Java 17 compatible versions"
    )

    def get_system_prompt(self, agent_type: str) -> str:
        """Get system prompt for specific agent type."""
        prompts = {
            "baseline": self.baseline_system_prompt,
            "pe": self.baseline_pe_system_prompt,
            "hybrid": self.hybrid_system_prompt,
            "rag": self.rag_system_prompt,
        }
        return prompts.get(agent_type, self.baseline_system_prompt)

    def apply_env_vars(self) -> None:
        """Apply configuration to environment variables."""
        os.environ["BYPASS_TOOL_CONSENT"] = str(self.bypass_tool_consent).lower()
        os.environ["SHELL_DEFAULT_TIMEOUT"] = str(self.shell_timeout)


@dataclass
class ExperimentConfig:
    """Configuration for experiment execution."""

    exp_id: str
    hf_dataset: str = "AmazonScience/migration-bench-java-selected"  # HuggingFace dataset name
    output_dir: str = "./migration_results"
    max_workers: int = 8
    require_maximal_migration: bool = True

    def get_repo_output_dir(self, repo_id: str) -> str:
        """Get output directory for a specific repository."""
        repo_id = repo_id.replace("/", "__")  # Sanitize repo_id for filesystem
        return os.path.join(self.output_dir, self.exp_id, repo_id)


@dataclass
class Config:
    """Complete configuration for the migration agent."""

    model: ModelConfig = field(default_factory=ModelConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    experiment: Optional[ExperimentConfig] = None

    @classmethod
    def from_dict(cls, config: dict) -> "Config":
        """Create Config from dictionary."""
        return cls(
            model=ModelConfig.from_dict(config.get("model", {})),
            agent=AgentConfig(**{k: v for k, v in config.get("agent", {}).items() if k in AgentConfig.__annotations__}),
            experiment=ExperimentConfig(**config["experiment"]) if "experiment" in config else None,
        )

    def initialize(self) -> None:
        """Initialize configuration (apply env vars, etc.)."""
        self.agent.apply_env_vars()
