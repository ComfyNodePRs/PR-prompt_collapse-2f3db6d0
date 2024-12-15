from typing import Any, List

from prompt_collapse.state import State

from .requirement import Requirement


class OneOfRequirement(Requirement):
    def __init__(
        self,
        variable: str,
        values: List[Any],
    ) -> None:
        self._variable = variable
        self._values = set(values)

    def apply(self, global_state: State) -> bool:
        variable = global_state.get(self._variable)

        return variable in self._values

    @classmethod
    def from_spec(cls, spec: Any) -> "OneOfRequirement":
        assert isinstance(spec, dict), "OneOfRequirement spec must be a dict"

        variable = spec.get("variable")

        values = spec.get("values")

        return cls(variable, values)
