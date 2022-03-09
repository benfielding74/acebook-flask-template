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
  def add_about_me(cls, id, text):
    db = get_db()
    db.execute(
      'UPDATE user SET about_me = ? WHERE id = ?',
      (text, id)
    )
    db.commit()

  @classmethod
  def find(cls, username):
    db = get_db()
    user = db.execute(
      'SELECT id, username, password, profile_picture FROM user WHERE username = ?', (username,)
    ).fetchone()
    if user:
      return User(user['username'], user['password'], user['profile_picture'], user['id'], user['about_me'])
    else:
      return None

  @classmethod
  def find_by_id(cls, user_id):
    user = get_db().execute(
      'SELECT id, username, password, profile_picture, about_me FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    if user:
      return User(user['username'], user['password'], user['profile_picture'], user['id'], user['about_me'])
    else:
      return None

  def __init__(self, username, password, profile_picture, id, about_me):
    self.username = username
    self.password = password
    self.profile_picture = profile_picture
    self.id = id
    self.about_me = about_me

  def authenticate(self, password):
    return check_password_hash(self.password, password)
