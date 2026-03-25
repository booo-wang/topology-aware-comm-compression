from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

from tacc.comm import build_compressor, build_topology
from tacc.config import ExperimentConfig, load_config
from tacc.envs import SensorFusionEnv


@dataclass(slots=True)
class EpisodeMetrics:
    mean_recall: float
    total_cost: int
    total_messages: int


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

    agent_memory = {
        agent_id: set(local_ids)
        for agent_id, local_ids in episode.local_observations.items()
    }

    total_cost = 0
    total_messages = 0
    for _ in range(config.hops):
        inbound: dict[int, list[tuple[int, ...]]] = {agent_id: [] for agent_id in agent_memory}
        for sender, neighbors in adjacency.items():
            sender_memory = agent_memory[sender]
            for receiver in neighbors:
                message = compressor.compress(
                    known_object_ids=agent_memory[receiver],
                    seen_object_ids=sender_memory,
                    budget=config.communication.message_budget,
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
    return EpisodeMetrics(
        mean_recall=sum(recalls) / len(recalls),
        total_cost=total_cost,
        total_messages=total_messages,
    )


def run_experiment(config: ExperimentConfig) -> dict[str, object]:
    per_episode = [
        run_episode(config, config.seed + offset)
        for offset in range(config.episodes)
    ]
    avg_recall = sum(item.mean_recall for item in per_episode) / len(per_episode)
    avg_cost = sum(item.total_cost for item in per_episode) / len(per_episode)
    avg_messages = sum(item.total_messages for item in per_episode) / len(per_episode)
    return {
        "config": asdict(config),
        "summary": {
            "avg_mean_recall": round(avg_recall, 4),
            "avg_total_cost": round(avg_cost, 2),
            "avg_total_messages": round(avg_messages, 2),
        },
        "episodes": [asdict(item) for item in per_episode],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a topology-aware communication compression experiment.")
    parser.add_argument("--config", required=True, help="Path to a TOML config file.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    result = run_experiment(config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
