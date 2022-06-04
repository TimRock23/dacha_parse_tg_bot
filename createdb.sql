CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY NOT NULL,
    username VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS category(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_category(
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(category_id) REFERENCES category(id)
);


INSERT INTO category(name) values
    ("Кино"), ("Йога"), ("Музыка"), ("Театр"), ("Дети"), ("Лекция"), ("Еда");
