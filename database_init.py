import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    UID TEXT NOT NULL UNIQUE
)
''')

# Insert sample data
cursor.execute("INSERT INTO employees (UID) VALUES (?)", ('1234567890',))
cursor.execute("INSERT INTO employees (UID) VALUES (?)", ('0987654321',))
cursor.execute("INSERT INTO employees (UID) VALUES (?)", ('1839402942',))

# Commit and close connection
conn.commit()
conn.close()
