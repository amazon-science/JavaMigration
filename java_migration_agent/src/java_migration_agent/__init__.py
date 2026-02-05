"""Java Migration Agent - A framework for automating Java 8 to Java 17 migrations."""

__version__ = "0.1.0"

from java_migration_agent.core.base_agent import BaseMigrationAgent
from java_migration_agent.agents.baseline_agent import BaselineAgent
from java_migration_agent.agents.hybrid_agent import HybridAgent
from java_migration_agent.agents.rag_agent import RAGAgent

__all__ = [
    "BaseMigrationAgent",
    "BaselineAgent",
    "HybridAgent",
    "RAGAgent",
]
