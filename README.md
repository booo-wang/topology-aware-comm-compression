# 拓扑感知通信压缩

Experimental sandbox for studying communication topology and message compression under partial observability in multi-agent sensor fusion.

**Topology-Aware Communication Compression for Multi-Agent Partial Observability**

This repository investigates a simple but useful question:

**How do communication topology and message compression affect information recovery when agents cannot directly observe the full global state?**

It is not intended to be the final paper repository for a single method.  
Instead, it serves as a lightweight comparative testbed for analyzing communication behavior, comparing heuristics, and organizing early experimental observations.

## 研究问题

The current version focuses on three linked questions:

- How much does topology matter under the same communication budget?
- When does novelty-based compression outperform naive full-state transmission?
- Which settings offer the best recovery-efficiency tradeoff rather than only the best raw recall?

## 研究背景

This project is motivated by a broader interest in set-structured representations and communication under partial observability.

In multi-agent systems, each agent often sees only a subset of the environment.  
To recover useful global information, the system must decide:

- what to communicate
- how much to communicate
- who should communicate with whom

This repository studies those questions in a controlled sensor-fusion setting.  
The goal is not to claim a new method yet, but to build a clean environment for comparing communication behavior before moving into a more method-centered research project.

## 当前观察

At the current heuristic stage, the experiments already suggest several useful patterns:

- fully connected communication tends to maximize recall quickly, but often at higher communication cost
- ring topologies can provide strong recall-efficiency tradeoffs under moderate budgets
- novelty-based compression usually behaves better than naive full-state transmission when bandwidth is constrained
- per-hop recall trajectories are often more informative than final recall alone

These are working observations rather than paper claims, but they make the project look more like an experimental investigation than a pure engineering demo.

## 项目亮点

- Synthetic sensor-fusion environment with partial observations
- Configurable communication topologies
- Multiple message compression strategies
- Message dropout for robustness testing
- Sweep-based experiment execution
- JSON result persistence
- Markdown report export
- Static HTML dashboard generation

## 项目结构

```text
configs/     experiment, sweep, and demo configs
docs/        notes and short research-facing context
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

If you prefer installed command entry points, you can also run:

```powershell
tacc-smoke
tacc-demo
tacc-benchmark
tacc-report
tacc-dashboard
```

Run the test suite:

```powershell
py -3 -m pytest tests -q
```

Run a single baseline experiment:

```powershell
py -3 scripts/run_smoke.py
```

Run the larger benchmark sweep:

```powershell
py -3 scripts/run_benchmark.py
```

Run the lighter demo suite:

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

### Communication Analysis

- Compare chain, ring, star, and fully connected topologies
- Evaluate budgeted message passing under constrained communication
- Observe how topology changes recall, cost, and efficiency

### Experimental Workflow

- Run single experiments and sweep configurations
- Save outputs automatically into the repository `results/` directory
- Reuse the same pipeline for quick demos and comparative runs

### Presentation Layer

- Produce JSON artifacts for reproducibility
- Export Markdown summaries for readable reporting
- Generate a static HTML dashboard for visual inspection

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
4. Review the generated files in `results/`

## 文档

- `docs/research_notes.md`: short research-facing framing and current observations
- `docs/roadmap.md`: implementation roadmap
