from typing import Any

from prompt_collapse.state import State

from .transformation import Transformation


class IdentityTransformation(Transformation):
    @classmethod
    def from_spec(cls, spec: Any) -> "IdentityTransformation":
        if spec is not None:
            raise ValueError(
                f"Identity transformation expects no arguments, but {spec} was provided"
            )

        return cls()

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Returning the value as is, without any modifications.

        :param value: The value to return
        :param local_state: The local state
        :param global_state: The global state
        :return: The original value
        """
        return value
