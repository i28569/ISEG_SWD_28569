from flask import Flask, request

app = Flask(__name__)

@app.route('/')

def index():
    return 'Hello World!'

@app.route('/users/<username>')
def show_user(username):
    return f'Hello {username} and welcome to my first web application!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    if username == 'test' and password == 'test':
        return 'Login successful'
    else:
        return 'Invalid username or password'


if __name__ == '__main__':
    app.run()