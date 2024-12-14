from prompt_collapse.common.registry import TypeRegistry

from .quota import Quota

QUOTA_REGISTRY: TypeRegistry[Quota] = TypeRegistry()
