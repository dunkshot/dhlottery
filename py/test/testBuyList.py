import seleniumController
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime
from bs4 import BeautifulSoup

import telegramSender

driver = webdriver.Chrome()
seleniumController.login(driver)
driver.get('https://dhlottery.co.kr/myPage.do?method=lottoBuyListView')

driver.find_element(By.CSS_SELECTOR,
                    '#frm > table > tbody > tr:nth-child(3) > td > span.period > a:nth-child(2)').click()  # 1주일
driver.find_element(By.CSS_SELECTOR, '#submit_btn').click()  # 조회

driver.switch_to.frame('lottoBuyList')

src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')
table = soup.find('table', attrs={'class': 'tbl_data tbl_data_col'})
trs = table.find_all('tr')
result_text = ''
for tr in trs:
    rowText = ''
    tds = tr.find_all('td')
    if len(tds) > 2:
        for td in range(0, len(tds)-2):
            rowText += tds[td].text.strip() + ' '
    result_text += rowText + '\n'

telegramSender.send(result_text)

driver.quit()
