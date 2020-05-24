from app import app, db
from app.models import User,Score,QA
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request

@app.route('/api/score',methods=['GET'])
def get_score_list():
  print('getting scorelist')
  score = Score.query.all()
  scores = []
  for s in score:
    scores.append({'score_id': s.id,'user_id': s.user_id, 'score': s.score,'Olevel': s.olevel})
  return jsonify({'ScoreList':scores})

