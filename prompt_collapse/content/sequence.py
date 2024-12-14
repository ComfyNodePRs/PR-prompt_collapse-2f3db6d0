import itertools
from typing import Any, List

from prompt_collapse.state import State

from .constant import ConstContent
from .content import Content
from .registry import CONTENT_REGISTRY


class SequenceContent(Content):
    def __init__(
        self,
        content_entries: List[Content],
    ) -> None:
        self._content_entries = content_entries

    def apply(self, local_state: State) -> List[str]:
        return list(
            itertools.chain.from_iterable(
                [entry.apply(local_state) for entry in self._content_entries]
            )
        )

    @classmethod
    def from_spec(cls, spec: Any) -> "SequenceContent":
        assert isinstance(spec, dict), f"Invalid spec for SequenceContent: {spec}"

        values = spec["values"]

        return cls([cls._parse_content(content_spec) for content_spec in values])

    @staticmethod
    def _parse_content(spec: Any) -> Content:
        if isinstance(spec, (str, int, float)):
            return ConstContent(str(spec))

        CONTENT_REGISTRY.parse(spec)
