from flask import render_template, flash, redirect, send_from_directory, request
from app.flask_app import *
from app.forms import *
from static.static_vars import *
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


@app.route('/product_editor', methods=['GET', 'POST'])
def add_or_edit_product():
    form = NewProduct()

    # If form data submitted, call database handler to put data in postgres
    if form.validate_on_submit():
        db_handler.product_manager(form.data)
    else:
        # If there is an ID parameter, it is editing an already existing product
        if request.args['id']:

            # grab product data on database
            product_data = db_handler.select_product_by_id(request.args['id'])[0]

            # Fill form with database data
            form.product_type.data = product_data[1]
            form.product_name.data = product_data[2]
            form.product_desc.data = product_data[3]
            form.kabum_link.data = kabum_base_url + product_data[4]
            form.pichau_link.data = pichau_base_url + product_data[5]
            form.terabyte_link.data = terabyte_base_url + product_data[6]

    return render_template('product_editor.html', title='Add new product to monitor', form=form)


@app.route('/edit_product', methods=['GET', 'POST'])  # TODO merge this with add product?
def edit_product():
    form = NewProduct()

    # product_data = db_handler.select_product_by_id(request.args['id'])[0]
    #
    # # Fill form with database data
    # form.product_type.data = product_data[1]
    # form.product_name.data = product_data[2]
    # form.product_desc.data = product_data[3]
    # form.kabum_link.data = kabum_base_url + product_data[4]
    # form.pichau_link.data = pichau_base_url + product_data[5]
    # form.terabyte_link.data = terabyte_base_url + product_data[6]

    return render_template('edit_product.html', form=form, edit_product=product_data)

#
# @app.route('/prices_table')
# def prices_table():
#     return render_template('placeholder.html')


@app.route('/product_list')
def prices_table():
    product_list = db_handler.select_all_products()

    return render_template('product_list.html', list=product_list)
