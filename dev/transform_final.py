import json
import re

# Regex source: https://coderpad.io/blog/development/the-complete-guide-to-regular-expressions-regex/

def fix_artifacts(text):
    text = text.replace('g round', 'ground')
    text = re.sub(r'^[\-\.\*~\s]+', '', text)
    text = re.sub(r'^[\d\s\/\.]+\s*', '', text)
    
    leading_units = r'^(?:tbsp|tsp|cup|cups|oz|dash|pinch|lb|lbs|g|ml|pint|pints|quart|quarts|gallon|gallons|tablespoon|tablespoons|teaspoon|teaspoons|ounce|ounces)\b\s*'
    text = re.sub(leading_units, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def get_matching_key(text):
    text = text.lower()
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    stop_words = [
        'organic', 'fresh', 'freshly', 'chopped', 'diced', 'minced', 
        'sliced', 'divided', 'packed', 'storebought', 'homemade', 
        'raw', 'roasted', 'toasted', 'powder', 'ground'
    ]
    
    words = text.split()
    filtered = [w for w in words if w not in stop_words]
    
    if not filtered:
        return text.strip()
        
    return " ".join(filtered).strip()

def main():
    with open('output2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    old_map = data.get('ingredient_map', {})
    recipes = data.get('recipes', [])

    grouped_ingredients = {}
    id_translation_map = {}
    new_id_counter = 1

    for old_id, ing_data in old_map.items():
        if isinstance(ing_data, dict):
            name = ing_data.get('name', '')
            notes = ing_data.get('notes', '')
        else:
            name = ing_data
            notes = ""

        clean_name = fix_artifacts(name)
        match_key = get_matching_key(clean_name)
        
        if not match_key:
            continue

        if match_key not in grouped_ingredients:
            grouped_ingredients[match_key] = {
                "new_id": new_id_counter,
                "display_name": clean_name, 
                "notes": [notes] if notes else []
            }
            id_translation_map[str(old_id)] = new_id_counter
            new_id_counter += 1
        else:
            existing = grouped_ingredients[match_key]
            id_translation_map[str(old_id)] = existing["new_id"]
            if notes and notes not in existing["notes"]:
                existing["notes"].append(notes)

    final_ingredient_map = {}
    for match_key, group_data in grouped_ingredients.items():
        valid_notes = [n for n in group_data["notes"] if n.strip()]
        notes_str = " | ".join(valid_notes)
        
        final_ingredient_map[str(group_data["new_id"])] = {
            "name": group_data["display_name"],
            "notes": notes_str
        }

    for recipe in recipes:
        new_ingredients = []
        for old_id in recipe.get("ingredients", []):
            str_old_id = str(old_id)
            if str_old_id in id_translation_map:
                new_id = id_translation_map[str_old_id]
                
                if new_id not in new_ingredients:
                    new_ingredients.append(new_id)
                    
        recipe["ingredients"] = new_ingredients

    final_output = {
        "ingredient_map": final_ingredient_map,
        "recipes": recipes
    }

    with open('final_output.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()