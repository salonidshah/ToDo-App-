from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()],render_kw={"placeholder": "enter your first name"})
    last_name = StringField('Last name', validators=[DataRequired()],render_kw={"placeholder": "enter your last name"})
    email = EmailField('Email', validators=[DataRequired()],render_kw={"placeholder": "enter your e-mail"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "enter password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')
    

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()],render_kw={"placeholder": "enter your e-mail"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "enter password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')