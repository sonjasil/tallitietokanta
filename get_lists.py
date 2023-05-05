from sqlalchemy.sql import text
from db import db

def get_lessons():
    sql = text("SELECT skill_level, price, max_riders FROM lessons")
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
