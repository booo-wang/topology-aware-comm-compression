from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from tacc.config import expand_sweep, load_config, resolve_output_dir
from tacc.training.runner import run_experiment


def run_benchmark(config_path: str | Path) -> dict[str, object]:
    base_config = load_config(config_path)
    experiments = []
    for experiment_config in expand_sweep(base_config):
        result = run_experiment(experiment_config)
        experiments.append(
            {
                "name": experiment_config.name,
                "communication": result["config"]["communication"],
                "environment": result["config"]["environment"],
                "summary": result["summary"],
            }
        )

    ranked = sorted(
        experiments,
        key=lambda item: (
            item["summary"]["avg_mean_recall"],
            item["summary"]["avg_efficiency"],
        ),
        reverse=True,
    )
    return {
        "benchmark": base_config.name,
        "num_experiments": len(experiments),
        "top_result": ranked[0] if ranked else None,
        "experiments": ranked,
    }


def save_benchmark(result: dict[str, object], output_dir: Path | str, benchmark_name: str) -> Path:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f'{benchmark_name}_{timestamp}.json'
    target_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
    return target_path


def build_cli_summary(result: dict[str, object], saved_to: str | None = None) -> dict[str, object]:
    experiments = result["experiments"]
    return {
        "benchmark": result["benchmark"],
        "num_experiments": result["num_experiments"],
        "saved_to": saved_to,
        "top_result": result["top_result"],
        "top_5": experiments[:5],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a benchmark sweep for topology-aware communication compression.")
    parser.add_argument("--config", required=True, help="Path to a TOML config file with a [sweep] section.")
    parser.add_argument("--save", action="store_true", help="Persist the benchmark result JSON.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    result = run_benchmark(args.config)
    saved_to = None
    if args.save:
        output_dir = resolve_output_dir(args.config, config.output_dir)
        output_path = save_benchmark(result, output_dir, config.name)
        saved_to = str(output_path)
    print(json.dumps(build_cli_summary(result, saved_to=saved_to), indent=2))


if __name__ == "__main__":
    main()
