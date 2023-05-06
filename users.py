from db import db
from sqlalchemy import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = text(f"SELECT id, pword FROM users WHERE username = '{username}'")
    result = db.session.execute(sql)
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return True
        else:
            return False

def logout():
    del session["user_id"]

def create_account(username, name, user_id, pword, role):
    hash_value = generate_password_hash(pword)
    try:
        sql = text("INSERT INTO users (username, pword, system_role) VALUES (:username, :pword, :system_role)")
        db.session.execute(sql, {"username":username, "pword":hash_value, "system_role":role})
        db.session.commit()
        create_rider(name, user_id)
        return True
    except:
        return False

def create_rider(name, user_id):
    try:
        sql = text("INSERT INTO riders (rider_name, user_id) VALUES (:rider_name, :user_id)")
        db.session.execute(sql, {"rider_name":name, "user_id":user_id})
        db.session.commit()
    except:
        return False
    
def user_id():
    return session.get("user_id", 0)

def system_role(id):
    sql = text(f"SELECT system_role FROM users WHERE id = '{id}'")
    result = db.session.execute(sql)
    return result.fetchone()
