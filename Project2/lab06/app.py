from flask import Flask, render_template, redirect, url_for, request, session
import os
import models
import controllers

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(controllers.bp)

if __name__ == "__main__":
    models.init_db()
    app.run(debug=True)