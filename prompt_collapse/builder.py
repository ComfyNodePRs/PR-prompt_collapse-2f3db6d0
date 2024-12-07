import random


class PromptBuilder:
    def __init__(self, repository, initial_selected=None, tags=None):
        self.repository = repository
        self.relationships = repository.get_relationship_graph()

        assert initial_selected is None or tags is None, "Cannot specify both initial_selected and tags"

        self.tags = tags or [] 
        initial_selected = [] if tags else initial_selected

        self.selected = []
        self.components = repository.get_all_components()

        self.candidates = set(self.components.values())

        if initial_selected:
            self.collapse_initial_selected(initial_selected)
        
        if tags:
            self.collapse_tags(tags)

        self.candidates -= set(self.selected)

    def is_compatible(self, comp):
        for s in self.selected:
            r = self.relationships.get_relationship(s.name, comp.name)

            if r["type"] == "negative":
                return False
            rev_r = self.relationships.get_relationship(comp.name, s.name)

            if rev_r["type"] == "negative":
                return False

        return True
    
    def are_components_compatible(self, a, b):
        if a.name == b.name:
            return True

        r = self.relationships.get_relationship(a.name, b.name)

        if r["type"] == "negative":
            return False
        rev_r = self.relationships.get_relationship(b.name, a.name)

        if rev_r["type"] == "negative":
            return False
        
        if a.tags & b.anti_tags or b.tags & a.anti_tags:
            return False

        return True

    def compute_candidate_weights(self):
        final_weights = {}
        for c in self.candidates:
            w = 1.0
            compatible = True
            for s in self.selected:
                if not self.are_components_compatible(s, c):
                    compatible = False
                    break

                w += self.relationships.get_relationship(s.name, c.name)["weight"]

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
                if (
                    s.name == candidate.name 
                    or not self.are_components_compatible(s, candidate)
                ):
                    print(f"Removing {candidate.name} because it's not compatible with {s.name}")
                    to_remove.add(candidate)

        self.clear_selected(to_remove)

    def build_prompt(self, max_components=None):
        print(self.selected)
        print(self.candidates)

        while True:
            if max_components is not None and len(self.selected) >= max_components:
                break

            if len(self.candidates) == 0:
                break

            chosen = self.select_component()
            if chosen is None:
                break

            self.selected.append(chosen)

            self.remove_contradictory_components()

        final_contents = []
        for c in self.selected:
            if not c.is_abstract:
                content = c.get_random_content()
                if content is not None:
                    final_contents.append(content)

        return self.flatten_iterative(final_contents)
    
    def collapse_tags(self, tags):
        for tag in tags:
            compatible_components = [
                component for component in self.candidates
                if tag in component.tags and tag not in component.anti_tags
            ]
            print(tag, compatible_components)

            if compatible_components:
                chosen = random.choice(compatible_components)

                self.selected.append(chosen)
                self.remove_contradictory_components()

    def collapse_initial_selected(self, initial_selected):
        for n in initial_selected:
            comp = self.components.get(n)
            if comp is None:
                raise ValueError(f"Initial component {n} not found.")
            self.selected.append(comp)
            self.remove_contradictory_components()

    def clear_selected(self, values):
        self.candidates.difference_update(values)

    @staticmethod
    def flatten_iterative(lst):
        stack = [lst]
        flattened = []
        
        while stack:
            current = stack.pop()
            if isinstance(current, (list, tuple)):
                stack.extend(reversed(current))
            else:
                flattened.append(current)
                
        return flattened[::-1]