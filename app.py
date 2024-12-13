from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from functools import wraps
from flask import request, jsonify

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "app.secret_key"  # Secret key for session management

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',         
    'password': 'root',        
    'database': 'users',
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Utility function to check allowed file extensions
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database connection helper
def get_db_connection():
    """Helper function to establish a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# Initialize database
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
            photo VARCHAR(255),
            is_admin BOOLEAN DEFAULT FALSE
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

# Initialize database tables
init_db()

# Route for registration form
@app.route('/')
def form():
    """Render the registration form."""
    return render_template('index.html')

# Route for index page
@app.route('/index')
def index():
    return render_template('index.html')

# Route to handle form submission
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

# Login route
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

# Logout route
@app.route('/logout')
def logout():
    """Logout the user by clearing the session."""
    session.pop('user_id', None)  # Remove user_id from session
    session.pop('is_admin', None)  # Remove is_admin flag from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('form'))  # Redirect to the registration page after logout

# Success route (user dashboard)
@app.route('/success')
def success():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch family members data for the logged-in user
    cursor.execute("SELECT * FROM family_members WHERE user_id = %s", (session['user_id'],))
    family_members = cursor.fetchall()

    # Debugging: Print the raw family_members data to see its structure
    print("Fetched family members data:", family_members)

    # Fetch the user details
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()  # This will give user data like first_name, last_name, etc.
    
    conn.close()

    # Prepare the family members data for rendering
    family_members_data = [{
        'id': member[0],         # ID
        'name': member[2],       # Name (index 2)
        'gender': member[3],     # Gender (index 3)
        'age': member[4],        # Age (index 4)
        'relation': member[9]    # Relation (index 9)
    } for member in family_members]

    # Debugging: Print the formatted family_members_data to check the structure
    print("Formatted family members data:", family_members_data)

    # Pass both user and family members data to the template
    return render_template('success.html', user=user, family_members=family_members_data)


# Display all registered users
@app.route('/display')
def display():
    """Display all registered users in a table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return render_template('display.html', rows=rows)

# Route to delete a user
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

# Route to delete a family member
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

# Add family member route
@app.route('/add_family_member', methods=['GET', 'POST'])
def add_family_member():
    if request.method == 'POST':
        # Get the form data
        user_id = request.form['user_id']  # Ensure this matches the field name in the form
        name = request.form['first_name']  # Assuming 'first_name' is the field for the family member name
        gender = request.form['gender']
        age = request.form['age']
        relation = request.form['relation']

        # Insert the new family member into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO family_members (user_id, name, gender, age, relation)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_id, name, gender, age, relation))
        conn.commit()
        conn.close()

        flash('Family member added successfully!', 'success')
        return redirect(url_for('success'))  # Redirect to success page or wherever appropriate
    
    # If GET request, render the page with the logged-in user ID
    return render_template('add_family_member.html', user_id=session['user_id'])



# Admin page route
@app.route('/admin', methods=['GET'])
def admin_page():
    """Direct access to the admin page, displaying all users and their family members' data."""
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query all users and their family members
    cursor.execute(''' 
        SELECT u.id, u.first_name, u.last_name, u.username, fm.name, fm.gender, fm.age, fm.relation
        FROM users u
        LEFT JOIN family_members fm ON u.id = fm.user_id
    ''')
    users_and_family = cursor.fetchall()
    
    conn.close()

    # Debug: Print users_and_family to see the raw data from the query
    print("Fetched users and family data:")
    print(users_and_family)

    # Organize data to display by user and their family members
    users_data = {}
    for row in users_and_family:
        user_id = row[0]
        if user_id not in users_data:
            users_data[user_id] = {
                'user': row[1:4],  # Store user data (first_name, last_name, username)
                'family_members': []
            }
        
        # Add family member data if exists
        if row[4]:  # Check if family member exists
            family_member = row[4:]  # Append family member data
            print(f"Adding family member: {family_member}")
            users_data[user_id]['family_members'].append(family_member)
    
    
    # Debug: Print the users_data structure to see how data is being organized
    print("Organized users_data:")
    print(users_data)

    # Pass the organized data to the template
    return render_template('admin.html', users_data=users_data)



@app.route('/admin-family-data', methods=['POST'])
def admin_family_data():
    """Receives and processes family members' data from the success page."""
    data = request.get_json()  # Get the data sent from the success.html page
    family_members = data.get('family_members', [])
    
    # Process the family member data here as needed (e.g., store it in the database or use it on the admin page)
    print("Family Members Data:", family_members)
    
    # You can send a response back to indicate success
    return jsonify({"status": "success", "family_members": family_members})

# Route for user profile
@app.route('/profile')
def profile():
    """Display user profile if logged in."""
    user_id = session.get('user_id')

    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('profile.html', user=user)
        else:
            flash("User not found.", "error")
            return redirect(url_for('login'))
    else:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for('login'))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
