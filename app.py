from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import pandas as pd
from flask import send_file
from io import BytesIO

app = Flask(__name__)
app.secret_key = "app.secret_key"  # For flashing messages

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',        # Replace with your MySQL host
    'user': 'root',             # Replace with your MySQL username
    'password': 'root',         # Replace with your MySQL password
    'database': 'users',        # Replace with your MySQL database name
}

# Allowed file extensions for photo uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    """Helper function to establish a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(50) NOT NULL,
            mobile VARCHAR(15) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            dob DATE NOT NULL,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            photo VARCHAR(255)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def form():
    """Render the registration form."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        gender = request.form['choice']
        mobile = request.form['mobile']
        email = request.form['email']
        dob = request.form['dob']
        username = request.form['username']
        password = request.form['password']
        photo = request.files['photo']
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            filepath ='static/uploads/'+filename
            photo.save(os.path.join('static/uploads/', filename))
            
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO users (first_name, last_name, age, gender, mobile, email, dob, username, password, photo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, age, gender, mobile, email, dob, username, hashed_password, filepath))
        conn.commit()
        conn.close()

        flash("Registration successful!")
        return redirect(url_for('form'))
    except mysql.connector.IntegrityError:
        flash("Error: Duplicate mobile, email, or username detected. Please use unique values.")
        return redirect(url_for('form'))

@app.route('/success')
def success():
    """Render the success page."""
    return render_template('success.html')

@app.route('/display')
def display():
    """Display all registered users in a table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return render_template('display.html', rows=rows)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user from the database by their ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        conn.commit()
        conn.close()
        flash("User deleted successfully!")
    except mysql.connector.Error as e:
        flash(f"Error deleting user: {e}")
    return redirect(url_for('display'))

if __name__ == '__main__':
    app.run(debug=True)
