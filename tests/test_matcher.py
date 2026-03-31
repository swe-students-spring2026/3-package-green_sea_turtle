import pytest
from whatscookin.matcher import match_recipes

class TestMatcher:
    def test_returns_a_list(self):
        results = match_recipes(["olive oil"])
        assert isinstance(results, list)

    def test_includes_partially_matching_recipe(self):
        ingredients = [
            "leeks", "beet", "olive oil", "salt", "pepper",
            "lentils", "vegetable stock", "kale", "tahini", "lemon"
        ]
        results = match_recipes(ingredients)
        recipe_names = [recipe["name"] for recipe in results]

        assert "Kale, Lentil & Roasted Beet Salad" in recipe_names

    def test_excludes_zero_match_recipes(self):
        results = match_recipes(["dragonfruit"])
        recipe_names = [recipe["name"] for recipe in results]

        assert "Kale, Lentil & Roasted Beet Salad" not in recipe_names

    def test_results_are_sorted_by_match_count(self):
        results = match_recipes(["olive oil", "salt", "pepper", "lemon"])

        assert len(results) > 0
        for i in range(len(results) - 1):
            assert results[i]["match_count"] >= results[i + 1]["match_count"]
