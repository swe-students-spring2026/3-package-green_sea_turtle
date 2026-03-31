![Python build & test](https://github.com/swe-students-spring2026/3-package-green_sea_turtle/actions/workflows/tests.yml/badge.svg)

# WhatsCookin

## About The Project

WhatsCookin is a Python package that interfaces with the command-line tool to solve the daily dilemma of figuring out what to cook. By inputting the ingredients you currently have in your kitchen, WhatsCookin queries a local JSON database to find potential recipes.

### Installation

```bash
pip install WhatsCookin
```

#### Local Dev Installation

Clone the repository and install dependencies using pipenv:

```bash
python3 -m pip install pipenv
python3 -m pipenv install --dev
```

Activate the environment:
`python3 -m pipenv shell`

Run tests:
`pytest`

Build the package:
`python3 -m build`

### Usage

#### 1. Find Recipes

Pass a list of ingredients you have on hand to see what you can make.

```
whatscookin find "chicken" "rice" "soy sauce" "broccoli"
```

###### Output

Matches Found:

ID: 101 | Name: Chicken and Broccoli Stir-Fry

ID: 102 | Name: Simple Chicken Fried Rice

#### 2. Get Recipe Details

Use a Recipe ID to get the full prep time and instructions.

```
whatscookin details 101
```

##### Output:

Recipe: Chicken and Broccoli Stir-Fry
Prep Time: 20 mins
Instructions: Dice the chicken and chop the broccoli ...

#### 3. Check Missing Ingredients

See what you need to buy at the store to make a specific recipe (using its ID) based on what you already have.

```
whatscookin missing 104 "chicken" "rice"
```

##### Output:

You still need:

- soy sauce
- broccoli

#### 4. Surprise Me!

Just ask for a random recipe!

```
whatscookin random
```

##### Output:

Spicy Peanut Noodles (ID: 212)
