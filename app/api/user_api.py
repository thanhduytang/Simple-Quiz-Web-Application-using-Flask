from app import app, db
from app.models import User, Score, QA
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
from app.api.auth import token_auth



@app.route('/api/users',methods=['GET'])
@token_auth.login_required
def get_all_users():
  if User.query.all() is None:
    abort(403)
  return jsonify(User.query.all_or_404().to_dict())


@app.route('/api/users/<int:id>',methods=['GET'])
@token_auth.login_required
def get_user(id):
  print(g.current_user)
  if g.current_user.id != id:
    abort(403)
  return jsonify(User.query.get_or_404(id).to_dict())


@app.route('/api/users',methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'id' not in data or 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User(username=data['username'], email = data['email'])
    user.from_dict(data)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_user', id=user.id)
    return response
  
@app.route('/api/users/<int:id>/score',methods=['GET'])
@token_auth.login_required
def getscoreuser(id):
    print(g.current_user)
    if g.current_user.id != id:
        abort(403)
    score_id = Score.query.filter_by(user_id = id).first().id
    return jsonify(Score.query.get_or_404(score_id).to_dict())