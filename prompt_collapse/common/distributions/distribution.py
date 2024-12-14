from abc import ABC, abstractmethod
from typing import Any, List, Type, TypeVar

T = TypeVar("T", bound="Distribution")


class Distribution(ABC):
    @classmethod
    @abstractmethod
    def from_spec(cls: Type[T], spec: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    def apply(self, k: int = 1) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def get_items(self) -> dict[int, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_item(self, index: int) -> Any:
        raise NotImplementedError
