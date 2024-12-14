from .constant import ConstContent
from .content import Content
from .registry import CONTENT_REGISTRY
from .sequence import SequenceContent
from .some_of import SomeOfContent

CONTENT_REGISTRY.register("const", ConstContent)
CONTENT_REGISTRY.register("constant", ConstContent)
CONTENT_REGISTRY.register("some_of", SomeOfContent)
CONTENT_REGISTRY.register("choice", SomeOfContent)
CONTENT_REGISTRY.register("sequence", SequenceContent)
CONTENT_REGISTRY.register("seq", SequenceContent)

__all__ = [
    "Content",
    "ConstContent",
    "SomeOfContent",
    "SequenceContent",
    "CONTENT_REGISTRY",
]
