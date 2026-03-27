from pathlib import Path

from tacc.comm import build_topology
from tacc.config import expand_sweep, load_config
from tacc.reporting.dashboard import build_dashboard_html
from tacc.reporting.markdown import build_markdown_report
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
    assert len(result["summary"]["avg_hop_mean_recalls"]) == config.hops


def test_benchmark_sweep_expands() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_config(repo_root / "configs" / "benchmark_grid.toml")
    expanded = expand_sweep(config)
    assert len(expanded) == 4 * 4 * 3 * 3 * 2


def test_markdown_report_contains_table() -> None:
    demo_result = {
        "benchmark": "demo",
        "num_experiments": 1,
        "top_result": {
            "name": "demo_scenario",
            "communication": {"topology": "star", "compressor": "novelty_topk", "message_budget": 3, "message_dropout_prob": 0.0},
            "environment": {"visibility_prob": 0.35},
            "summary": {"avg_mean_recall": 0.95, "avg_efficiency": 0.02, "avg_hop_mean_recalls": [0.5, 0.8, 0.95]},
        },
        "experiments": [
            {
                "name": "demo_scenario",
                "communication": {"topology": "star", "compressor": "novelty_topk", "message_budget": 3, "message_dropout_prob": 0.0},
                "environment": {"visibility_prob": 0.35},
                "summary": {"avg_mean_recall": 0.95, "avg_efficiency": 0.02, "avg_hop_mean_recalls": [0.5, 0.8, 0.95]},
            }
        ],
    }
    report = build_markdown_report(demo_result, Path('demo.json'))
    assert "# Demo Report" in report
    assert "| Scenario | Topology | Compressor | Budget | Recall | Efficiency |" in report


def test_dashboard_contains_heading() -> None:
    demo_result = {
        "benchmark": "demo",
        "num_experiments": 1,
        "top_result": {
            "name": "demo_scenario",
            "communication": {"topology": "ring", "compressor": "novelty_topk", "message_budget": 3, "message_dropout_prob": 0.0},
            "environment": {"visibility_prob": 0.35},
            "summary": {"avg_mean_recall": 0.95, "avg_efficiency": 0.02, "avg_hop_mean_recalls": [0.5, 0.8, 0.95]},
        },
        "experiments": [
            {
                "name": "demo_scenario",
                "communication": {"topology": "ring", "compressor": "novelty_topk", "message_budget": 3, "message_dropout_prob": 0.0},
                "environment": {"visibility_prob": 0.35},
                "summary": {"avg_mean_recall": 0.95, "avg_efficiency": 0.02, "avg_hop_mean_recalls": [0.5, 0.8, 0.95]},
            }
        ],
    }
    dashboard = build_dashboard_html(demo_result, Path('demo.json'))
    assert "Communication Strategy Explorer" in dashboard
    assert "<table>" in dashboard
