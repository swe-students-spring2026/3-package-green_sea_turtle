from .matcher import match_recipes

def main():
    print("Welcome to What's Cookin!")
    raw = input("Enter ingredients you have, separated by commas: ").strip()

    if not raw:
        print("No ingredients entered.")
        return
    
    user_ingredients = [item.strip() for item in raw.split(",") if item.strip()]
    
    # === match_recipes ===
    matches = match_recipes(user_ingredients)

    if not matches:
        print("No matching recipes found.")
        return
    
    print(f"\nTop{min(10,len(matches))} matching recipes:")
    for i, item in enumerate(matches[:10], start=1):
        print(f"{i}. {item['name']} ({item['match_count']} ingredient matches)")

if __name__ =="__main__":
    main()
