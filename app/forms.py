from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NewProduct(FlaskForm):
    product_name = StringField('Product name', validators=[DataRequired()])
    product_type = StringField('Type of product')  # TODO change this to a select with categories later
    kabum_link = StringField('Kabum product URL (full link)')
    pichau_link = StringField('Pichau product URL (full link)')
    terabyte_link = StringField('Terabyte product URL (full link)')
    submit = SubmitField("ADD")
