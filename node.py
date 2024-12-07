import os
from .prompt_collapse import PromptBuilder, ComponentRepository

_CACHED_REPO = None


class PromptCollapseNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "label": "Prompt"}),
                "components_directory_path": ("STRING", {"default": "", "label": "Components Directory Path"}),
                "reload_on_generation": ("BOOLEAN", {"default": False, "label": "Reload on Generation"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "process"
    CATEGORY = "prompt_collapse"


    def process(self, prompt, components_directory_path, reload_on_generation):
        global _CACHED_REPO

        if not components_directory_path:
            components_directory_path = os.path.join(os.path.dirname(__file__), "components")

        if _CACHED_REPO is None or reload_on_generation:
            _CACHED_REPO = ComponentRepository()
            _CACHED_REPO.load_from_directory(components_directory_path)

        component_names = [c_name.strip() for c_name in prompt.split(",")]

        builder = PromptBuilder(repository=_CACHED_REPO, initial_selected=component_names)
        result = ", ".join(builder.build_prompt())

        return (result,)