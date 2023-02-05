from flask import Flask, request, make_response, render_template

app = Flask(__name__)

# @app.route('/')
# def index():
#     response = make_response('Hello World!')
#     response.headers['Content-Type'] = 'text/plain'
#     return response

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

@app.route('/')
def index():
    return render_template('index.html',name='Ricardo')


if __name__ == '__main__':
    app.run()