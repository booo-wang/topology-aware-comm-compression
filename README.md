# Topology-Aware Communication Compression

Research scaffold for studying communication-efficient multi-agent coordination under partial observability.

This repository is the skeleton for Project B:

**Topology-Aware Communication Compression for Multi-Agent Partial Observability**

The project now supports more than a single smoke run:

- a synthetic sensor-fusion environment with partial observations
- configurable communication topologies
- multiple message compressors, including adaptive heuristics
- message dropout for robustness experiments
- batch benchmark sweeps over topologies, budgets, and visibility settings
- JSON result persistence for later plotting and report writing

## Research Question

Under a fixed communication budget, which message compression strategies preserve the most useful global information across different multi-agent communication topologies?

## Current Components

- Environments:
  - synthetic sensor fusion
- Topologies:
  - chain
  - ring
  - star
  - fully connected
- Compression baselines:
  - `full_state`
  - `novelty_topk`
  - `novelty_then_fill`
  - `degree_aware_novelty`
  - `random_k`
- Metrics:
  - mean / min / max recall
  - communication cost
  - message count
  - recall-per-cost efficiency
  - per-hop recall trajectory

## Repository Layout

```text
configs/     experiment and sweep configs
docs/        project notes and roadmap
results/     saved benchmark outputs
scripts/     runnable helper scripts
src/tacc/    library code
tests/       smoke tests
```

## Quick Start

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
```

Run a single experiment:

```powershell
$env:PYTHONPATH='D:\github_project\topology-aware-comm-compression\src'
py -3 scripts/run_smoke.py
```

Run a benchmark sweep and persist results:

```powershell
$env:PYTHONPATH='D:\github_project\topology-aware-comm-compression\src'
py -3 scripts/run_benchmark.py
```

Or run the package entry point directly:

```powershell
$env:PYTHONPATH='D:\github_project\topology-aware-comm-compression\src'
py -3 -m tacc.training.runner --config configs/sensor_fusion_baseline.toml --save
```

## Why This Repo Exists

This repo is meant to become the engineering companion to a research project, not just a one-off demo. The goal is to make future experiments easy to run, compare, save, and explain.
