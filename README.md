# Topology-Aware Communication Compression

Practical toolkit for exploring communication-efficient multi-agent coordination under partial observability.

This repository is the skeleton for Project B:

**Topology-Aware Communication Compression for Multi-Agent Partial Observability**

The project is positioned as a portfolio-ready engineering artifact in the multi-agent direction:

- a synthetic sensor-fusion environment with partial observations
- configurable communication topologies
- multiple message compressors, including adaptive heuristics
- message dropout for robustness experiments
- batch benchmark sweeps over topologies, budgets, and visibility settings
- JSON result persistence for later plotting and report writing
- curated demo scenarios for quick showcase runs
- Markdown report export for GitHub-friendly summaries
- static HTML dashboard generation for presentation-ready visuals

## Project Goal

Build a clean, extensible sandbox for experimenting with how communication topology and message compression affect shared state recovery in a multi-agent system.

## What This Shows

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
- Engineering maturity:
  - configurable experiment runs
  - reusable sweep pipeline
  - result persistence
  - Markdown report export
  - static dashboard export
- Systems understanding:
  - communication topology effects
  - budgeted message passing
  - robustness to dropout
  - tradeoffs between recall and efficiency

## Repository Layout

```text
configs/     experiment, sweep, and demo configs
docs/        project notes and roadmap
results/     saved benchmark outputs and generated reports
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
py -3 scripts/run_smoke.py
```

Run a benchmark sweep and persist results:

```powershell
py -3 scripts/run_benchmark.py
```

Run a smaller demo suite that is easier to show in a portfolio:

```powershell
py -3 scripts/run_demo_suite.py
```

Export the latest benchmark output into a Markdown summary:

```powershell
py -3 scripts/export_markdown_report.py
```

Generate a static dashboard page from the latest benchmark output:

```powershell
py -3 scripts/generate_dashboard.py
```

Or run the package entry point directly:

```powershell
py -3 -m tacc.training.runner --config configs/sensor_fusion_baseline.toml --save
```

## Why This Repo Exists

This repo is meant to strengthen practical credibility in the multi-agent direction. The goal is to show that you can design a usable simulation toolkit, compare strategy variants cleanly, and present results in a way that feels polished on GitHub.
