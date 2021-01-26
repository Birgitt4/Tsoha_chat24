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
            return True
        else:
            return False

def logout():
    del session["user_id"]

def signup(username, password):
    hash_val = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, status) VALUES (:username, :password, normal)"
        db.session.execute(sql, {"username":username, "password":hash_val})
        db.session.commit()
    except:
        return False
    return login(username, password)
