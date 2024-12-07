# PromptCollapse

A prompt generation system that manages relationships between prompt components to maintain logical consistency. Integrates with ComfyUI as a custom node.

## Overview

PromptCollapse builds prompts by selecting components based on their inferred relationships. Components have tags associated with them, and relationships are defined through them.
Each component has two sets of tags:
- **Tags**: Tags that the component implements.
- **Anti-tags**: Tags that the component contradicts.

Components also have dependencies, which are other components that must be included in the prompt for the component to be selected.
Dependencies are defined as a list of tags that must be present in the prompt and a budget for the number of components that must be included.
Default budget is exactly one component implementing the requested tags.


## Usage

Components are defined in YAML files and have the following structure:

```yaml
- name: "city"
  tags:
    - urban
    - modern
    - location
  dependencies:
    - tags:
        - daytime
      budget:
        e
  anti_tags:
    - countryside
    - nature
    - location
  content:
    - "cityscape, urban environment, city lights"

- name: "countryside"
  tags:
    - countryside
    - nature
    - location
  dependencies:
    - tags:
        - daytime
      budget:
        min: 1
        max: 1
  anti_tags:
    - urban
    - modern
    - location
  content:
    - "countryside, nature, rural landscape"
```

Folder hierarchy is represented in component names.
For example, `a/b/c.yaml` with a component named `d` within the file will have a component named `a.b.c.d`.

The resulting prompt could contain wildcard names that could be processed by nodes such as `ImpactWildcardProcessor`.

Relationships can be used to control the selection of components.
For example, a component with a positive relationship with another component will be more likely to be selected when that component is selected.

Neutral relationships have no effect on component selection.

Negative relationships prevent a component from being selected if the other component is selected.

## ComfyUI Integration

The system provides a custom node with the following inputs:

- **Prompt**: Initial components (comma-separated)
- **Components Directory Path**: Location of YAML component definitions  
- **Reload on Generation**: Toggle component reloading
- **Seed**: Random seed for component selection
