from prompt_collapse.common.registry import TypeRegistry

from .content import Content

CONTENT_REGISTRY: TypeRegistry[Content] = TypeRegistry()
