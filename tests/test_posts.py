from seleniumbase import BaseCase
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By

fake = Faker()
browser = webdriver.Firefox(executable_path="/opt/homebrew/Cellar/geckodriver/0.30.0/bin/geckodriver")

def return_tags_in_xpath(xpath):
  print("list of elements")
  elements = browser.find_elements(by=By.XPATH,value=xpath)
  for e in range(len(elements)):
    print(e, elements[e].tag_name)


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


  def test_liking_a_post(self):
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
    self.open('http://127.0.0.1:5000/')
    self.click('input[value="Like"]')
    self.assert_text("1 like(s)")
    #return_tags_in_xpath('//*')   # debugging function use with pytest -s flag





        
    
