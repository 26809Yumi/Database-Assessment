# Recipe organiser app

import sqlite3

# Database setup
def create_database():
    """Creates the recipes table if it doesn't already exist."""
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Allow users to add in new recipes
def add_recipe():
    """Allows the user to add a new recipe."""

    print("\n--- Add New Recipe ---")

    name = input("Enter recipe name: ").strip()
    ingredients = input("Enter ingredients (separate with commas): ").strip()
    instructions = input("Enter cooking instructions: ").strip()

    if not name or not ingredients or not instructions:
        print("Error: All fields are required.")
        return

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO recipes (name, ingredients, instructions)
    VALUES (?, ?, ?)
    """, (name, ingredients, instructions))

    conn.commit()
    conn.close()

    print("Recipe added successfully!")

    # View Recipes
def view_recipes():
    """Displays all stored recipes."""

    print("\n--- Stored Recipes ---")

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()

    conn.close()

    if not recipes:
        print("No recipes found.")
        return

    for recipe in recipes:
        print("\n" + "=" * 40)
        print(f"ID: {recipe[0]}")
        print(f"Name: {recipe[1]}")
        print(f"Ingredients: {recipe[2]}")
        print(f"Instructions: {recipe[3]}")
        print("=" * 40)

# Search Recipe
def search_recipe():
    """Searches for recipes by name."""

    keyword = input("\nEnter recipe name to search: ").strip()

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM recipes
    WHERE name LIKE ?
    """, ('%' + keyword + '%',))

    results = cursor.fetchall()

    conn.close()

    if not results:
        print("No matching recipes found.")
        return

    print("\nSearch Results:")

    for recipe in results:
        print("\n" + "=" * 40)
        print(f"ID: {recipe[0]}")
        print(f"Name: {recipe[1]}")
        print(f"Ingredients: {recipe[2]}")
        print(f"Instructions: {recipe[3]}")
        print("=" * 40)