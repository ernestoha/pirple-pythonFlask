-- SqlLite Schema

CREATE TABLE `users` (
	`id`	INTEGER NOT NULL,
	`first_name`	TEXT NOT NULL,
	`last_name`	TEXT NOT NULL,
	`email`	TEXT NOT NULL UNIQUE,
	`password`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);

CREATE TABLE `todo` (
	`id`	INTEGER NOT NULL,
	`user_id`	INTEGER NOT NULL, /* FK */
	`title`	TEXT NOT NULL,
	`done`	INTEGER DEFAULT 0,
	PRIMARY KEY(`id`)
);
