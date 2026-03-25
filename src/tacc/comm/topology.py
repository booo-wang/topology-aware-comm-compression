from __future__ import annotations


def build_topology(name: str, num_agents: int) -> dict[int, list[int]]:
    if num_agents < 2:
        return {0: []}

    if name == "chain":
        adjacency = {idx: [] for idx in range(num_agents)}
        for idx in range(num_agents - 1):
            adjacency[idx].append(idx + 1)
            adjacency[idx + 1].append(idx)
        return adjacency

    if name == "ring":
        adjacency = build_topology("chain", num_agents)
        adjacency[0].append(num_agents - 1)
        adjacency[num_agents - 1].append(0)
        return {idx: sorted(set(neighbors)) for idx, neighbors in adjacency.items()}

    if name == "star":
        return {
            idx: ([agent for agent in range(1, num_agents)] if idx == 0 else [0])
            for idx in range(num_agents)
        }

    if name == "fully_connected":
        return {
            idx: [other for other in range(num_agents) if other != idx]
            for idx in range(num_agents)
        }

    raise ValueError(f"Unknown topology: {name}")
