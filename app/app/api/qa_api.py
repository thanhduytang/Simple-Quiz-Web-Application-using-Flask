from app import app, db
from app.models import User,Score,QA
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request


@app.route('/api/question',methods=['GET'])
def get_questions_list():
  question = QA.query.all()
  questions = []
  for q in question:
    questions.append({'id'      : q.id, 
                      'quesiton': q.question,
                      'option1' : q.option1,
                      'option2' : q.option2,
                      'option3' : q.option3,
                      'option4' : q.option4,
                      'answer'  : q.answer})  
  return jsonify({'QuestionList':questions})

@app.route('/api/question/<int:id>',methods=['GET'])
def get_question(id):
  if QA.query.filter_by(id = id) is None:
    abort(403)
  return jsonify(QA.query.get_or_404(id).to_dict())
