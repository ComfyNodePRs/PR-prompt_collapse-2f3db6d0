from prompt_collapse.components import Component


def test_component_content_list():
    # Given
    c = Component(name="test.comp", content="a single value")
    
    # When
    content_length = len(c.content)
    random_content = c.get_random_content()
    
    # Then
    assert content_length == 1
    assert random_content == "a single value"


def test_component_random_choice():
    # Given
    c = Component(name="test.comp2", content=["val1", "val2"])
    
    # When
    chosen = c.get_random_content()
    
    # Then
    assert chosen in ["val1", "val2"]
