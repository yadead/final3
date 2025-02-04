import sqlite3
import os

database_name = "DATABASE/database.db"
table_name = "user_table"
print("Database path:", os.path.abspath(database_name))

#connect sqlite3 to the database
connection = sqlite3.connect(database_name)
cursor = connection.cursor()

#Create a table if it dosent exist yet
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        username TEXT,
        password TEXT
    );
""")
connection.commit()


#ability to input a username and password into the database
def signup(username, password):
    query = f"INSERT INTO {table_name} (username, password) VALUES (?, ?);"
    cursor.execute(query, (username, password))
    connection.commit()
#ability to find and return that specific username and password to check if it is valid
def signin(username, password):
    query = f"SELECT * FROM {table_name} WHERE username = ? AND password = ?;"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result is not None
