from flask import Blueprint, current_app, send_from_directory

frontend = Blueprint("frontend", __name__)

@frontend.route("/")
def serve_index():
  return send_from_directory(current_app.config['BUILD_DIR'], "index.html")

@frontend.route("/<path:path>")
def serve_static_files(path):
  return send_from_directory(current_app.config['BUILD_DIR'], path)
  