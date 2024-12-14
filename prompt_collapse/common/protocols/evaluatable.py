from typing import Protocol, TypeVar

T = TypeVar("T")


class Evaluatable(Protocol):
    def apply(self) -> T: ...
