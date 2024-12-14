from typing import Any, List

from prompt_collapse.state import State

from .registry import REQUIREMENT_REGISTRY
from .requirement import Requirement


class NoneOfRequirement(Requirement):
    def __init__(
        self,
        conditions: List[Requirement],
    ) -> None:
        self._conditions = conditions

    def apply(self, global_state: State) -> bool:
        return not any(
            condition.apply(global_state) for condition in self._conditions
        )

    @classmethod
    def from_spec(cls, spec: Any) -> "NoneOfRequirement":
        assert isinstance(spec, dict), "NoneOfRequirement spec must be a dict"

        conditions = spec.get("conditions")

        return cls(
            [
                REQUIREMENT_REGISTRY.parse(condition_spec)
                for condition_spec in conditions
            ]
        )
