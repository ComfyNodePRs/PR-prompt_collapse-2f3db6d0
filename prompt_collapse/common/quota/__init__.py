from .fixed import FixedQuota
from .quota import Quota
from .range import RangeQuota
from .registry import QUOTA_REGISTRY

QUOTA_REGISTRY.register("fixed", FixedQuota)
QUOTA_REGISTRY.register("const", FixedQuota)
QUOTA_REGISTRY.register("range", RangeQuota)
QUOTA_REGISTRY.register("random", RangeQuota)

__all__ = ["Quota", "FixedQuota", "RangeQuota", "QUOTA_REGISTRY"]
