import random
from collections import Counter

from .components import Dependency, RequestBudget


class PromptBuilder:
    def __init__(self, repository, tags=None, max_components=None):
        self.repository = repository

        self.max_components = max_components
        self.tags = Counter()
        self.anti_tags = set()
        self.dependencies = self.build_initial_dependencies(tags)

        self.context = []
        self.candidates = self.repository.get_components()

        self.do_state_maintenance()

    def build_prompt(self):
        while not self.stop_condition_fulfilled():
            chosen = self.get_next_candidate()

            if chosen is None:
                break

            self.add_component(chosen)

        return self.get_final_prompt()

    def are_components_compatible(self, a, b):
        if a.name == b.name:
            return True

        if a.tags & b.anti_tags or b.tags & a.anti_tags:
            return False

        return True

    def contradicts_current_state(self, comp):
        for s in self.selected:
            if not self.are_components_compatible(s, comp):
                return True
        return False

    def remove_contradictory_components(self):
        to_remove = set()

        for s in self.context:
            for candidate in self.candidates:
                has_anti_tag = any(tag in self.anti_tags for tag in candidate.tags)
                is_not_compatible = not self.are_components_compatible(s, candidate)
                same_name = s.name == candidate.name

                if has_anti_tag or is_not_compatible or same_name:
                    to_remove.add(candidate)

        self.clear_selected(to_remove)

    def remove_unsolvable_tag_requests(self):
        to_remove = set()

        for dependency in self.dependencies:
            compatible_components = [
                component
                for component in self.candidates
                if not any(
                    tag in component.non_contradictory_anti_tags
                    for tag in dependency.tags
                )
                and any(tag in component.tags for tag in dependency.tags)
            ]

            if not compatible_components:
                to_remove.add(dependency)

        self.dependencies.difference_update(to_remove)

    def remove_fulfilled_dependencies(self):
        to_remove = set()

        for dependency in self.dependencies:
            dep_tags = set(dependency.tags)

            for tag in dependency.tags:
                if self.tags[tag] >= dependency.budget.exact and tag in dep_tags:
                    dep_tags.remove(tag)

            if not dep_tags:
                to_remove.add(dependency)

        self.dependencies.difference_update(to_remove)

    def remove_incompatible_tagged_components(self):
        to_remove = set()
        all_current_tags = self.get_all_positive_tags()

        for candidate in self.candidates:
            if any(tag in all_current_tags for tag in candidate.anti_tags):
                to_remove.add(candidate)

        self.clear_selected(to_remove)

    def get_final_prompt(self):
        final_contents = []
        for c in self.context:
            if not c.is_abstract:
                content = c.get_random_content()
                if content is not None:
                    final_contents.append(content)

        return self.flatten_iterative(final_contents)

    def clear_selected(self, values):
        self.candidates.difference_update(values)

    def do_state_maintenance(self):
        self.remove_incompatible_tagged_components()
        self.remove_fulfilled_dependencies()
        self.remove_unsolvable_tag_requests()
        self.remove_contradictory_components()

    def stop_condition_fulfilled(self):
        if (
            self.max_components is not None
            and len(self.selected) >= self.max_components
        ):
            return True

        if len(self.candidates) == 0:
            return True

        return False

    def build_initial_dependencies(self, tags):
        return {Dependency([tag], RequestBudget(exact=1, min=1, max=1)) for tag in tags}

    def get_all_positive_tags(self):
        all_tags = set()

        for dependency in self.dependencies:
            all_tags.update(dependency.tags)

        for component in self.context:
            all_tags.update(component.tags)

        return all_tags

    def get_unfulfilled_tags(self):
        tags = set()

        for dependency in self.dependencies:
            tags.update(dependency.tags)

        return tags

    def get_next_candidate_conditional(
        self, tags=None, exclude_tags=None, sort_by_matching_tags=False
    ):
        candidates = list(self.candidates)

        if tags:
            candidates = [c for c in candidates if any(tag in c.tags for tag in tags)]

        if exclude_tags:
            candidates = [
                c for c in candidates if not any(tag in c.tags for tag in exclude_tags)
            ]

        if sort_by_matching_tags:
            candidates = sorted(candidates, key=lambda c: len(tags & c.tags))

            if not candidates:
                return None

            top_candidate_match_level = len(tags & candidates[0].tags)
            top_match_candidates = [
                c for c in candidates if len(tags & c.tags) == top_candidate_match_level
            ]

            return random.choice(top_match_candidates)

        if candidates:
            return random.choice(candidates)

        return None

    def satisfy_random_dependency(self):
        dependency = random.choice(list(self.dependencies))

        return self.get_next_candidate_conditional(
            set(dependency.tags), sort_by_matching_tags=True
        )

    def get_next_candidate(self):
        if self.dependencies:
            candidate = self.satisfy_random_dependency()

            if candidate:
                return candidate

        tags = self.get_unfulfilled_tags()
        anti_tags = self.anti_tags

        return self.get_next_candidate_conditional(tags, anti_tags)

    def add_component(self, component):
        self.context.append(component)
        self.anti_tags.update(component.anti_tags)

        for dependency in component.dependencies:
            self.dependencies.add(
                Dependency(
                    dependency.tags,
                    RequestBudget(
                        exact=(
                            dependency.budget.exact
                            or random.randint(
                                dependency.budget.min, dependency.budget.max
                            )
                        )
                    ),
                )
            )

        for tag in component.tags:
            self.tags[tag] += 1

        self.do_state_maintenance()

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
