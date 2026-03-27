from pathlib import Path

from tacc.training.benchmark import main


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "configs" / "benchmark_grid.toml"
    main(["--config", str(config_path), "--save"])
