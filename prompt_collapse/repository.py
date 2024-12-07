import os

import yaml

from .components import Component


class ComponentRepository:
    def __init__(self):
        self.components = set()

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

                        if data:
                            for comp_dict in data:
                                self.components.add(
                                    Component.from_dict(comp_dict, prefix=prefix)
                                )

    def get_components(self):
        return self.components.copy()
