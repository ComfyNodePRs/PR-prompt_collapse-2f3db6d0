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
                "use_tags": ("BOOLEAN", {"default": False, "label": "Use Tags"}),
                "reload_on_generation": ("BOOLEAN", {"default": False, "label": "Reload on Generation"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "process"
    CATEGORY = "prompt_collapse"


    def process(self, prompt, components_directory_path, use_tags, reload_on_generation, seed):
        global _CACHED_REPO

        if not components_directory_path:
            components_directory_path = os.path.join(os.path.dirname(__file__), "components")

        if _CACHED_REPO is None or reload_on_generation:
            _CACHED_REPO = ComponentRepository()
            _CACHED_REPO.load_from_directory(components_directory_path)

        names = [c_name.strip() for c_name in prompt.strip().split(",")]
        names = [c_name for c_name in names if c_name]

        print(names)

        initial_selected = None if use_tags else names
        tags = names if use_tags else None

        items = PromptBuilder(
            repository=_CACHED_REPO, 
            initial_selected=initial_selected, 
            tags=tags,
        ).build_prompt()
        result = ", ".join(set(items))

        return (result,)