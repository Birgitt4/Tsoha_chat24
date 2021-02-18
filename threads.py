from db import db
import users

def get_threads():
    sql = "SELECT title, id FROM threads WHERE privat=0 ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_thread(id):
    sql = "SELECT T.title, T.content, U.username, T.user_id FROM threads T, users U WHERE T.id=:id AND U.id=T.user_id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def new_thread(title, content, privat):
    user_id = users.user_id()
    if user_id == 0:
        return 0
    sql = "INSERT INTO threads (title, content, user_id, privat) VALUES (:title, :content, :user_id, :privat) RETURNING id"
    result = db.session.execute(sql, {"title":title, "content":content, "user_id":user_id, "privat":privat})
    db.session.commit()
    thread_id = result.fetchone()[0]
    if privat == 1:
        add_user(users.user_id(), thread_id)
    return thread_id

def add_user(user_id, thread_id):
    sql = "INSERT INTO privateThreads (thread_id, user_id) VALUES (:thread_id, :user_id)"
    db.session.execute(sql, {"thread_id":thread_id, "user_id":user_id})
    db.session.commit()

def follow(thread_id):
    sql = "INSERT INTO follows (thread_id, user_id) VALUES (:thread_id, :user_is)"
    db.session.execute(sql, {"thread_id":thread_id, "user_id":users.user_id()})
    db.session.commit()

def search_title(title):
    sql = "SELECT title FROM threads WHERE title LIKE '%:title%'"
    result = db.session.execute(sql, {"title":title})
    return result.fetchall()

def search_message(message):
    sql = "SELECT title FROM threads WHERE id=(SELECT title_id FROM messages WHERE content LIKE '%:message%'"
    result = db.session.execute(sql, {"message":message})
    return result.fetchall()