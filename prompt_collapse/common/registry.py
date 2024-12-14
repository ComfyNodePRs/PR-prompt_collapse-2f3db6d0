from typing import Any, Generic, Type, TypeVar

T = TypeVar("T")


class TypeRegistry(Generic[T]):
    """
    A registry for transformations, allowing to register and retrieve transformations by alias.
    Actively used to resolve transformations from their aliases in the configuration during parsing.
    """

    def __init__(self):
        self._types: dict[str, Type[T]] = {}

    def register(self, alias: str, cls: Type[T]) -> None:
        self._types[alias] = cls

    def get(self, alias: str) -> Type[T]:
        if alias not in self._types:
            raise ValueError(f"Alias {alias} not found in registry")

        return self._types[alias]

    def parse(self, spec: Any) -> T:
        if not isinstance(spec, dict):
            raise ValueError(f"Expected a dictionary, but got {spec}")

        name = spec.get("name")

        if name is None:
            raise ValueError("Expected a name for the type")

        cls = self.get(name)

        return cls.from_spec(spec)
