from flask import render_template, flash, redirect, url_for, request, abort, json, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, ScoreController, QAController
from app.models import User, Score, QA
from werkzeug.urls import url_parse

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=302)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return UserController.login()
    

@app.route('/logout')
def logout():
    logout_user()
    return UserController.logout()



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return UserController.register()

@app.route('/editquestion', methods=['GET', 'POST'])
@login_required
def editquestion():
    if not current_user.is_admin:
        flash("You are not allowed to access this page. Administrator only !!!")
        return redirect(url_for('index'))
    return QAController.editquestion()


@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if Score.query.filter_by(user_id = current_user.id).first() is not None:
        flash("You have taken the test already")
        return redirect(url_for('index'))
    else:
        return QAController.quiz()


@app.route('/requiz', methods=['GET', 'POST'])
@login_required
def requiz():
    if Score.query.filter_by(user_id = current_user.id).first() is None:
        flash("You haven't done the quiz before. Please start the quiz !!!")
        return redirect(url_for('quiz'))
    else:
        flash('Do this quiz again !!!')
        return QAController.requiz()
        


@app.route('/getscore', methods=['GET','POST'])
@login_required
def get_score():
    return ScoreController.get_score()

@app.route('/result', methods=['GET','POST'])
@login_required
def result():
    return ScoreController.result()

    
