from flask import Blueprint, current_app, send_from_directory, render_template, redirect, url_for, request
from flask_jwt_extended import jwt_required, get_jwt_identity

webui = Blueprint("frontend", __name__)

@webui.route("/")
def index():
  return send_from_directory(current_app.config['BUILD_DIR'], "index.html")

@webui.route("/<path:path>")
def serve_static_files(path):
  return send_from_directory(current_app.config['BUILD_DIR'], path)
  