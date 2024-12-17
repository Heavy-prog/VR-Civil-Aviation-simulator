from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import sqlite3
import os

app = Flask(__name__ , template_folder="./templates" , static_folder="./static")
app.secret_key = os.urandom(24)  # Secret key for session management

# SQLite Database Configuration
DATABASE = 'database.db'


# Helper Function: Connect to the SQLite Database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn



# Initialize the Database: Create Tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users Table: Manage Admins and Pilots
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL  
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES
            ('admin', 'admin', 'admin'),
            ('PK-01', 'pilot', 'pilot')
    """)

    # Flight Conditions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_conditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_url TEXT
        )
    """)

    # Performance Metrics Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_id INTEGER NOT NULL,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Training Tests Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT NOT NULL,
            scenario TEXT NOT NULL,
            difficulty_level TEXT
        )
    """)

    conn.commit()
    conn.close()


# Initialize the Database
init_db()

# --------------------------------------
# Routes
# --------------------------------------

@app.route('/')
def index():
    if 'username' in session:
        user = get_user(session['username'])
        if user:
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'pilot':
                return redirect(url_for('home'))
    return redirect(url_for('login'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.json)
        username = request.json['username']
        password = request.json['password']

        user = get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            if user['role'] == 'admin':
                return jsonify({"redirect": url_for('admin_dashboard')})
            elif user['role'] == 'pilot':
                return jsonify({"redirect": url_for('home')})
        return jsonify({"error": "Invalid Username or Password"}), 401

    return render_template('Authenticate/index.html')




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))




@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return "Unauthorized!", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('Admin Dashboard/dashboard.html', users=users)




@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    if user['role'] == 'pilot':
        return render_template('Authenticate/Home/index.html', user=user)
    return redirect(url_for('login'))  # redirect if not a pilot



@app.route('/flight-conditions')
def flight_conditions():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = get_user(session['username'])
    if user['role'] != 'pilot':
        return redirect(url_for('home'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flight_conditions")
    conditions = cursor.fetchall()
    conn.close()

    return render_template('./Flight Conditions/flight_conditions.html', conditions=conditions)



@app.route('/performance-analytics')
def performance_analytics():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = get_user(session['username'])
    if user['role'] != 'pilot':
        return redirect(url_for('home'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.username, pm.metric_name, pm.metric_value
    FROM performance_metrics AS pm
    JOIN users AS u ON u.id = pm.user_id
    WHERE u.username = ?
    """, (user['username'],))
    analytics = cursor.fetchall()
    conn.close()


    return render_template('./Performance Analytics/performance_analytics.html', analytics=analytics)



@app.route('/test')
def test():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM training_tests")
    tests = cursor.fetchall()
    conn.close()

    return render_template('Test/index.html', tests=tests)


@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not is_admin():
        return "Unauthorized!", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return "", 204


# --------------------------------------
# Helper Functions
# --------------------------------------

def get_user(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def is_admin():
    if 'username' in session:
        user = get_user(session['username'])
        if user and user['role'] == 'admin':
            return True
    return False


# --------------------------------------
# Run Flask App
# --------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
