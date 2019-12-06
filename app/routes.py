from flask import render_template, flash, redirect, send_from_directory
from app.flask_app import *
from app.forms import *


user = 'Test'

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    try:
        global user
    except NameError:
        user = 'Danilo'
    return render_template("index.html", title="Home", user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title="Login test page", form=form)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
