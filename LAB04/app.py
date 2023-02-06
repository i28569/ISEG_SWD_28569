from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

DATABASE = 'db.sqlite'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with connect_db() as con:
        con.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
        return(print('Table created successfully!'))

def create_user(name):
    with connect_db() as con:
        con.execute("INSERT INTO users (name) VALUES (?)", (name,))

def get_users():
    with connect_db() as con:
        cursor = con.execute("SELECT * FROM users")
        return cursor.fetchall()

def update_user(id, name):
    with connect_db() as con:
        con.execute("UPDATE users SET name = ? WHERE id = ?", (name, id))

def delete_user(id):
    with connect_db() as con:
        con.execute("DELETE FROM users WHERE id = ?", (id,))


if __name__ == "__main__":
    app.run()