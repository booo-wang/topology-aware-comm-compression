from pathlib import Path

from tacc.reporting.markdown import main


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    results_dir = repo_root / "results"
    main(["--results-dir", str(results_dir), "--write"])
