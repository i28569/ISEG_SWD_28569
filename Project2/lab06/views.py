from flask import render_template

def register():
    return render_template("register.html")

def login():
    return render_template("login.html")

def profile(user, posts):
    return render_template("profile.html", user=user, posts=posts)

def submit_post():
    return render_template("submit_post.html")

