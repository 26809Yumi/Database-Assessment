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
