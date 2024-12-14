from prompt_collapse.common.registry import TypeRegistry

from .declaration import Declaration

DECLARATION_REGISTRY: TypeRegistry[Declaration] = TypeRegistry()
