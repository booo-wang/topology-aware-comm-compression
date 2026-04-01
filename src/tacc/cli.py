from __future__ import annotations

from pathlib import Path

from tacc.reporting.dashboard import main as dashboard_main
from tacc.reporting.markdown import main as report_main
from tacc.training.benchmark import main as benchmark_main
from tacc.training.runner import main as runner_main


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIGS_DIR = REPO_ROOT / "configs"
RESULTS_DIR = REPO_ROOT / "results"


def smoke() -> None:
    runner_main(["--config", str(CONFIGS_DIR / "sensor_fusion_baseline.toml"), "--save"])


def benchmark() -> None:
    benchmark_main(["--config", str(CONFIGS_DIR / "benchmark_grid.toml"), "--save"])


def demo() -> None:
    benchmark_main(["--config", str(CONFIGS_DIR / "demo_scenarios.toml"), "--save"])


def report() -> None:
    report_main(["--results-dir", str(RESULTS_DIR), "--write"])


def dashboard() -> None:
    dashboard_main(["--results-dir", str(RESULTS_DIR), "--write"])
