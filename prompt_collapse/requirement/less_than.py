from typing import Any

from prompt_collapse.state import State

from .requirement import Requirement


class LessThanRequirement(Requirement):
    def __init__(
        self,
        variable: str,
        value: int,
    ) -> None:
        self._variable = variable
        self._value = value

    def apply(self, global_state: State) -> bool:
        value = global_state.get(self._variable)

        return value < self._value

    @classmethod
    def from_spec(cls, spec: Any) -> "LessThanRequirement":
        assert isinstance(spec, dict), "LessThanRequirement spec must be a dict"

        variable = spec.get("variable")
        value = spec.get("value")

        assert isinstance(variable, str) and isinstance(
            value, int
        ), "LessThanRequirement spec must have a string variable and an integer value"

        return cls(variable, value)
