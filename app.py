import sqlite3

DB_NAME = "recipes.db"


def get_db_connection():
    """Helper function to connect and ensure foreign keys are enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Adding new recipe(s)
def add_recipe():
    print("\n--- ADD RECIPE ---")
    recipe_name = input("Recipe name: ").strip()
    category = input("Category: ").strip()

    while True:
        try:
            cooking_time = int(input("Cooking time (minutes): "))
            break
        except ValueError:
            print("Please enter a valid number.")

    instructions = input("Instructions: ").strip()

    try:
        # Using a context manager ensures commits happen automatically if successful
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO recipes (recipe_name, category, cooking_time, instructions)
                VALUES (?, ?, ?, ?)
            """,
                (recipe_name, category, cooking_time, instructions),
            )

            recipe_id = cursor.lastrowid

            print("\n--- ADD INGREDIENTS (type 'done' to finish) ---")
            while True:
                ingredient_name = input("Ingredient: ").strip()
                if ingredient_name.lower() == "done":
                    break

                quantity = input("Quantity: ").strip()

                cursor.execute(
                    """
                    INSERT INTO ingredients (ingredients_name, quantity, recipe_id)
                    VALUES (?, ?, ?)
                """,
                    (ingredient_name, quantity, recipe_id),
                )

        print("Recipe added successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


# Viewing all recipe(s)
def view_recipes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT recipes.recipe_id, recipe_name, category, cooking_time, instructions,
               ingredients_name, quantity
        FROM recipes
        LEFT JOIN ingredients ON recipes.recipe_id = ingredients.recipe_id
        ORDER BY recipes.recipe_id;
    """
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No recipes found.")
        return

    current_recipe_id = None
    for row in rows:
        # Check if we have moved to a new recipe
        if row[0] != current_recipe_id:
            print("\n======================")
            print(f"Recipe ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Category: {row[2]}")
            print(f"Time: {row[3]} mins")
            print(f"Instructions: {row[4]}")
            print("Ingredients:")
            current_recipe_id = row[0]

        # Print ingredient if it exists (handles recipes without ingredients)
        if row[5]:
            print(f" - {row[5]}: {row[6]}")


# Searching recipe(s)
def search_recipe():
    name = input("Enter recipe name to search: ").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fixed: Added a WHERE clause to actually filter by name
    cursor.execute(
        """
        SELECT recipes.recipe_id, recipe_name, category, cooking_time, instructions,
               ingredients_name, quantity
        FROM recipes
        LEFT JOIN ingredients ON recipes.recipe_id = ingredients.recipe_id
        WHERE recipe_name LIKE ?
        ORDER BY recipes.recipe_id;
    """,
        (f"%{name}%",),
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No matching recipes found.")
        return

    current_recipe_id = None
    for row in rows:
        if row[0] != current_recipe_id:
            print("\n======================")
            print(f"Recipe ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Category: {row[2]}")
            print(f"Time: {row[3]} mins")
            print(f"Instructions: {row[4]}")
            print("Ingredients:")
            current_recipe_id = row[0]

        if row[5]:
            print(f" - {row[5]}: {row[6]}")


# Deleting recipes
def delete_recipe():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Show simplified list for deletion overview
    cursor.execute("SELECT recipe_id, recipe_name FROM recipes;")
    rows = cursor.fetchall()

    if not rows:
        print("No recipes available to delete.")
        conn.close()
        return

    print("\n--- CURRENT RECIPES ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")

    recipe_id = input("\nEnter recipe ID to delete: ").strip()

    try:
        # Delete ingredients first to maintain integrity, then the recipe
        cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        cursor.execute("DELETE FROM recipes WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        print("Recipe deleted!")
    except sqlite3.Error as e:
        print(f"Database error during deletion: {e}")
    finally:
        conn.close()


# The main menu
def menu():
    while True:
        print("\n===== RECIPE ORGANISER!! =====")
        print("1. Add Recipe")
        print("2. View Recipes")
        print("3. Search Recipe")
        print("4. Delete Recipe")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_recipe()
        elif choice == "2":
            view_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()