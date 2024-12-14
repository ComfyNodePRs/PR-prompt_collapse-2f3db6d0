from abc import ABC, abstractmethod
from typing import Any, List, Type, TypeVar

from prompt_collapse.state import State

T = TypeVar("T", bound="Content")


class Content(ABC):
    @abstractmethod
    def apply(self, local_state: State) -> List[str]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_spec(cls: Type[T], spec: Any) -> T:
        raise NotImplementedError
