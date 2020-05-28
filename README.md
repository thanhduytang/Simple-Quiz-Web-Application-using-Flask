# CITS5505 AGILE WEB DEVELOPMENT PROJECT2

COVID-19 QUIZ APP 

Group Member:<br>
Duy Tang 22803018<br>
Eddie Liu 22781942<br>
Jasmine Meng 22665473<br>
Vian Tian 22593034<br>

This project designs and builds a web page of Covid-19 quiz. The purpose of this quiz is trying to help the users to improve their awareness of Covid-19. Users need to register or login before taking the quiz. By taking the quiz, users can get a feedback which consists the overall score and suggestions based on the final result.

## Prerequisites

This application will be run under python(python3) with virtual enviroment, flask, and sqlite. Follow requirement.txt to set up the virtual enviroment and download the required packages.

## Getting Started

Install virtual envinronment in linux:
`python -m venv venv` 

To open Visual Studio Code:
`code .`

Activate the python virtual environment:
`source venv/bin/activate`

Set FLASK_APP=project2.py:
`export FLASK_APP=project2.py`

To run the app:
`flask run`

To stop the app:
`$deactivate`
## Database

We have put 12 questions in the database. To set as administrator, the following python code is required. <br>
`from app import db` <br>
`from app.models import User`  <br>
`u = User.query.get(1)`  <br>
`u.is_admin = True`  <br>
`db.session.commit()`  <br>


We have one account which is administrator. <br>
username: duy <br>
password:cat <br>

We also have account which is a normal account. <br>
username:huy <br>
password:cat <br>


## Installing

1. Set up a virtual environment:
 - use pip or another package manager to install virtualenv package `pip install virtualenv`
 - start the provided virtual environment
   `source venv/bin/activate`
 - This should include flask and all the required packages
2. Install sqlite
 - [Windows instructions](http://www.sqlitetutorial.net/download-install-sqlite/)
 - In linux, `sudo apt-get install sqlite`
3. Build the database: `flask db init`
4. `flask run`

## Running the test

Both unit test and system test require to set the TestConfig correctly to initialize and use test.db

Running unit test by python3 -m tests.unittest : testing the whether password field works correctly, testing the relationship between tables and if they can be successfully committed.

Running system test by python3 -m tests.systemtest, a chrome webdriver is used here, the executable should be in the same directory as the test script to automate the test process. A 'login -> do quiz -> see result' action squence is tested in one run, to test if these actions can be done properly and if the correct information can be store in the database. Then a register action is tested in another run to gurantee a register process.

## Contributing

Please read [gitlog.md]() for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **THANH DUY TANG** - *Initial work* - [thanhduytang](https://github.com/thanhduytang/CITS5505-PROJECT2)
* **EDDIE LIU**
* **Jasmine Meng**
* **Vian Tian**

## Deployment

Via localhost

## Acknowledgments

* Built following the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by **Miguel Grinberg**.
