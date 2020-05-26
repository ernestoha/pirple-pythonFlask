import sqlite3

#To Check:
#>sqlite3
#>.open Task.db
#>.tables
#>.schema users
#>.schema tasks
#>.exit

connection = sqlite3.connect('Task.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        password VARCHAR(32) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks(
        id	INTEGER NOT NULL,
        user_id	INTEGER NOT NULL,
        title	TEXT NOT NULL,
        done	BOOLEAN DEFAULT FALSE,
        PRIMARY KEY(id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        UNIQUE(user_id, title)
    );
    """
)

connection.commit()
cursor.close()
connection.close()
