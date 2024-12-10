CREATE TABLE IF NOT EXISTS family_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
SELECT * FROM USERS;
DELETE FROM users WHERE id = 37;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    gender TEXT,
    mobile TEXT,
    email TEXT,
    dob TEXT,
    username TEXT UNIQUE,
    password TEXT
);
