import random
from typing import List, Optional, Callable

from .state import State
from .component import Component
from .repository import ComponentRepository

ComponentFilter = Callable[[Component], bool]


class Solver:
    def __init__(
        self,
        repository: ComponentRepository,
    ) -> None:
        self._repository = repository

        self._unused_components: List[Component] = []
        self._context: List[Component] = []
        self._prompt_fragments: List[str] = []
        self._state = State()

    def generate_prompt(
        self, initial_tags: List[str]
    ) -> str:
        """
        Generates a prompt based on the initial tags

        :param initial_tags: Initial tags to generate the prompt
        :return: Generated prompt
        """
        self._reset()

        self._populate_with_initial_tags(initial_tags)

        while self._add_random_compatible_component():
            pass

        return ", ".join(set(self._prompt_fragments))

    def _populate_with_initial_tags(self, initial_tags: List[str]) -> None:
        """
        Populates the context with components that match the initial tags

        :param initial_tags: Initial tags to populate the context
        :return: None
        """
        initial_tags = list(set(initial_tags))
        random.shuffle(initial_tags)

        for tag in initial_tags:
            self._add_random_compatible_component(
                lambda c: tag in c.tags
            )

    def _add_random_compatible_component(self, extra_condition: Optional[ComponentFilter] = None) -> bool:
        """
        Adds a random compatible component to the context

        :return: None
        """
        components = self._get_compatible_components(extra_condition=extra_condition)

        if not components:
            return False

        component = random.choice(components)

        self._add_component(component)

        return True

    def _add_component(self, component: Component) -> None:
        """
        Adds a component to the context

        :param component: Component to add
        :return: None
        """
        self._context.append(component)
        self._unused_components.remove(component)

        local_state = component.build_local_state(self._state)

        values = component.apply(local_state, self._state)

        self._prompt_fragments.extend(values)

    def _get_compatible_components(self, extra_condition: Optional[ComponentFilter] = None) -> List[Component]:
        """
        Returns a list of compatible components

        :return: List of compatible components
        """
        components = [component for component in self._unused_components if component.check(self._state)]

        if extra_condition:
            components = [component for component in components if extra_condition(component)]

        return components

    def _reset(self) -> None:
        """
        Resets the context

        :return: None
        """
        self._context = []
        self._prompt_fragments = []
        self._state = State()
        self._unused_components = self._repository.get_all()

    @property
    def repository(self) -> ComponentRepository:
        return self._repository
