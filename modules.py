from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin, login_user, login_required, logout_user, current_user


from extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    comments = db.relationship('Reviews', backref='user', lazy='dynamic')


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviews = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, reviews, user_id):
        self.reviews = reviews
        self.user_id = user_id


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class SignupForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])


class Survey_form(db.Model):
    __tablename__ = 'Survey_form'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    age = db.Column(db.Integer)
    current_role = db.Column(db.String())
    recommendation = db.Column(db.String())
    preferences = db.Column(db.String())
    projects = db.Column(db.String())
    comments = db.Column(db.Text())

    def __init__(self, name, email, age, current_role, recommendation, preferences, projects, comments):
        self.name = name
        self.email = email
        self.age = age
        self.current_role = current_role
        self.recommendation = recommendation
        self.preferences = preferences
        self.projects = projects
        self.comments = comments


class Book(db.Model):
    isbn = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(50))
    year = db.Column(db.Integer)
