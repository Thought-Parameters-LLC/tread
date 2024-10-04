import base64
import os
import platform
import random
from pathlib import Path
from unittest.mock import DEFAULT
import logging

log = logging.getLogger(__name__)
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
  
  SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
  
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default="sqlite:///" + DB_DIR + "/tread.db")
  
  JWT_SECRET_KEY = SECRET_KEY
  
  JWT_COOKIE_NAME = "jwt_tread"
  JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE", default=False)
  JWT_COOKIE_HTTPONLY = os.environ.get("JWT_COOKIE_HTTPONLY", default=True)
  
  # in hours but converted to minutes for more accurate token expiration
  JWT_TOKEN_EXPIRATION = os.environ.get("JWT_TOKEN_EXPIRATION", default=(24 * 60))
  
  ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", default="admin")
  ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", default="P@assw0rd")
  UPLOAD_MAX_SIZE = int(os.environ.get("UPLOAD_MAX_SIZE", default=1000000000))
  
  def __init__(self):
    if self.SECRET_KEY==None:
      self.SECRET_KEY: None = Config.get_secret_key()
      
    log.info(msg="SECRET_KEY: " + self.SECRET_KEY)
  
  @staticmethod
  def get_secret_key():
    if os.environ.get("SECRET_KEY") is None:
      if not Config.KEY_FILE.exists():
        with open(Config.KEY_FILE, "wb") as f:
          f.write(base64.b64encode(os.urandom(32)).decode("utf-8"))
          f.close()
          log.info(msg="Secret key created.")
        
    with open(Config.KEY_FILE, "r") as f:
      secret_key = f.read()
      f.close()
      
    return secret_key
  
  