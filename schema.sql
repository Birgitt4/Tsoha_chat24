CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT, status TEXT
);
CREATE TABLE threads (
    id SERIAL PRIMARY KEY, 
    title TEXT, 
    content TEXT, 
    user_id INTEGER REFERENCES users, 
    privat INTEGER DEFAULT 0,
    visible INTEGER DEFAULT 1,
    topic_id INTEGER REFERENCES topics
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY, 
    content TEXT, 
    thread_id INTEGER REFERENCES threads, 
    user_id INTEGER REFERENCES users
);
CREATE TABLE friends (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    friend_id INTEGER REFERENCES users
);
CREATE TABLE privateThreads (
    id SERIAL PRIMARY KEY, 
    thread_id INTEGER REFERENCES threads, 
    user_id INTEGER REFERENCES users
);
CREATE TABLE saved (
    id SERIAL PRIMARY KEY, 
    thread_id INTEGER REFERENCES threads, 
    user_id INTEGER REFERENCES users, 
    UNIQUE(thread_id, user_id)
);
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT
);