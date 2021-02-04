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

def get_sender(id):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result[0][0]

def new_thread(title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (title, content, user_id) VALUES (:title, :content, :user_id)"
    db.session.execute(sql, {"title":title, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def get_messages(id):
    sql = "SELECT content, user_id, id FROM messages WHERE thread_id=:id"
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

def search(title):
    sql = "SELECT title FROM threads WHERE title LIKE '%:title%'"
    result = db.session.execute(sql, {"title":title})
    return result.fetchall()

def search(message):
    sql = "SELECT title FROM threads WHERE id=(SELECT title_id FROM messages WHERE content LIKE '%:message%'"
    result = db.session.execute(sql, {"message":message})
    return result.fetchall()

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
