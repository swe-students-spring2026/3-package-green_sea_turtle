import pytest
from whatscookin.utils import random_recipe, missing_ingredients, get_recipe_by_id

sample_recipes = [
    {
        "id": 1,
        "name": "Chicken Rice",
        "ingredients": [
            {"name": "chicken"},
            {"name": "rice"},
            {"name": "soy sauce"}
        ]
    },
    {
        "id": 2,
        "name": "Tomato Egg",
        "ingredients": [
            {"name": "tomato"},
            {"name": "egg"},
            {"name": "salt"}
        ]
    }
]

def test_get_recipe_by_id_found():
    recipe = get_recipe_by_id(1, sample_recipes)

    assert recipe is not None
    assert recipe["id"] == 1
    assert recipe["name"] == "Chicken Rice"

def test_get_recipe_by_id_not_found():
    recipe = get_recipe_by_id(99, sample_recipes)

    assert recipe is None

def test_missing_ingredients_some_missing():
    recipe = sample_recipes[0]
    result = missing_ingredients(["chicken"], recipe)

    assert "rice" in result
    assert "soy sauce" in result
    assert len(result) == 2

def test_missing_ingredients_none_missing():
    recipe = {
        "id": 3,
        "name": "Simple Dish",
        "ingredients": [{"name": "egg"}, {"name": "salt"}]
    }
    result = missing_ingredients(["egg", "salt"], recipe)

    assert result == []
    
def test_missing_ingredients_invalid_recipe():
    with pytest.raises(ValueError):
        missing_ingredients(["egg"], {"id": 4, "name": "Broken"})

def test_random_recipe_returns_valid_recipe():
    recipe = random_recipe(sample_recipes)

    assert recipe in sample_recipes
    assert "id" in recipe
    assert "name" in recipe

def test_random_recipe_seed_reproducible():
    recipe1 = random_recipe(sample_recipes, seed=42)
    recipe2 = random_recipe(sample_recipes, seed=42)

    assert recipe1 == recipe2

def test_random_recipe_empty_list():
    with pytest.raises(ValueError):
        random_recipe([])
