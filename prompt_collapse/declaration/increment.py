from typing import Any

from prompt_collapse.state import State

from .declaration import Declaration


class IncrementDeclaration(Declaration):
    def __init__(self, name: str) -> None:
        self._name = name

    def name(self) -> str:
        return self._name

    def apply(self, local_state: State, global_state: State) -> Any:
        value = global_state.get(self._name)

        global_state.update(self._name, value + 1)

        return value + 1

    @classmethod
    def from_spec(cls, spec: Any) -> "IncrementDeclaration":
        assert isinstance(spec, dict), f"Invalid spec for IncrementDeclaration: {spec}"

        return cls(spec["variable"])
