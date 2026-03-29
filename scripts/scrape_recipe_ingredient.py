import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

BASE_URL = "https://minimalistbaker.com/recipe-index/"
RECIPE_LINK_SELECTOR = "h3.post-summary__title a" 
TITLE_SELECTOR = "h2.wprm-recipe-name"
INGREDIENT_SELECTOR = "li.wprm-recipe-ingredient"

ingredient_to_id = {}
id_to_ingredient = {}
next_ingredient_id = 1
recipes_data = []

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        return response.text
    except requests.RequestException:
        return None

def parse_index(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.select(RECIPE_LINK_SELECTOR):
        href = a.get('href')
        if href:
            links.append(href)
    return set(links)

def parse_recipe(html):
    global next_ingredient_id
    soup = BeautifulSoup(html, 'html.parser')
    
    title_elem = soup.select_one(TITLE_SELECTOR)
    if not title_elem:
        return

    title = title_elem.get_text(strip=True)
    ingredient_ids = []

    for item in soup.select(INGREDIENT_SELECTOR):
        ing_text = item.get_text(strip=True).lower()
        if not ing_text:
            continue
            
        if ing_text not in ingredient_to_id:
            ingredient_to_id[ing_text] = next_ingredient_id
            id_to_ingredient[next_ingredient_id] = ing_text
            next_ingredient_id += 1
            
        ingredient_ids.append(ingredient_to_id[ing_text])

    recipes_data.append({
        "name": title,
        "ingredients": ingredient_ids
    })

def main():
    page_num = 1
    all_recipe_links = set()
    
    while True:
        if page_num == 1:
            page_url = BASE_URL
        else:
            page_url = f"{BASE_URL}?fwp_paged={page_num}"
            
        print(f"Scraping index page {page_num}...")
        html = get_html(page_url)
        
        if not html:
            break
            
        new_links = parse_index(html)
        if not new_links:
            break
            
        all_recipe_links.update(new_links)
        page_num += 1
        time.sleep(1)

    print("Finished getting all recipe links")

    count = 1
    for link in all_recipe_links:
        print(f"Scraping recipe {count} of {len(all_recipe_links)}")
        full_url = urljoin(BASE_URL, link)
        recipe_html = get_html(full_url)
        if recipe_html:
            parse_recipe(recipe_html)
        time.sleep(1)
        count += 1

    output = {
        "ingredient_map": id_to_ingredient,
        "recipes": recipes_data
    }

    with open('output2.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()