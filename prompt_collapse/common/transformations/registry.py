from prompt_collapse.common.registry import TypeRegistry

from .transformation import Transformation

TRANSFORMATION_REGISTRY: TypeRegistry[Transformation] = TypeRegistry()
