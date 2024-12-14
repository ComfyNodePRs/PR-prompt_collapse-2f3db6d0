import random
from typing import Any

from .quota import Quota


class RangeQuota(Quota):
    def __init__(self, min_count: int, max_count: int) -> None:
        self.min_count = min_count
        self.max_count = max_count

    def apply(self) -> int:
        return random.randint(self.min_count, self.max_count)

    @classmethod
    def from_spec(cls, spec: Any) -> "RangeQuota":
        min_val = int(spec.get("min", 0))
        max_val = int(spec.get("max", 0))

        return cls(min_val, max_val)

    def __repr__(self) -> str:
        return "RangeQuota(min=%s, max=%s)" % (self.min_count, self.max_count)

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))
