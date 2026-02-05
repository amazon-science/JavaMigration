# JavaMigration
<table>
  <tr>
    <td style="padding: 0;">
      <a href="https://huggingface.co/collections/AmazonScience/migrationbench-68125452fc21a4564b92b6c3">
        <img src="https://img.shields.io/badge/-🤗 MigrationBench-4d5eff?style=flatten&labelColor" alt="MigrationBench (Hugging Face)">
      </a>
    </td>
    <td style="padding: 0;">
      <a href="https://github.com/amazon-science/MigrationBench">
        <img src="https://img.shields.io/badge/MigrationBench-000000?style=flatten&logo=github" alt="MigrationBench (GitHub)">
      </a>
    </td>
    <td style="padding: 0;">
      <a href="https://github.com/amazon-science/JavaMigration">
        <img src="https://img.shields.io/badge/JavaMigration-000000?style=flatten&logo=github&logoColor=white" alt="JavaMigration (GitHub)">
      </a>
    </td>
    <td style="padding: 0;">
      <a href="https://arxiv.org/abs/2505.09569">
        <img src="https://img.shields.io/badge/arXiv-2505.09569-b31b1b.svg?style=flatten" alt="MigrationBench (arXiv)">
      </a>
    </td>
    <td style="padding: 0; padding-left: 10px; vertical-align: middle;">
      <a href="https://huggingface.co/datasets/AmazonScience/migration-bench-java-full">
        <img src="https://img.shields.io/badge/-🤗 java--full-8a98ff?style=flat&labelColor" alt="java-full">
      </a>
    </td>
    <td style="padding: 0; vertical-align: middle;">
      <a href="https://huggingface.co/datasets/AmazonScience/migration-bench-java-selected">
        <img src="https://img.shields.io/badge/-🤗 java--selected-8a98ff?style=flat&labelColor" alt="java-selected">
      </a>
    </td>
  </tr>
</table>

Repository for automated Java code migration research, part of the [MigrationBench](https://huggingface.co/collections/AmazonScience/migrationbench-68125452fc21a4564b92b6c3) project.

## Packages

This repository contains two main packages for Java code migration:

### [java_migration_agent](./java_migration_agent)
LLM-based agent library for automated Java 8 to Java 17 migration, built on the [Strands Agents](https://strandsagents.com/latest/) framework. Supports multiple migration strategies including baseline, PE (prompt engineering), RAG, and hybrid approaches.

### [self_debug](./self_debug)
SDFeedback implementation for code migration with LLMs using self-debugging feedback. Includes both single-job and batch processing capabilities with AWS EMRS support.

## Resources

- [MigrationBench (Hugging Face)](https://huggingface.co/collections/AmazonScience/migrationbench-68125452fc21a4564b92b6c3)
- [MigrationBench (GitHub)](https://github.com/amazon-science/MigrationBench)
- [arXiv Paper](https://arxiv.org/abs/2505.09569)

## Citation

```bibtex
@misc{liu2025migrationbenchrepositorylevelcodemigration,
      title={MIGRATION-BENCH: Repository-Level Code Migration Benchmark from Java 8},
      author={Linbo Liu and Xinle Liu and Qiang Zhou and Lin Chen and Yihan Liu and Hoan Nguyen and Behrooz Omidvar-Tehrani and Xi Shen and Jun Huan and Omer Tripp and Anoop Deoras},
      year={2025},
      eprint={2505.09569},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2505.09569},
}
```
