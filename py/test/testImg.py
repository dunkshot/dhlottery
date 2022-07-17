import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import telegram
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get('https://nid.naver.com/nidlogin.login?url=http%3A%2F%2Fmail.naver.com%2F')

ele = driver.find_element(By.CLASS_NAME, 'panel_inner')
b64 = ele.screenshot_as_png

now = datetime.today().strftime("%Y%m%d-%H%M%S")

open('test-' + now + '.png', 'wb').write(b64)

token = '5260793847:AAHQBZljoUiNTHAJ-y1orZHxO25U2KBPlKE'
chat_id = 370311245

bot = telegram.Bot(token=token)
bot.send_photo(chat_id, open('test' + now + '.png', 'rb'))
