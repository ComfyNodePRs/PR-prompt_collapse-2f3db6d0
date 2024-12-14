from typing import Any, List

from prompt_collapse.state import State

from .registry import REQUIREMENT_REGISTRY
from .requirement import Requirement


class SomeOfRequirement(Requirement):
    def __init__(
        self,
        conditions: List[Requirement],
    ) -> None:
        self._conditions = conditions

    def apply(self, global_state: State) -> bool:
        return any(
            condition.apply(global_state) for condition in self._conditions
        )

    @classmethod
    def from_spec(cls, spec: Any) -> "SomeOfRequirement":
        assert isinstance(spec, dict), "SomeOfRequirement spec must be a dict"

        conditions = spec.get("conditions")

        return cls(
            [
                REQUIREMENT_REGISTRY.parse(condition_spec)
                for condition_spec in conditions
            ]
        )
