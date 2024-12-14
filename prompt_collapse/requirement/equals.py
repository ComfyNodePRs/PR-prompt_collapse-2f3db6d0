from typing import Any

from prompt_collapse.state import State

from .requirement import Requirement


class EqualsRequirement(Requirement):
    def __init__(
        self,
        variable: str,
        value: Any,
    ) -> None:
        self._variable = variable
        self._value = value

    def apply(self, global_state: State) -> bool:
        value = global_state.get(self._variable)

        return value == self._value

    @classmethod
    def from_spec(cls, spec: Any) -> "EqualsRequirement":
        assert isinstance(spec, dict), "EqualsRequirement spec must be a dict"

        variable = spec.get("variable")
        value = spec.get("value")

        assert isinstance(
            variable, str
        ), "EqualsRequirement spec must have a string variable name"

        return cls(variable, value)
