from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_latest_benchmark_result(results_dir: str | Path) -> tuple[Path, dict[str, object]]:
    results_path = Path(results_dir)
    candidates: list[tuple[Path, dict[str, object]]] = []
    for candidate in sorted(results_path.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True):
        data = json.loads(candidate.read_text(encoding="utf-8"))
        if "benchmark" in data and "experiments" in data:
            candidates.append((candidate, data))

    if not candidates:
        raise FileNotFoundError(f"No benchmark-style result JSON files found in {results_path}")
    return candidates[0]


def _format_hops(hops: list[float]) -> str:
    return " -> ".join(f"{hop:.3f}" for hop in hops)


def build_markdown_report(result: dict[str, object], source_path: Path) -> str:
    top_result = result.get("top_result")
    experiments = result.get("experiments", [])
    top_five = experiments[:5]

    lines = [
        "# Demo Report",
        "",
        f"- Source: `{source_path.name}`",
        f"- Benchmark: `{result['benchmark']}`",
        f"- Number of scenarios: `{result['num_experiments']}`",
        "",
    ]

    if top_result:
        summary = top_result["summary"]
        comm = top_result["communication"]
        env = top_result["environment"]
        lines.extend(
            [
                "## Best Configuration",
                "",
                f"- Scenario: `{top_result['name']}`",
                f"- Topology: `{comm['topology']}`",
                f"- Compressor: `{comm['compressor']}`",
                f"- Budget: `{comm['message_budget']}`",
                f"- Dropout: `{comm['message_dropout_prob']}`",
                f"- Visibility: `{env['visibility_prob']}`",
                f"- Mean recall: `{summary['avg_mean_recall']}`",
                f"- Efficiency: `{summary['avg_efficiency']}`",
                f"- Hop trajectory: `{_format_hops(summary['avg_hop_mean_recalls'])}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Top 5 Scenarios",
            "",
            "| Scenario | Topology | Compressor | Budget | Recall | Efficiency |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )

    for item in top_five:
        comm = item["communication"]
        summary = item["summary"]
        lines.append(
            "| {name} | {topology} | {compressor} | {budget} | {recall:.4f} | {efficiency:.6f} |".format(
                name=item["name"],
                topology=comm["topology"],
                compressor=comm["compressor"],
                budget=comm["message_budget"],
                recall=summary["avg_mean_recall"],
                efficiency=summary["avg_efficiency"],
            )
        )

    lines.extend(
        [
            "",
            "## Portfolio Notes",
            "",
            "- This project demonstrates practical multi-agent systems engineering rather than a paper-first benchmark.",
            "- The main value is configurable simulation, reusable experiment workflows, and exportable reports for communication strategy comparisons.",
            "- A useful next step would be an interactive visualization or small web dashboard on top of these saved results.",
            "",
        ]
    )

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export the latest benchmark result as a Markdown report.")
    parser.add_argument("--results-dir", required=True, help="Directory containing saved result JSON files.")
    parser.add_argument("--write", action="store_true", help="Write the generated report to REPORT.md in the results directory.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    source_path, result = load_latest_benchmark_result(args.results_dir)
    report = build_markdown_report(result, source_path)
    if args.write:
        output_path = Path(args.results_dir) / "REPORT.md"
        output_path.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
