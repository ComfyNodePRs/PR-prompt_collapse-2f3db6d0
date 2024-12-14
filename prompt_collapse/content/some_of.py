import itertools
from typing import Any, List

from prompt_collapse.common.distributions import WeightedDistribution
from prompt_collapse.common.quota import QUOTA_REGISTRY, FixedQuota, Quota
from prompt_collapse.state import State

from .constant import ConstContent
from .content import Content
from .registry import CONTENT_REGISTRY


class SomeOfContent(Content):
    def __init__(
        self,
        distribution: WeightedDistribution,
        index_to_content: dict[int, Content],
        quota: Quota,
    ) -> None:
        self._distribution = distribution
        self._index_to_content = index_to_content
        self._quota = quota

    def apply(self, local_state: State) -> List[str]:
        count = self._quota.apply()
        indices = self._distribution.apply(k=count)

        return list(
            itertools.chain.from_iterable(
                [self._index_to_content[index].apply(local_state) for index in indices]
            )
        )

    @classmethod
    def from_spec(cls, spec: Any) -> "SomeOfContent":
        assert isinstance(spec, (list, dict)), f"Invalid spec for SomeOfContent: {spec}"

        quota: Quota = FixedQuota(1)

        if isinstance(spec, dict):
            quota = cls._parse_quota(spec.get("quota"))
            spec = spec["values"]

        distribution = WeightedDistribution.from_spec(spec)

        index_to_content = {
            index: cls._parse_content(content_spec)
            for index, content_spec in distribution.get_items().items()
        }

        return cls(distribution, index_to_content, quota)

    @staticmethod
    def _parse_content(spec: Any) -> Content:
        if isinstance(spec, (str, int, float)):
            return ConstContent(str(spec))

        CONTENT_REGISTRY.get(spec["name"]).from_spec(spec)

        raise ValueError(f"Invalid spec for ConstContent: {spec}")

    @staticmethod
    def _parse_quota(spec: Any) -> Quota:
        if spec is None:
            return FixedQuota(1)

        if isinstance(spec, (int, str, float)):
            return FixedQuota(int(spec))

        return QUOTA_REGISTRY.parse(spec)
