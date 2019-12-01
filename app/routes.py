from flask import render_template
from app.flask_app import *
from app.forms import *


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = 'Danilo'
    return render_template("index.html", user=user)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Login test page", form=form)
