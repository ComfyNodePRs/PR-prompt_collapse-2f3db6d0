from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from prompt_collapse.state import State

T = TypeVar("T", bound="Requirement")


class Requirement(ABC):
    @abstractmethod
    def apply(self, global_state: State) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_spec(cls: Type[T], spec: Any) -> T:
        raise NotImplementedError
