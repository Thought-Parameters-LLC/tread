import os
from pathlib import Path
from flask import Flask
from .config import Config
from .jwt import jwt
from .routes.webui import webui
from .routes.api import api
from .bcrypt import bcrypt
from .database import db

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
        
    if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_object(Config)
    else:
      # load the test config if passed in
      app.config.from_mapping(test_config)
    
    try:  
      Path(app.config['DATA_DIR']).mkdir(parents=True, exist_ok=True)
    except OSError:
      pass
    
    try:
      Path(app.config['DB_DIR']).mkdir(parents=True, exist_ok=True)
    except OSError:
      pass
    
    try:
      Path(app.config['UPLOAD_DIR']).mkdir(parents=True, exist_ok=True)
    except OSError:
      pass
    
    try:
      Path(app.config['DOCS_DIR']).mkdir(parents=True, exist_ok=True)
    except OSError:
      pass
    
    try:
      Path(app.config['CACHE_DIR']).mkdir(parents=True, exist_ok=True)
    except OSError:
      pass
    
    try:
      Path(app.config['BUILD_DIR']).mkdir(parents=True, exist_ok=True)
    except OSError:
      pass
    
    app.register_blueprint(webui)
    app.register_blueprint(api)
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    with app.app_context():
      db.create_all()
      
    return app
    
    
if __name__ == "__main__":
    app = create_app()