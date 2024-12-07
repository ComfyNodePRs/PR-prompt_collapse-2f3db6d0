import os

import yaml

from .components import Component
from .relationships import RelationshipGraph


class ComponentRepository:
    def __init__(self):
        self.components = {}
        self.relationships = RelationshipGraph()

    def load_from_directory(self, directory):
        base_dir = os.path.abspath(directory)
        base_len = len(base_dir) + 1

        for root, dirs, files in os.walk(directory):
            for fname in files:
                if fname.lower().endswith((".yaml", ".yml")):
                    path = os.path.join(root, fname)
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            data = [data]

                        # Compute prefix from path
                        relative_path = os.path.abspath(path)[base_len:]
                        relative_path = os.path.splitext(relative_path)[0]
                        prefix = relative_path.replace(os.path.sep, ".")

                        for comp_dict in data:
                            base_name = comp_dict["name"]
                            full_name = f"{prefix}.{base_name}" if prefix else base_name

                            content = comp_dict.get("content")
                            alias = comp_dict.get("alias")
                            is_abstract = comp_dict.get("is_abstract", False)
                            c = Component(full_name, alias, content, is_abstract)
                            self.components[full_name] = c

                            rels = comp_dict.get("relationships", {})

                            for target, rel_info in rels.items():
                                rtype = rel_info.get("type", "neutral")
                                rweight = rel_info.get("weight", 1.0)

                                self.relationships.add_relationship(
                                    full_name, target, rtype, rweight
                                )

    def get_component(self, name):
        return self.components.get(name)

    def get_all_components(self):
        return self.components

    def get_relationship_graph(self):
        return self.relationships
