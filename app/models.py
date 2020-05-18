from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#Create the User table in the database



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    email         = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    scores        = db.relationship('Score', backref='candidate', lazy='dynamic')

    
    #Printing out which user is current
    def __repr__(self):
        return '[Username {}]'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Score(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score   = db.Column(db.Integer)
    
    

    #Printing out the score of the current user.
    def __repr__(self):
        return '[Score {}]'.format(self.score)

class QA(db.Model):
    id       = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(256), index = True)
    option1  = db.Column(db.String(256), index = True)
    option2  = db.Column(db.String(256), index = True)
    option3  = db.Column(db.String(256), index = True)
    option4  = db.Column(db.String(256), index = True)
    answer   = db.Column(db.String(256), index = True)

    #Printing out the current question.
    def __repr__(self):
        return '[Question{}: {},Option1: {}, Option2: {}, Option3: {}, Option4: {}, Answer: {} ]'.format(self.id, self.question,\
         self.option1, self.option2, self.option3, self.option4, self.option5)

