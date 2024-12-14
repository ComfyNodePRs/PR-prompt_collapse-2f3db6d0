from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from prompt_collapse.state import State

T = TypeVar("T", bound="Declaration")


class Declaration(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def apply(self, local_state: State, global_state: State) -> Any:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_spec(cls: Type[T], spec: Any) -> T:
        raise NotImplementedError
