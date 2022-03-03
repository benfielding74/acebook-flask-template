from seleniumbase import BaseCase
from faker import Faker

fake = Faker()

class TestPosts(BaseCase):
  def test_create_and_list(self):
    self.open('http://127.0.0.1:5000/auth/register')
    username = fake.name()
    self.type('input[name="username"]', username)
    self.type('input[name="password"]', "12345678")
    self.click('input[value="Register"]')
    self.type('input[name="username"]', username)
    self.type('input[name="password"]', "12345678")
    self.click('input[value="Log In"]')
    self.click_link("New")
    title = fake.sentence()
    body = fake.sentence()
    self.type('input[name="title"]', title)
    self.type('textarea[name="body"]', body)
    self.click('input[value="Save"]')
    self.assert_text(title)
    self.assert_text(body)

class TestCancel(BaseCase):
  def test_cancel_post(self):
    self.open('http://127.0.0.1:5000/auth/login')
    self.type('input[name="username"]', "Morgan Sparks")
    self.type('input[name="password"]', "12345678")
    self.click('input[value="Log In"]')
    self.click_link("New")
    self.click('input[value="Cancel"]')
    self.assert_text('Posts')