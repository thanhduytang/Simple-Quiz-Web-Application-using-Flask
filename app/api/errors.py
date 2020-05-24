from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
  payload={'error': HTTP_STATUS_CODES.get(status_code, 'Unknown Error')}
  if message:
    payload['message'] = message
  response = jsonify(payload)
  response.status_code = status_code
  return response

def bad_request(message):
  return error_response(400, message)

def unauthorized(message):
  response = jsonify({'error': 'unauthorized', 'message': message})
  response.status_code = 401
  return response


def forbidden(message):
  response = jsonify({'error': 'forbidden', 'message': message})
  response.status_code = 403
  return response