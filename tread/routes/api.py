import email
from flask import Blueprint, current_app, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, current_user
import datetime
import logging

import jwt
from ..database.user import User

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/v1", methods=["GET"])
def get_api_v1():
  return jsonify({
    "version": "1.0.0",
    "endpoints": [
      "/auth",
      "/user"
    ],
  })
  
@api.route("/v1/auth", methods=['GET'])
def get_v1_auth():
  return jsonify({
    "status": "success",
    "endpoints": [
      "/login",
      "/logout",
      "/refresh",
    ],
  })
  
@api.route("/v1/auth/login", methods=["POST"])
def login():
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
    
  access_token = create_access_token(identity=username)
  return jsonify(access_token=access_token)
  
api.route("/v1/auth/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh_token():
  return jsonify(access_token=create_access_token(identity=get_jwt_identity()))

  return None, 200

# TODO: Add get all users endpoint
@api.route("/v1/user", methods=["GET"])
@jwt_required()
def get_users():
  return None, 200

# TODO: Add user creation endpoint
@api.route("/v1/user", methods=["POST"])
@jwt_required()
def create_user():
  return None, 200

# TODO: Add get user endpoint
@api.route("/v1/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
  return None, 200

# TODO: Add delete user endpoint
@api.route("/v1/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
  return None, 200

# TODO: Add update user endpoint
@api.route("/v1/user/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
  return None, 200

      



    