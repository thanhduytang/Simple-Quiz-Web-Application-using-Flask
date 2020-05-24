from flask import render_template, flash, redirect, url_for, request, abort, json, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Score, QA
from werkzeug.urls import url_parse

class UserController():
    def login():
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

    def logout():
        logout_user()
        return redirect(url_for('index'))

    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you have successfully registered account.!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)


    
class ScoreController():
    def get_score():
        score = None
        if request.method == "POST":
            score = request.form['score']
            newscore = Score(score = score, user_id = current_user.id)
            db.session.add(newscore)
            db.session.commit()
            score = Score.query.filter_by(user_id=current_user.id).first().score
        return render_template('result.html')

    def result():
        if Score.query.filter_by(user_id = current_user.id).first() is None:
            flash("You haven't done the quiz yet !!! Please do the quiz")
            return redirect(url_for('quiz'))
        else:
            score = Score.query.filter_by(user_id = current_user.id).first().score
            if score > 100 and score <= 120:
                olevel = "Sufficient"
            elif score <= 100 & score >= 80:
                olevel = "Medium"
            else:
                olevel = "Insufficient"
            Score.query.filter_by(user_id = current_user.id).first().olevel = olevel
            db.session.commit()
            olevel = Score.query.filter_by(user_id = current_user.id).first().olevel
            questions = QA.query.all()
            answerlist= []
            for i in range(len(questions)):
                if questions[i].answer == 1:
                    answerlist.append(questions[i].option1)
                elif questions[i].answer == 2:
                    answerlist.append(questions[i].option2)
                elif questions[i].answer == 3:
                    answerlist.append(questions[i].option3)
                else:
                    answerlist.append(questions[i].option4)
            return render_template('result.html', score = score, olevel=olevel, answerlist = answerlist, questions = questions)


class QAController():
    def editquestion():
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
                            option4 = edit_form.option4.data,
                            answer  = edit_form.answer.data)
            db.session.add(newquestion)
            db.session.commit()
            return render_template('edit.html', form=edit_form, questions=questions)
        return render_template('edit.html', form=edit_form, questions=questions)
    

    def quiz():
        lists=[]
        len_QA = len(QA.query.all())
        for i in range(1, len_QA + 1, 1):
            q_id = QA.query.get(i)
            quest = {
                    'question': q_id.question,
                    'option1': q_id.option1,
                    'option2': q_id.option2,
                    'option3': q_id.option3,
                    'option4': q_id.option4,
                    'answer' : q_id.answer}
            lists.append(quest)  
        return render_template('quiz.html', lists = lists)

    def requiz():
        if Score.query.filter_by(user_id = current_user.id).first() is not None: 
            u = Score.query.filter_by(user_id = current_user.id).first()
            db.session.delete(u)
            db.session.commit()
            return redirect(url_for('quiz'))
        else:
            return redirect(url_for('quiz'))