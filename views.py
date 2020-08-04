from flask import Blueprint
from flask import render_template, request, url_for, redirect
from modules import LoginForm, SignupForm, Reviews, User, Survey_form
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_script import Manager
from extensions import db, login_manager
from send_mail import send_mail

main = Blueprint('main', __name__, template_folder='templates',
                 static_folder='static')


login_manager.login_view = '.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/home')
@main.route('/')
def home():
    return render_template('main.html')


@main.route('/index')
def index():
    return '<h2>Index<h2>'


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('.test'))
            return render_template('login.html', message='Invalid user name or password', form=form)
    return render_template('login.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
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


@main.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    comments = Reviews.query.limit(7).all()
    if request.method == "POST":
        review = request.form.get("review")
        reviews.append(review)
        data = Reviews(reviews=review, user_id=current_user.id)
        db.session.add(data)
        db.session.commit()
    return render_template('test.html', name=current_user.username, comments=comments, reviews=reviews)


@main.route('/survey_form', methods=['GET', 'POST'])
def survey_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        current_role = request.form.get('current_role')
        recommendation = request.form.get('recommendation')
        preferences = request.form.get('preferences')
        projects = request.form.getlist('projects')
        comments = request.form.get('comments')
        if db.session.query(Survey_form).filter(Survey_form.name == name).count() == 0:
            data = Survey_form(name, email, age, current_role,
                               recommendation, preferences, projects, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(name, email, age, current_role,
                      recommendation, preferences, projects, comments)
            return redirect(url_for('.test'))
        return render_template('survey_form.html', message='You have already submitted the Survey Form!')
    return render_template('survey_form.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
