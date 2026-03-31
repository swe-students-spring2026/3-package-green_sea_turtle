from whatscookin.matcher import load_recipes, match_recipes
from whatscookin.utils import random_recipe, missing_ingredients, get_recipe_by_id

def main():
    # === load_recipes ===
    recipes = load_recipes()

    # === match_recipes ===
    user_ingredients = ["garlic", "olive oil", "salt", "pepper", "lemon","avocado oil"]
    matches = match_recipes(user_ingredients, recipes)
    print("Your ingredients:")
    for ing in user_ingredients:
        print("-", ing)

    if not matches:
        print("No matching recipes found.")
        return
    
    print(f"\nTop {min(10,len(matches))} matching recipes:")
    for i, item in enumerate(matches[:10], start=1):
        print(f"ID: {item['id']} | Name: {item['name']}, ({item['match_count']} ingredient matches)")

    # === get_recipe_by_id ===
    top_match = matches[0]
    recipe = get_recipe_by_id(top_match["id"], recipes)

    print(f"\n{recipe['name']}")
    print("Ingredients:")
    for ing in recipe["ingredients"]:
        print("-", ing["name"])
    print("Recipe URL:", recipe["source_url"])

    # == missing ==
    missing = missing_ingredients(user_ingredients, recipe)
    print(f"\nFor {recipe['name']}, you still need:")
    for m in missing:
        print("-", m)

    # == random ==
    recipe = random_recipe(recipes)
    print("\nHeres a random recipe!")
    print(f"{recipe['name']} (ID: {recipe['id']})")

if __name__ == "__main__":
    main()


    


   




