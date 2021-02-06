from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["loggedin"] = True
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["loggedin"]

def signup(username, password):
    hash_val = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, status) VALUES (:username, :password, 'normal')"
        db.session.execute(sql, {"username":username, "password":hash_val})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def logged():
    return session.get("loggedin", 0)

def my_threads():
    sql = "SELECT title FROM threads WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":session.get("user_id", 0)})
    return result.fetchall()

def is_admin():
    sql = "SELECT status FROM users WHERE id=:user_id"
    result =db.session.execute(sql, {"user_id":session.get("user_id")})
    if result.first()[0] == "admin":
        return True
    else:
        return False

def add_friend(friend_id):
    sql = "INSERT INTO friends (user_id, friend_id) VALUES (:user_id, :friend_id)"
    db.session.execute(sql, {"user_id":user_id(), "friend_id":friend_id})
    db.session.commit()
