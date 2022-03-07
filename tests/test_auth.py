from seleniumbase import BaseCase
from faker import Faker

fake = Faker()
class TestAuth(BaseCase):
  def test_registration_and_login(self):
    self.open('http://127.0.0.1:5000/auth/register')
    username = fake.name()
    self.type('input[name="username"]', username)
    self.type('input[name="password"]', "12345678")
    self.click('input[value="Register"]')
    self.type('input[name="username"]', username)
    self.type('input[name="password"]', "12345678")
    self.click('input[value="Log In"]')
    self.assert_text(username)
    self.assert_text("Log Out")

class TestPhoto(BaseCase):
  def test_upload_photo(self):
    self.open('http://127.0.0.1:5000/auth/register')
    username = fake.name()
    self.type('input[name="username"]', username)
    self.type('input[name="password"]', "12345678")
    self.click('input[value="Upload a Photo"]')

    self.click('input[value="Register"]')

    