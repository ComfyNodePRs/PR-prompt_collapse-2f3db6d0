class RelationshipGraph:
    def __init__(self):
        self.relationships = {}

    def add_relationship(self, source, target, rtype="neutral", weight=1.0):
        if source not in self.relationships:
            self.relationships[source] = {}

        self.relationships[source][target] = {"type": rtype, "weight": weight}

    def get_relationship(self, a, b):
        if a in self.relationships and b in self.relationships[a]:
            rel = self.relationships[a][b]
        else:
            rel = {"type": "neutral", "weight": 1.0}
        if "weight" not in rel:
            rel["weight"] = 1.0
        return rel
