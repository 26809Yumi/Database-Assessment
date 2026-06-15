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


# Update Recipe
def update_recipe():
    """Updates an existing recipe."""

    view_recipes()

    try:
        recipe_id = int(input("\nEnter Recipe ID to update: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()

    if not recipe:
        print("Recipe not found.")
        conn.close()
        return

    print("\nLeave field blank to keep current value.")

    new_name = input(f"New Name [{recipe[1]}]: ").strip()
    new_ingredients = input(f"New Ingredients [{recipe[2]}]: ").strip()
    new_instructions = input(f"New Instructions [{recipe[3]}]: ").strip()

    if not new_name:
        new_name = recipe[1]

    if not new_ingredients:
        new_ingredients = recipe[2]

    if not new_instructions:
        new_instructions = recipe[3]

    cursor.execute("""
    UPDATE recipes
    SET name = ?, ingredients = ?, instructions = ?
    WHERE id = ?
    """, (new_name, new_ingredients, new_instructions, recipe_id))

    conn.commit()
    conn.close()

    print("Recipe updated successfully!")


# Delete Recipe
def delete_recipe():
    """Deletes a recipe from the database."""

    view_recipes()

    try:
        recipe_id = int(input("\nEnter Recipe ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()

    if not recipe:
        print("Recipe not found.")
        conn.close()
        return

    confirm = input(
        f"Are you sure you want to delete '{recipe[1]}'? (y/n): "
    ).lower()

    if confirm == "y":
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        print("Recipe deleted successfully.")
    else:
        print("Deletion cancelled.")

    conn.close()


# Main Menu
def menu():
    """Displays the application menu."""

    while True:
        print("\n")
        print("=" * 50)
        print("      RECIPE ORGANIZER SYSTEM")
        print("=" * 50)
        print("1. Add Recipe")
        print("2. View Recipes")
        print("3. Search Recipe")
        print("4. Update Recipe")
        print("5. Delete Recipe")
        print("6. Exit")
        print("=" * 50)

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            add_recipe()

        elif choice == "2":
            view_recipes()

        elif choice == "3":
            search_recipe()

        elif choice == "4":
            update_recipe()

        elif choice == "5":
            delete_recipe()

        elif choice == "6":
            print("Thank you for using Recipe Organizer!")
            break

        else:
            print("Invalid option. Please try again.")


# Program Entry Point
if __name__ == "__main__":
    create_database()
    menu()

