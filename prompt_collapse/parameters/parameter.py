from typing import Any

from prompt_collapse.common.transformations import (
    TRANSFORMATION_REGISTRY,
    Transformation,
)
from prompt_collapse.state import State


class Parameter:
    def __init__(self, name: str, transformation: Transformation) -> None:
        self._name = name
        self._transformation = transformation

    def name(self) -> str:
        return self._name

    def apply(self, local_state: State, global_state: State) -> Any:
        value = self._transformation.apply(None, local_state, global_state)
        local_state.set(self._name, value)

        return value

    @classmethod
    def from_spec(cls, spec: Any) -> "Parameter":
        if not isinstance(spec, dict):
            raise ValueError(f"Expected a dictionary, but got {spec}")

        name = spec["name"]
        transformation_spec = spec["transform"]

        transformation = TRANSFORMATION_REGISTRY.get(
            transformation_spec.get("name")
        ).from_spec(transformation_spec)

        return cls(name, transformation)

    def __repr__(self) -> str:
        return f"Parameter(name={self._name}, transformation={self._transformation})"

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))
