import sqlite3
import FillData as F
#To Check:
#>sqlite3
#>.open Task.db
#>.tables
#>.schema users
#>.schema tasks
#>.exit

#Add Admin Users:
#>insert into admin(first_name, last_name, password, email) values ('erne','1','123','test01@test.com')

#Main
connection = sqlite3.connect('Task.db', check_same_thread = False)
cursor = connection.cursor()

f = F.FillData(cursor)
f.dropTables()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        password VARCHAR(32) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        created TIMESTAMP DEFAULT CURRENT_DATE
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks(
		id INTEGER NOT NULL,
		user_id INTEGER NOT NULL,
		title TEXT NOT NULL,
		done BOOLEAN DEFAULT FALSE,
		created TIMESTAMP DEFAULT CURRENT_DATE,
		PRIMARY KEY(id),
		FOREIGN KEY(user_id) REFERENCES users(id),
		UNIQUE(user_id, title)
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        password VARCHAR(32) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        created TIMESTAMP DEFAULT CURRENT_DATE
    );
    """
)

f.fillUsersTable()
f.fillTasksTable()
f.fillAdminTable()

connection.commit()
cursor.close()
connection.close()
