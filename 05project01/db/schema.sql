-- SqlLite Schema

CREATE TABLE users(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	password VARCHAR(32) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE
);

	CREATE TABLE tasks (
		id INTEGER NOT NULL,
		user_id INTEGER NOT NULL,
		title TEXT NOT NULL,
		done BOOLEAN DEFAULT FALSE,
		PRIMARY KEY(id),
		FOREIGN KEY(user_id) REFERENCES users(id),
		UNIQUE(user_id, title)
	);
