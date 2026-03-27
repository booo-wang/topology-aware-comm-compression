from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "src"))

from tacc.reporting.markdown import main


if __name__ == "__main__":
    results_dir = repo_root / "results"
    main(["--results-dir", str(results_dir), "--write"])
