from flask import Blueprint, render_template, redirect, url_for, request, session
import models, views
import os
from werkzeug.utils import secure_filename

bp = Blueprint("controller", __name__)

@bp.route("/")
def index():
    return redirect(url_for("controller.register"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        image = request.files["image"]

        filename = secure_filename(image.filename)
        #image.save(os.path.join("/DOC/UC/SDP/static/uploads/", filename))
        #image.save(os.path.join("static/", filename))
        image.save(os.path.join("labs/lab06/static/", filename))
        models.register_user(name, email, password, filename)
        return redirect(url_for("controller.login"))
    return views.register()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = models.get_user(email, password)
        if user:
            session["user_id"] = user[0]
            return redirect(url_for("controller.profile"))
        else:
            return "Incorrect email or password. Please try again."
    return views.login()

@bp.route("/profile")
def profile():
    if "user_id" in session:
        user = models.get_user_by_id(session["user_id"])
        posts = models.get_posts_by_user_id(user[0])
        return render_template("profile.html", user=user, posts=posts)
    else:
        return redirect(url_for("controller.login"))

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return views.login()

@bp.route('/submit_post', methods=['GET', 'POST'])
def submit_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']

        models.add_post(user_id, title, content)
        return redirect(url_for('controller.profile'))
    return views.submit_post()
    #return render_template('submit_post.html')
