import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime
from bs4 import BeautifulSoup

import telegramSender
import loadConfig
import logging

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
    driver = init_driver()
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
    driver = init_driver()
    login(driver)
    driver.get(prefix + '/userSsl.do?method=myPage')

    send_screenshot(driver)

    # 총 예치금
    deposit = driver.find_element(By.CLASS_NAME, 'total_new').find_element(By.TAG_NAME, 'strong').text

    msg = '🤑 현재 예치금\n' + deposit + ' 원'
    telegramSender.send(msg)
    driver.quit()


# 구매
def buy():
    driver = init_driver()
    login(driver)

    # 모바일버전 접속을 피하려면 URL 직접 접속해야 함
    # 홈피 메뉴로 구매 접속시 팝업창으로 진입하이여 모바일 버전이 뜸
    # 팝업창은 기존 크롬 초기화 설정내용이 적용되지 않는 듯
    driver.get('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')

    # 창내 팝업 핸들링
    if driver.find_element(By.CLASS_NAME, 'popup_section').is_displayed():
        driver.find_element(By.CSS_SELECTOR, '#popAlert > div > div > div.content > div.btns_submit > a').click()
        logging.info(driver.find_element(By.CLASS_NAME, 'popup_section').text)

    driver.switch_to.frame('ifrm_tab')

    # 자동번호발급
    driver.find_element(By.ID, "num2").click()

    # 수량선택: 5
    driver.find_element(By.XPATH, '//*[@id="amoundApply"]').send_keys('5')
    driver.find_element(By.NAME, 'btnSelectNum').click()
    logging.info(driver.find_element(By.ID, 'payAmt').text)

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
    driver = init_driver()
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


def init_driver():
    is_headless = loadConfig.chrome_headless

    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = is_headless
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36')
    chrome_options.add_argument('sec-ch-ua-mobile=?0')
    chrome_options.add_argument('sec-ch-ua-platform="macOS"')
    chrome_options.add_argument('Sec-Fetch-Mode=navigate')
    driver = webdriver.Chrome(options=chrome_options)

    # 동행복권은 js로 navigator.platform 을 체크하여 모바일 디바이스를 판단한다.
    # 때문에 아래 filter 화이트 리스트에 해당하는 값을 platform 값으로 override 한다.
    # filter = 'win16|win32|win64|macintel';
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "python 2.7", "platform": "macintel"})

    driver.set_window_position(0, 0)
    driver.set_window_size(1400, 900)

    return driver


def send_screenshot(driver):
    element_png = driver.find_element(By.XPATH, '/html/body').screenshot_as_png
    open('img_temp', 'wb').write(element_png)
    telegramSender.send_img('img_temp')