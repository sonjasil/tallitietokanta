from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_lesson", methods=["POST"])
def add_lesson():
    level = request.form["level"]
    price = request.form["price"]
    number = request.form["number"]
    sql = text("INSERT INTO lessons (skill_level, price, max_riders) VALUES (:level, :price, :number)")
    db.session.execute(sql, {"level":level, "price":price, "number":number})
    db.session.commit()
    return redirect("admin_lessons")

@app.route("/admin_lessons")
def admin_lessons():
    sql = text("SELECT skill_level, price, max_riders FROM lessons")
    result = db.session.execute(sql)
    lesson_list = result.fetchall()
    return render_template("admin_lessons.html", lesson_list=lesson_list)

@app.route("/add_horse", methods=["POST"])
def add_horse():
    name = request.form["name"]
    year = request.form["year"]
    lessons = request.form["lessons"]
    feed = request.form["feed"]
    amount = request.form["amount"]
    sql = text("INSERT INTO horses (horse_name, birthyear, max_lessons, feed, feed_amount) VALUES (:name, :year, :lessons, :feed, :amount)")
    db.session.execute(sql, {"name":name, "year":year, "lessons":lessons, "feed":feed, "amount":amount})
    db.session.commit()
    return redirect("admin_horses")

@app.route("/admin_horses")
def admin_horses():
    sql = text("SELECT horse_name, birthyear, max_lessons, feed, feed_amount from horses")
    result = db.session.execute(sql)
    horse_list = result.fetchall()
    return render_template("admin_horses.html", horse_list=horse_list)

@app.route("/teacher_lessons")
def teacher_lessons():
    sql1 = text("SELECT skill_level, price, max_riders FROM lessons")
    result1 = db.session.execute(sql1)
    lesson_list = result1.fetchall()
    sql2 = text("SELECT horse_name, birthyear, max_lessons, feed, feed_amount from horses")
    result2 = db.session.execute(sql2)
    horse_list = result2.fetchall()
    return render_template("teacher_lessons.html", lesson_list=lesson_list, horse_list=horse_list)

@app.route("/student_add_lesson")
def student_add_lesson():
    return render_template("student_add_lesson.html")

@app.route("/student_own_lessons")
def student_own_lessons():
    return render_template("student_own_lessons.html")