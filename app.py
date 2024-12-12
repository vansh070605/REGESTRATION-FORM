from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from functools import wraps

hashed_password = generate_password_hash('admin@123')
print(hashed_password)

app = Flask(__name__)
app.secret_key = "app.secret_key"  # Secret key for session management

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',         
    'password': 'root',        
    'database': 'users',
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Helper function to establish a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialize the database and create the users and family_members tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
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

    # Create family_members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS family_members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(50) NOT NULL,
            age INT NOT NULL,
            relation VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def form():
    """Render the registration form."""
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        gender = request.form.get('choice')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        dob = request.form.get('dob')
        username = request.form.get('username')
        password = request.form.get('password')
        photo = request.files.get('photo')

        # Validate that all required fields are filled
        if not first_name or not last_name or not mobile or not email or not username or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('form'))

        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            filepath = 'static/uploads/' + filename
            photo.save(os.path.join('static/uploads/', filename))

        hashed_password = generate_password_hash(password)

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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[9], password):  # user[9] is the password field
            session['user_id'] = user[0]  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('success'))  # Redirect to success route
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout the user by clearing the session."""
    session.pop('user_id', None)  # Remove user_id from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('form'))  # Redirect to the registration page after logout

@app.route('/success')
def success():
    """Display logged-in user's details and family members."""
    user_id = session.get('user_id')

    if user_id:
        # Query the database to get user details
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()  # Fetch user data from the database

        # Query to fetch family members
        cursor.execute('SELECT * FROM family_members WHERE user_id = %s', (user_id,))
        family_members = cursor.fetchall()

        conn.close()

        if user:
            # Pass user details and family members to the template
            return render_template('success.html', user=user, family_members=family_members)
        else:
            flash("User not found.", "error")
            return redirect(url_for('login'))  # Redirect to login if user not found
    else:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))  # Redirect to login if no session

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

@app.route('/delete_family_member/<int:family_member_id>', methods=['GET'])
def delete_family_member(family_member_id):
    """Delete a family member from the database by their ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM family_members WHERE id = %s', (family_member_id,))
        conn.commit()
        conn.close()
        flash("Family member deleted successfully!")
    except mysql.connector.Error as e:
        flash(f"Error deleting family member: {e}")
    return redirect(url_for('success'))  # Redirect back to the success page

@app.route('/add_family_member', methods=['GET', 'POST'])
def add_family_member():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        gender = request.form['gender']
        age = request.form['age']
        relation = request.form['relation']  # This should now work correctly

        user_id = session['user_id']  # Assuming logged-in user has an ID in the session

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert family member into the database
        cursor.execute('''
            INSERT INTO family_members (user_id, first_name, gender, age, relation)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_id, first_name, gender, age, relation))

        conn.commit()
        conn.close()

        return redirect(url_for('success'))  # Redirect to success page after adding

    return render_template('add_family_member.html')



@app.route('/admin', methods=['GET'])
def admin_page():
    """Direct access to the admin page with login check."""
    if 'user_id' in session:
        # Check if the logged-in user is an admin (if you have an admin flag in the users table)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
        
        if user and user[10] == 'admin':  # Assume user[10] is the 'role' field
            return render_template('admin.html')
        else:
            flash('You do not have access to this page.', 'error')
            return redirect(url_for('form'))
    else:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
