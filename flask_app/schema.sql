DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS cubes;
DROP TABLE IF EXISTS user_cubes;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE cubes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flat_string TEXT UNIQUE
);

CREATE TABLE user_cubes (
    user_id INTEGER,
    cube_id INTEGER,
    last_used TEXT,
    PRIMARY KEY (user_id, cube_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (cube_id) REFERENCES cubes (id)
);