# Topology-Aware Communication Compression

Research scaffold for studying communication-efficient multi-agent coordination under partial observability.

This repository is the skeleton for Project B:

**Topology-Aware Communication Compression for Multi-Agent Partial Observability**

The current version focuses on a lightweight, reproducible core:

- a synthetic sensor-fusion environment with partial observations
- configurable communication topologies
- baseline message compressors
- a small evaluation runner for communication budget vs. recovery quality

## Research Question

Under a fixed communication budget, which message compression strategies preserve the most useful global information across different multi-agent communication topologies?

## Initial Scope

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
- Metrics:
  - object recall
  - communication cost
  - message count
  - hop-wise recovery

## Repository Layout

```text
configs/     experiment configs
docs/        project notes and roadmap
scripts/     runnable helper scripts
src/tacc/    library code
tests/       smoke tests
```

## Quick Start

Create a virtual environment with Python 3 and install the package in editable mode:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
```

Run the smoke experiment:

```powershell
py -3 scripts/run_smoke.py
```

Or run the package entry point directly:

```powershell
py -3 -m tacc.training.runner --config configs/sensor_fusion_baseline.toml
```

## Near-Term Milestones

1. Replace hand-crafted compression with learnable set encoders.
2. Add topology-aware routing and budget allocation.
3. Evaluate topology shift, noise, and scaling to more agents.
4. Add visualization for message propagation and hop degradation.

## Why This Repo Exists

This repo is meant to become the engineering companion to a research project, not just a one-off demo. The goal is to make future experiments easy to run, compare, and explain.
