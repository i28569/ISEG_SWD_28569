from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

import models
import sqlite3
#import base64
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm


app = Flask(__name__)
app.secret_key = 'secret_key' # a secret key is required for sessions
CSRFProtect(app)


conn = sqlite3.connect('sarcastic_network.db',check_same_thread=False)
c = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # validate inputs
        if not username or not email or not password:
            return render_template('register.html', error='Please enter all fields')
        if len(username) < 3 or len(email) < 3 or len(password) < 3:
            return render_template('register.html', error='Fields must be at least 3 characters long')
        
        hashed_password = generate_password_hash(password, method='sha256')
        

        c.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        user = c.fetchone()
        if user:
            return render_template('register.html', error='Username or Email already exists')

        c.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, hashed_password))
        conn.commit()
        #conn.close()
        
        return redirect(url_for('login'))
        
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            

            c.execute("SELECT * FROM users WHERE username=?", (str(username),))
            conn.commit()
            user = c.fetchone()
            if user:
                
                print(user[3])
                if check_password_hash(user[3], password):
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    error = 'Incorrect Password'
                    return render_template('login.html', form=form, error=error)
            else:
                error = 'Username not found'
                return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile/<username>')
def profile(username):
    form = LoginForm()
    c.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,))
    user = c.fetchone()
    if not user:
        return 'User not found', 404
    print(user)
    c.execute("""
        SELECT * FROM posts
        WHERE user_id = ?
        ORDER BY posts.created_at DESC
    """, (user[1],))
    posts = c.fetchall()
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()
    return render_template('user_profile.html', user=user, posts=posts, comments = comments,form = form)

@app.route('/feed')
def feed():
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()
    form = LoginForm()
    #for post in posts:
        #with open(post.picture, "rb") as image_file:
        #    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        #post.picture = encoded_string
    return render_template('feed.html', posts=posts, form = form, comments = comments)
    #print(posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = LoginForm()
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()

    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()
    if request.method == 'POST':
        # Get the uploaded image
        #image = request.files['image']

        # Read the image into memory
        #image_bytes = image.read()
        #img_b = sqlite3.Binary(image_bytes)
        img_b = ''

        # Get the post content
        content = request.form['content']

        # Get the user ID of the logged-in user
        user_id = session['username']

        # Insert the post into the database
        #c = get_db().cursor()
        c.execute('INSERT INTO posts (user_id, picture, content) VALUES (?, ?, ?)', (user_id, img_b , content))
        conn.commit()
        #get_db().commit()

        c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
        """)
        posts = c.fetchall()
        print(posts)

        return render_template('feed.html',posts=posts, form = form, comments= comments)

    return render_template('feed.html', form = form ,posts=posts,comments = comments)

@app.route('/comment', methods=['POST'])
def comment():
    form = LoginForm()
    post_id = request.form.get('post_id')
    user_id = session['username']
    content = request.form.get('content')
    c.execute("""
        INSERT INTO comments (post_id, user_id, content, timestamp)
        VALUES (?,?,?,datetime('now'))
    """, (post_id, user_id, content))
    conn.commit()

    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()

    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()

    return render_template('feed.html', form = form, posts = posts, comments = comments )

@app.route('/upvote_comment', methods=['POST'])
def upvote_comment():
    form = LoginForm()
    comment_id = request.form.get('comment_id')
    c.execute("""
        UPDATE comments
        SET upvotes = upvotes + 1
        WHERE id = ?
    """, (comment_id,))

    conn.commit()
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()

    return render_template('feed.html', posts=posts, form = form, comments = comments)

@app.route('/downvote_comment', methods=['POST'])
def downvote_comment():
    comment_id = request.form.get('comment_id')
    c.execute("""
        UPDATE comments
        SET upvotes = upvotes - 1
        WHERE id = ?
    """, (comment_id,))
    conn.commit()
    return 'Comment upvoted'


@app.errorhandler(404)
def error_occurred(error):
    return render_template('error.html'), 404


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = LoginForm()
    if request.method == 'POST':
        # Connect to the database
        #conn = sqlite3.connect('mydatabase.db')
        #c = conn.cursor()

        # Retrieve the search query from the form
        search_query = request.form['query']

        # Query the database for posts that match the search query
        c.execute("SELECT * FROM posts WHERE content LIKE ?", ('%' + search_query + '%',))
        results = c.fetchall()

        c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
        """)
        comments = c.fetchall()


        # Close the connection to the database
        #conn.close()

        # Render the search results page
        return render_template('search.html', posts=results, search_query=search_query, 
                               form = form,comments = comments)
    else:
        return render_template('search.html',form = form)



if __name__ == '__main__':
    models.init_db()
    app.run(debug=True)








