from pathlib import Path

from tacc.comm import build_topology
from tacc.config import load_config
from tacc.training.runner import run_experiment


def test_ring_topology_has_two_neighbors() -> None:
    topology = build_topology("ring", 5)
    assert len(topology[0]) == 2
    assert len(topology[3]) == 2


def test_smoke_experiment_runs() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_config(repo_root / "configs" / "sensor_fusion_baseline.toml")
    result = run_experiment(config)
    assert 0.0 <= result["summary"]["avg_mean_recall"] <= 1.0
    assert result["summary"]["avg_total_messages"] > 0
