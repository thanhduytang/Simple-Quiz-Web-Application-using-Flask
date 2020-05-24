import unittest, os, time
from app import app, db
from app.models import User, Score, QA
from selenium import webdriver
basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
  driver = None

  def setUp(self):
    self.driver = webdriver.Chrome(executable_path=os.path.join(basedir,'chromedriver.exe'))
    if not self.driver:
      self.skipTest
    else:
      db.init_app(app)
      db.create_all()
      db.session.query(User).delete()
      db.session.query(QA).delete()
      db.session.query(Score).delete()
      u = User(id=1, username="susan", email="001@test.com")
      u.set_password('test')
      q1 = QA(id=1, question='How good are you?', option1='fantastic', option2='good', option3='bad', option4='awful', answer=1)
      q2 = QA(id=2, question='How is the weather?', option1='sunny', option2='cloudy', option3='rainy', option4='foggy',answer=1)
      db.session.add(u)
      db.session.add(q1)
      db.session.add(q2)
      db.session.commit()
      self.driver.maximize_window()
      self.driver.get('http://localhost:5000/')

  def tearDown(self):
    if self.driver:
      self.driver.close()
      db.session.query(User).delete()
      db.session.query(QA).delete()
      db.session.query(Score).delete()
      db.session.commit()
      db.session.remove()

  def test_login_quiz(self):
    user_field = self.driver.find_element_by_id('username') 
    password_field = self.driver.find_element_by_id('password')  
    submit = self.driver.find_element_by_id('submit')

    user_field.send_keys('susan')
    password_field.send_keys('test')
    submit.click()
    time.sleep(1)

    # check greeting message
    greeting = self.driver.find_element_by_id('greeting').get_attribute('innerHTML')
    self.assertEqual(greeting, 'Hi, susan!')

    # check button is start not see_result
    button = self.driver.find_element_by_class_name('button')
    self.assertEqual(button.get_attribute('innerHTML'), 'Start')
    button.click()
    time.sleep(1)
    
    # test quiz
    opt1 = self.driver.find_element_by_id('opt1')
    opt1.click()
    next_btn = self.driver.find_element_by_id('nextButton')
    next_btn.click()
    time.sleep(2)

    opt2 = self.driver.find_element_by_id('opt2')
    opt2.click()
    next_btn.click()
    time.sleep(2)
    
    score = self.driver.find_element_by_id('result1')
    level = self.driver.find_element_by_id('result2')
    self.assertEqual(score.get_attribute('innerHTML'), '10')
    self.assertEqual(level.get_attribute('innerHTML'), "Insufficient")

    save = self.driver.find_element_by_id('savescore')
    save.click()
    time.sleep(1)

    # check score for susan in database
    s = Score.query.get(1)
    self.assertEqual(s.user_id, 1)
    self.assertEqual(s.score, 10, msg='score stored in database')


  def test_register(self):
    register = self.driver.find_element_by_link_text("Click to Register!")
    register.click()

    user_field = self.driver.find_element_by_id('username') 
    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    password2_field = self.driver.find_element_by_id('password2')  
    submit = self.driver.find_element_by_id('submit')

    user_field.send_keys('mike')
    email_field.send_keys('002@test.com')
    password_field.send_keys('0000')
    password2_field.send_keys('0000')
    submit.click()
    self.driver.implicitly_wait(5)
    time.sleep(1)

    # check logout link
    mike = User.query.get(2)
    self.assertEqual(mike.email,'002@test.com',msg='mike now exists in db')


if __name__=='__main__':
  unittest.main(verbosity=2)