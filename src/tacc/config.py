from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(slots=True)
class EnvironmentConfig:
    name: str
    num_agents: int
    num_objects: int
    visibility_prob: float


@dataclass(slots=True)
class CommunicationConfig:
    topology: str
    compressor: str
    message_budget: int


@dataclass(slots=True)
class ExperimentConfig:
    seed: int
    episodes: int
    hops: int
    environment: EnvironmentConfig
    communication: CommunicationConfig


def load_config(path: str | Path) -> ExperimentConfig:
    config_path = Path(path)
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    env = EnvironmentConfig(**raw["environment"])
    comm = CommunicationConfig(**raw["communication"])
    return ExperimentConfig(
        seed=raw["seed"],
        episodes=raw["episodes"],
        hops=raw["hops"],
        environment=env,
        communication=comm,
    )
