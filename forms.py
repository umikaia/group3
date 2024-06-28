from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FileField, SelectField

class AddProduct(FlaskForm):
    name = StringField(label="name")
    file = FileField(label="file")
    price = IntegerField(label="price")
    category = SelectField(label ="category")
    submit = SubmitField(label="submit")
    
class RegisterForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    register = SubmitField(label="register")

class LoginForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    login = SubmitField(label="login")