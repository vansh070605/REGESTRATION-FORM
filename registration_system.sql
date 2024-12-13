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

ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
UPDATE users SET is_admin = TRUE WHERE username = 'admin_user';
SELECT id FROM users WHERE username = 'admin_user';
hashed_password = generate_password_hash('admin_password')

INSERT INTO users (first_name, last_name, age, gender, mobile, email, dob, username, password, photo, is_admin) 
VALUES ('Admin', 'User', 30, 'Male', '9876543210', 'admin@example.com', '1993-05-01', 'admin_user', 'hashed_password_here', 'path_to_image.jpg', TRUE);

UPDATE users
SET is_admin = TRUE
WHERE username = 'existing_user_username';

SELECT * FROM users WHERE is_admin = TRUE;
SELECT * FROM users WHERE username = 'admin_user';
SELECT username, is_admin FROM users WHERE username = 'admin_user';

UPDATE users
SET password = 'admin@123'
WHERE id = 44;

ALTER TABLE users
MODIFY first_name VARCHAR(255) NOT NULL;

SHOW COLUMNS FROM users;
SELECT * FROM family_members;
ALTER TABLE family_members MODIFY COLUMN first_name VARCHAR(255) NULL;

ALTER TABLE family_members MODIFY COLUMN first_name VARCHAR(255) DEFAULT 'Unknown';


