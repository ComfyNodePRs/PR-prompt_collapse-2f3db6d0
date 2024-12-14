from prompt_collapse.common.registry import TypeRegistry

from .requirement import Requirement

REQUIREMENT_REGISTRY: TypeRegistry[Requirement] = TypeRegistry()
