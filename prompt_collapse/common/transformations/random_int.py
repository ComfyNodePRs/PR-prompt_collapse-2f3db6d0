import random
from typing import Any

from prompt_collapse.state import State

from .transformation import Transformation


class RandomIntTransformation(Transformation):
    def __init__(self, min_value: int, max_value: int) -> None:
        self._min_value = min_value
        self._max_value = max_value

    @classmethod
    def from_spec(cls, spec: Any) -> "RandomIntTransformation":
        min_value = spec.get("min")
        max_value = spec.get("max")

        return cls(min_value, max_value)

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Returning a random integer between the min and max values.
        :param value: Ignored value
        :param local_state: Local state
        :param global_state: Global state
        :return: Random integer between min and max values
        """
        return random.randint(self._min_value, self._max_value)
