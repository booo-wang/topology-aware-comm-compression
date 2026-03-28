# 拓扑感知通信压缩

Practical toolkit for exploring communication-efficient multi-agent coordination under partial observability.

**Topology-Aware Communication Compression for Multi-Agent Partial Observability**

This repository is designed as a portfolio-oriented systems project in the multi-agent direction.  
It focuses on configurable simulation, communication strategy comparison, and polished result presentation.

## 项目定位

This is not a paper-first benchmark repo.

Instead, it is meant to show practical capability in:

- building reusable multi-agent simulation tooling
- comparing communication strategies under constraints
- organizing experiment outputs into readable artifacts
- presenting technical work clearly on GitHub

## 项目亮点

- Synthetic sensor-fusion environment with partial observations
- Configurable communication topologies
- Multiple message compression strategies
- Robustness testing with message dropout
- Sweep-based experiment execution
- JSON result persistence
- Markdown report export
- Static HTML dashboard generation

## 项目结构

```text
configs/     experiment, sweep, and demo configs
docs/        project notes and roadmap
results/     saved benchmark outputs and generated reports
scripts/     runnable helper scripts
src/tacc/    library code
tests/       smoke tests
```

## 快速开始

Create a virtual environment and install the package:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
```

Run a single baseline experiment:

```powershell
py -3 scripts/run_smoke.py
```

Run the larger benchmark sweep:

```powershell
py -3 scripts/run_benchmark.py
```

Run the lighter demo suite for portfolio presentation:

```powershell
py -3 scripts/run_demo_suite.py
```

Export the latest benchmark output as Markdown:

```powershell
py -3 scripts/export_markdown_report.py
```

Generate a static dashboard page:

```powershell
py -3 scripts/generate_dashboard.py
```

## 核心能力

### Communication Design

- Compare chain, ring, star, and fully connected topologies
- Evaluate budgeted message passing under constrained communication
- Observe how topology changes recall and efficiency

### Experiment Workflow

- Run single experiments and sweep configurations
- Save outputs automatically into the repository `results/` directory
- Reuse the same pipeline for quick demos and larger comparisons

### Presentation Layer

- Produce JSON artifacts for reproducibility
- Export Markdown summaries for GitHub-friendly reporting
- Generate a static HTML dashboard for visual presentation

## 当前支持

### Topologies

- `chain`
- `ring`
- `star`
- `fully_connected`

### Compressors

- `full_state`
- `novelty_topk`
- `novelty_then_fill`
- `degree_aware_novelty`
- `random_k`

### Outputs

- experiment JSON files
- benchmark JSON files
- `REPORT.md`
- `dashboard.html`

## 推荐使用流程

1. Run `py -3 scripts/run_demo_suite.py`
2. Run `py -3 scripts/export_markdown_report.py`
3. Run `py -3 scripts/generate_dashboard.py`
4. Use the generated files in `results/` as portfolio artifacts
