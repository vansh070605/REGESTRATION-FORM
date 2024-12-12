from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from functools import wraps

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
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

def login_required(f):
    """Decorator to protect routes from unauthenticated access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Check if user is logged in
            flash('You need to log in first!', 'warning')
            return redirect(url_for('login'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def form():
    """Render the registration form."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
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
    """Handle the login functionality."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()  # Fetch the first row

        if user and check_password_hash(user[9], password):  # Index 9 is the 'password' field in the result tuple
            session['user_id'] = user[0]  # Index 0 is the 'id' field in the result tuple
            flash('Login successful!', 'success')
            return redirect(url_for('success'))  # Redirect to a success page after login
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))  # Redirect back to login if invalid credentials

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout the user by clearing the session."""
    session.pop('user_id', None)  # Remove user_id from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('form'))  # Redirect to the registration page after logout

@app.route('/success')
@login_required
def success():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get logged-in user's details
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    # Get the logged-in user's family members
    cursor.execute('SELECT * FROM family_members WHERE user_id = %s', (user_id,))
    family_members = cursor.fetchall()

    # Get all registered users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    cursor.execute('SELECT * FROM family_members WHERE user_id = %s', (user_id,))
    family_members = cursor.fetchall()

    print(family_members)

    conn.close()
    return render_template('success.html', user=user, family_members=family_members, users=users)


@app.route('/display')
@login_required
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
@login_required
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
@login_required
def add_family_member():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        gender = request.form['gender']
        age = request.form['age']
        parent_name = request.form['parent_name']
        parent_gender = request.form['parent_gender']
        parent_mobile = request.form['parent_mobile']
        parent_email = request.form['parent_email']
        relation = request.form['relation']

        user_id = session['user_id']  # Assuming logged-in user has an ID in the session

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert family member into the database
        cursor.execute('''
    INSERT INTO family_members (user_id, first_name, gender, age, parent_name, parent_gender, parent_mobile, parent_email, relation)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
''', (user_id, first_name, gender, age, parent_name, parent_gender, parent_mobile, parent_email, relation))



        conn.commit()
        conn.close()

        return redirect(url_for('success'))  # Redirect to success page after adding

    return render_template('add_family_member.html')

if __name__ == '__main__':
    app.run(debug=True)
