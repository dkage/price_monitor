from flask import render_template, flash, redirect, send_from_directory, request, url_for
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
    user = 'Danilo'  # TODO Maybe add login later?

    products_data = db_handler.products_info_and_prices()
    return render_template("index.html", title="Home", user=user, products=products_data, stores=stores_analyzed)


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
        # If contains ID already, it is passed as an argument in a product EDIT
        if 'id' in request.args:
            db_handler.product_manager(form.data, request.args['id'])
            return redirect(url_for('index'), 302)
        # Else it adds new product do database table
        else:
            db_handler.product_manager(form.data)
            return redirect(url_for('index'), 302)
    else:
        # If there is an ID parameter, it is editing an already existing product
        if 'id' in request.args:

            # grab product data on database
            product_data = db_handler.select_products(request.args['id'])
            print(product_data)
            if not product_data:
                return render_template('not_found.html', title='Product not found', id=request.args['id'])
            else:
                product_data = product_data[0]
                # Fill form with database data
                form.product_type.data = product_data[1]
                form.product_name.data = product_data[2]
                form.product_desc.data = product_data[3]
                form.kabum_link.data = kabum_base_url + product_data[4]
                form.pichau_link.data = pichau_base_url + product_data[5]
                form.terabyte_link.data = terabyte_base_url + product_data[6]

    return render_template('product_editor.html', title='Add new product to monitor', form=form)


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    product_id = request.args['id']

    if product_id:
        db_call = db_handler.delete_product(product_id)
    else:
        return render_template('not_found.html')

    if db_call[0] == 'error':
        return render_template('error.html', message=db_call[1])
    return render_template('success_delete.html', message=db_call[1])


@app.route('/product_list')
def prices_table():
    product_list = db_handler.select_products()

    return render_template('product_list.html', list=product_list, kabum=kabum_base_url, pichau=pichau_base_url,
                           terabyte=terabyte_base_url)
