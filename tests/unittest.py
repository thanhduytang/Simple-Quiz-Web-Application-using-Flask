import unittest, os
from app import app, db
from app.models import User, Score, QA

class UserCase(unittest.TestCase):

  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']=\
        'sqlite:///'+os.path.join(basedir,'test.db')
    self.app = app.test_client()#creates a virtual test environment
    db.create_all()
    u1 = User(id=1, username="susan", email="000@test.com")
    u2 = User(id=2, username="mike", email="001@test.com")
    Q1 = QA(id=1, question='how good are you?', option1='1', option2='2', option3='3', option4='4',answer=2)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(Q1)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_password_hashing(self):
    u = User.query.get(1)
    u.set_password('test')
    self.assertFalse(u.check_password('case'))
    self.assertTrue(u.check_password('test'))

  def test_is_committed(self):
    u1 = User.query.get(1)
    u2 = User.query.get(2)
    score1 = Score(score=10, candidate = u1)
    score2 = Score(score=20, candidate = u2)
    self.assertFalse(score1.is_committed())
    db.session.add(score1)
    db.session.add(score2)
    db.session.commit()
    self.assertTrue(score1.is_committed())
    self.assertTrue(score2.is_committed())

if __name__=='__main__':
  unittest.main(verbosity=2)