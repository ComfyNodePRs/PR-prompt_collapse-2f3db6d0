from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

T = TypeVar("T", bound="Quota")


class Quota(ABC):
    @abstractmethod
    def apply(self) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_spec(cls: Type[T], spec: Any) -> T:
        raise NotImplementedError
