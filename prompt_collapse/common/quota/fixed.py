from typing import Any

from .quota import Quota


class FixedQuota(Quota):
    def __init__(self, count: int) -> None:
        self.count = count

    def apply(self) -> int:
        return self.count

    @classmethod
    def from_spec(cls, spec: Any) -> "FixedQuota":
        return cls(int(spec))

    def __repr__(self) -> str:
        return "FixedQuota(count=%s)" % self.count

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))
