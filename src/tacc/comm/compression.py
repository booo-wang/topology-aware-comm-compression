from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from random import Random
from typing import Iterable


@dataclass(slots=True)
class Message:
    object_ids: tuple[int, ...]

    @property
    def cost(self) -> int:
        return len(self.object_ids)


@dataclass(slots=True)
class MessageContext:
    hop_index: int
    total_hops: int
    sender_degree: int
    receiver_degree: int
    rng: Random


class BaseCompressor:
    name = "base"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
        context: MessageContext,
    ) -> Message:
        raise NotImplementedError


class FullStateCompressor(BaseCompressor):
    name = "full_state"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
        context: MessageContext,
    ) -> Message:
        del known_object_ids
        del context
        unique_ids = sorted(set(seen_object_ids))
        if budget > 0:
            unique_ids = unique_ids[:budget]
        return Message(object_ids=tuple(unique_ids))


class NoveltyTopKCompressor(BaseCompressor):
    name = "novelty_topk"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
        context: MessageContext,
    ) -> Message:
        del context
        novelty = sorted(set(seen_object_ids) - known_object_ids)
        if budget > 0:
            novelty = novelty[:budget]
        return Message(object_ids=tuple(novelty))


class NoveltyThenFillCompressor(BaseCompressor):
    name = "novelty_then_fill"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
        context: MessageContext,
    ) -> Message:
        del context
        seen = sorted(set(seen_object_ids))
        novelty = [item for item in seen if item not in known_object_ids]
        if budget <= 0:
            return Message(object_ids=tuple(novelty))
        if len(novelty) >= budget:
            return Message(object_ids=tuple(novelty[:budget]))
        fill = [item for item in seen if item in known_object_ids]
        merged = novelty + fill[: max(0, budget - len(novelty))]
        return Message(object_ids=tuple(merged))


class DegreeAwareNoveltyCompressor(BaseCompressor):
    name = "degree_aware_novelty"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
        context: MessageContext,
    ) -> Message:
        novelty = sorted(set(seen_object_ids) - known_object_ids)
        if budget <= 0:
            return Message(object_ids=tuple(novelty))

        degree_penalty = max(0, context.sender_degree - 2)
        receiver_bonus = max(0, 2 - context.receiver_degree)
        effective_budget = max(1, min(budget, budget - degree_penalty + receiver_bonus))

        if context.hop_index == context.total_hops - 1:
            effective_budget = min(budget, effective_budget + 1)

        return Message(object_ids=tuple(novelty[:effective_budget]))


class RandomKCompressor(BaseCompressor):
    name = "random_k"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
        context: MessageContext,
    ) -> Message:
        del known_object_ids
        pool = sorted(set(seen_object_ids))
        if budget <= 0 or len(pool) <= budget:
            return Message(object_ids=tuple(pool))
        picks = context.rng.sample(pool, k=budget)
        return Message(object_ids=tuple(sorted(picks)))


def build_compressor(name: str) -> BaseCompressor:
    registry = {
        FullStateCompressor.name: FullStateCompressor,
        NoveltyTopKCompressor.name: NoveltyTopKCompressor,
        NoveltyThenFillCompressor.name: NoveltyThenFillCompressor,
        DegreeAwareNoveltyCompressor.name: DegreeAwareNoveltyCompressor,
        RandomKCompressor.name: RandomKCompressor,
    }
    try:
        return registry[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown compressor: {name}") from exc
