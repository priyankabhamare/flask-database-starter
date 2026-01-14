"""
Part 3: Flask-SQLAlchemy ORM
============================
Say goodbye to raw SQL! Use Python classes to work with databases.

What You'll Learn:
- Setting up Flask-SQLAlchemy
- Creating Models (Python classes = database tables)
- ORM queries instead of raw SQL
- Relationships between tables (One-to-Many)

Prerequisites: Complete part-1 and part-2
Install: pip install flask-sqlalchemy
"""


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret-key"

# ================= DATABASE CONFIG =================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================
# EXERCISE 1 SOLVED: Teacher ↔ Course relationship

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    courses = db.relationship("Course", backref="teacher", lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))

    students = db.relationship("Student", backref="course", lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

# ================= ROUTES =================

@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)

@app.route("/courses")
def courses():
    courses = Course.query.all()
    return render_template("courses.html", courses=courses)

@app.route("/teachers")
def teachers():
    teachers = Teacher.query.all()
    return render_template("teachers.html", teachers=teachers)

@app.route("/teacher/<int:id>")
def teacher_courses(id):
    teacher = Teacher.query.get_or_404(id)
    return render_template("teacher_courses.html", teacher=teacher)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student = Student(
            name=request.form["name"],
            email=request.form["email"],
            course_id=request.form["course_id"]
        )
        db.session.add(student)
        db.session.commit()
        flash("Student added!", "success")
        return redirect(url_for("index"))

    courses = Course.query.all()
    return render_template("add.html", courses=courses)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.course_id = request.form["course_id"]
        db.session.commit()
        flash("Student updated!", "success")
        return redirect(url_for("index"))

    courses = Course.query.all()
    return render_template("edit.html", student=student, courses=courses)

@app.route("/delete/<int:id>")
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted!", "danger")
    return redirect(url_for("index"))

@app.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course = Course(
            name=request.form["name"],
            description=request.form.get("description")
        )
        db.session.add(course)
        db.session.commit()
        flash("Course added!", "success")
        return redirect(url_for("courses"))

    return render_template("add_course.html")

# ================= EXERCISE 2 SOLVED =================
# ORM Queries: filter(), order_by(), limit()

def orm_query_examples():
    print("\n--- ORM QUERY EXAMPLES ---")

    students_a = Student.query.filter(Student.name.like("%a%")).all()
    print("Filter (name contains 'a'):", students_a)

    ordered_students = Student.query.order_by(Student.name).all()
    print("Order By (name):", ordered_students)

    limited_students = Student.query.limit(2).all()
    print("Limit (2 students):", limited_students)

@app.route("/query-demo")
def query_demo():
    return render_template(
        "query_demo.html",
        students_a=Student.query.filter(Student.name.like("%a%")).all(),
        ordered=Student.query.order_by(Student.name).all(),
        limited=Student.query.limit(2).all()
    )

# ================= INIT DATABASE =================

def init_db():
    with app.app_context():
        db.create_all()

        if Teacher.query.count() == 0:
            db.session.add_all([
                Teacher(name="Mr. Sharma", email="sharma@example.com"),
                Teacher(name="Ms. Patil", email="patil@example.com")
            ])
            db.session.commit()

        if Course.query.count() == 0:
            teachers = Teacher.query.all()
            db.session.add_all([
                Course(name="Python Basics", description="Learn Python", teacher_id=teachers[0].id),
                Course(name="Web Development", description="HTML CSS Flask", teacher_id=teachers[1].id)
            ])
            db.session.commit()

        # Exercise logic executed
        orm_query_examples()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

# =============================================================================
# ORM vs RAW SQL COMPARISON:
# =============================================================================
#
# Operation      | Raw SQL                          | SQLAlchemy ORM
# ---------------|----------------------------------|---------------------------
# Get all        | SELECT * FROM students           | Student.query.all()
# Get by ID      | SELECT * WHERE id = ?            | Student.query.get(id)
# Filter         | SELECT * WHERE name = ?          | Student.query.filter_by(name='John')
# Insert         | INSERT INTO students VALUES...   | db.session.add(student)
# Update         | UPDATE students SET...           | student.name = 'New'; db.session.commit()
# Delete         | DELETE FROM students WHERE...    | db.session.delete(student)
#
# =============================================================================
# COMMON QUERY METHODS:
# =============================================================================
#
# Student.query.all()                    - Get all records
# Student.query.first()                  - Get first record
# Student.query.get(1)                   - Get by primary key
# Student.query.get_or_404(1)            - Get or show 404 error
# Student.query.filter_by(name='John')   - Filter by exact value
# Student.query.filter(Student.name.like('%john%'))  - Filter with LIKE
# Student.query.order_by(Student.name)   - Order results
# Student.query.count()                  - Count records
#
# =============================================================================


# =============================================================================
# EXERCISE:
# =============================================================================
#
# 1. Add a `Teacher` model with a relationship to Course
# 2. Try different query methods: `filter()`, `order_by()`, `limit()`
#
# =============================================================================
