# coding: utf-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from datetime import datetime


@app.route('/')
@app.route('/index')
#@login_required
#@login_required protects a view function against anonymous
#users is with a decorator called @login_required. When you
#add this decorator to a view function below the @app.route
#decorators from Flask, the function becomes protected and
# will not allow access to users that are not authenticated
def index():
    #student = {'username': 'User'}
    posts = [
        {
            'author': {'username': 'Empresa'},
            'body': 'O que procuramos em um estagiario do CEFET-MG?!'
        },
        {
            'author': {'username': 'Estudante'},
            'body': 'O que as empresas querem de um formando do CEFET-MG?'
        }
    ]
    #return render_template('index.html', title='FCM Home', user=student, posts=posts)

    return render_template('index.html', title='FCM Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, area=form.area.data, hability=form.hability.data, course=form.course.data, contact=form.contact.data, description=form.description.data , codecpfcnpj = form.codecpfcnpj.data , blocked=form.blocked.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
