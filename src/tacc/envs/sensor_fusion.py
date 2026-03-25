from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(slots=True)
class SensorFusionEpisode:
    global_object_ids: set[int]
    local_observations: dict[int, set[int]]


class SensorFusionEnv:
    def __init__(self, num_agents: int, num_objects: int, visibility_prob: float, seed: int) -> None:
        self.num_agents = num_agents
        self.num_objects = num_objects
        self.visibility_prob = visibility_prob
        self.random = Random(seed)

    def sample_episode(self) -> SensorFusionEpisode:
        global_object_ids = set(range(self.num_objects))
        local_observations: dict[int, set[int]] = {idx: set() for idx in range(self.num_agents)}

        for object_id in global_object_ids:
            observed = False
            for agent_id in range(self.num_agents):
                if self.random.random() < self.visibility_prob:
                    local_observations[agent_id].add(object_id)
                    observed = True

            if not observed:
                local_observations[self.random.randrange(self.num_agents)].add(object_id)

        return SensorFusionEpisode(
            global_object_ids=global_object_ids,
            local_observations=local_observations,
        )
