import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

c = "Accept= text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
"Accept-Encoding= gzip, deflate, br"
"Accept-Language= ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
"Connection= keep-alive"
"DNT= 1"
"Sec-Fetch-Dest= document"
"Sec-Fetch-Mode= navigate"
"Sec-Fetch-Site= same-origin"
"Sec-Fetch-User= ?1"
"Upgrade-Insecure-Requests= 1"
"Cache-Control= max-age=0"

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36")
# chrome_options.add_argument(c)
chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_position(0, 0)
driver.set_window_size(1400, 900)

time.sleep(1)

# driver.get('https://www.dhlottery.co.kr/common.do?method=main')
driver.get('https://www.dhlottery.co.kr/user.do?method=login&returnUrl=')

time.sleep(1)

driver.quit()