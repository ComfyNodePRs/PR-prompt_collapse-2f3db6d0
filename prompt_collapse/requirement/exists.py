from typing import Any

from prompt_collapse.state import State

from .requirement import Requirement


class ExistsRequirement(Requirement):
    def __init__(
        self,
        variable: str,
    ) -> None:
        self._variable = variable

    def apply(self, global_state: State) -> bool:
        return global_state.exists(self._variable)

    @classmethod
    def from_spec(cls, spec: Any) -> "ExistsRequirement":
        assert isinstance(spec, dict), "GreaterThanRequirement spec must be a dict"

        variable = spec.get("variable")

        assert isinstance(
            variable, str
        ), "ExistsRequirement spec must have a string variable name"

        return cls(variable)
