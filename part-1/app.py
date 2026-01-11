"""
Part 1: Basic Flask with SQLite Database
=========================================
"""

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'students.db'


# ===============================
# DATABASE HELPERS
# ===============================
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ===============================
# ROUTES
# ===============================
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)


# ✅ EXERCISE SOLUTION 
@app.route('/add')
def add_sample_student():
    conn = get_db_connection()

    students = [
        ('Priyanka', 'priyanka@gmail.com', 'MCA'),
        ('Amit', 'amit@gmail.com', 'Python'),
        ('Sneha', 'sneha@gmail.com', 'Data Science'),
        ('Rahul', 'rahul@gmail.com', 'Web Development')
    ]

    conn.executemany(
        'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
        students
    )

    conn.commit()
    conn.close()
    return 'Students added! <a href="/">Go back to home</a>'


# ===============================
# MAIN
# ===============================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
