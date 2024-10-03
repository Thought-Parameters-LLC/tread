from typing import Any
from flask import request, current_app, jsonify
from functools import wraps
import logging
import jwt
import datetime

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

# Decorator to check the JWT in cookies
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.cookies.get(current_app.config['JWT_COOKIE_NAME'])
    
    if not token:
      log.info(msg="Token is missing. Returning 403.")
      return jsonify({'message': 'Token is missing'}), 403
    
    try:
      # Decode the token and extract user information
      data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
      current_user = data['user']
      role: str = data['role']
      created_at: Any = data['created_at']
      exp: datetime.datetime = data['exp']
    except:
      log.info(msg='Token is invalid. Returning 403.')
      return jsonify({'message': 'Token is invalid'}), 403
    
    if exp < datetime.datetime.now(datetime.timezone.utc):
      log.info(msg='Token has expired. Returning 403.')
      return jsonify({'message': 'Token has expired'}), 403
    
    return f(current_user, role, created_at, exp, *args, **kwargs)
  
  return decorated
