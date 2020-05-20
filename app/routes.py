from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from app.forms import LoginForm, RegistrationForm, QuizForm, EditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Score, QA
from werkzeug.urls import url_parse
from sqlalchemy.sql.expression import func

@app.route('/')
@app.route('/index')
@login_required

def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=302)


@app.route('/login', methods = ['GET', 'POST'])
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

    return render_template('login.html', title = "Sign in", form = form)


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have successfully registered account.!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/editquestion', methods=['GET', 'POST'])
@login_required
def editquestion():
    if not current_user.is_admin:
        flash("You are not allowed to access this page. Administrator only !!!")
        return redirect(url_for('index'))
    
    questions = QA.query.all()
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        flash("You have successfully created a question")
        if QA.query.get(edit_form.question_num.data) is not None:
            db.session.delete(QA.query.get(edit_form.question_num.data))
            db.session.commit()
        newquestion = QA(id      = edit_form.question_num.data,
                         question= edit_form.question.data,
                         option1 = edit_form.option1.data,
                         option2 = edit_form.option2.data,
                         option3 = edit_form.option3.data,
                         answer  = edit_form.answer.data)
        db.session.add(newquestion)
        db.session.commit()
        return render_template('edit.html', form=edit_form, questions=questions)
    return render_template('edit.html', form=edit_form, questions=questions)




@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    pullquest = QA.query.all()
    pullquest1 = pullquest[0:4]
    pullquest2 = pullquest[4:9]
    pullquest3 = pullquest[9:13]
    if form.validate_on_submit():
        return redirect(url_for('info'))
    else:
        return render_template('quiz.html', form = form, pullquest1 =pullquest1, pullquest2=pullquest2, pullquest3 =pullquest3)


@app.route('/result', methods=['POST'])
@login_required
def info():
    score=0
    choices  = QA.query.filter(QA.id).all()
    for i in range(13):
        answered = request.args.get('value', i, type=str)
        if choices[i].answer == answered:
            score += 10
            return render_template('result.html', score=score)
        else:
            return abort(500)
