from flask import render_template, flash, redirect
from app.flask_app import *
from app.forms import *


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = 'Danilo'
    return render_template("index.html", user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Received login user {}'.format(form.username.data))
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title="Login test page", form=form)
