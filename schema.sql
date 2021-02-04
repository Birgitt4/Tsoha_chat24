CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, status TEXT);
CREATE TABLE threads (id SERIAL PRIMARY KEY, title TEXT, content TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, thread_id INTEGER REFERENCES threads, user_id INTEGER REFERENCES users);
CREATE TABLE friends (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, friend_id INTEGER REFERENCES users);
