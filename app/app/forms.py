from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from app.models import User

class LoginForm(FlaskForm):
  username    = StringField('Username', validators=[DataRequired()])
  password    = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit      =SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username  = StringField('Username', validators=[DataRequired()])
    email     = StringField('Email', validators=[DataRequired(), Email()])
    password  = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditForm(FlaskForm):
    question_num  = IntegerField('Please input the question number', validators=[DataRequired()] )
    question      = StringField('Please input the question', validators=[DataRequired()] )
    option1       = StringField('Option1 of the question', validators=[DataRequired()] )
    option2       = StringField('Option2 of the question', validators=[DataRequired()] )
    option3       = StringField('Option3 of the question', validators=[DataRequired()] )
    option4       = StringField('Option4 of the question', validators=[DataRequired()] )
    answer        = IntegerField('Answer of the question', validators=[DataRequired(), NumberRange(min = 1, max = 4, message='The number of answer must be from 1 to 4 only')] )
    submit        = SubmitField('Edit question') 
    