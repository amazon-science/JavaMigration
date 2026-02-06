# ☕ JavaMigration
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


🚀 Repository for automated Java code migration research, part of the [MigrationBench](https://huggingface.co/collections/AmazonScience/migrationbench-68125452fc21a4564b92b6c3) project.


## 📦 Packages

This repository contains **two** sub-packages to conduct Java code migration with LLMs:

### 1. 🤖 [JavaMigrationAgent](./java_migration_agent)

[**JavaMigrationAgent**](./java_migration_agent) is an LLM-based agent to automate Java 8 to Java 17 (21) migration,
built on top of the [Strands Agents](https://strandsagents.com/latest/) framework.

- It supports multiple migration strategies including baseline, PE (prompt engineering), RAG, and a hybrid approach (More cost effective).

### 2. 🔧 [SDFeedback](./self_debug)

[**SDFeedback**](./self_debug) runs code migration implementation with LLMs by providing self debugging feedback,
motivated by the [Teaching Large Language Models to Self-Debug](https://arxiv.org/abs/2304.05128) paper.

- It includes both single-job and batch processing capabilities with AWS EMRS support.


## 📊 Data

Agent trajectories and execution results are stored in the `data/` folder.

## 🔗 Resources

1. 🤗 [MigrationBench (Hugging Face)](https://huggingface.co/collections/AmazonScience/migrationbench-68125452fc21a4564b92b6c3)
1. 💻 [MigrationBench (GitHub)](https://github.com/amazon-science/MigrationBench)
1. 📄 [arXiv Paper](https://arxiv.org/abs/2505.09569)


## 📚 Citation

```bibtex
@misc{liu2025migrationbenchrepositorylevelcodemigration,
      title={MigrationBench: Repository-Level Code Migration Benchmark from Java 8},
      author={Linbo Liu and Xinle Liu and Qiang Zhou and Lin Chen and Yihan Liu and Hoan Nguyen and Behrooz Omidvar-Tehrani and Xi Shen and Jun Huan and Omer Tripp and Anoop Deoras},
      year={2025},
      eprint={2505.09569},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2505.09569},
}
```
