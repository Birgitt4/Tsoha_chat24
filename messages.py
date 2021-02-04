from db import db
import users

#lankoja koskevat metodit voisi viedä omaan luokkaansa

def get_threads():
    sql = "SELECT title, id FROM threads ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_thread(id):
    sql = "SELECT title, content FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def new_thread(title, content, privat):
    user_id = users.user_id()
    if user_id == 0:
        return 0
    sql = "INSERT INTO threads (title, content, user_id, privat) VALUES (:title, :content, :user_id, :privat) RETURNING id"
    result = db.session.execute(sql, {"title":title, "content":content, "user_id":user_id, "privat":privat})
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

#viestejä koskevat
def get_sender(id):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()[0][0]

def get_messages(id):
    sql = "SELECT content, user_id, id FROM messages WHERE thread_id=:id ORDER BY id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def add_message(content, id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, thread_id, user_id) VALUES (:content, :thread_id, :user_id)"
    db.session.execute(sql, {"content":content, "thread_id":id, "user_id":user_id})
    db.session.commit()
    return True

def delete(message_id):
    allow = False
    if users.is_admin():
        allow = True
    elif users.user_id() == get_sender(message_id):
        allow = True
    if allow:
        sql = "DELETE FROM messages WHERE id=:message_id"
        db.session.execute(sql, {"message_id":message_id})
        db.session.commit()

def edit(message_id, content):
    if users.user_id() == get_sender(message_id):
        sql = "UPDATE messages SET content=:content WHERE id=:message_id"
        db.session.execute(sql, {"content":content, "message_id":message_id})
        db.session.commit()
