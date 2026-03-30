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


def _rank(summary: dict[str, dict[str, float]], metric: str) -> list[tuple[str, dict[str, float]]]:
    return sorted(summary.items(), key=lambda item: item[1][metric], reverse=True)


def build_findings(result: dict[str, object]) -> list[str]:
    experiments = result.get("experiments", [])
    if not experiments:
        return []

    findings: list[str] = []
    topology_summary = _average_by(experiments, "topology")
    recall_rank = _rank(topology_summary, "avg_recall")
    efficiency_rank = _rank(topology_summary, "avg_efficiency")

    best_recall_name, best_recall_stats = recall_rank[0]
    if len(recall_rank) > 1:
        second_recall_name, second_recall_stats = recall_rank[1]
        recall_gap = best_recall_stats["avg_recall"] - second_recall_stats["avg_recall"]
        findings.append(
            f"A first pass over the sweep suggests that `{best_recall_name}` is the strongest topology for raw recovery. "
            f"Its average recall is {best_recall_stats['avg_recall']:.3f}, about {recall_gap:.3f} higher than `{second_recall_name}`."
        )
    else:
        findings.append(
            f"In the current sweep, `{best_recall_name}` gives the strongest raw recovery with average recall {best_recall_stats['avg_recall']:.3f}."
        )

    best_eff_name, best_eff_stats = efficiency_rank[0]
    if best_eff_name == best_recall_name:
        findings.append(
            f"Interestingly, the same topology also looks strongest on recall-efficiency tradeoff, with average efficiency {best_eff_stats['avg_efficiency']:.5f}."
        )
    else:
        findings.append(
            f"The tradeoff picture is different from the raw-recall ranking: `{best_eff_name}` looks best on efficiency ({best_eff_stats['avg_efficiency']:.5f}), "
            f"even though `{best_recall_name}` still leads on absolute recall."
        )

    full_state = [item for item in experiments if item["communication"]["compressor"] == "full_state"]
    novelty = [item for item in experiments if "novelty" in item["communication"]["compressor"]]
    if full_state and novelty:
        full_recall = sum(item["summary"]["avg_mean_recall"] for item in full_state) / len(full_state)
        full_eff = sum(item["summary"]["avg_efficiency"] for item in full_state) / len(full_state)
        nov_recall = sum(item["summary"]["avg_mean_recall"] for item in novelty) / len(novelty)
        nov_eff = sum(item["summary"]["avg_efficiency"] for item in novelty) / len(novelty)
        findings.append(
            "One pattern that looks fairly consistent in this synthetic setting is that novelty-oriented compression behaves better than naive retransmission. "
            f"Averaged over the current runs, novelty-based variants reach {nov_recall:.3f} recall / {nov_eff:.5f} efficiency, compared with {full_recall:.3f} / {full_eff:.5f} for `full_state`."
        )

    top_result = result.get("top_result")
    if top_result:
        hops = top_result["summary"].get("avg_hop_mean_recalls", [])
        if hops:
            if len(hops) >= 2:
                findings.append(
                    f"Looking at hop-wise behavior, the best configuration already reaches {hops[1]:.3f} recall by hop 2 and then saturates near {hops[-1]:.3f}. "
                    "That makes the hop trajectory itself worth tracking, not just the final score."
                )
            else:
                findings.append(
                    "The best configuration improves quickly across hops: "
                    + " -> ".join(f"{hop:.3f}" for hop in hops)
                    + "."
                )

    return findings
