from typing import Any

from prompt_collapse.state import State

from .transformation import Transformation


class LookupTransformation(Transformation):
    def __init__(self, variable: str) -> None:
        self._variable = variable

    @classmethod
    def from_spec(cls, spec: Any) -> "LookupTransformation":
        if not isinstance(spec, dict):
            raise ValueError(f"Expected a dictionary, but got {spec}")

        variable = spec.get("variable")

        if not isinstance(variable, str):
            raise ValueError(f"Expected a string variable, but got {variable}")

        return cls(variable)

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Replacing the current value with the value of the specified variable in one of the provided states.
        The lookup order is local state -> global state, similar to the variable lookup order in Python.

        :param value: The value to replace
        :param local_state: The local state
        :param global_state: The global state
        :return: The value of the specified variable
        """

        if local_state.exists(self._variable):
            return local_state.get(self._variable)

        if global_state.exists(self._variable):
            return global_state.get(self._variable)

        raise ValueError(
            f"Variable {self._variable} not found in local or global state"
        )
