import sqlite3

DB_NAME = "recipes.db"


# Adding new recipe(s)
def add_recipe():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
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
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO recipes
                (recipe_name, category, cooking_time, instructions)
                VALUES (?, ?, ?, ?)
            """, (recipe_name, category, cooking_time, instructions))

            recipe_id = cursor.lastrowid

            print("\n--- ADD INGREDIENTS (type 'done' to finish) ---")

            while True:
                ingredient_name = input("Ingredient: ").strip()

                if ingredient_name.lower() == "done":
                    break

                quantity = input("Quantity: ").strip()

                cursor.execute("""
                    INSERT INTO ingredients
                    (ingredients_name, quantity, recipe_id)
                    VALUES (?, ?, ?)
                """, (ingredient_name, quantity, recipe_id))

        print("Recipe added successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    conn.close()

# Viewing all recipe(s)
def view_recipes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM recipes
    JOIN ingredients
    ON recipes.recipe_id = ingredients.recipe_id
    ORDER BY recipes.recipe_id;
    """)

    rows = cursor.fetchall()

    if not rows:
        print("No recipes found.")
        conn.close()
        return

    current = None

    for row in rows:
        if row[0] != current:
            print("\n======================")
            print("Recipe ID:", row[0])
            print("Name:", row[1])
            print("Category:", row[2])
            print("Time:", row[3])
            print("Instructions:", row[4])
            print("Ingredients:")
            current = row[0]

        print(" -", row[6], ":", row[7])

    conn.close()

# Searching recipe(s)
def search_recipe():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    name = input("Enter recipe name: ")

    cursor.execute("""
    SELECT *
    FROM recipes
    JOIN ingredients
    ON recipes.recipe_id = ingredients.recipe_id
    ORDER BY recipes.recipe_id;
    """)


    rows = cursor.fetchall()

    if not rows:
        print("Recipe not found.")
        conn.close()
        return

    print("\n======================")
    print("Recipe ID:", rows[0][0])
    print("Name:", rows[0][1])
    print("Category:", rows[0][2])
    print("Time:", rows[0][3])
    print("Instructions:", rows[0][4])
    print("Ingredients:")

    for row in rows:
        print(" -", row[6], ":", row[7])

    conn.close()

# Deleting recipes
def delete_recipe():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM recipes
    JOIN ingredients
    ON recipes.recipe_id = ingredients.recipe_id
    ORDER BY recipes.recipe_id;
    """)

    rows = cursor.fetchall()

    if rows:
        print("\n--- CURRENT RECIPES ---")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[6]} - {row[7]}")

    recipe_id = input("\nEnter recipe ID to delete: ")

    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE recipe_id = ?", (recipe_id,))

    conn.commit()
    conn.close()

    print("Recipe deleted!")


# The main menu
def menu():
    while True:
        print("\n===== RECIPE ORGANISER!! =====")
        print("1. Add Recipe")
        print("2. View Recipes")
        print("3. Search Recipe")
        print("4. Delete Recipe")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_recipe()
        elif choice == "2":
            view_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            break
        else:
            print("Invalid option")

menu()

