from abc import ABC, abstractmethod
from typing import Any, TypeVar

from prompt_collapse.state import State

T = TypeVar("T", bound="Transformation")


class Transformation(ABC):
    @classmethod
    @abstractmethod
    def from_spec(cls, spec: Any) -> "T":
        raise NotImplementedError

    @abstractmethod
    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Applying the transformation to the provided value (if any) given both the local and global state.
        Local state only exists during component evaluation, while global state is used throughout the entire
        prompt generation process.

        :param value: The value to apply the transformation to
        :param local_state: The local state obtained after "collapsing" component parameters
        :param global_state: The global state/context
        :return: The transformed value
        """
        raise NotImplementedError
