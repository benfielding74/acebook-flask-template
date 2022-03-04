from acebook.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

class User():
  
  @classmethod
  def create(cls, username, password, profile_picture):
    db = get_db()
    db.execute(
      'INSERT INTO user (username, password, profile_picture) VALUES (?, ?, ?)',
      (username, generate_password_hash(password), profile_picture)
    )
    db.commit()

  @classmethod
  def find(cls, username):
    db = get_db()
    user = db.execute(
      'SELECT id, username, password, profile_picture FROM user WHERE username = ?', (username,)
    ).fetchone()
    if user:
      return User(user['username'], user['password'], user['profile_picture'], user['id'])
    else:
      return None

  @classmethod
  def find_by_id(cls, user_id):
    user = get_db().execute(
      'SELECT id, username, password, profile_picture FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    if user:
      return User(user['username'], user['password'], user['profile_picture'], user['id'])
    else:
      return None

  def __init__(self, username, password, profile_picture, id):
    self.username = username
    self.password = password
    self.profile_picture = profile_picture
    self.id = id

  def authenticate(self, password):
    return check_password_hash(self.password, password)
