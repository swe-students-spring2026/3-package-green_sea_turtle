import re

UNIT_PATTERN = (
    r"cups?|cup|tbsp|tablespoons?|tsp|teaspoons?|oz|ounces?|lb|lbs|pounds?|"
    r"g|grams?|kg|ml|l|liters?|litres?|pinch|pinches|dash|dashes|cloves?|"
    r"cans?|packages?|packets?|jars?|bottles?|heads?|stalks?|sprigs?|slices?|"
    r"sticks?|pieces?|bunches?|quarts?|pints?|gallons?"
)

QUANTITY_PATTERN = (
    r"\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?"
)

LEADING_QUANTITY_RE = re.compile(
    rf"^(?P<quantity>(?:{QUANTITY_PATTERN})(?:\s*[–-]\s*(?:{QUANTITY_PATTERN}))?)(?=\s|$)",
    re.IGNORECASE,
)

LEADING_UNIT_RE = re.compile(
    rf"^(?P<unit>{UNIT_PATTERN})\b",
    re.IGNORECASE,
)

PAREN_RE = re.compile(r"\([^()]*\)")

def normalize_text(text):
    text = text.replace("\u00bd", "1/2").replace("\u00bc", "1/4").replace("\u00be", "3/4")
    text = re.sub(r"\s+", " ", text.replace("\n", " "))
    return text.strip()

def extract_notes(text):
    notes = [match.group(0).strip() for match in PAREN_RE.finditer(text)]
    cleaned = PAREN_RE.sub(" ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned, " ".join(notes).strip()

def parse_ingredient_text(text):
    normalized = normalize_text(text)
    body, notes = extract_notes(normalized)

    quantity = ""
    unit = ""
    name = body

    quantity_match = LEADING_QUANTITY_RE.match(body)
    if quantity_match:
        quantity = quantity_match.group("quantity").strip()
        body = body[quantity_match.end():].strip(" ,-")

    unit_match = LEADING_UNIT_RE.match(body)
    if unit_match:
        unit = unit_match.group("unit").strip()
        body = body[unit_match.end():].strip(" ,-")
    elif not quantity:
        fallback_unit_match = LEADING_UNIT_RE.match(name)
        if fallback_unit_match:
            unit = fallback_unit_match.group("unit").strip()
            body = name[fallback_unit_match.end():].strip(" ,-")

    if body:
        name = body

    return {
        "text": normalized,
        "quantity": quantity,
        "unit": unit,
        "name": name.strip(),
        "notes": notes,
    }