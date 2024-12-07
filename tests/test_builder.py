from prompt_collapse.builder import PromptBuilder
from prompt_collapse.components import Component
from prompt_collapse.repository import ComponentRepository


def test_remove_contradictory_components_immediately():
    # Given
    repo = ComponentRepository()
    
    c_hoodie = Component(name="clothes.upper.warm.long_sleeved.hoodie", content=["a warm hoodie"])
    c_suit = Component(name="mens_business_suits", content=["a formal business suit"])
    c_hat = Component(name="accessories.head.hat", content=["a stylish hat"])
    
    repo.components[c_hoodie.name] = c_hoodie
    repo.components[c_suit.name] = c_suit
    repo.components[c_hat.name] = c_hat
    
    repo.relationships.add_relationship(c_hoodie.name, c_suit.name, rtype="negative")
    
    # When
    builder = PromptBuilder(repository=repo, initial_selected=[c_hoodie.name])
    
    # Then
    assert c_suit not in builder.candidates


def test_builder_collapses_prompt_avoiding_contradictions():
    # Given
    repo = ComponentRepository()

    c_hoodie = Component(name="clothes.upper.warm.long_sleeved.hoodie", content=["a warm hoodie"])
    c_suit = Component(name="mens_suits", content=["a suit"])
    c_hat = Component(name="accessories.head.hat", content=["a stylish hat"])
    c_boots = Component(name="accessories.foot.boots", content=["a pair of boots"])
    c_shoes = Component(name="accessories.foot.shoes", content=["a pair of shoes"])
    c_glasses = Component(name="accessories.face.glasses", content=["a pair of glasses"])
    c_monocle = Component(name="accessories.face.monocle", content=["a monocle"])

    repo.components[c_hoodie.name] = c_hoodie
    repo.components[c_suit.name] = c_suit
    repo.components[c_hat.name] = c_hat
    repo.components[c_boots.name] = c_boots
    repo.components[c_shoes.name] = c_shoes
    repo.components[c_glasses.name] = c_glasses
    repo.components[c_monocle.name] = c_monocle

    repo.relationships.add_relationship(c_hoodie.name, c_suit.name, rtype="negative")
    repo.relationships.add_relationship(c_glasses.name, c_monocle.name, rtype="negative")
    repo.relationships.add_relationship(c_boots.name, c_shoes.name, rtype="negative")

    builder = PromptBuilder(
        repository=repo, 
        initial_selected=[
            c_suit.name,
            c_shoes.name,
            c_monocle.name,
        ]
    )

    # When
    contents = builder.build_prompt()

    # Then
    assert len(contents) == 4
    assert set(contents) == {
        "a suit",
        "a pair of shoes",
        "a monocle",
        "a stylish hat",
    }
