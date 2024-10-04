from typing import Any
from . import db
from ..bcrypt import bcrypt
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  password: Any = db.Column(db.String(150), nullable=False)
  full_name = db.Column(db.String(150), nullable=False)
  role = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(150), nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
  updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
  
  def __init__(self, username, password, full_name, role, email):
    self.username = username
    self.set_password(password) # hash the password
    self.full_name = full_name
    self.role = role
    self.email = email
      
  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode("utf-8")
    
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)
  
  def save(self):
    try:
      db.session.add(self)
      db.session.commit()
      log.info(msg="User saved to database.")
    except:
      db.session.rollback()
      log.error(msg="Error saving user to database, rolling back.")
      return False
      
    return True