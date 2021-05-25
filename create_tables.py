import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# id assigned automatically, has to be INTEGER not int...
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# real is just a decimal!
create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()

connection.close()

