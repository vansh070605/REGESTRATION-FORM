from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT NOT NULL,
            dob TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
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

    # Save to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO users (first_name, last_name, age, gender, mobile, email, dob, username, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, age, gender, mobile, email, dob, username, password))
    conn.commit()
    conn.close()

    # Pass data to success page
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'age': age,
        'gender': gender,
        'mobile': mobile,
        'email': email,
        'dob': dob,
        'username': username,
        'password': password,  # You can choose whether to display the password or not
    }
    
    return render_template('success.html', user_data=user_data)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/display')
def display():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return render_template('display.html', rows=rows)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(''' DELETE FROM users WHERE id = ? ''', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('display'))  # Redirect to the display page to refresh the list

if __name__ == '__main__':
    app.run(debug=True)
