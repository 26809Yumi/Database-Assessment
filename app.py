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
