import json
import yaml
import os

from typing import List

from .component import Component


class ComponentRepository:
    def __init__(self):
        self._components: dict[str, Component] = {}

    def load(self, path: str) -> None:
        """
        Loads all component files recursively from a given path

        :param path: Path to a component collection
        :return: None
        """
        # List all files in the directory
        # For each file, parse all the components within it and add them to the repository
        filenames = self._list_files(path)

        for filename in filenames:
            components = self._parse_components(filename)

            for component in components:
                if component.alias in self._components:
                    raise ValueError(f"Component with alias {component.alias} already exists")

                self._components[component.alias] = component

    def get(self, alias: str) -> Component:
        if alias not in self._components:
            raise ValueError(f"Component with alias {alias} not found")

        return self._components[alias]

    def get_all(self) -> List[Component]:
        return list(self._components.values())

    def _parse_components(self, file_path: str) -> List[Component]:
        expected_extensions = [".yaml", ".yml", ".json"]

        if not any(file_path.endswith(ext) for ext in expected_extensions):
            return []

        if file_path.endswith(".json"):
            return self._parse_json(file_path)

        return self._parse_yaml(file_path)

    @staticmethod
    def _parse_json(file_path: str) -> List[Component]:
        with open(file_path, "r") as file:
            data = json.load(file)

        return [Component.from_spec(spec) for spec in data]

    @staticmethod
    def _parse_yaml(file_path: str) -> List[Component]:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        return [Component.from_spec(spec) for spec in data]

    @staticmethod
    def _list_files(path: str) -> List[str]:
        filenames = []

        for root, _, files in os.walk(path):
            for file in files:
                filenames.append(os.path.join(root, file))

        return filenames
