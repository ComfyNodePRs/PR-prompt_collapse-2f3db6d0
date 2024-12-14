from typing import Any, List, Set

from prompt_collapse.content import CONTENT_REGISTRY, Content, SequenceContent, ConstContent
from prompt_collapse.declaration import DECLARATION_REGISTRY, Declaration
from prompt_collapse.parameters import Parameter
from prompt_collapse.requirement import (
    REQUIREMENT_REGISTRY,
    AllOfRequirement,
    Requirement,
)
from prompt_collapse.state import State


class Component:
    def __init__(
        self,
        alias: str,
        parameters: List[Parameter],
        declares: List[Declaration],
        requires: List[Requirement],
        generates: List[Content],
        tags: List[str],
    ) -> None:
        self._alias = alias
        self._parameters = parameters
        self._declarations = declares
        self._requirement = AllOfRequirement(requires)
        self._content = SequenceContent(generates)
        self._tags = set(tags)

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def tags(self) -> Set[str]:
        return self._tags.copy()

    def build_local_state(self, global_state: State) -> State:
        local_state = State()

        for parameter in self._parameters:
            parameter.apply(local_state, global_state)

        return local_state

    def apply(self, local_state: State, global_state: State) -> list[str]:
        for declaration in self._declarations:
            declaration.apply(local_state, global_state)

        return self._content.apply(local_state)

    def check(self, global_state: State) -> bool:
        return self._requirement.apply(global_state)

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> "Component":
        alias = cls._get_alias(spec)
        parameters = cls._get_parameters(spec)
        declares = cls._get_declarations(spec)
        requires = cls._get_requirements(spec)
        generates = cls._get_content(spec)
        tags = cls._get_tags(spec)

        return cls(
            alias,
            parameters,
            declares,
            requires,
            generates,
            tags,
        )

    @staticmethod
    def _get_alias(spec: dict[str, Any]) -> str:
        alias = spec.get("alias")
        assert isinstance(alias, str), "Component spec must have a string alias"
        return alias

    @staticmethod
    def _get_parameters(spec: dict[str, Any]) -> List[Parameter]:
        parameters = spec.get("parameters", [])
        assert isinstance(parameters, list), "Component spec parameters must be a list"

        return [Parameter.from_spec(p) for p in parameters]

    @staticmethod
    def _get_declarations(spec: dict[str, Any]) -> List[Declaration]:
        declares = spec.get("declares", [])
        assert isinstance(declares, list), "Component spec declares must be a list"

        return [DECLARATION_REGISTRY.parse(d) for d in declares]

    @staticmethod
    def _get_requirements(spec: dict[str, Any]) -> List[Requirement]:
        requires = spec.get("requires", [])
        assert isinstance(requires, list), "Component spec requires must be a list"

        return [REQUIREMENT_REGISTRY.parse(r) for r in requires]

    @staticmethod
    def _get_content(spec: dict[str, Any]) -> List[Content]:
        generates = spec.get("generates", [])
        assert isinstance(generates, list), "Component spec generates must be a list"

        content = []

        for entry in generates:
            if not isinstance(entry, dict):
                content.append(ConstContent(entry))

            else:
                content.append(CONTENT_REGISTRY.parse(entry))

        return content

    @staticmethod
    def _get_tags(spec: dict[str, Any]) -> List[str]:
        tags = spec.get("tags", [])
        assert isinstance(tags, list), "Component spec tags must be a list"

        return tags

    def __repr__(self) -> str:
        return (
            f"Component("
            f"alias={self._alias}"
            f", parameters={self._parameters}"
            f", declares={self._declarations}"
            f", requires={self._requirement}"
            f", generates={self._content}"
            f", tags={self._tags})"
        )

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))
