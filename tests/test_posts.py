from seleniumbase import BaseCase
from faker import Faker
from selenium import webdriver

fake = Faker()
browser = webdriver.Firefox(executable_path="/opt/homebrew/Cellar/geckodriver/0.30.0/bin/geckodriver")

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
    button = browser.find_element_by_xpath('/html/body/section/article[1]/header/div/a[1]')
    button.click()
    self.open('http://127.0.0.1:5000/')
    like_string = driver.findElement(By.xpath("/html/body/section/article[1]/header/div/div")).getText()
    self.assertTrue(like_string.contains("1 like(s)"))
        
    
