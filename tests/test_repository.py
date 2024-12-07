import os
import tempfile
import yaml
from prompt_collapse.repository import ComponentRepository


def test_load_components_from_directory():
    # Given
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_dir = os.path.join(tmpdir, "clothes", "upper", "warm")
        os.makedirs(nested_dir, exist_ok=True)

        yaml_file = os.path.join(nested_dir, "long_sleeved.yaml")
        data = [{
            "name": "hoodie",
            "content": ["a warm long-sleeved hoodie", "a cozy hoodie"],
            "relationships": {
                "mens_business_suits": {
                    "type": "negative"
                }
            }
        }]

        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)

        repo = ComponentRepository()
        
        # When
        repo.load_from_directory(tmpdir)
        comp_name = "clothes.upper.warm.long_sleeved.hoodie"
        component = repo.get_component(comp_name)
        relationship = repo.get_relationship_graph().get_relationship(
            comp_name, 
            "mens_business_suits"
        )

        # Then
        assert component is not None
        assert component.name == comp_name
        assert len(component.content) == 2
        assert relationship["type"] == "negative"
