import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "data" / "parsed_recipes.json"

"""returns a list of recipes sorted by most number of ingredients 
matched to least amount of ingredients matched. """
def match_recipes(user_ingredients) :

    matched_recipes = []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for recipe in data["recipes"]:
        match_count = 0

        for user_ing in user_ingredients:

            for ingredient in recipe["ingredients"]:
                ingredient_name = ingredient["name"].lower()
                
                if user_ing.lower() in "eggs" and user_ing in ingredient_name:
                    if "eggplant" not in ingredient_name and "veggie" not in ingredient_name: # specifically check for eggs in the word eggplant
                        match_count += 1
                        break
                elif user_ing.lower() in ingredient_name:
                    match_count += 1
                    break
            
        if match_count > 0: # only append if there's more than one matched ingredient
            matched_recipes.append({
                "name": recipe["name"],
                "match_count": match_count,
                "recipe": recipe
            })

    matched_recipes.sort(key=lambda x: x["match_count"], reverse=True)
    return matched_recipes
