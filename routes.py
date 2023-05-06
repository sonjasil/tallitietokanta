from flask import redirect, render_template, request
from sqlalchemy.sql import text
from app import app
from db import db
from get_lists import get_lessons, get_horses, get_users, get_riders, get_lesson_riders
import users

@app.route("/")
def index():
    id = users.user_id()
    role = users.system_role(id)
    return render_template("index.html", role=role)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/login")
    if request.method == "POST":
        username = request.form["username"]
        pword = request.form["password"]
        if users.login(username, pword):
            return redirect("/")
        else:
            return render_template("error.html", message="Kirjautuminen ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return render_template("new_account.html")
    if request.method == "POST":
        username = request.form["username"]
        rider_name = request.form["name"]
        pword = request.form["password"]
        pword2 = request.form["password2"]
        system_role = request.form["role"]
        user_id = users.user_id()
        if 1 <= len(rider_name) <= 15 and 8 <= len(pword) <= 20 and 1 <= len(username) <= 15:
            if pword != pword2:
                return render_template("error.html", message="Salasanat eivät ole samat")
            if users.create_account(username, rider_name, user_id, pword, system_role):
                return redirect("/")
            else:
                return render_template("error.html", message="Rekisteröinti epäonnistui")
        else:
            return render_template("error.html", message="Tarkista tekstin pituus")
    

@app.route("/add_lesson", methods=["POST"])
def add_lesson():
    level = request.form["level"]
    price = request.form["price"]
    number = request.form["number"]
    date = request.form["date"]
    time = request.form["time"]
    sql = text("INSERT INTO lessons (skill_level, price, max_riders, lesson_date, lesson_time) VALUES (:level, :price, :number, :date, :time)")
    db.session.execute(sql, {"level":level, "price":price, "number":number, "date":date, "time":time})
    db.session.commit()
    return redirect("admin_lessons")

@app.route("/admin_lessons")
def admin_lessons():
    lesson_list = get_lessons()
    return render_template("admin_lessons.html", lesson_list=lesson_list)

@app.route("/add_horse", methods=["POST"])
def add_horse():
    name = request.form["name"]
    year = request.form["year"]
    lessons = request.form["lessons"]
    feed = request.form["feed"]
    amount = request.form["amount"]
    visible = True
    sql = text("INSERT INTO horses (horse_name, birthyear, max_lessons, feed, feed_amount, visible) VALUES (:name, :year, :lessons, :feed, :amount, :visible)")
    db.session.execute(sql, {"name":name, "year":year, "lessons":lessons, "feed":feed, "amount":amount, "visible":visible})
    db.session.commit()
    return redirect("admin_horses")

@app.route("/admin_horses")
def admin_horses():
    horse_list = get_horses()
    return render_template("admin_horses.html", horse_list=horse_list)

@app.route("/remove_horse", methods=["POST"])
def remove_horse():
    name = request.form["name"]
    sql = text(f"UPDATE horses SET visible=FALSE WHERE horse_name = '{name}'")
    db.session.execute(sql)
    db.session.commit()
    return redirect("admin_horses")

@app.route("/filter_feed", methods=["POST"])
def filter_feed():
    feed = request.form["feed"]
    sql = text(f"SELECT horse_name, feed, feed_amount from horses WHERE visible=TRUE AND feed='{feed}'")
    result = db.session.execute(sql)
    feed_list = result.fetchall()
    sql2 = text(f"SELECT SUM(feed_amount) from horses WHERE visible=TRUE AND feed='{feed}'")
    result2 = db.session.execute(sql2)
    feed_sum = result2.fetchone()[0]
    horse_list = get_horses()
    return render_template("admin_horses.html", feed_list=feed_list, feed_sum=feed_sum, horse_list=horse_list)

@app.route("/admin_users")
def admin_users():
    user_list = get_users()
    return render_template("admin_users.html", user_list=user_list)

@app.route("/change_role", methods=["POST"])
def change_role():
    username = request.form["user"]
    role = request.form["role"]
    sql = text(f"UPDATE users SET system_role='{role}' WHERE username='{username}'")
    db.session.execute(sql)
    db.session.commit()
    return redirect("admin_users")

@app.route("/teacher_lessons")
def teacher_lessons():
    lesson_list = get_lessons()
    horse_list = get_horses()
    rider_list = get_riders()
    return render_template("teacher_lessons.html", lesson_list=lesson_list, horse_list=horse_list, rider_list=rider_list)

@app.route("/select_lesson", methods=["POST"])
def select_lesson():
    lesson = request.form["individual_lesson"]
    lesson_riders = get_lesson_riders(lesson)

@app.route("/add_rider", methods=["POST"])
def add_rider():
    lesson_id = request.form["lesson"]
    rider = request.form["rider"]
    sql1 = text(f"SELECT id FROM riders WHERE rider_name = '{rider}'")
    result1 = db.session.execute(sql1)
    rider_id = result1.fetchone()[0]
    horse = request.form["horse"]
    sql2 = text(f"SELECT id FROM horses WHERE horse_name = '{horse}'")
    result2 = db.session.execute(sql2)
    horse_id = result2.fetchone()[0]
    sql = text("INSERT INTO lesson_riders (lesson_id, rider_id, horse_id) VALUES (:lesson_id, :rider_id, horse_id)")
    db.session.execute(sql, {"lesson_id":lesson_id, "rider_id":rider_id, "horse_id":horse_id})
    db.session.commit()
    return redirect("teacher_lessons")

@app.route("/student_add_lesson")
def student_add_lesson():
    return render_template("student_add_lesson.html")

@app.route("/student_own_lessons")
def student_own_lessons():
    return render_template("student_own_lessons.html")