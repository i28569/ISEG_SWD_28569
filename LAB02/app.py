from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route('/')
def index():
    response = make_response('Hello World!')
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/users/<user>')
def show_user(user):
    return f'Hello {user} and welcome to my first web application!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    if username == 'test' and password == 'test':
        return 'Login successful'
    else:
        return 'Invalid username or password'

@app.route('/template')
def index_template():
    name = 'Ricardo'
    return render_template('index.html',name=name)


if __name__ == '__main__':
    app.run()