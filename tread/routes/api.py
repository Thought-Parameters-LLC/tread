from flask import Blueprint, current_app, jsonify, request, make_response
import datetime
import logging
import jwt
from ..database.user import User
from ..jwt import token_required

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/v1", methods=["GET"])
def get_api_v1():
  return jsonify({
    "version": "1.0.0",
    "endpoints": ["/auth", "/users", "/roles", "/config"]
  })
  
@api.route("/v1/auth", methods=['GET'])
def get_v1_auth():
  return jsonify({
    "status": "success",
    "endpoints": [
      "/login",
      "/register",
      "/logout",
      "/check",
      "/refresh",
    ],
  })

@api.route("/v1/auth/register", methods=["POST"])
def post_v1_auth_register(): 
  data: dict = request.get_json()
  username: str | None = data.get("username")
  password: str | None = data.get("password")
  role: str | None = current_app.config['DEFAULT_USER_ROLE']
  created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
  
  if not username or not password:
    log.info('Missing username or password. Returning 401.')
    return jsonify({
      "status": "error",
      "message": "Missing username or password."
    }), 401
    
  user = User(username, password, role, created_at)
  
  try:
    user.save()
  except Exception as e:
    log.info(msg=f"{str(e)}. Returning 409.")
    return jsonify({
      "status": "error",
      "message": f"{str(e)}"
    }), 409
  
  log.info(msg=f"User created successfully. Returning 201.")
  return jsonify({
    "status": "success",
    "message": "User created successfully."
  }), 201
  
@api.route("/v1/auth/login", methods=["POST"])
def post_v1_auth_login():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")
  
  user = User.query.filter_by(username=username).first()
  if not user or not user.check_password(password):
    log.info(msg="Invalid username or password. Returning 401.")
    return jsonify({
      "status": 'unauthorized',
      'message': 'Invalid username or password.'
    }), 401
    
  token = jwt.encode({
    'user': user.username,
    'role': user.role,
    'created_at': user.created_at,
    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=current_app.config.TOKEN_EXPIRATION_MINUTES)
  }, current_app.config['SECRET_KEY'], algorithm='HS256')
  
  resp = make_response(jsonify({
    "status": "success",
    "message": "Logged in successfully."}))
  resp.set_cookie(current_app.config['JWT_COOKIE_NAME'], token, httponly=current_app.config['JWT_COOKIE_HTTPONLY'], secure=current_app.config['JWT_COOKIE_SECURE'])
  
  log.info(msg="Logged in successfully. Returning 200.")
  
  return resp

@api.route("/v1/auth/logout", methods=["GET"])
@token_required
def get_v1_auth_logout(current_user):
  resp = make_response(jsonify({
    "status": "success",
    "message": "Logged out successfully."}))
  resp.set_cookie(current_app.config['JWT_COOKIE_NAME'], '', expires=0)

  log.info(msg="Logged out successfully. Returning 200.")

  return resp

@api.route("/v1/auth/check", methods=["GET"])
@token_required
def get_v1_auth_check(current_user, role, created_at, exp):
  log.info(msg="Logged in. Returning 200.")
  return jsonify({
    "status": "success",
    "isAuthenticated": True,
    "message": f"Logged in as {current_user}.",
    "user": current_user,
    "role": role,
    "created_at": created_at,
    "exp": str(exp)
  })
  
api.route("/v1/auth/refresh", methods=["GET"])
@token_required
def get_v1_auth_refresh(current_user, role, theme, profile_picture_url, created_at, exp):
  token = jwt.encode({
    'user': current_user,
    'role': role,
    'theme': theme,
    'profile_picture_url': profile_picture_url,
    'created_at': created_at,
    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=current_app.config.TOKEN_EXPIRATION_MINUTES)}, current_app.config['SECRET_KEY'], algorithm='HS256')
  
  resp = make_response(jsonify({
    "status": "success",
    "message": "Token refreshed successfully."}))
  resp.set_cookie(current_app.config['JWT_COOKIE_NAME'], token, httponly=current_app.config['JWT_COOKIE_HTTPONLY'], secure=current_app.config['JWT_COOKIE_SECURE'])

  log.info(msg="Token refreshed successfully. Returning 200.")

  return resp