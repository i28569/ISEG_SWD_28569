import sqlite3

def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        image TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)
    conn.commit()
    conn.close()

def register_user(name, email, password, image):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (name, email, password, image)
    VALUES (?, ?, ?, ?);
    """, (name, email, password, image))
    conn.commit()
    conn.close()

def get_user(email, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users
    WHERE email = ? AND password = ?;
    """, (email, password))
    a=cursor.fetchone()
    conn.close()
    return a

def get_user_by_id(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users
    WHERE id = ?;
    """, (user_id,))
    a=cursor.fetchone()
    conn.close()
    return a

def get_posts_by_user_id(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM posts
    WHERE user_id = ?;
    """, (user_id,))
    a=cursor.fetchall()
    conn.close()
    return a

def add_post(user_id, title, content):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO posts (user_id, title, content)
    VALUES (?, ?, ?);
    """, (user_id, title, content))
    conn.commit()
    conn.close()