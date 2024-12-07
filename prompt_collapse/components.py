import random


class RequestBudget:
    def __init__(self, min=None, max=None, exact=None):
        self.min = min
        self.max = max
        self.exact = exact

    def __repr__(self):
        return f"RequestBudget(min={self.min}, max={self.max}, exact={self.exact})"

    def __str__(self):
        return f"{self.min or ''} {self.exact or ''} {self.max or ''}"

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def from_dict(data):
        if isinstance(data, dict):
            return RequestBudget(data.get("min"), data.get("max"), data.get("exact"))

        if isinstance(data, int):
            return RequestBudget(exact=data)

        return RequestBudget(exact=1)


class Dependency:
    def __init__(self, tags, budget):
        self.tags = tags
        self.budget = budget

    def __repr__(self):
        return f"Dependency(tags={self.tags}, budget={self.budget})"

    def __str__(self):
        return f"{self.tags} ({self.budget})"

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def from_dict(data):
        return Dependency(data["tags"], RequestBudget.from_dict(data.get("budget")))


class Component:
    def __init__(
        self,
        name,
        alias=None,
        content=None,
        is_abstract=False,
        tags=None,
        dependencies=None,
        anti_tags=None,
    ):
        self.name = name
        self.alias = alias
        self.tags = set(tags)
        self.dependencies = set(dependencies)
        self.anti_tags = set(anti_tags)
        self.non_contradictory_anti_tags = self.anti_tags - self.tags

        if content is not None and not isinstance(content, list):
            content = [content]

        self.content = content
        self.is_abstract = is_abstract

    def get_random_content(self):
        if self.content and len(self.content) > 0:
            return random.choice(self.content)
        return None

    def __repr__(self):
        return (
            f"Component("
            f"name={self.name}, "
            f"alias={self.alias}, "
            f"abstract={self.is_abstract}, "
            f"tags={self.tags}, "
            f"dependencies={self.dependencies}, "
            f"anti_tags={self.anti_tags}, "
            f"non_contradictory_anti_tags={self.non_contradictory_anti_tags})"
        )

    @staticmethod
    def from_dict(data, prefix=None):
        return Component(
            f"{prefix}.{data['name']}" if prefix else data["name"],
            data.get("alias"),
            data.get("content"),
            data.get("is_abstract", False),
            data.get("tags", []),
            map(Dependency.from_dict, data.get("dependencies", [])),
            data.get("anti_tags", []),
        )
