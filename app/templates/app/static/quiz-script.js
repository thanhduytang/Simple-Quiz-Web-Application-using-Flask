var currentQuestion = 0;
var score = 0;
var totQuestions = questions.length;

var container = document.getElementById('quizContainer');
var questionEl = document.getElementById('question');
var opt1 = document.getElementById('opt1');
var opt2 = document.getElementById('opt2');
var opt3 = document.getElementById('opt3');
var opt4 = document.getElementById('opt4');
var nextButton = document.getElementById('nextButton');
var resultCont = document.getElementById('result');
var resultCont1 = document.getElementById('result1');
var resultCont2 = document.getElementById('result2');

function loadQuestion (questionIndex) {
	var q = questions[questionIndex];
	questionEl.textContent = (questionIndex + 1) + '. ' + q.question;
	opt1.textContent = q.option1;
	opt2.textContent = q.option2;
	opt3.textContent = q.option3;
	opt4.textContent = q.option4;
};

function loadNextQuestion () {
	var selectedOption = document.querySelector('input[type=radio]:checked');
	if(!selectedOption){
		alert('Please select your answer!');
		return;
	}
	var answer = selectedOption.value;
	if(questions[currentQuestion].answer == answer){
		score += 10;
	}
	selectedOption.checked = false;
	currentQuestion++;
	if(currentQuestion == totQuestions - 1){
		nextButton.textContent = 'Finish';
	}
	if(currentQuestion == totQuestions){
		container.style.display = 'none';
		resultCont.style.display = 'block';
		resultCont1.style.display = '';
		resultCont2.style.display = '';
		/* get overall level */
		if(score > 100 && score <= 120){Olevel = "Sufficient";}
		else if(score <= 100 && score >= 80){Olevel = "Medium";}
		else {Olevel = "Insufficient"}
		resultCont1.textContent = score;
		resultCont2.textContent = Olevel;
		return;
		
	}
	loadQuestion(currentQuestion);
}

loadQuestion(currentQuestion);

function do_ajax() {
	var button_save  = document.getElementById('savescore');
	var button_getsc = document.getElementById('getscore');
	button_save.style.display  ='none';
	button_getsc.style.display ='block';
	var req = new XMLHttpRequest();
	var x = score;
	document.getElementsByName('secret').value = x;
	req.open('POST', '/getscore', true);
	req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	req.send('score=' + document.getElementsByName('secret').value);
  }