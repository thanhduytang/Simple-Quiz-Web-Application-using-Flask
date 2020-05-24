from flask import g
from flask_httpauth import HTTPBasicAuth
from app.models import User
from app.api.errors import error_response
from flask_httpauth import HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

#password required for granting tokens 
@basic_auth.verify_password
def verify_password(username, password):
  user = User.query.filter_by(username = username).first()
  if user and user.check_password(password):
    g.current_user = user
    return g.current_user

@basic_auth.error_handler
def basic_auth_error():
  return error_response(401)

#token auth below
@token_auth.verify_token
def verify_token(token):
  g.current_user = User.check_token(token) if token else None
  return g.current_user

@token_auth.error_handler
def token_auth_error():
  return error_response(401)

