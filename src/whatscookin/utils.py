import random

def random_recipe(recipes, seed=None):
    if not recipes:
        raise ValueError("Recipe list is empty")

    rng = random.Random(seed)
    return rng.choice(recipes)

def missing_ingredients(user_ingredients, recipe):
    recipe_ings = [ing["name"].lower() for ing in recipe["ingredients"]]
    user_ings = [ing.lower() for ing in user_ingredients]

    missing = []
    for recipe_ing in recipe_ings:
        matched = any(user_ing in recipe_ing for user_ing in user_ings)
        if not matched:
            missing.append(recipe_ing)

    return missing

def get_recipe_by_id(recipe_id, recipes):
    for recipe in recipes:
        if recipe.get("id") == recipe_id:
            return recipe
    return None