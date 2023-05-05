from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
from get_lists import get_lessons, get_horses, get_users, get_riders


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    pword = request.form["password"]
    session["username"] = username
    sql = text(f"SELECT id, pword FROM users WHERE username = '{username}'")
    result = db.session.execute(sql)
    user = result.fetchone()
    if not user:
        return render_template("error.html", message="Tunnusta ei ole olemassa")
    else:
        hash_value = user.pword
        if check_password_hash(hash_value, pword):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä salasana")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    rider_name = request.form["name"]
    pword = request.form["password"]
    pword2 = request.form["password2"]
    hash_value = generate_password_hash(pword)
    system_role = request.form["role"]
    user_id = session.get("user_id")
    sql = text("INSERT INTO users (username, pword, system_role) VALUES (:username, :pword, :system_role)")
    sql2 = text("INSERT INTO riders (rider_name, user_id) VALUES (:rider_name, :user_id)")
    if 1 <= len(rider_name) <= 15:
        db.session.execute(sql2, {"rider_name":rider_name, "user_id":user_id})
        db.session.commit()
    if 8 <= len(pword) <= 20:
        if 1 <= len(username) <= 15:
            if pword == pword2:
                try:
                    db.session.execute(sql, {"username":username, "pword":hash_value, "system_role":system_role})
                    db.session.commit()
                    return redirect("/")
                except:
                    return render_template("error.html", message="Tunnus on jo käytössä")
            else:
                return render_template("error.html", message="Salasanat eivät ole samat")
        else:
            return render_template("error.html", message="Käyttäjätunnus ei ole oikean pituinen")
        
    else:
        return render_template("error.html", message="Salasana ei ole oikean pituinen")

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
    lesson_list = get_lessons()
    horse_list = get_horses()
    rider_list = get_riders()
    lesson = request.form(["skill_level"])
    sql = text(f"SELECT R.rider_name, H.horse_name lesson_riders LR JOIN ")

@app.route("/student_add_lesson")
def student_add_lesson():
    return render_template("student_add_lesson.html")

@app.route("/student_own_lessons")
def student_own_lessons():
    return render_template("student_own_lessons.html")