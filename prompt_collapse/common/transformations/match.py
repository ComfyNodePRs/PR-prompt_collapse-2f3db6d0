from typing import Any, Optional, Tuple

from prompt_collapse.state import State

from .transformation import Transformation


class MatchTransformation(Transformation):
    def __init__(
        self,
        match_cases: dict[Optional[Any], Any],
        default: Optional[Any],
    ) -> None:
        assert len(match_cases) > 0, "Expected at least one match case"

        self._match_cases = match_cases
        self._default = default

    @classmethod
    def from_spec(cls, spec: Any) -> "MatchTransformation":
        if not isinstance(spec, dict):
            raise ValueError(f"Expected a list of transformations, but got {spec}")

        return cls(
            dict(
                cls._parse_transformation(transformation_spec)
                for transformation_spec in spec.get("cases", [])
            ),
            spec.get("default"),
        )

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Matching the provided value to one of the cases and returning the corresponding value.
        If no match is found, the default value is returned.

        :param value: The value to match
        :param local_state: The local state
        :param global_state: The global state
        :return: The matched value or the default value
        """
        return self._match_cases.get(value, self._default)

    @staticmethod
    def _parse_transformation(transformation_spec: Any) -> Tuple[Optional[Any], Any]:
        if not isinstance(transformation_spec, dict):
            raise ValueError(f"Expected a dictionary, but got {transformation_spec}")

        match_value = transformation_spec.get("match")
        new_value = transformation_spec.get("value")

        if new_value is None:
            raise ValueError(f"Expected a value for the match case {match_value}")

        return match_value, new_value
