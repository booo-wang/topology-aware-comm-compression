from __future__ import annotations


def _average_by(experiments: list[dict[str, object]], key: str) -> dict[str, dict[str, float]]:
    buckets: dict[str, list[dict[str, object]]] = {}
    for item in experiments:
        buckets.setdefault(item["communication"][key], []).append(item)

    summary: dict[str, dict[str, float]] = {}
    for bucket, items in buckets.items():
        avg_recall = sum(entry["summary"]["avg_mean_recall"] for entry in items) / len(items)
        avg_efficiency = sum(entry["summary"]["avg_efficiency"] for entry in items) / len(items)
        summary[bucket] = {
            "avg_recall": avg_recall,
            "avg_efficiency": avg_efficiency,
            "count": float(len(items)),
        }
    return summary


def build_findings(result: dict[str, object]) -> list[str]:
    experiments = result.get("experiments", [])
    if not experiments:
        return []

    findings: list[str] = []
    topology_summary = _average_by(experiments, "topology")
    best_topology = max(topology_summary.items(), key=lambda item: item[1]["avg_recall"])
    findings.append(
        f"Across the current sweep, `{best_topology[0]}` achieves the highest average recall ({best_topology[1]['avg_recall']:.3f})."
    )

    efficient_topology = max(topology_summary.items(), key=lambda item: item[1]["avg_efficiency"])
    findings.append(
        f"For recall-efficiency tradeoffs, `{efficient_topology[0]}` currently looks strongest with average efficiency {efficient_topology[1]['avg_efficiency']:.5f}."
    )

    full_state = [item for item in experiments if item["communication"]["compressor"] == "full_state"]
    novelty = [item for item in experiments if "novelty" in item["communication"]["compressor"]]
    if full_state and novelty:
        full_recall = sum(item["summary"]["avg_mean_recall"] for item in full_state) / len(full_state)
        full_eff = sum(item["summary"]["avg_efficiency"] for item in full_state) / len(full_state)
        nov_recall = sum(item["summary"]["avg_mean_recall"] for item in novelty) / len(novelty)
        nov_eff = sum(item["summary"]["avg_efficiency"] for item in novelty) / len(novelty)
        findings.append(
            "Novelty-oriented compressors outperform `full_state` on average "
            f"({nov_recall:.3f} recall / {nov_eff:.5f} efficiency vs {full_recall:.3f} / {full_eff:.5f})."
        )

    top_result = result.get("top_result")
    if top_result:
        hops = top_result["summary"].get("avg_hop_mean_recalls", [])
        if hops:
            findings.append(
                "The best configuration recovers information quickly across hops: "
                + " -> ".join(f"{hop:.3f}" for hop in hops)
                + "."
            )

    return findings
