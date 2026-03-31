import sys
from .matcher import match_recipes, load_recipes
from .utils import random_recipe, missing_ingredients, get_recipe_by_id

def main():
    print("Welcome to What's Cookin!")
    
    args = sys.argv
    if len(args) < 2:
        print("How to use: whatscookin [find|details|missing|random] ...")
        return
    
    command = args[1]
    
    
    # === load_recipes ===
    recipes = load_recipes()

    # === match_recipes ===
    if command == "find":
        if len(args) < 3:
            print("Please enter at least one ingredient to find matching recipes.")
            print("How to use: whatscookin find <ingredient1> <ingredient2> ...")
            return
        user_ingredients = args[2:]
    
        matches = match_recipes(user_ingredients, recipes)

        if not matches:
            print("No matching recipes found.")
            return
    
        print(f"\nTop{min(10,len(matches))} matching recipes:")
        for i, item in enumerate(matches[:10], start=1):
            print(f"{i}, {item['name']} ({item['match_count']} ingredient matches)")

    # === details ===
    elif command == "details":
        if len(args) < 3:
            print("Please provide a recipe ID to view details.")
            print("How to use: whatscookin details <id>")
            return

        recipe_id = int(args[2])
        recipe = get_recipe_by_id(recipe_id, recipes)

        if not recipe:
            print("Recipe not found.")
            return

        print(f"{recipe['name']}")
        print("Ingredients:")
        for ing in recipe["ingredients"]:
            print("-", ing["name"])
        print("Recipe URL:", recipe["source_url"])

    # === missing ===
    elif command == "missing":
        if len(args) < 4:
            print("Please provide a recipe ID and at least one ingredient you have.")
            print("How to use: whatscookin missing <id> <ingredients>")
            return

        recipe_id = int(args[2])
        user_ingredients = args[3:]

        recipe = get_recipe_by_id(recipe_id, recipes)

        if not recipe:
            print("Recipe not found.")
            return

        missing = missing_ingredients(user_ingredients, recipe)

        print("You still need:")
        for m in missing:
            print("-", m)

    # === random ===
    elif command == "random":
        recipe = random_recipe(recipes)
        print(f"{recipe['name']} (ID: {recipe['id']})")

    else:
        print("Unknown command")
        print("Try these commands: whatscookin [find|details|missing|random] ...")


if __name__ =="__main__":
    main()
