from typing import Any, List

from prompt_collapse.common.utils import apply_parameters, find_parameters
from prompt_collapse.state import State

from .content import Content


class ConstContent(Content):
    def __init__(self, value: str) -> None:
        self._value = value
        self._parameters = find_parameters(value)

    def apply(self, local_state: State) -> List[str]:
        return [apply_parameters(self._value, self._parameters, local_state)]

    @classmethod
    def from_spec(cls, spec: Any) -> "ConstContent":
        if isinstance(spec, (str, int, float)):
            return cls(str(spec))

        raise ValueError(f"Invalid spec for ConstContent: {spec}")
