import base64
import os
import platform
import random
from pathlib import Path
from unittest.mock import DEFAULT

class Config:
  
  if platform.system() == 'Darwin' or platform.system() == 'Windows':
    PREFIX = os.path.expanduser("~")
  else:
    PREFIX = ''
    
  APP_DIR: str = str(Path(os.environ.get("APP_DIR", Path(PREFIX +"/app"))))
  DATA_DIR: str = str(Path(os.environ.get("DATA_DIR", default=APP_DIR + "/data")))
  DB_DIR: str = str(Path(os.environ.get("DB_DIR", default=DATA_DIR + "/db")))
  UPLOAD_DIR: str = str(Path(os.environ.get("UPLOAD_DIR", default=DATA_DIR + "/uploads")))
  DOCS_DIR: str = str(Path(os.environ.get("DOCS_DIR", default=DATA_DIR + "/docs")))
  CACHE_DIR: str = str(Path(os.environ.get("CACHE_DIR", default=DATA_DIR + "/cache")))
  
  instance_path = os.path.abspath(os.path.dirname(__file__))
  INSTANCE_DIR: str = str(Path(instance_path))
  APP_ROOT: str = str(os.path.dirname(str(Path(os.path.dirname(str(INSTANCE_DIR))))))
  BUILD_DIR: str = str(Path(os.environ.get("BUILD_DIR", default=APP_ROOT + "/frontend/public")))

  KEY_FILE: str = APP_DIR + "/.secret_key"
      
  if os.environ.get("SECRET_KEY") is None:
    if not KEY_FILE.exists():
      with open(KEY_FILE, "wb") as f:
        f.write(base64.b64encode(os.urandom(32)).decode("utf-8"))
        f.close()
        
    with open(KEY_FILE, "r") as f:
      SECRET_KEY = f.read()
      f.close()
      
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default="sqlite:///" + DB_DIR + "/tpnewsletter.db")
  
  JWT_COOKIE_NAME = os.environ.get("JWT_COOKIE_NAME", default="jwt_token")
  JWT_COOKIE_SECURE = bool(os.environ.get("JWT_COOKIE_SECURE", default=False))
  JWT_COOKIE_HTTPONLY = bool(os.environ.get("JWT_COOKIE_HTTPONLY", default=True))
  
  TOKEN_EXPIRATION_MINUTES = int(os.environ.get("TOKEN_EXPIRATION_MINUTES", default=60))
  
  ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", default="admin")
  ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", default="P@assw0rd")
  
  DEFAULT_USER_ROLE = os.environ.get("DEFAULT_USER_ROLE", default="user")
  DEFAULT_USER_THEME = os.environ.get("DEFAULT_USER_THEME", default="light")
  DEFAULT_USER_PROFILE_PICTURE_URL = os.environ.get("DEFAULT_USER_PROFILE_PICTURE_URL", default="https://i.imgur.com/6kOZ4H1.png")
  
  
      
  