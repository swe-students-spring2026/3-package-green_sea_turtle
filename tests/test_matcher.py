import pytest
from whatscookin.matcher import match_recipes

class Tests:

    @pytest.fixture
    def example_fixture(self):
       yield
    
    def test_sanity_check(self, example_fixture):
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True!"

    def test_empty_ingredients_list(self):
        results = match_recipes([])
        assert len(results) == 0, "Expected an empty list of results!"

    def test_matches_kale_salad(self):
        ingredients = ["leeks", "beet", "olive oil", "salt", "pepper", 
                   "lentils", "vegetable stock", "kale", "tahini", 
                   "lemon", "maple syrup"]
        results = match_recipes(ingredients)
        
        recipe_names = [recipe["name"] for recipe in results]
        
        assert "Kale, Lentil & Roasted Beet Salad" in recipe_names, "Expected Kale, Lentil & Roasted Beet Salad to be in the results!"
    
    def test_excludes_non_matching_recipes(self):
        ingredients = ["leeks", "beet", "olive oil", "salt", "pepper", 
                   "lentils", "vegetable stock", "kale", "tahini", 
                   "lemon"]
        results = match_recipes(ingredients)

        recipe_names = [recipe["name"] for recipe in results]

        assert "Kale, Lentil & Roasted Beet Salad" not in recipe_names, "Expected Kale, Lentil & Roasted Beet Salad to not be in the results!"