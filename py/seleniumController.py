from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime
from bs4 import BeautifulSoup

import telegramSender
import loadConfig

prefix = loadConfig.url_prefix


def login(driver):
    driver.get(prefix + '/user.do?method=login&returnUrl=')
    driver.find_element(By.NAME, 'userId').send_keys(loadConfig.user_id)
    driver.find_element(By.NAME, 'password').send_keys(loadConfig.password)
    driver.find_element(By.XPATH, "//a[@href='javascript:check_if_Valid3();']").click()

    # 새창 팝업 핸들링
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])


# 예치금 충전
def payment(money):
    driver = webdriver.Chrome()
    login(driver)
    driver.get(prefix + '/payment.do?method=payment')
    money_select = Select(driver.find_element(By.ID, 'Amt'))
    money_select.select_by_value(money)
    driver.find_element(By.CSS_SELECTOR, '#btn2 > button').click()

    charge_user = driver.find_element(By.CSS_SELECTOR, '#contents > table > tbody > tr:nth-child(3) > td').text
    charge_amount = driver.find_element(By.CLASS_NAME, 'color_key1').text
    charge_account = driver.find_element(By.CLASS_NAME, 'pay_lt').text

    telegramSender.send(charge_amount + '\n' + charge_account + '\n' + charge_user)
    driver.quit()


# 예치금 조회
def check_charge():
    driver = webdriver.Chrome()
    login(driver)
    driver.get(prefix + '/userSsl.do?method=myPage')

    # 총 예치금
    deposit = driver.find_element(By.CLASS_NAME, 'total_new').find_element(By.TAG_NAME, 'strong').text

    msg = '🤑 현재 예치금\n' + deposit + ' 원'
    telegramSender.send(msg)
    driver.quit()


# 구매
def buy():
    driver = webdriver.Chrome()
    login(driver)
    driver.find_element(By.XPATH, "//a[@href='javascript:void(0)']").click()
    driver.find_element(By.XPATH, "//a[@href='javascript:goLottoBuy(2);']").click()
    driver.switch_to.window(driver.window_handles[1])

    # 창내 팝업 핸들링
    if driver.find_element(By.CLASS_NAME, 'popup_section').is_displayed():
        driver.find_element(By.CSS_SELECTOR, '#popAlert > div > div > div.content > div.btns_submit > a').click()
        print(driver.find_element(By.CLASS_NAME, 'popup_section').text)

    driver.switch_to.frame('ifrm_tab')

    # 자동번호발급
    driver.find_element(By.ID, "num2").click()

    # 수량선택: 1
    driver.find_element(By.NAME, 'btnSelectNum').send_keys('1')
    driver.find_element(By.NAME, 'btnSelectNum').click()
    print(driver.find_element(By.ID, 'payAmt').text)

    # 구매하기: YES
    driver.find_element(By.NAME, 'btnBuy').click()
    driver.find_element(By.CSS_SELECTOR, '#popupLayerConfirm > div > div.btns > input:nth-child(1)').click()

    # 결과메시지 전송
    if driver.find_element(By.CSS_SELECTOR, '#popReceipt > h2').is_displayed():
        current_time = datetime.today().strftime("%Y%m%d-%H%M%S")
        img_name = 'test-' + current_time + '.png'

        element_png = driver.find_element(By.CSS_SELECTOR, '#popReceipt').screenshot_as_png
        open(img_name, 'wb').write(element_png)
        telegramSender.send_img(img_name)
    else:  # 구매 실패
        result_text = driver.find_element(By.CSS_SELECTOR, '#popupLayerAlert > div > div.noti > span').text
        telegramSender.send(result_text)

    driver.quit()


def check_result():
    driver = webdriver.Chrome()
    login(driver)
    driver.get(prefix + '/myPage.do?method=lottoBuyListView')

    # 1주일 기간 조회
    driver.find_element(By.CSS_SELECTOR,
                        '#frm > table > tbody > tr:nth-child(3) > td > span.period > a:nth-child(2)').click()  # 1주일
    driver.find_element(By.CSS_SELECTOR, '#submit_btn').click()  # 조회

    # iframe 전환
    driver.switch_to.frame('lottoBuyList')

    # 구매내역 테이블 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', attrs={'class': 'tbl_data tbl_data_col'})
    trs = table.find_all('tr')
    result_text = '최근 1주일'
    for tr in trs:
        row_text = ''
        tds = tr.find_all('td')
        if len(tds) > 2:
            for td in range(0, len(tds) - 2):
                row_text += tds[td].text.strip() + ' '
        result_text += row_text + '\n'

    telegramSender.send(result_text)
    driver.quit()
