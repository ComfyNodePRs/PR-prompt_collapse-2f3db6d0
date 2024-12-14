from typing import Any

from prompt_collapse.state import State

from .requirement import Requirement


class GreaterThanRequirement(Requirement):
    def __init__(
        self,
        variable: str,
        value: int,
    ) -> None:
        self._variable = variable
        self._value = value

    def apply(self, global_state: State) -> bool:
        if not global_state.exists(self._variable):
            return False

        value = global_state.get(self._variable)

        return value > self._value

    @classmethod
    def from_spec(cls, spec: Any) -> "GreaterThanRequirement":
        assert isinstance(spec, dict), "GreaterThanRequirement spec must be a dict"

        variable = spec.get("variable")
        value = spec.get("value")

        assert isinstance(variable, str) and isinstance(
            value, int
        ), "GreaterThanRequirement spec must have a string variable and an integer value"

        return cls(variable, value)
