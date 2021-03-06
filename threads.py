from db import db
import users

def get_threads(topic_id):
    if topic_id == 0:
        sql = "SELECT title, id FROM threads WHERE privat=0 AND visible=1 ORDER BY id"
        result = db.session.execute(sql)
    else:
        sql = """SELECT title, id FROM threads WHERE privat=0 AND visible=1 AND 
                topic_id=:topic_id ORDER BY id"""
        result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_thread(id):
    sql = """SELECT T.title, T.content, U.username, T.user_id, T.privat FROM threads T, 
            users U WHERE T.id=:id AND U.id=T.user_id"""
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def is_private(id):
    sql = "SELECT privat FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.first()[0]

def new_thread(title, content, privat, topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return 0
    sql = """INSERT INTO threads (title, content, user_id, privat, topic_id) VALUES 
            (:title, :content, :user_id, :privat, :topic_id) RETURNING id"""
    result = db.session.execute(sql, {"title":title, "content":content, "user_id":user_id,
                                     "privat":privat, "topic_id":topic_id})
    db.session.commit()
    thread_id = result.fetchone()[0]
    if privat == 1:
        add_user(users.user_id(), thread_id)
    return thread_id

def add_user(user_id, thread_id):
    sql = "INSERT INTO privateThreads (thread_id, user_id) VALUES (:thread_id, :user_id)"
    db.session.execute(sql, {"thread_id":thread_id, "user_id":user_id})
    db.session.commit()

def search(word):
    sql = """SELECT id, title, content FROM threads WHERE (LOWER(title) LIKE LOWER(:word) 
            OR LOWER(content) LIKE LOWER(:message)) AND privat=0 AND visible=1 ORDER BY id"""
    result = db.session.execute(sql, {"word":"%"+word+"%", "message":"%"+word+"%"})
    return result.fetchall()

def edit_content(id, content):
    sql = "UPDATE threads SET content=:content WHERE id=:id"
    db.session.execute(sql, {"content":content, "id":id})
    db.session.commit()

def delete(id):
    sql = "UPDATE threads SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def get_topics():
    sql = "SELECT id, topic FROM topics"
    result = db.session.execute(sql)
    return result.fetchall()