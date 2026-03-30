import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "data" / "parsed_recipes.json"

# returns a list of recipe objects that match the user's ingredients
def match_recipes(user_ingredients) :

    matched_recipes = []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for recipe in data["recipes"]:
        all_ingredients_matched = True
        
        for ingredient in recipe["ingredients"]:
            ingredient_name = ingredient["name"].lower()
            
            # Check if ANY user ingredient matches this recipe ingredient
            found_match = False
            for user_ing in user_ingredients:
                if user_ing.lower() in ingredient_name:
                    found_match = True
                    break
            
            if not found_match:
                all_ingredients_matched = False
                break
        
        if all_ingredients_matched:
            matched_recipes.append(recipe)

    return matched_recipes
