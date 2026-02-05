"""Evaluator for migration success."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Evaluator:
    """Evaluates the success of a migration."""

    def __init__(self):
        """Initialize the evaluator."""
        pass

    def evaluate(
        self,
        repo_path: str,
        github_url: Optional[str] = None,
        require_maximal_migration: bool = False,
    ) -> bool:
        """
        Evaluate migration success.

        Args:
            repo_path: Path to the migrated repository
            github_url: Optional GitHub URL for the repository
            require_maximal_migration: Whether to require maximal migration

        Returns:
            True if migration succeeded, False otherwise

        Raises:
            ImportError: If migration_bench is not installed
        """
        # Import here to avoid circular dependencies
        from migration_bench.common import maven_utils
        from migration_bench.eval.final_eval import run_eval

        if github_url:
            success = run_eval(
                github_url=github_url,
                migrated_root_dir=repo_path,
                require_maximal_migration=require_maximal_migration,
            )
            return success

        return False
