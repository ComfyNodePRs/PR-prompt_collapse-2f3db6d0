from typing import Any

from prompt_collapse.state import State

from .transformation import Transformation


class ConstantTransformation(Transformation):
    def __init__(self, value: Any):
        self._value = value

    @classmethod
    def from_spec(cls, spec: Any) -> "ConstantTransformation":
        return cls(spec)

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Returning the value stored in the transformation, ignoring the provided value.

        :param value: The value to ignore
        :param local_state: The local state
        :param global_state: The global state
        :return: The value stored in the transformation
        """
        return self._value
