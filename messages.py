from db import db
import users

def get_sender(id):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()[0][0]

def get_messages(id):
    sql = """SELECT M.content, M.user_id, M.id, U.username FROM messages M, 
            users U WHERE M.thread_id=:id AND M.user_id=U.id ORDER BY M.id"""
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

def search(word):
    sql = """SELECT T.id, M.id, M.content FROM threads T, messages M WHERE LOWER(M.content)
         LIKE LOWER(:word) AND T.id=M.thread_id AND T.privat=0 AND T.visible=1"""
    result = db.session.execute(sql, {"word":"%"+word+"%"})
    return result.fetchall()