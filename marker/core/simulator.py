from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Simulator:

    def __init__(self) -> None:
        self.browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    def login(self):
        self.browser.get('https://accounts.douban.com/passport/login?redir=https://accounts.douban.com/')
        self.browser.find_element(By.CLASS_NAME, value="account-tab-account").click()
        print('Please log in to your Douban account manually on Selenium, 20 secs is given')
        WebDriverWait(self.browser, 30).until(EC.url_to_be('https://accounts.douban.com/passport/setting'))

    def search(self, name):
        self.browser.get('https://movie.douban.com/')
        self.browser.find_element(By.ID, value='inp-query').send_keys(name)
        self.browser.find_element(By.ID, value='inp-query').send_keys(Keys.ENTER)
        self.browser.find_elements(By.CLASS_NAME, value='cover-link')[0].click()

    def mark(self, star):
        self.browser.find_element(By.ID, value=f'star{star}').click()
        # wait for element to load
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, 'save')))
        self.browser.find_element(By.NAME, value='save').click()
