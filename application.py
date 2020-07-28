import os
import email_validator


from flask import Flask, session, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy import Column, String
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from modules import Survey_form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:921016@localhost/books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


@app.route('/')
def main():
    print("Server starting")
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('test'))

        return render_template('login.html', message='Invalid user name or password', form=form)

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)


reviews = []

comments = []


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/test', methods=["GET", "POST"])
@login_required
def test():
    comments = Reviews.query.limit(7).all()
    if request.method == "POST":
        review = request.form.get("review")
        reviews.append(review)
        data = Reviews(reviews=review, user_id=current_user.id)
        db.session.add(data)
        db.session.commit()
    return render_template('test.html', name=current_user.username, reviews=reviews, comments=comments)


@app.route('/survey_form', methods=['GET', 'POST'])
@login_required
def survey_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        current_role = request.form['current_role']
        recommendation = request.form['recommendation']
        preferences = request.form['preferences']
        projects = request.form['projects']
        comments = request.form['comments']
        if db.session.query(Survey_form).filter(Survey_form.name == name).count() == 0:
            data = Survey_form(name, email, age, current_role,
                               recomendation, preferences, projects, comments)
            db.session.add(data)
            db.session.commit()
            return "Thanks for your time"
        return render_template('survey_form', message='You have already submitted the Survey Form')
    return render_template('survey_form.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    manager.run()
