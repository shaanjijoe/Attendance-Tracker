import sqlite3

def connect_to_database():
    # Path to the SQLite database file on Android
    database_path = 'database.db'

    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(database_path)
        # print("Connection to SQLite database successful!")
        # cursorobj= connection.cursor()
        # return cursorobj
        return connection

    except sqlite3.Error as error:
        print("Error connecting to SQLite database:", error)
        return None
    except Exception:
        return None