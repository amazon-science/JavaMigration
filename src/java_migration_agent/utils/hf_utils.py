"""HuggingFace utility functions."""

import logging
from typing import List

logger = logging.getLogger(__name__)


def get_repo_ids_from_dataset(dataset_name: str) -> List[str]:
    """
    Get all repository IDs from a HuggingFace dataset.

    Args:
        dataset_name: HuggingFace dataset name (e.g., "AmazonScience/migration-bench-java-selected")

    Returns:
        List of repository IDs (format: "owner/repo")
    """
    try:
        from datasets import load_dataset
    except ImportError:
        raise ImportError(
            "The 'datasets' package is required to load from HuggingFace. "
            "Install it with: pip install datasets"
        )

    logger.info(f"Loading dataset {dataset_name} from HuggingFace (test split)")
    dataset = load_dataset(dataset_name, split="test")

    repo_ids = []
    for item in dataset:
        # The column is called "repo" and contains values like "owner/repo"
        repo = item.get("repo")
        if repo:
            repo_ids.append(repo)

    logger.info(f"Found {len(repo_ids)} repositories in {dataset_name}")
    return repo_ids
