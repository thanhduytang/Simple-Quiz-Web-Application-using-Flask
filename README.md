# CITS5505 AGILE WEB DEVELOPMENT PROJECT2

COVID-19 QUIZ APP 

Group Member:
Duy Tang 22803018
Eddie Liu 22781942
Jasmine Meng 22665473
Vian Tian 22593034

This project designs and builds a web page of Covid-19 quiz. The purpose of this quiz is trying to help the users to improve their awareness of Covid-19. Users need to register or login before taking the quiz. By taking the quiz, users can get a feedback which consists the overall score and suggestions based on the final result.

##Prerequisites
This application will be run under python virtual enviroment. Follow Enable_virtual_environment.txt to set up the virtual enviroment and download the required packages.

##Installing

```

```

##Running the test<br>

Both unit test and system test require to set the TestConfig correctly to initialize and use test.db

Running unit test by ``` python3 -m tests.unittest  ``` : testing the whether password field works correctly, testing the relationship between tables and if they can be successfully committed.
 
Running system test by ``` python3 -m tests.systemtest ```, a chrome webdriver is used here, the executable should be in the same directory as the test script to automate the test process. A 'login -> do quiz -> see result' action squence is tested in one run, to test if these actions can be done properly and if the correct information can be store in the database. Then a register action is tested in another run to gurantee a register process.
 


##Break down into end to end tests
Explain what these tests test and why
```

```
###Coding style tests


##Deployment
Add additional notes about how to deploy this on a live system
