from .all_of import AllOfRequirement
from .equals import EqualsRequirement
from .exists import ExistsRequirement
from .greater_than import GreaterThanRequirement
from .less_than import LessThanRequirement
from .none_of import NoneOfRequirement
from .registry import REQUIREMENT_REGISTRY
from .requirement import Requirement
from .some_of import SomeOfRequirement
from .value_in import OneOfRequirement

REQUIREMENT_REGISTRY.register("less_than", LessThanRequirement)
REQUIREMENT_REGISTRY.register("greater_than", GreaterThanRequirement)
REQUIREMENT_REGISTRY.register("exists", ExistsRequirement)
REQUIREMENT_REGISTRY.register("all_of", AllOfRequirement)
REQUIREMENT_REGISTRY.register("some_of", SomeOfRequirement)
REQUIREMENT_REGISTRY.register("none_of", NoneOfRequirement)
REQUIREMENT_REGISTRY.register("equals", EqualsRequirement)
REQUIREMENT_REGISTRY.register("one_of", OneOfRequirement)

REQUIREMENT_REGISTRY.register("lt", LessThanRequirement)
REQUIREMENT_REGISTRY.register("gt", GreaterThanRequirement)
REQUIREMENT_REGISTRY.register("and", AllOfRequirement)
REQUIREMENT_REGISTRY.register("or", SomeOfRequirement)
REQUIREMENT_REGISTRY.register("not", NoneOfRequirement)
REQUIREMENT_REGISTRY.register("in", OneOfRequirement)

__all__ = [
    "Requirement",
    "LessThanRequirement",
    "GreaterThanRequirement",
    "ExistsRequirement",
    "AllOfRequirement",
    "SomeOfRequirement",
    "NoneOfRequirement",
    "EqualsRequirement",
    "OneOfRequirement",
    "REQUIREMENT_REGISTRY",
]
