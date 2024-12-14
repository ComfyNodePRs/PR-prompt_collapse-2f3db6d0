from typing import Any, List

from prompt_collapse.state import State

from .registry import TRANSFORMATION_REGISTRY
from .transformation import Transformation


class SequenceTransformation(Transformation):
    def __init__(self, transformations: List[Transformation]) -> None:
        assert len(transformations) > 0, "Expected at least one transformation"

        self._transformations = transformations

    @classmethod
    def from_spec(cls, spec: Any) -> "SequenceTransformation":
        if not isinstance(spec, list):
            raise ValueError(f"Expected a list of transformations, but got {spec}")

        return cls(
            [
                cls._parse_transformation(transformation_spec)
                for transformation_spec in spec
            ]
        )

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Applying each transformation in the sequence to the provided value, with the output of the previous
        transformation being the input of the next one.

        :param value: The initial value of the sequence
        :param local_state: The local state
        :param global_state: The global state
        :return: The final value after applying all transformations
        """
        for transformation in self._transformations:
            value = transformation.apply(value, local_state, global_state)

        return value

    @staticmethod
    def _parse_transformation(transformation_spec: Any) -> Transformation:
        return TRANSFORMATION_REGISTRY.parse(transformation_spec)
