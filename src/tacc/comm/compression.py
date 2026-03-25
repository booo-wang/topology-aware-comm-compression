from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class Message:
    object_ids: tuple[int, ...]

    @property
    def cost(self) -> int:
        return len(self.object_ids)


class BaseCompressor:
    name = "base"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
    ) -> Message:
        raise NotImplementedError


class FullStateCompressor(BaseCompressor):
    name = "full_state"

    def compress(
        self,
        known_object_ids: set[int],
        seen_object_ids: Iterable[int],
        budget: int,
    ) -> Message:
        del known_object_ids
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
    ) -> Message:
        novelty = sorted(set(seen_object_ids) - known_object_ids)
        if budget > 0:
            novelty = novelty[:budget]
        return Message(object_ids=tuple(novelty))


def build_compressor(name: str) -> BaseCompressor:
    registry = {
        FullStateCompressor.name: FullStateCompressor,
        NoveltyTopKCompressor.name: NoveltyTopKCompressor,
    }
    try:
        return registry[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown compressor: {name}") from exc
