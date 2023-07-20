import sqlite3
import sys
def check_database():
    # Path to the SQLite database file
    database_path = 'database.db'

    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(database_path)

        # Check if tables exist, and create them if necessary
        cursor = connection.cursor()

        # Check if the 'users' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        users_exists = cursor.fetchone()

        if not users_exists:
            cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, data TEXT)")
            print("Created 'users' table")

        # Check if the 'ALLTABLES' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ALLTABLES'")
        alltables_exists = cursor.fetchone()

        if not alltables_exists:
            cursor.execute("CREATE TABLE ALLTABLES (activity VARCHAR NOT NULL UNIQUE)")
            print("Created 'ALLTABLES' table")

        connection.commit()
        cursor.close()
        connection.close()

    except sqlite3.Error as error:
        print("Error connecting to SQLite database:", error)
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)