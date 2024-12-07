# PromptCollapse

A prompt generation system that manages relationships between prompt components to maintain logical consistency. Integrates with ComfyUI as a custom node.

## Overview

PromptCollapse builds prompts by selecting components based on their defined relationships. Components can have positive, negative, or neutral relationships with other components, affecting their selection probability and compatibility.


## Usage

Components are defined in YAML files and have the following structure:

```yaml
- name: "component_name"
  content:  # list of strings
    - "prompt text"
  relationships:
    other_component:
      type: "positive|negative|neutral"  # pick one of the three
      weight: 1.0
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
