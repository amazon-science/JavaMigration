# Java Migration Agent

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

<!-- toc -->

- [1. Overview](#1-overview)
- [2. MigrationBench Datasets](#2-migrationbench-datasets)
- [3. Installation](#3-installation)
  * [3.1 Prerequisites](#31-prerequisites)
  * [3.2 Install Package](#32-install-package)
- [4. Usage](#4-usage)
  * [4.1 Agent Types](#41-agent-types)
  * [4.2 Running Migration](#42-running-migration)
  * [4.3 Command Line Options](#43-command-line-options)
- [5. Citation](#5-citation)

<!-- tocstop -->

## 1. Overview

Java Migration Agent is a library for automated code migration from Java 8 to Java 17 using LLM-based agents built on the [Strands Agents](https://github.com/strands-agents/strands-agents) framework.

It provides multiple agent strategies for migration:
- **Baseline**: Direct LLM-based migration
- **PE (Prompt Engineering)**: Baseline with enhanced prompts for dependency updates
- **RAG**: Uses retrieval-augmented generation for dependency version lookup
- **Hybrid**: Pre-processes dependencies before LLM migration

The agent relies on the [MigrationBench](https://github.com/amazon-science/MigrationBench) package for evaluation.

## 2. [MigrationBench](https://huggingface.co/collections/AmazonScience/migrationbench-68125452fc21a4564b92b6c3) Datasets

| Index | Dataset                                       | Size  | Notes                                                                                               |
|-------|-----------------------------------------------|-------|-----------------------------------------------------------------------------------------------------|
| 1     | [AmazonScience/migration-bench-java-full](https://huggingface.co/datasets/AmazonScience/migration-bench-java-full)         | 5,102 | Each repo has a test directory or at least one test case                              |
| 2     | [AmazonScience/migration-bench-java-selected](https://huggingface.co/datasets/AmazonScience/migration-bench-java-selected) |   300 | A **subset** of migration-bench-java-full                                          |

## 3. Installation

### 3.1 Prerequisites

Verify you have `java 17` and `maven 3.9.6` installed:

```bash
# java
$ java --version
openjdk 17.0.15 2025-04-15 LTS
OpenJDK Runtime Environment Corretto-17.0.15.6.1 (build 17.0.15+6-LTS)
OpenJDK 64-Bit Server VM Corretto-17.0.15.6.1 (build 17.0.15+6-LTS, mixed mode, sharing)
```

```bash
# maven
$ mvn --version
Apache Maven 3.9.6 (bc0240f3c744dd6b6ec2920b3cd08dcc295161ae)
Maven home: /usr/local/bin/apache-maven-3.9.6
Java version: 17.0.15, vendor: Amazon.com Inc., runtime: /usr/lib/jvm/java-17-amazon-corretto.x86_64
```
If you haven't done it yet, follow the instructions in [MigrationBench](https://github.com/amazon-science/MigrationBench) to install Maven.

### 3.2 Install Package

```bash
cd java_migration_agent
pip install -e .
```

Or with uv:

```bash
cd java_migration_agent
uv pip install -e .
```

## 4. Usage

### 4.1 Agent Types

| Agent Type | Description |
|------------|-------------|
| `baseline` | Direct LLM migration with `mvn clean verify` |
| `pe`       | Baseline with prompt engineering for dependency updates |
| `rag`      | Uses dependency version lookup tool for migration |
| `hybrid`   | Pre-processes pom.xml dependencies before LLM migration |

### 4.2 Running Migration

Run batch migration on the MigrationBench dataset:

```bash
python -m java_migration_agent \
    --agent-type baseline \
    --exp-id exp-001 \
    --hf-dataset AmazonScience/migration-bench-java-selected \
    --model-id global.anthropic.claude-sonnet-4-5-20250929-v1:0 \
    --max-workers 8 \
    --output-dir ./migration_results
```

### 4.3 Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--agent-type` | (required) | Agent type: `baseline`, `pe`, `rag`, or `hybrid` |
| `--exp-id` | (required) | Experiment identifier for organizing results |
| `--hf-dataset` | `AmazonScience/migration-bench-java-selected` | HuggingFace dataset name |
| `--model-id` | `global.anthropic.claude-sonnet-4-5-20250929-v1:0` | Bedrock model ID |
| `--temperature` | `1.0` | Model temperature |
| `--max-messages` | `80` | Maximum messages per conversation |
| `--max-workers` | `8` | Maximum parallel workers |
| `--output-dir` | `./migration_results` | Output directory for results |

## 5. 📚 Citation
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
