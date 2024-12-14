import os

from .prompt_collapse import ComponentRepository, Solver

_CACHED_SOLVER = None


class PromptCollapseNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {"multiline": True, "default": "", "label": "Prompt"},
                ),
                "components_directory_path": (
                    "STRING",
                    {"default": "", "label": "Components Directory Path"},
                ),
                "reload_on_generation": (
                    "BOOLEAN",
                    {"default": False, "label": "Reload on Generation"},
                ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "process"
    CATEGORY = "prompt_collapse"

    def process(self, prompt, components_directory_path, reload_on_generation, seed):
        global _CACHED_SOLVER

        if not components_directory_path:
            components_directory_path = os.path.join(
                os.path.dirname(__file__), "components"
            )

        if _CACHED_SOLVER is None:
            repo = ComponentRepository()
            repo.load(str(components_directory_path))
            _CACHED_SOLVER = Solver(repo)

        if reload_on_generation:
            _CACHED_SOLVER.repository.load(str(components_directory_path))

        tags = [c_name.strip() for c_name in prompt.strip().split(",")]
        tags = [c_name for c_name in tags if c_name]

        prompt = _CACHED_SOLVER.generate_prompt(tags)

        return (prompt,)
