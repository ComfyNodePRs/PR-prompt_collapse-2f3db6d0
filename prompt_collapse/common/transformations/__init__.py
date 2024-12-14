from .constant import ConstantTransformation
from .identity import IdentityTransformation
from .lookup import LookupTransformation
from .match import MatchTransformation
from .random_value import RandomValueTransformation
from .random_int import RandomIntTransformation
from .registry import TRANSFORMATION_REGISTRY
from .sequence import SequenceTransformation
from .transformation import Transformation

TRANSFORMATION_REGISTRY.register("lookup", LookupTransformation)
TRANSFORMATION_REGISTRY.register("constant", ConstantTransformation)
TRANSFORMATION_REGISTRY.register("identity", IdentityTransformation)
TRANSFORMATION_REGISTRY.register("sequence", SequenceTransformation)
TRANSFORMATION_REGISTRY.register("match", MatchTransformation)
TRANSFORMATION_REGISTRY.register("random_value", RandomValueTransformation)
TRANSFORMATION_REGISTRY.register("random_int", RandomIntTransformation)

TRANSFORMATION_REGISTRY.register("const", ConstantTransformation)
TRANSFORMATION_REGISTRY.register("seq", SequenceTransformation)
TRANSFORMATION_REGISTRY.register("id", IdentityTransformation)
TRANSFORMATION_REGISTRY.register("one_of", RandomValueTransformation)
TRANSFORMATION_REGISTRY.register("range", RandomIntTransformation)


__all__ = [
    "Transformation",
    "LookupTransformation",
    "ConstantTransformation",
    "IdentityTransformation",
    "SequenceTransformation",
    "MatchTransformation",
    "TRANSFORMATION_REGISTRY",
]
