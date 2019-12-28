from flask import render_template, flash, redirect, send_from_directory, request
from app.flask_app import *
from app.forms import *
from functions import *
from DatabaseHandler import DatabaseHandler


user = 'Danilo'  # TODO remove placeholder
db_handler = DatabaseHandler()


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    try:
        global user
    except NameError:
        user = 'Danilo'
    return render_template("index.html", title="Home", user=user)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title="Login test page", form=form)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = NewProduct()
    if form.validate_on_submit():
        db_handler.add_new_product(form.data)
    return render_template('add_product.html', title='Add new product to monitor', form=form)


@app.route('/edit_product', methods=['GET', 'POST'])
def edit_product():
    id = request.args['id']

    return render_template('placeholder.html')

#
# @app.route('/prices_table')
# def prices_table():
#     return render_template('placeholder.html')


@app.route('/product_list')
def prices_table():
    product_list = db_handler.select_all_products()

    return render_template('product_list.html', list=product_list)
