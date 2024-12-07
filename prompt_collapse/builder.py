import random


class PromptBuilder:
    def __init__(self, repository, initial_selected=None):
        self.repository = repository
        self.relationships = repository.get_relationship_graph()

        if initial_selected is None:
            initial_selected = []

        self.selected = []
        self.components = repository.get_all_components()

        for n in initial_selected:
            comp = self.components.get(n)
            if comp is None:
                raise ValueError(f"Initial component {n} not found.")
            self.selected.append(comp)

        self.candidates = set(self.components.values()) - set(self.selected)

        for comp in self.selected:
            if not self.is_compatible(comp):
                raise ValueError(f"Initial subset is incompatible: {comp.name}")

        self.remove_contradictory_components()

    def is_compatible(self, comp):
        for s in self.selected:
            r = self.relationships.get_relationship(s.name, comp.name)

            if r["type"] == "negative":
                return False
            rev_r = self.relationships.get_relationship(comp.name, s.name)

            if rev_r["type"] == "negative":
                return False

        return True

    def compute_candidate_weights(self):
        final_weights = {}
        for c in self.candidates:
            w = 1.0
            compatible = True
            for s in self.selected:
                rel = self.relationships.get_relationship(s.name, c.name)
                if rel["type"] == "negative":
                    compatible = False
                    break
                w *= rel["weight"]

                rev_rel = self.relationships.get_relationship(c.name, s.name)
                if rev_rel["type"] == "negative":
                    compatible = False
                    break

            if compatible and w > 0:
                final_weights[c] = w

        return final_weights

    def select_component(self):
        final_weights = self.compute_candidate_weights()
        if not final_weights:
            return None

        total = sum(final_weights.values())
        r = random.uniform(0, total)
        cumulative = 0.0
        items = list(final_weights.items())
        random.shuffle(items)
        for c, w in items:
            cumulative += w
            if r <= cumulative:
                return c
        return None

    def remove_contradictory_components(self):
        to_remove = set()

        for s in self.selected:
            for candidate in self.candidates:
                selected_to_candidate = self.relationships.get_relationship(
                    s.name, candidate.name
                )["type"]
                candidate_to_selected = self.relationships.get_relationship(
                    candidate.name, s.name
                )["type"]

                if (
                    selected_to_candidate == "negative"
                    or candidate_to_selected == "negative"
                ):
                    to_remove.add(candidate)

        self.candidates -= to_remove

    def build_prompt(self, max_components=None):
        while True:
            if max_components is not None and len(self.selected) >= max_components:
                break

            chosen = self.select_component()
            if chosen is None:
                break

            self.selected.append(chosen)
            self.candidates.remove(chosen)

            self.remove_contradictory_components()

        final_contents = []
        for c in self.selected:
            if not c.is_abstract:
                content = c.get_random_content()
                if content is not None:
                    final_contents.append(content)

        return final_contents
