from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import base64
from flask import url_for
#Create the User table in the database



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    email         = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    scores        = db.relationship('Score', backref = 'candidate', lazy='dynamic')
    is_admin      = db.Column(db.Boolean, nullable=False, default=False)

    #token authetication for api
    token = db.Column(db.String(32), index=True, unique = True)
    token_expiration=db.Column(db.DateTime)
    

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now+timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '[Number:{}, username:{}, email:{}]'.format(self.id, \
        self.username, \
        self.email)

    def getscore(self):
        return Score.query.filter_by(user_id = self.id).first()

    def getolevel(self):
        score = self.getscore()
        if not score:
            return None
        olevel = score.getolevel()
        return olevel

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }
        return data

    def from_dict(self, data):
        if 'password'and 'username' and 'email' in data:
            self.set_password(data['password'])

class Score(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score   = db.Column(db.Integer)
    olevel  = db.Column(db.String(256), index = True)
    

    def getolevel(self):
        return Score.query.filter_by(user_id = self.id).first().olevel



    def to_dict(self):
        data = {
        'id': self.id,
        'score':self.score,
        'olevel':self.olevel
        }
        return data

    def from_dict(self, data):
        if 'score' in data:
            self.score = data['score']
        if 'olevel' in data:
            self.olevel = data['olevel']


    #Printing out the score of the current user.
    def __repr__(self):
        return '{}, {}'.format(self.score, self.olevel)

    def is_committed(self):
        return self.user_id is not None

class QA(db.Model):
    id       = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(256), index = True)
    option1  = db.Column(db.String(256), index = True)
    option2  = db.Column(db.String(256), index = True)
    option3  = db.Column(db.String(256), index = True)
    option4  = db.Column(db.String(256), index = True)
    answer   = db.Column(db.Integer, index = True)

    #Printing out the current question.
    def __repr__(self):
         return ('{"question": "%s", "option1": "%s", "option2": "%s", "option3": "%s", "option4": "%s", "answer": "%s"}' %
                 (self.question, self.option1, self.option2, self.option3, self.option4, self.answer))


    def getquestion(self):
        return QA.query.filter(id = self.id).first()
    
    
    def to_dict(self):
        data = {
                'question': self.question,
                'option1': self.option1,
                'option2': self.option2,
                'option3': self.option3,
                'option4': self.option4,
                'answer' : self.answer
        }
        return data
    
    def from_dict(self, data):
        if 'question' in data:
            self.question = data['question']
        if 'option1' in data:
            self.option1 = data['option1']
        if 'option2' in data:
            self.option2 = data['option2']
        if 'option3' in data:
            self.option3 = data['option3']
        if 'option4' in data:
            self.option4 = data['option4']
        if 'answer' in data:
            self.answer = data['answer']
