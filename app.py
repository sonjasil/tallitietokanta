from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    sql = text("SELECT id, pword FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("error.html", message="Tunnusta ei ole olemassa")
    else:
        hash_value = user.pword
        if check_password_hash(hash_value, password):
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
    pword = request.form["password"]
    pword2 = request.form["password2"]
    hash_value = generate_password_hash(pword)
    system_role = request.form["role"]
    sql = text("INSERT INTO users (username, pword, system_role) VALUES (:username, :pword, :system_role)")
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
    visible = True
    sql = text("INSERT INTO horses (horse_name, birthyear, max_lessons, feed, feed_amount, visible) VALUES (:name, :year, :lessons, :feed, :amount, :visible)")
    db.session.execute(sql, {"name":name, "year":year, "lessons":lessons, "feed":feed, "amount":amount, "visible":visible})
    db.session.commit()
    return redirect("admin_horses")

@app.route("/admin_horses")
def admin_horses():
    sql = text("SELECT horse_name, birthyear, max_lessons, feed, feed_amount from horses WHERE visible=TRUE")
    result = db.session.execute(sql)
    horse_list = result.fetchall()
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
    sql3 = text("SELECT horse_name, birthyear, max_lessons, feed, feed_amount from horses WHERE visible=TRUE")
    result3 = db.session.execute(sql3)
    horse_list = result3.fetchall()
    return render_template("admin_horses.html", feed_list=feed_list, feed_sum=feed_sum, horse_list=horse_list)

@app.route("/teacher_lessons")
def teacher_lessons():
    sql1 = text("SELECT skill_level, price, max_riders FROM lessons")
    result1 = db.session.execute(sql1)
    lesson_list = result1.fetchall()
    sql2 = text("SELECT horse_name, birthyear, max_lessons, feed, feed_amount from horses WHERE visible=TRUE")
    result2 = db.session.execute(sql2)
    horse_list = result2.fetchall()
    return render_template("teacher_lessons.html", lesson_list=lesson_list, horse_list=horse_list)

@app.route("/student_add_lesson")
def student_add_lesson():
    return render_template("student_add_lesson.html")

@app.route("/student_own_lessons")
def student_own_lessons():
    return render_template("student_own_lessons.html")