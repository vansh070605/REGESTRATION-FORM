CREATE TABLE IF NOT EXISTS family_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    parent_name VARCHAR(255),
    parent_gender VARCHAR(50),
    parent_mobile VARCHAR(15),
    parent_email VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
SELECT * FROM USERS;
DELETE FROM users WHERE id = 8;
DESCRIBE family_members;


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

ALTER TABLE family_members
ADD COLUMN parent_name VARCHAR(255),
ADD COLUMN parent_gender VARCHAR(50),
ADD COLUMN parent_mobile VARCHAR(15),
ADD COLUMN parent_email VARCHAR(255);

ALTER TABLE family_members MODIFY COLUMN name VARCHAR(255) NULL;
DESCRIBE family_members;

ALTER TABLE family_members
MODIFY COLUMN last_name VARCHAR(255) DEFAULT 'Unknown';

SELECT * FROM family_members;


ALTER TABLE family_members MODIFY COLUMN relation VARCHAR(255) NULL;

DESCRIBE family_members;

CREATE TABLE IF NOT EXISTS family_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
