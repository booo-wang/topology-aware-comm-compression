from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from random import Random

from tacc.comm import build_compressor, build_topology
from tacc.comm.compression import MessageContext
from tacc.config import ExperimentConfig, load_config, resolve_output_dir
from tacc.envs import SensorFusionEnv


@dataclass(slots=True)
class EpisodeMetrics:
    mean_recall: float
    min_recall: float
    max_recall: float
    total_cost: int
    total_messages: int
    efficiency: float
    hop_mean_recalls: list[float]


def run_episode(config: ExperimentConfig, episode_seed: int) -> EpisodeMetrics:
    env = SensorFusionEnv(
        num_agents=config.environment.num_agents,
        num_objects=config.environment.num_objects,
        visibility_prob=config.environment.visibility_prob,
        seed=episode_seed,
    )
    episode = env.sample_episode()
    adjacency = build_topology(config.communication.topology, config.environment.num_agents)
    compressor = build_compressor(config.communication.compressor)
    rng = Random(episode_seed)

    agent_memory = {
        agent_id: set(local_ids)
        for agent_id, local_ids in episode.local_observations.items()
    }

    total_cost = 0
    total_messages = 0
    hop_mean_recalls: list[float] = []
    for hop_index in range(config.hops):
        inbound: dict[int, list[tuple[int, ...]]] = {agent_id: [] for agent_id in agent_memory}
        for sender, neighbors in adjacency.items():
            sender_memory = agent_memory[sender]
            sender_degree = len(neighbors)
            for receiver in neighbors:
                if rng.random() < config.communication.message_dropout_prob:
                    continue
                message = compressor.compress(
                    known_object_ids=agent_memory[receiver],
                    seen_object_ids=sender_memory,
                    budget=config.communication.message_budget,
                    context=MessageContext(
                        hop_index=hop_index,
                        total_hops=config.hops,
                        sender_degree=sender_degree,
                        receiver_degree=len(adjacency[receiver]),
                        rng=rng,
                    ),
                )
                inbound[receiver].append(message.object_ids)
                total_cost += message.cost
                total_messages += 1

        for receiver, received_messages in inbound.items():
            for object_ids in received_messages:
                agent_memory[receiver].update(object_ids)

        recalls = [
            len(memory & episode.global_object_ids) / len(episode.global_object_ids)
            for memory in agent_memory.values()
        ]
        hop_mean_recalls.append(sum(recalls) / len(recalls))

    final_recalls = [
        len(memory & episode.global_object_ids) / len(episode.global_object_ids)
        for memory in agent_memory.values()
    ]
    mean_recall = sum(final_recalls) / len(final_recalls)
    efficiency = mean_recall / total_cost if total_cost else 0.0
    return EpisodeMetrics(
        mean_recall=mean_recall,
        min_recall=min(final_recalls),
        max_recall=max(final_recalls),
        total_cost=total_cost,
        total_messages=total_messages,
        efficiency=efficiency,
        hop_mean_recalls=hop_mean_recalls,
    )


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def run_experiment(config: ExperimentConfig) -> dict[str, object]:
    per_episode = [
        run_episode(config, config.seed + offset)
        for offset in range(config.episodes)
    ]
    hop_count = len(per_episode[0].hop_mean_recalls) if per_episode else 0
    avg_hop_recalls = [
        round(_average([episode.hop_mean_recalls[idx] for episode in per_episode]), 4)
        for idx in range(hop_count)
    ]
    return {
        "config": asdict(config),
        "summary": {
            "avg_mean_recall": round(_average([item.mean_recall for item in per_episode]), 4),
            "avg_min_recall": round(_average([item.min_recall for item in per_episode]), 4),
            "avg_max_recall": round(_average([item.max_recall for item in per_episode]), 4),
            "avg_total_cost": round(_average([item.total_cost for item in per_episode]), 2),
            "avg_total_messages": round(_average([item.total_messages for item in per_episode]), 2),
            "avg_efficiency": round(_average([item.efficiency for item in per_episode]), 6),
            "avg_hop_mean_recalls": avg_hop_recalls,
        },
        "episodes": [asdict(item) for item in per_episode],
    }


def save_result(result: dict[str, object], output_dir: Path | str, experiment_name: str) -> Path:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f'{experiment_name}_{timestamp}.json'
    target_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a topology-aware communication compression experiment.")
    parser.add_argument("--config", required=True, help="Path to a TOML config file.")
    parser.add_argument("--save", action="store_true", help="Persist the result JSON into the configured output directory.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    result = run_experiment(config)
    if args.save:
        output_dir = resolve_output_dir(args.config, config.output_dir)
        output_path = save_result(result, output_dir, config.name)
        result["saved_to"] = str(output_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
