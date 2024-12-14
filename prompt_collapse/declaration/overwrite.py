from typing import Any

from prompt_collapse.common.utils import find_parameters
from prompt_collapse.state import State

from .declaration import Declaration


class OverwriteDeclaration(Declaration):
    def __init__(
        self,
        name: str,
        value: Any,
    ) -> None:
        self._name = name
        self._value = value

        self._parameters = find_parameters(str(value))

    def name(self) -> str:
        return self._name

    def apply(self, local_state: State, global_state: State) -> Any:
        global_state.update(self._name, self._value)

        return self._value

    @classmethod
    def from_spec(cls, spec: Any) -> "OverwriteDeclaration":
        assert isinstance(spec, dict), f"Invalid spec for OverwriteDeclaration: {spec}"

        return cls(spec["variable"], spec["value"])
