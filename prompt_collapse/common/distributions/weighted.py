import random
from typing import Any, List

from .distribution import Distribution


class WeightedDistribution(Distribution):
    def __init__(self, weights: List[tuple[float, Any]]) -> None:
        assert len(weights) > 0, "Cannot create an empty WeightedDistribution"

        weight_values, items = zip(*weights)
        indices = list(range(len(weight_values)))

        self._indices = indices
        self._weights = weight_values
        self._indices_to_items = dict(zip(indices, items))

    def apply(self, k: int = 1) -> List[int]:
        item_indices = random.choices(self._indices, weights=self._weights, k=k)

        return list(item_indices)[:k]

    def get_items(self) -> dict[int, Any]:
        return self._indices_to_items.copy()

    def get_item(self, index: int) -> Any:
        return self._indices_to_items[index]

    @classmethod
    def from_spec(cls, spec: Any) -> "WeightedDistribution":
        if not isinstance(spec, list):
            raise ValueError(f"Invalid spec for WeightedDistribution: {spec}")

        weights = [cls._load_weighted_item(item_spec) for item_spec in spec]

        return cls(weights)

    @staticmethod
    def _load_weighted_item(spec: Any) -> tuple[float, Any]:
        if not isinstance(spec, dict):
            raise ValueError(f"Invalid spec for WeightedDistribution: {spec}")

        weight = spec.get("weight", 1.0)
        value = spec.get("value")

        return float(weight), value
