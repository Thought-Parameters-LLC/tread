from typing import Any
from . import db
from ..bcrypt import bcrypt

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  password_hash: Any = db.Column(db.String(150), nullable=False)
  role = db.Column(db.String(50), nullable=False)
  theme: Any = db.Column(db.String(50), nullable=True)
  profile_picture_url: Any = db.Column(db.String(250), nullable=True)
  created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
  
  def set_password(self, password):
    self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)