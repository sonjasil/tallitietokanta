from sqlalchemy.sql import text
from db import db

def get_lessons():
    sql = text("SELECT id, skill_level, price, max_riders, lesson_date, lesson_time FROM lessons ORDER BY lesson_date, lesson_time")
    result = db.session.execute(sql)
    return result.fetchall()

def get_horses():
    sql = text("SELECT horse_name, birthyear, max_lessons, feed, feed_amount from horses WHERE visible=TRUE")
    result = db.session.execute(sql)
    return result.fetchall()

def get_users():
    sql = text("SELECT username, system_role from users")
    result = db.session.execute(sql)
    return result.fetchall()

def get_riders():
    sql = text("SELECT rider_name from riders")
    result = db.session.execute(sql)
    return result.fetchall()