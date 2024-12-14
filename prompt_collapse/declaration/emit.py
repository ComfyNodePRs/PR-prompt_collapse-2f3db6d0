from typing import Any, Optional

from prompt_collapse.common.utils import apply_parameters, find_parameters
from prompt_collapse.state import State

from .declaration import Declaration


class EmitDeclaration(Declaration):
    def __init__(
        self,
        name: str,
        value: Any,
        cast_to: Optional[str] = None,
    ) -> None:
        self._name = name
        self._value = value
        self._cast_to = cast_to

        self._parameters = find_parameters(str(value))

    def name(self) -> str:
        return self._name

    def apply(self, local_state: State, global_state: State) -> Any:
        value = apply_parameters(self._value, self._parameters, local_state)

        if self._cast_to is not None:
            value = self._cast(value)

        global_state.set(self._name, value)

        return value

    def _cast(self, value: Any) -> Any:
        if self._cast_to == "int":
            return int(value)
        elif self._cast_to == "float":
            return float(value)
        elif self._cast_to == "str":
            return str(value)
        else:
            raise ValueError(f"Invalid cast_to value: {self._cast_to}")

    @classmethod
    def from_spec(cls, spec: Any) -> "EmitDeclaration":
        assert isinstance(spec, dict), f"Invalid spec for EmitDeclaration: {spec}"

        return cls(spec["variable"], spec.get("value", True), spec.get("cast_to"))
