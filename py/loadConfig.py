import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
config.sections()

telegram_token = config['TELEGRAM_INFO']['telegram_token']
url_prefix = config['LOGIN_INFO']['prefix']
user_id = config['LOGIN_INFO']['id']
password = config['LOGIN_INFO']['pw']
chrome_headless = config.getboolean('CHROME', 'chrome_headless')

