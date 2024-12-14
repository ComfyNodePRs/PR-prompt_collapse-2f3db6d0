from typing import Any

from prompt_collapse.state import State

from ..distributions import WeightedDistribution
from .transformation import Transformation


class RandomValueTransformation(Transformation):
    def __init__(self, distribution: WeightedDistribution):
        self._distribution = distribution

    @classmethod
    def from_spec(cls, spec: Any) -> "RandomValueTransformation":
        values = spec.get("values")

        return cls(WeightedDistribution.from_spec(values))

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Returning the value stored in the transformation, ignoring the provided value.

        :param value: The value to ignore
        :param local_state: The local state
        :param global_state: The global state
        :return: The value stored in the transformation
        """
        index = self._distribution.apply(k=1)[0]

        return self._distribution.get_items()[index]
