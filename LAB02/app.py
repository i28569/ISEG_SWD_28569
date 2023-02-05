from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return 'Hello World!'

@app.route('/users/<username>')
def show_user(username):
    return f'Hello {username} and welcome to my first web application!'

if __name__ == '__main__':
    app.run()