from __future__ import annotations

from dataclasses import dataclass, replace
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
    message_dropout_prob: float = 0.0


@dataclass(slots=True)
class SweepConfig:
    topologies: list[str] | None = None
    compressors: list[str] | None = None
    message_budgets: list[int] | None = None
    visibility_probs: list[float] | None = None
    message_dropout_probs: list[float] | None = None


@dataclass(slots=True)
class ExperimentConfig:
    seed: int
    episodes: int
    hops: int
    environment: EnvironmentConfig
    communication: CommunicationConfig
    name: str = "experiment"
    output_dir: str = "results"
    sweep: SweepConfig | None = None


def load_config(path: str | Path) -> ExperimentConfig:
    config_path = Path(path)
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    env = EnvironmentConfig(**raw["environment"])
    comm = CommunicationConfig(**raw["communication"])
    sweep = SweepConfig(**raw["sweep"]) if "sweep" in raw else None
    return ExperimentConfig(
        seed=raw["seed"],
        episodes=raw["episodes"],
        hops=raw["hops"],
        environment=env,
        communication=comm,
        name=raw.get("name", config_path.stem),
        output_dir=raw.get("output_dir", "results"),
        sweep=sweep,
    )


def expand_sweep(config: ExperimentConfig) -> list[ExperimentConfig]:
    if config.sweep is None:
        return [config]

    sweep = config.sweep
    topologies = sweep.topologies or [config.communication.topology]
    compressors = sweep.compressors or [config.communication.compressor]
    budgets = sweep.message_budgets or [config.communication.message_budget]
    visibility_probs = sweep.visibility_probs or [config.environment.visibility_prob]
    dropout_probs = sweep.message_dropout_probs or [config.communication.message_dropout_prob]

    expanded: list[ExperimentConfig] = []
    for topology in topologies:
        for compressor in compressors:
            for budget in budgets:
                for visibility_prob in visibility_probs:
                    for dropout in dropout_probs:
                        environment = replace(config.environment, visibility_prob=visibility_prob)
                        communication = replace(
                            config.communication,
                            topology=topology,
                            compressor=compressor,
                            message_budget=budget,
                            message_dropout_prob=dropout,
                        )
                        name = f"{topology}__{compressor}__budget{budget}__vis{visibility_prob:.2f}__drop{dropout:.2f}"
                        expanded.append(
                            replace(
                                config,
                                environment=environment,
                                communication=communication,
                                name=name,
                                sweep=None,
                            )
                        )
    return expanded
