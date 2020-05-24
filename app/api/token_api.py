from flask import jsonify, g
from app import app, db
from app import db
from app.api.auth import basic_auth, token_auth

@app.route('/api/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
  token = g.current_user.get_token()
  db.session.commit()
  return jsonify({'token':token})

@app.route('/api/token', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
  token_auth.current_user().revoke_token()
  db.session.commit()
  return '', 204  # no response body required

