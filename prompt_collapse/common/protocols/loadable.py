from typing import Any, Protocol, Type, TypeVar

T = TypeVar("T", bound="Loadable")


class Loadable(Protocol):
    @classmethod
    def from_spec(cls: Type[T], spec: Any) -> T: ...
